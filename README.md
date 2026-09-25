# Finn.no Jobs Scraper

Extract job listings from Finn.no, Norway's largest job board and marketplace. Perfect for recruitment automation, job market analysis, and AI-powered job matching.

## Features

- 🎯 Search by keywords, location, and job type
- 🌍 Extract jobs from all Norwegian regions
- ⚡ Fast httpx-based scraping (no browser needed)
- 🔄 Works with Claude, ChatGPT & AI agents via Apify MCP
- 📊 Structured JSON output

## Input

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| searchQuery | string | Job title, skills, or keywords | "" |
| location | string | Location code (0.20001 = Oslo, 0.20061 = Bergen) | "0.20001" |
| jobType | string | Filter: All, Fulltime, Parttime, Contract, Freelance | "All" |
| sector | string | Industry: All, IT, Sales, Marketing, etc. | "All" |
| maxResults | integer | Maximum number of jobs to scrape | 3 |
| proxyConfiguration | object | Proxy settings (optional) | - |

## Output

Each job listing contains:

- `jobUrl` - Full URL to the job posting
- `jobTitle` - Job title/position
- `company` - Employer name
- `location` - Job location
- `salary` - Salary information (if available)
- `jobType` - Employment type
- `description` - Job description
- `publishedDate` - When the job was posted
- `scrapedAt` - Timestamp of scraping

## Use Cases

1. **Recruitment Automation** - Auto-collect relevant job postings for candidate matching
2. **Market Research** - Analyze hiring trends in Norwegian tech sector
3. **Salary Benchmarking** - Track compensation across industries
4. **AI Job Matching** - Feed job data to ChatGPT/Claude for candidate recommendations
5. **Career Guidance** - Help job seekers discover opportunities

## Integration with AI Agents

This scraper is compatible with Claude Code, ChatGPT, and other AI agents via the Apify MCP (Model Context Protocol). Use it to:

- Automatically fetch jobs matching a candidate's profile
- Generate job market reports for specific skills
- Compare salaries across Norwegian cities
- Extract job requirements for resume optimization

## Pricing

- **Per Result**: $0.005 per job listing scraped
- **Startup Fee**: $0.05 per actor run

Example: Scraping 100 jobs = $0.05 + (100 × $0.005) = **$0.55**

## Example

```json
{
  "searchQuery": "python developer",
  "location": "0.20001",
  "jobType": "Fulltime",
  "maxResults": 50
}
```

## FAQ

**Q: How accurate is the data?**
A: Extremely accurate - scraped directly from Finn.no's HTML with multiple fallback selectors.

**Q: Do I need proxies?**
A: Not required for small-scale scraping. Finn.no is generally accessible.

**Q: What regions are supported?**
A: All of Norway. Use location codes: 0.20001 (Oslo), 0.20061 (Bergen), 0.20002 (Trondheim), etc.

**Q: Can I use this with ChatGPT?**
A: Yes! This actor is fully compatible with ChatGPT, Claude, and other AI agents via Apify MCP integration.

---

Built for AI agents | Compatible with Claude, ChatGPT & MCP
