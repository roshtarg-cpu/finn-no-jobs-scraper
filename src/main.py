"""Finn.no Jobs Scraper - Extract job listings from Norwegian job board"""
print("DEBUG: main.py loaded")
import os
import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode, urljoin

import httpx
from apify import Actor
from bs4 import BeautifulSoup
print("DEBUG: imports complete")


async def main():
    """Main scraper entry point."""
    print("DEBUG: main() called!")
    async with Actor:
        print("DEBUG: inside Actor context")
        # Get input
        print("DEBUG: getting input...")
        actor_input = await Actor.get_input()
        print(f"DEBUG: got input: {actor_input}")
        if not actor_input:
            Actor.log.error('No input provided')
            actor_input = {}  # Use defaults instead of returning
        
        print("DEBUG: starting scraper")
        print("DEBUG: about to call Actor.log.info")
        Actor.log.info('Starting Finn.no Jobs scraper...')
        print("DEBUG: log call succeeded")
        
        # Parse input
        search_query = actor_input.get('searchQuery', '')
        location = actor_input.get('location', '')
        job_type = actor_input.get('jobType', 'All')
        max_results = actor_input.get('maxResults', 3)
        
        # Build search URL
        params = {}
        if search_query:
            params['q'] = search_query
        if location:
            params['location'] = location
        
        # Map job type to Finn.no paths
        if job_type == 'Fulltime':
            path = '/job/fulltime/search.html'
        elif job_type == 'Parttime':
            path = '/job/parttime/search.html'
        else:
            path = '/job/fulltime/search.html'  # Default
        
        search_url = f"https://www.finn.no{path}"
        if params:
            search_url += f"?{urlencode(params)}"
        
        Actor.log.info(f'Search URL: {search_url}')
        
        # Setup proxy if provided
        proxy_config = actor_input.get('proxyConfiguration')
        proxy_url = None
        if proxy_config and proxy_config.get('useApifyProxy'):
            proxy_password = os.getenv('APIFY_PROXY_PASSWORD')
            if proxy_password:
                proxy_url = f"http://auto:{proxy_password}@proxy.apify.com:8000"
        
        client_kwargs = {'follow_redirects': True, 'timeout': 30.0}
        if proxy_url:
            client_kwargs['proxy'] = proxy_url
        
        results_count = 0
        
        async with httpx.AsyncClient(**client_kwargs) as client:
            # Fetch listing page
            Actor.log.info('Fetching job listings...')
            response = await client.get(
                search_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find job containers using multi-strategy approach
            containers = set()
            
            # Strategy 1: data-testid attributes
            for e in soup.find_all(attrs={'data-testid': re.compile(r'ad|listing|object')}):
                containers.add(e)
            
            # Strategy 2: article tags
            for e in soup.find_all('article'):
                if e.find('a'):
                    containers.add(e)
            
            # Strategy 3: class-based (fallback)
            if not containers:
                for e in soup.find_all('div', class_=re.compile(r'ad-|item|card|result', re.I)):
                    if e.find('a'):
                        containers.add(e)
            
            Actor.log.info(f'Found {len(containers)} job listings')
            
            if not containers:
                Actor.log.warning('No job listings found on page')
                return
            
            for container in list(containers)[:max_results]:
                try:
                    # Extract job URL
                    link = container.find('a', href=True)
                    if not link:
                        continue
                    
                    job_url = urljoin(search_url, link['href'])
                    
                    # Extract title
                    title_elem = container.find(['h1','h2','h3','a'], class_=re.compile(r'title|heading', re.I))
                    if not title_elem:
                        title_elem = link
                    job_title = title_elem.get_text(strip=True) if title_elem else None
                    
                    # Extract company
                    company_elem = container.find(class_=re.compile(r'company|employer|advertiser', re.I))
                    company = company_elem.get_text(strip=True) if company_elem else None
                    
                    # Extract location
                    location_elem = container.find(class_=re.compile(r'location|place|address', re.I))
                    location_text = location_elem.get_text(strip=True) if location_elem else None
                    
                    # Extract date
                    date_elem = container.find(class_=re.compile(r'date|time|published', re.I))
                    published_date = date_elem.get_text(strip=True) if date_elem else None
                    
                    # Push result
                    result = {
                        'jobUrl': job_url,
                        'jobTitle': job_title,
                        'company': company,
                        'location': location_text,
                        'salary': None,
                        'jobType': job_type if job_type != 'All' else None,
                        'description': None,
                        'publishedDate': published_date,
                        'scrapedAt': datetime.now(timezone.utc).isoformat()
                    }
                    
                    await Actor.push_data(result)
                    results_count += 1
                    Actor.log.info(f'Scraped {results_count}/{max_results}: {job_title}')
                    
                    if results_count >= max_results:
                        break
                        
                except Exception as e:
                    Actor.log.warning(f'Failed to parse job listing: {e}')
                    continue
        
        Actor.log.info(f'Scraping completed! Total jobs scraped: {results_count}')
