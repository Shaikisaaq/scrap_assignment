import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin  # Import urljoin for URL concatenation

# Function to scrape additional information from a product URL
def scrape_product_details(product_url):
    try:
        # Check if the URL is "N/A" and skip processing
        if product_url == "N/A":
            return {
                "Description": "N/A",
                "ASIN": "N/A",
                "Product Description": "N/A",
                "Manufacturer": "N/A",
            }

        # Check if the URL is relative and make it complete
        if product_url.startswith('/'):
            product_url = urljoin(base_url, product_url)

        response = requests.get(product_url)

        if response.status_code != 200:
            return {
                "Description": "N/A",
                "ASIN": "N/A",
                "Product Description": "N/A",
                "Manufacturer": "N/A",
            }

        soup = BeautifulSoup(response.text, 'html.parser')

        # Use the 'string' argument instead of 'text'
        description = soup.find('div', {'id': 'productDescription'}).find(string=True, recursive=False).strip() if soup.find('div', {'id': 'productDescription'}) else "N/A"
        asin = soup.find('th', text='ASIN').find_next('td').string if soup.find('th', text='ASIN') else "N/A"
        manufacturer = soup.find('th', text='Manufacturer').find_next('td').string if soup.find('th', text='Manufacturer') else "N/A"

        # Check if 'description', 'asin', and 'manufacturer' are None and set them to "N/A" if they are
        description = description if description else "N/A"
        asin = asin if asin else "N/A"
        manufacturer = manufacturer if manufacturer else "N/A"

        return {
            "Description": description,
            "ASIN": asin,
            "Product Description": "N/A",  # You can scrape this separately if needed
            "Manufacturer": manufacturer,
        }
    except Exception as e:
        print(f"Error while processing {product_url}: {e}")
        return {
            "Description": "N/A",
            "ASIN": "N/A",
            "Product Description": "N/A",
            "Manufacturer": "N/A",
        }

# Load the list of product URLs from the original CSV file
csv_filename = 'amazon_products.csv'

product_details = []  # Initialize a list to store product details

# Set the base URL
base_url = "https://www.amazon.in"

with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        product_url = row["Product URL"]
        details = scrape_product_details(product_url)
        product_details.append(details)

# Save the product details to a new CSV file
details_csv_filename = 'amazon_product_details.csv'

with open(details_csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ["Description", "ASIN", "Product Description", "Manufacturer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_details)

print(f"Scraped additional details from {len(product_details)} products and saved to {details_csv_filename}")
