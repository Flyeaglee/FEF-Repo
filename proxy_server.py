#!/usr/bin/env python3
"""
Backend proxy server for fetching taostats.io portfolio data.
This server fetches data from taostats.io and serves it to the frontend,
bypassing CORS restrictions.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import re
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Cache for storing fetched data
cache = {
    'data': None,
    'timestamp': None
}
CACHE_DURATION = 300  # Cache for 5 minutes

WALLET_ADDRESS = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'

def fetch_taostats_data():
    """Fetch portfolio data from taostats.io"""
    url = f'https://taostats.io/pro/portfolio/{WALLET_ADDRESS}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            content = response.text
            
            # Check if we got redirected to login (data is behind auth)
            if 'login' in content.lower() and 'redirect' in content.lower():
                return {
                    'success': False,
                    'error': 'Portfolio data requires authentication. Using fallback data source.',
                    'requiresAuth': True
                }
            
            # Try to extract data from the page
            # Look for JSON data in script tags
            data = extract_data_from_html(content)
            
            if data:
                return {
                    'success': True,
                    'data': data,
                    'source': 'taostats.io',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'Could not extract data from page',
                    'requiresAuth': True
                }
        else:
            return {
                'success': False,
                'error': f'HTTP {response.status_code}',
                'requiresAuth': True
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'requiresAuth': True
        }

def extract_data_from_html(html):
    """Extract subnet holdings data from HTML"""
    # Look for various data patterns
    
    # Pattern 1: Look for JSON in script tags
    json_patterns = [
        r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
        r'window\.__INITIAL_STATE__\s*=\s*({.*?});?',
        r'window\.__DATA__\s*=\s*({.*?});?',
    ]
    
    for pattern in json_patterns:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                # Try to extract portfolio data from the JSON structure
                portfolio_data = extract_portfolio_from_json(data)
                if portfolio_data:
                    return portfolio_data
            except:
                pass
    
    # Pattern 2: Look for table data
    # This would parse HTML tables if present
    
    return None

def extract_portfolio_from_json(data):
    """Extract portfolio data from parsed JSON"""
    # Navigate through common React/Next.js data structures
    if isinstance(data, dict):
        # Check for Next.js data structure
        if 'props' in data and 'pageProps' in data['props']:
            page_props = data['props']['pageProps']
            # Look for portfolio or subnet data
            for key in ['portfolio', 'subnets', 'holdings', 'data']:
                if key in page_props:
                    return page_props[key]
    
    return None

def get_fallback_data():
    """Get fallback data from alternative sources or return empty"""
    # Since taostats requires auth, we return an empty structure
    # In a real scenario, you might want to use a different data source
    return {
        'success': True,
        'data': [],
        'source': 'fallback',
        'message': 'Portfolio data requires taostats.io Pro subscription. Please visit the taostats.io link directly.',
        'timestamp': datetime.now().isoformat()
    }

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """API endpoint to get portfolio data"""
    # Check cache
    if cache['data'] and cache['timestamp']:
        age = (datetime.now() - cache['timestamp']).total_seconds()
        if age < CACHE_DURATION:
            return jsonify(cache['data'])
    
    # Fetch fresh data
    result = fetch_taostats_data()
    
    if result['success']:
        cache['data'] = result
        cache['timestamp'] = datetime.now()
        return jsonify(result)
    else:
        # Return fallback data
        fallback = get_fallback_data()
        return jsonify(fallback)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting proxy server on http://localhost:5000")
    print("API endpoints:")
    print("  - GET /api/portfolio  - Get portfolio data")
    print("  - GET /api/health     - Health check")
    app.run(host='0.0.0.0', port=5000, debug=True)
