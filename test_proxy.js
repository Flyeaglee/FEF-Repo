// Let's test if we can fetch the page content using a CORS proxy
// We'll use a common public CORS proxy for testing

async function testCorsProxy() {
    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
    const targetUrl = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ';
    
    try {
        console.log('Testing CORS proxy...');
        const response = await fetch(proxyUrl + targetUrl);
        console.log('Response status:', response.status);
        const text = await response.text();
        console.log('Content length:', text.length);
        
        // Check if we got the actual page content
        if (text.includes('subnet') || text.includes('TAO')) {
            console.log('Successfully fetched page content');
        } else {
            console.log('Content may not be what we expected');
        }
        
        return text;
    } catch (error) {
        console.error('Error with CORS proxy:', error);
        return null;
    }
}

testCorsProxy();