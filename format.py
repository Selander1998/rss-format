import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import re
import os
from dotenv import load_dotenv

def parse_watchlist_from_url(urls, output_file_path="plex_watchlist.txt"):
    if isinstance(urls, str):
        urls = [urls]
    
    all_items = []
    
    for url in urls:
        try:
            print()
            print(f"Fetching data from: {url}")
            with urllib.request.urlopen(url) as response:
                xml_content = response.read()
            
            root = ET.fromstring(xml_content)
            
            channel = root.find('channel')
            if channel is None:
                raise ValueError("No channel element found in RSS feed")
            
            items = channel.findall('item')
            all_items.extend(items)
            
            print(f"Successfully parsed {len(items)} items from this feed")
            
        except urllib.error.URLError as e:
            print(f"Error fetching URL: {e}")
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    if not all_items:
        return False
    
    output_lines = []
    
    for i, item in enumerate(all_items, 1):
        title_element = item.find('title')
        title_raw = title_element.text if title_element is not None else "Unknown Title"
        
        year_match = re.search(r'\((\d{4})\)', title_raw)
        if year_match:
            year = year_match.group(1)
            title = re.sub(r'\s*\(\d{4}\)\s*', ' ', title_raw).strip()
        else:
            year = "Unknown release Year"
            title = title_raw

        category_element = item.find('category')
        category = category_element.text if category_element is not None else "Unknown"

        link_element = item.find('link')
        link = link_element.text if link_element is not None else "No link"

        output_lines.append(f"#{i}:")
        output_lines.append(f"   Title: {title}")
        output_lines.append(f"   Released: {year}")
        output_lines.append(f"   Type: {category.upper()}")
        output_lines.append(f"   Link: {link}")
        output_lines.append("")
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\nSuccessfully parsed {len(all_items)} total items from watchlist")
    
    return True

if __name__ == "__main__":
    load_dotenv()
    
    rss_urls_env = os.getenv('RSS_URLS')
    
    if not rss_urls_env:
        print("Error: RSS_URLS not found in .env file")
        print("Please create a .env file with: RSS_URLS=url1,url2,url3")
        exit(1)
    
    RSS_URLS = [url.strip() for url in rss_urls_env.split(',')]
    
    OUTPUT_FILE = "output.txt"
    
    if parse_watchlist_from_url(RSS_URLS, OUTPUT_FILE):
        print("Output file created successfully")
    else:
        print("Failed to create output file")

    print(f"\nDone!")