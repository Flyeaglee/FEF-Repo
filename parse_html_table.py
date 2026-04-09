
import sys, pytest, collections, collections.abc, urllib3.exceptions, _pytest.pytester, numpy;
collections.Mapping = collections.abc.Mapping;
collections.MutableMapping = collections.abc.MutableMapping;
collections.MutableSet = collections.abc.MutableSet;
collections.Sequence = collections.abc.Sequence;
collections.Callable = collections.abc.Callable;
collections.Iterable = collections.abc.Iterable;
collections.Iterator = collections.abc.Iterator;
urllib3.exceptions.SNIMissingWarning = urllib3.exceptions.DependencyWarning;
pytest.RemovedInPytest4Warning = DeprecationWarning;
_pytest.pytester.Testdir = _pytest.pytester.Pytester;
numpy.PINF = numpy.inf;
numpy.unicode_ = numpy.str_;
numpy.bytes_ = numpy.bytes_;
numpy.float_ = numpy.float64;
numpy.string_ = numpy.bytes_;
numpy.NaN = numpy.nan;


import requests
import json
import re
from bs4 import BeautifulSoup

# Try using a CORS proxy to access taostats
proxy = 'https://api.codetabs.com/v1/proxy?quest='
url = proxy + 'https://taostats.io/subnets'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    print(f"Status: {response.status_code}")
    content = response.text
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all tables
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"\nTable {i+1}: {len(rows)} rows")
        
        if len(rows) > 0:
            # Get headers
            headers_row = rows[0]
            header_cells = headers_row.find_all(['th', 'td'])
            headers_text = [cell.get_text(strip=True) for cell in header_cells]
            print(f"Headers: {headers_text[:10]}")
            
            # Check if this looks like subnet data
            if any('subnet' in h.lower() for h in headers_text):
                print("This looks like a subnet table!")
                
                # Extract data rows
                data = []
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(['td', 'th'])
                    row_data = {}
                    for j, cell in enumerate(cells):
                        if j < len(headers_text):
                            row_data[headers_text[j]] = cell.get_text(strip=True)
                    if row_data:
                        data.append(row_data)
                
                print(f"Extracted {len(data)} data rows")
                if data:
                    print(f"Sample row: {data[0]}")
                break
    
    # Also try to find div-based tables or grid layouts
    print("\n\nLooking for div-based data structures...")
    
    # Look for rows with subnet data
    all_text = soup.get_text()
    
    # Try to find subnet numbers and associated data
    subnet_pattern = r'Subnet\s+(\d+)'
    subnets = re.findall(subnet_pattern, all_text)
    print(f"Found {len(subnets)} subnet references: {subnets[:10]}")
    
    # Look for price patterns
    price_pattern = r'\$([\d,]+\.?\d*)'
    prices = re.findall(price_pattern, all_text)
    print(f"Found {len(prices)} price values: {prices[:10]}")
    
    # Look for TAO emission patterns
    tao_pattern = r'([\d,]+\.?\d*)\s*TAO'
    tao_values = re.findall(tao_pattern, all_text)
    print(f"Found {len(tao_values)} TAO values: {tao_values[:10]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()