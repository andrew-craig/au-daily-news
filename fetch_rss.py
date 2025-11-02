#!/usr/bin/env python3
"""
RSS Feed Fetcher for ABC News Australia
Fetches RSS feed and saves entries from the past 24 hours as markdown.
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import argparse
import re
from email.utils import parsedate_to_datetime


def fetch_rss_feed(url: str) -> ET.Element:
    """
    Fetch and parse an RSS feed from the given URL or local file.

    Args:
        url: The RSS feed URL or local file path

    Returns:
        Parsed XML root element
    """
    # Check if it's a local file
    import os
    if os.path.isfile(url):
        with open(url, 'rb') as f:
            return ET.fromstring(f.read())

    # Otherwise fetch from URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, application/atom+xml, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return ET.fromstring(response.content)


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse a date string from RSS feed (RFC 822 format).

    Args:
        date_string: Date string to parse

    Returns:
        datetime object or None if parsing fails
    """
    try:
        return parsedate_to_datetime(date_string)
    except Exception:
        return None


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.

    Args:
        text: Text with HTML tags

    Returns:
        Text without HTML tags
    """
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # Decode HTML entities
    import html
    text = html.unescape(text)
    return text.strip()


def filter_recent_entries(root: ET.Element, hours: int = 24) -> tuple[Dict, List[Dict]]:
    """
    Filter feed entries from the past N hours.

    Args:
        root: XML root element
        hours: Number of hours to look back (default: 24)

    Returns:
        Tuple of (feed_info, recent_entries)
    """
    cutoff_time = datetime.now(tz=None).replace(tzinfo=None) - timedelta(hours=hours)
    recent_entries = []

    # Extract channel info
    channel = root.find('channel')
    feed_info = {
        'title': channel.findtext('title', 'RSS Feed'),
        'description': channel.findtext('description', ''),
        'link': channel.findtext('link', '')
    }

    # Extract items
    for item in channel.findall('item'):
        entry = {}

        # Extract basic fields
        entry['title'] = item.findtext('title', 'No Title')
        entry['link'] = item.findtext('link', '')

        # Get description with all text content (including text within child elements)
        desc_element = item.find('description')
        if desc_element is not None:
            # Get all text content recursively
            entry['description'] = ''.join(desc_element.itertext())
        else:
            entry['description'] = ''

        entry['author'] = item.findtext('author', '')
        entry['pub_date_raw'] = item.findtext('pubDate', '')

        # Parse publication date
        if entry['pub_date_raw']:
            entry_date = parse_date(entry['pub_date_raw'])
            if entry_date:
                # Make timezone-naive for comparison
                entry['pub_date'] = entry_date.replace(tzinfo=None)
                if entry['pub_date'] >= cutoff_time:
                    recent_entries.append(entry)
            else:
                # If we can't parse the date, skip this entry
                continue
        else:
            # If no date is available, skip this entry
            continue

    return feed_info, recent_entries


def format_as_markdown(feed_info: Dict, entries: List[Dict]) -> str:
    """
    Format feed entries as markdown.

    Args:
        feed_info: Dictionary containing feed metadata
        entries: List of entries to format

    Returns:
        Markdown formatted string
    """
    markdown = []

    # Header
    markdown.append(f"# {feed_info['title']}\n")

    if feed_info['description']:
        markdown.append(f"_{feed_info['description']}_\n")

    markdown.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    markdown.append(f"**Entries from the past 24 hours:** {len(entries)}\n")
    markdown.append("\n---\n")

    # Entries
    for entry in entries:
        # Title
        markdown.append(f"\n## {entry['title']}\n")

        # Published date
        if entry['pub_date_raw']:
            markdown.append(f"**Published:** {entry['pub_date_raw']}\n")

        # Link
        if entry['link']:
            markdown.append(f"**Link:** [{entry['link']}]({entry['link']})\n")

        # Author
        if entry['author']:
            markdown.append(f"**Author:** {entry['author']}\n")

        # Summary/Description
        if entry['description']:
            summary = remove_html_tags(entry['description'])
            markdown.append(f"\n{summary}\n")

        markdown.append("\n---\n")

    return '\n'.join(markdown)


def save_markdown(content: str, filename: str) -> None:
    """
    Save markdown content to a file.

    Args:
        content: Markdown content to save
        filename: Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved to {filename}")


def main():
    """Main function to orchestrate the RSS feed fetching and saving."""
    parser = argparse.ArgumentParser(
        description='Fetch ABC News RSS feed and save as markdown'
    )
    parser.add_argument(
        '--url',
        default='https://www.abc.net.au/news/feed/5555986/rss.xml',
        help='RSS feed URL (default: ABC News Australia)'
    )
    parser.add_argument(
        '--output',
        default='abc_news.md',
        help='Output markdown filename (default: abc_news.md)'
    )
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Number of hours to look back (default: 24)'
    )

    args = parser.parse_args()

    try:
        print(f"Fetching RSS feed from: {args.url}")
        root = fetch_rss_feed(args.url)

        print(f"Filtering entries from the past {args.hours} hours...")
        feed_info, recent_entries = filter_recent_entries(root, args.hours)

        print(f"Found {len(recent_entries)} recent entries")

        if len(recent_entries) == 0:
            print("No recent entries found. No file will be created.")
            return

        print("Formatting as markdown...")
        markdown_content = format_as_markdown(feed_info, recent_entries)

        print(f"Saving to {args.output}...")
        save_markdown(markdown_content, args.output)

        print("Done!")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
