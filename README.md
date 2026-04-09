# Devin's Subnet Holdings

A simple, one-page dark mode website displaying subnet holdings data for a TAO wallet address.

## Features

- 🌙 **Dark Mode Design**: Modern dark theme with gradient background
- 📊 **Clean Data Table**: Three columns showing Subnet Name, Balance, and Current Price
- 📱 **Responsive Layout**: Works on desktop and mobile devices
- ⚡ **Fast Loading**: Lightweight single HTML file with embedded CSS and JavaScript
- 🔗 **Real-time Data**: Backend proxy server for fetching live data from taostats.io

## Wallet Address

`5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ`

## Quick Start

### Option 1: View Static Page (No Backend)
Simply open `index.html` in any modern web browser. The page will show an info message with a link to taostats.io.

```bash
# Using Python HTTP server
python -m http.server 8000

# Then visit http://localhost:8000
```

### Option 2: Full Setup with Backend Proxy (Recommended)
To see real-time data, start the backend proxy server:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the proxy server
python proxy_server.py

# In another terminal, serve the frontend
python -m http.server 8000

# Visit http://localhost:8000
```

## Data Source

Data is sourced from [taostats.io](https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ).

**Note**: The taostats.io portfolio data requires authentication. The backend proxy server attempts to fetch data, and if authentication is required, it provides a helpful message with a direct link to taostats.io.

## Technical Details

- **Frontend**: Pure HTML5, CSS3, and vanilla JavaScript
- **Backend**: Flask proxy server to bypass CORS restrictions
- **Data Fetching**: Real-time API calls with caching
- **Design**: Gradient text effect, hover effects, responsive layout

## File Structure

```
.
├── index.html        # Main website file
├── proxy_server.py   # Backend proxy server
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## API Endpoints

When the proxy server is running:

- `GET /api/portfolio` - Returns portfolio data for the wallet
- `GET /api/health` - Health check endpoint

## CORS Solution

This implementation uses a backend proxy server to solve CORS issues when fetching data from taostats.io. The proxy server:

1. Makes requests to taostats.io from the server side (no CORS restrictions)
2. Caches responses for 5 minutes to improve performance
3. Returns data in JSON format to the frontend
4. Handles authentication requirements gracefully
