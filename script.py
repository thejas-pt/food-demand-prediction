import os
import csv
import requests
import base64
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def get_first_image_from_google(driver, search_query):
    driver.get(f"https://www.google.com/search?q={search_query}&tbm=isch")
    try:
        # Wait for the search div to be visible
        search_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'eA0Zlc')))
        # Find all img elements within the search div using XPath
        img_elements = search_div.find_elements(By.XPATH, './/img[@class="YQ4gaf"]')  # Modified XPath here
        # Get the src attribute of the first img element
        if img_elements:
            image_element = img_elements[0]
            image_url = image_element.get_attribute('src')
            return image_url
        image_url = None
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        image_url = None

    return image_url

# Create the directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Create a logger to log to both terminal and file
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

with open('recipes.csv', mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    
    # Skip the header row if it exists
    next(csv_reader)
    
    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Extract the ingredient from the row
        name = row[1]
        
        # Log the ingredient
        logger.info(f"Processing ingredient: {name}")

        # Ask the user for the search query
        search_query = name

        # Create a Chrome driver
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

        # Get the first image URL
        image_url = get_first_image_from_google(driver, search_query)

        if image_url:
            data_url = image_url

            # Extract the base64-encoded data
            data_index = data_url.find(',') + 1
            image_data = data_url[data_index:]

            # Decode the base64-encoded data
            image_binary = base64.b64decode(image_data)

            # Specify the file path where you want to save the image
            file_path = "images/"+search_query+".jpg"

            # Write the decoded image data to a file
            with open(file_path, 'wb') as f:
                f.write(image_binary)

            logger.info("Image downloaded successfully!")
        else:
            logger.warning("No image found.")

        driver.quit()