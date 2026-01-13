from _json import make_scanner
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import re
import os
from typing import List, Dict, Optional, Set
from dotenv import load_dotenv

def fetch_feed_data(url: str) -> Optional[str]:
    """
    Fetches XML content from a URL.
    
    Args:
        url: The URL to fetch.
        
    Returns:
        The XML content as a string, or None if fetching failed.
    """
    try:
        print(f"Fetching data from: {url}")
        with urllib.request.urlopen(url) as response:
            return response.read()
    except urllib.error.URLError as e:
        print(f"Error fetching URL {url}: {e}")
    except Exception as e:
        print(f"Unexpected error fetching {url}: {e}")
    return None

def parse_rss_items(xml_content: str) -> List[ET.Element]:
    """
    Parses RSS items from XML content.
    
    Args:
        xml_content: The XML string to parse.
        
    Returns:
        A list of 'item' Elements found in the RSS feed.
    """
    try:
        root = ET.fromstring(xml_content)
        channel = root.find('channel')
        if channel is None:
            # Maybe it's a different RSS flavor?
            # Fallback: try finding items directly under root if channel missing or root is channel
            # usage: root.findall('.//item')
            print("Warning: No 'channel' element found. Attempting to find items directly.")
            return root.findall('.//item') or []
            
        items = channel.findall('item')
        return items
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Unexpected error parsing XML: {e}")
    return []

def extract_item_data(item: ET.Element) -> Dict[str, str]:
    """
    Extracts relevant data (title, year, category, link) from an RSS item element.
    
    Args:
        item: The XML element representing an item.
        
    Returns:
        A dictionary containing cleaned title, year, category, and link.
    """
    title_element = item.find('title')
    title_raw = title_element.text if title_element is not None and title_element.text else "Unknown Title"
    
    year_match = re.search(r'\((\d{4})\)', title_raw)
    if year_match:
        year = year_match.group(1)
        # Remove the year from the title for cleaner output
        title = re.sub(r'\s*\(\d{4}\)\s*', ' ', title_raw).strip()
    else:
        year = "Unknown release Year"
        title = title_raw

    category_element = item.find('category')
    category = category_element.text if category_element is not None and category_element.text else "Unknown"

    link_element = item.find('link')
    link = link_element.text if link_element is not None and link_element.text else "No link"
    
    return {
        "title": title,
        "year": year,
        "category": category,
        "link": link
    }

def format_output(items_data: List[Dict[str, str]]) -> str:
    """
    Formats the parsed items into the desired string output.
    
    Args:
        items_data: A list of dicts with item data.
        
    Returns:
        A formatted string ready for writing to file.
    """
    output_lines = []
    
    for i, data in enumerate(items_data, 1):
        output_lines.append(f"#{i}:")
        output_lines.append(f"   Title: {data['title']}")
        output_lines.append(f"   Released: {data['year']}")
        output_lines.append(f"   Type: {data['category'].upper()}")
        output_lines.append(f"   Link: {data['link']}")
        output_lines.append("")
        
    return '\n'.join(output_lines)

def process_watchlist(urls: List[str], output_file_path: str = "plex_watchlist.txt") -> bool:
    """
    Main logic to fetch, parse, and save watchlist data.
    
    Args:
        urls: List of RSS feed URLs.
        output_file_path: Path to the output file.
        
    Returns:
        True if successful (items found and written), False otherwise.
    """
    all_items_data: List[Dict[str, str]] = []
    seen_links: Set[str] = set()

    for url in urls:
        xml_content = fetch_feed_data(url)
        if not xml_content:
            continue
            
        items = parse_rss_items(xml_content)
        print(f"Parsed {len(items)} items from {url}")
        
        for item in items:
            data = extract_item_data(item)
            # Simple deduplication based on link
            if data['link'] not in seen_links:
                seen_links.add(data['link'])
                all_items_data.append(data)

    if not all_items_data:
        print("No items found to write.")
        # If we failed to find items, we might not want to overwrite the file 
        # with empty content, or maybe we do? 
        # The original code returned False.
        return False

    formatted_content = format_output(all_items_data)
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        print(f"\nSuccessfully parsed {len(all_items_data)} total unique items from watchlist")
        return True
    except IOError as e:
        print(f"Error writing to file {output_file_path}: {e}")
        return False

def main():
    load_dotenv()
    
    rss_urls_env = os.getenv('RSS_URLS')
    
    if not rss_urls_env:
        print("Error: RSS_URLS not found in .env file")
        print("Please create a .env file with: RSS_URLS=url1,url2,url3")
        exit(1)
    
    # Split by comma and strip whitespace
    rss_urls = [url.strip() for url in rss_urls_env.split(',') if url.strip()]
    
    if not rss_urls:
        print("Error: No valid URLs found in RSS_URLS environment variable.")
        exit(1)

    output_file = "output.txt"
    
    if process_watchlist(rss_urls, output_file):
        print("Output file created successfully")
    else:
        print("Failed to create output file")
    
    print(f"\nDone!")

if __name__ == "__main__":
    main()
