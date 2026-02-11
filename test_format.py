import unittest
import xml.etree.ElementTree as ET
from format import extract_item_data, parse_rss_items

class TestFormat(unittest.TestCase):

    def test_extract_item_data_full(self):
        """Test extraction when all fields are present"""
        xml = """
        <item>
            <title>Test Movie (2023)</title>
            <category>movie</category>
            <link>http://example.com/movie</link>
        </item>
        """
        item = ET.fromstring(xml)
        data = extract_item_data(item)
        
        self.assertEqual(data['title'], "Test Movie")
        self.assertEqual(data['year'], "2023")
        self.assertEqual(data['category'], "movie")
        self.assertEqual(data['link'], "http://example.com/movie")

    def test_extract_item_data_missing_year(self):
        """Test extraction when year is missing from title"""
        xml = """
        <item>
            <title>Test Show</title>
            <category>show</category>
            <link>http://example.com/show</link>
        </item>
        """
        item = ET.fromstring(xml)
        data = extract_item_data(item)
        
        self.assertEqual(data['title'], "Test Show")
        self.assertEqual(data['year'], "Unknown release Year")
        self.assertEqual(data['category'], "show")

    def test_extract_item_data_missing_fields(self):
        """Test extraction when optional fields are missing"""
        xml = "<item><title>Just Title</title></item>"
        item = ET.fromstring(xml)
        data = extract_item_data(item)
        
        self.assertEqual(data['title'], "Just Title")
        self.assertEqual(data['category'], "Unknown")
        self.assertEqual(data['link'], "No link")

    def test_parse_rss_items_valid(self):
        """Test parsing valid RSS XML"""
        xml = """
        <rss>
            <channel>
                <item><title>Item 1</title></item>
                <item><title>Item 2</title></item>
            </channel>
        </rss>
        """
        items = parse_rss_items(xml)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].find('title').text, "Item 1")

    def test_parse_rss_items_no_channel(self):
        """Test parsing XML without channel element (fallback)"""
        xml = """
        <root>
            <item><title>Direct Item</title></item>
        </root>
        """
        items = parse_rss_items(xml)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].find('title').text, "Direct Item")

if __name__ == '__main__':
    unittest.main()
