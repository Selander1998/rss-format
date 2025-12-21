import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import os
from dotenv import load_dotenv

def parse_watchlist_from_url(url, output_file_path="plex_watchlist.txt"):
    try:
        print(f"Fetching data from: {url}")
        with urllib.request.urlopen(url) as response:
            xml_content = response.read()
        
        root = ET.fromstring(xml_content)
        
        channel = root.find('channel')
        if channel is None:
            raise ValueError("No channel element found in RSS feed")
        
        items = channel.findall('item')
        
        print(f"Successfully parsed {len(items)} items from this feed")
        
    except urllib.error.URLError as e:
        print(f"Error fetching URL: {e}")
        return False
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    if not items:
        return False
    
    output_lines = []
    
    for i, item in enumerate(items, 1):
        title = item.find('title').text if item.find('title') is not None else "Unknown Title"
        category = item.find('category').text if item.find('category') is not None else "Unknown"
        link = item.find('link').text if item.find('link') is not None else "No link"
        
        output_lines.append(f"#{i}:")
        output_lines.append(f"   Title: {title}")
        output_lines.append(f"   Type: {category.upper()}")
        output_lines.append(f"   Link: {link}")
        
        output_lines.append("")
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\nSuccessfully parsed {len(items)} total items from watchlist")
    
    return True

if __name__ == "__main__":
    load_dotenv()
    
    RSS_URL = os.getenv('RSS_URL')
    
    if not RSS_URL:
        print("Error: RSS_URL not found in .env file")
        print("Please create a .env file with: RSS_URL=your_rss_url_here")
        exit(1)
    
    OUTPUT_FILE = "output.txt"
    
    if parse_watchlist_from_url(RSS_URL, OUTPUT_FILE):
        print("Output file created successfully")
    else:
        print("Failed to create output file")

    print(f"\nDone!")