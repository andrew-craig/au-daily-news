# au-daily-news

A Python program to fetch ABC News Australia RSS feed and save entries from the past 24 hours as a markdown document.

## Installation

### Option 1: Docker (Recommended)

Using Docker Compose:

```bash
docker-compose up
```

Or build and run with Docker:

```bash
docker build -t au-daily-news .
docker run -v $(pwd)/output:/app/output au-daily-news --output /app/output/news.md
```

### Option 2: Local Python Installation

Install dependencies using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Using Docker Compose (Easiest)

1. **Basic usage with defaults:**
   ```bash
   docker-compose up
   ```
   This will create an `output` folder with `abc_news.md` containing the last 24 hours of news.

2. **Customize with environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   docker-compose up
   ```

3. **One-time custom run:**
   ```bash
   RSS_URL=https://example.com/feed.xml OUTPUT_FILE=custom.md HOURS=12 docker-compose up
   ```

### Using Docker Directly

```bash
# Build the image
docker build -t au-daily-news .

# Run with custom options
docker run -v $(pwd)/output:/app/output au-daily-news \
  --url https://example.com/feed.xml \
  --output /app/output/news.md \
  --hours 12
```

### Using Python Directly

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