from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

base_url = 'https://www.airbnb.com'
url = 'https://www.airbnb.com/s/Iowa--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-11-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Iowa%2C%20United%20States&place_id=ChIJGWD48W9e7ocR2VnHV0pj78Y&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change&price_max=39'

data = []  # List to store listing data

while url:
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')

    listing_elements = soup.find_all('div', class_='c4mnd7m dir dir-ltr')

#loop through the listing and find the elements
    
  for element in listing_elements:
        listing_name = element.find('div', class_='t1jojoys dir dir-ltr').text
        listing_description = element.find('span', class_='t6mzqp7 dir dir-ltr').text
        listing_price = element.find('div', '_1jo4hgw').text
        listing_links = ('https://www.airbnb.com') + element.find('a').get('href')
        listing_size = element.find('span', 'dir dir-ltr').text
        
        # Initialize Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(listing_links)
        
        # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        try:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_8x4fjw')))
            
            element_text = element.text
        except:
            element_text = "Element not found"
        
        # Scrape the ratings element
        try:
            ratings_element = driver.find_element(By.CLASS_NAME, '_1uaq0z1l')
            ratings = ratings_element.text
        except:
            ratings = "Ratings not found"
        
        # Close the browser
        driver.quit()
        
        data.append({
            'Name': listing_name,
            'Description': listing_description,
            'Price': listing_price,
            'Links': listing_links,
            'Size': listing_size,
            'Location': element_text,
            'Ratings': ratings  # Add the scraped ratings
        })

    next_page_link = soup.find('a', class_='l1ovpqvx c1ytbx3a dir dir-ltr')

    if next_page_link:
        next_page_url = base_url + next_page_link.get('href')
        url = next_page_url
    else:
        url = None

# Create a DataFrame from the collected data
df = pd.DataFrame(data)
print(df)
df.to_csv("Iowaairbnb_2023_with_element.csv")# change the name as needed(inside the brackets)
