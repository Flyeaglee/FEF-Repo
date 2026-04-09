
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
import re
import json

url = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
content = response.text

# Try different patterns for Next.js data
patterns = [
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
    r'<script id="__NEXT_DATA__">(.*?)</script>',
    r'window\.__NEXT_DATA__\s*=\s*(\{.*?\});?'
]

for pattern in patterns:
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print(f"Found match with pattern: {pattern[:50]}...")
        try:
            data = json.loads(match.group(1))
            print(f"Successfully parsed! Keys: {list(data.keys())[:5]}")
            break
        except Exception as e:
            print(f"Failed to parse: {e}")

# Look for any script tags with large content
print("\n\nLooking for large script tags...")
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
large_scripts = [(i, len(s)) for i, s in enumerate(scripts) if len(s) > 1000]
print(f"Found {len(large_scripts)} large scripts")
for idx, length in large_scripts[:5]:
    print(f"  Script {idx}: {length} chars")
    # Check if it contains data
    if 'portfolio' in scripts[idx].lower() or 'subnet' in scripts[idx].lower():
        print(f"    -> Contains portfolio/subnet data")
        print(f"    -> First 200 chars: {scripts[idx][:200]}")

# Look for API endpoints in the page
print("\n\nLooking for API endpoints...")
api_patterns = [
    r'["\'](https?://[^"\']*api[^"\'"]*)["\']',
    r'["\'](/api/[^"\'"]*)["\']',
    r'fetch\(["\']([^"\'"]+)["\']\)'
]
for pattern in api_patterns:
    matches = re.findall(pattern, content)
    if matches:
        print(f"Found API endpoints: {matches[:5]}")