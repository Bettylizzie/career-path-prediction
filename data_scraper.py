import requests
from bs4 import BeautifulSoup
import json

class CareerDataScraper:
    @staticmethod
    def scrape_occupation_outlook():
        """Scrape career data from online sources"""
        try:
            # Example: Scrape from Bureau of Labor Statistics
            url = "https://www.bls.gov/ooh/"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            careers = []
            for item in soup.select('.ooh-occupation'):
                title = item.select_one('h2 a').text.strip()
                growth = item.select_one('.growth-percent').text.strip()
                salary = item.select_one('.median-salary').text.strip()
                
                careers.append({
                    'title': title,
                    'growth': growth,
                    'salary': salary,
                    'source': 'BLS'
                })
            
            return careers
        except Exception as e:
            print(f"Scraping error: {e}")
            return []