"""
Selenium-based analyzer for dynamic content and performance metrics
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json


class SeleniumAnalyzer:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        
    def _setup_driver(self):
        """Initialize Chrome driver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
        
    def analyze_page(self, url):
        """Analyze a single page with Selenium"""
        if not self.driver:
            self._setup_driver()
            
        try:
            start_time = time.time()
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            load_time = time.time() - start_time
            
            # Get performance metrics
            performance_metrics = self.driver.execute_script("""
                return {
                    navigation: performance.timing,
                    paint: performance.getEntriesByType('paint'),
                    navigationTiming: performance.getEntriesByType('navigation')[0]
                };
            """)
            
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract additional dynamic content
            analysis = {
                'url': url,
                'load_time': load_time,
                'performance_metrics': performance_metrics,
                'page_size': len(page_source),
                'has_structured_data': self._check_structured_data(soup),
                'has_analytics': self._check_analytics(soup),
                'has_social_meta': self._check_social_meta(soup),
                'viewport_meta': self._check_viewport(soup),
                'mobile_friendly': self._check_mobile_friendly(soup),
            }
            
            return analysis
            
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'load_time': None,
            }
    
    def _check_structured_data(self, soup):
        """Check for structured data (JSON-LD, microdata, etc.)"""
        has_json_ld = bool(soup.find_all('script', type='application/ld+json'))
        has_microdata = bool(soup.find_all(attrs={'itemscope': True}))
        return has_json_ld or has_microdata
    
    def _check_analytics(self, soup):
        """Check for analytics scripts"""
        scripts = soup.find_all('script')
        analytics_indicators = ['google-analytics', 'gtag', 'ga(', 'analytics', 'mixpanel', 'segment']
        for script in scripts:
            script_text = str(script).lower()
            if any(indicator in script_text for indicator in analytics_indicators):
                return True
        return False
    
    def _check_social_meta(self, soup):
        """Check for social media meta tags"""
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        return len(og_tags) > 0 or len(twitter_tags) > 0
    
    def _check_viewport(self, soup):
        """Check for viewport meta tag"""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return viewport is not None
    
    def _check_mobile_friendly(self, soup):
        """Basic mobile-friendly check"""
        viewport = self._check_viewport(soup)
        # Additional checks can be added here
        return viewport
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None

