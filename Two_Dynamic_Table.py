import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urls = [
    'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08548',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08549',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05285',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08553',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08554',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08555',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05282',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08556',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05288',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08550',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05287',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=08551',
]

driver = webdriver.Chrome()

all_data = []  # List to store dictionaries containing scraped data

for url in urls:
    driver.get(url)
    
    try:
        data = {}  # Dictionary to store heading-value pairs for the current page
        
        # Wait for the rows to be present for the first table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './/div[@class="row group--micro-end-mills"]'))
        )
        
        headings = driver.find_elements(By.XPATH, '//div[@class="row group--micro-end-mills"]//app-hub-attribute[@class="col-md-6"]//div[contains(@class,"attribute__name")]')
        values = driver.find_elements(By.XPATH, '//div[@class="row group--micro-end-mills"]//app-hub-attribute[@class="col-md-6"]//div[contains(@class,"attribute__value")]')
        
        for heading, value in zip(headings, values):
            heading_text = heading.text
            value_text = value.text
            data[heading_text] = value_text
        
        # Wait for the rows to be present for the second table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './/div[@class="row group--product-information"]'))
        )
        
        second_table_headings = driver.find_elements(By.XPATH, '//div[@class="row product-details group--product-information"]/following-sibling::div[1]//div[@class="col-md-4 attribute__name"]')
        second_table_values = driver.find_elements(By.XPATH, '//div[@class="row product-details group--product-information"]/following-sibling::div[1]//div[contains(@class,"value")]')
        
        for heading, value in zip(second_table_headings, second_table_values):
            heading_text = heading.text
            value_text = value.text
            data[heading_text] = value_text
        
        # Extract static data using XPaths
        Title = driver.find_element(By.XPATH, '//h1').text
        Part_Number = driver.find_element(By.XPATH, '//div[@class="d-flex mr-2"]//span[2]').text
        Downloads = driver.find_element(By.XPATH, '//ul//a').text
        
        # Add static data to the dictionary
        data["Title"] = Title
        data["Part_Number"] = Part_Number
        data["Downloadables"] = Downloads
        
        # Add the dictionary to the list
        all_data.append(data)
        
    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()

# Collect all unique headings
all_headings = set()
for data in all_data:
    all_headings.update(data.keys())

# Write data to CSV
csv_file = "app-catsy-output.csv"

with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["URL"] + list(all_headings))
    writer.writeheader()
    
    for data in all_data:
        row = {"URL": data.get("URL")}  # Assuming URL is stored in the dictionary as "URL"
        row.update(data)
        writer.writerow(row)

print("Data saved to:", csv_file)
