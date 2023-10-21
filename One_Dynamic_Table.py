import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urls = [
    'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05300',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05309',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05303',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05308',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05307',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05306',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05305',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05311',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05314',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05313',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05312',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05319',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05318',
'https://app.catsy.com/app/share/739/o/collections/4004662148/digitalcatalog/item?sku=05317',]

driver = webdriver.Chrome()

all_data = []  # List to store dictionaries containing scraped data

for url in urls:
    driver.get(url)
    
    try:
        data = {}  # Dictionary to store heading-value pairs for the current page
        
        # Wait for the rows to be present (assuming you're waiting for the whole table to load)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './/div[@class="row group--micro-end-mills"]'))
        )
        
        headings = driver.find_elements(By.XPATH, '//div[@class="row group--micro-end-mills"]//app-hub-attribute[@class="col-md-6"]//div[contains(@class,"attribute__name")]')
        values = driver.find_elements(By.XPATH, '//div[@class="row group--micro-end-mills"]//app-hub-attribute[@class="col-md-6"]//div[contains(@class,"attribute__value")]')
        
        for heading, value in zip(headings, values):
            heading_text = heading.text
            value_text = value.text
            data[heading_text] = value_text
        
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
csv_file = "output_data.csv"

with open(csv_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["URL"] + list(all_headings))
    writer.writeheader()
    
    for data in all_data:
        row = {"URL": data.get("URL")}  # Assuming URL is stored in the dictionary as "URL"
        row.update(data)
        writer.writerow(row)

print("Data saved to:", csv_file)
