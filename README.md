# au-daily-news

A Python program to fetch ABC News Australia RSS feed and save entries from the past 24 hours as a markdown document.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage (fetches ABC News Australia feed):

```bash
python fetch_rss.py
```

Custom options:

```bash
python fetch_rss.py --url <RSS_URL> --output <OUTPUT_FILE> --hours <HOURS>
```

### Options

- `--url`: RSS feed URL (default: https://www.abc.net.au/news/feed/5555986/rss.xml)
- `--output`: Output markdown filename (default: abc_news.md)
- `--hours`: Number of hours to look back (default: 24)

### Example

```bash
python fetch_rss.py --output news_today.md --hours 12
```

## Output

The program generates a markdown file containing:
- Feed title and metadata
- All entries published within the specified time period
- Each entry includes: title, publication date, link, author (if available), and summary

## Troubleshooting

### 403 Forbidden Error

Some websites (including ABC News) may block automated requests with a 403 Forbidden error. This is an anti-bot protection measure. If you encounter this issue:

**Option 1: Use a different RSS feed**
Try another news source that doesn't block automated requests:
```bash
python fetch_rss.py --url "https://example.com/rss" --output news.md
```

**Option 2: Test with a local file**
Download the RSS feed manually through your browser and save it, then run:
```bash
python fetch_rss.py --url /path/to/downloaded/feed.xml --output news.md
```

**Option 3: Use a proxy or RSS aggregator service**
Consider using services like:
- Feedly API
- RSS2JSON
- RSSHub

The program itself is working correctly - the issue is with the website's access restrictions.