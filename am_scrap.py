import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the Amazon product listing page you want to scrape
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Initialize an empty list to store the scraped data
data = []

# Set the number of pages you want to scrape
num_pages = 20

for page_number in range(1, num_pages + 1):
    url = f"{base_url}&page={page_number}"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}")
        continue

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data from the page
    for product in soup.find_all('div', {'class': 's-result-item'}):
        product_data = {
            "Product URL": product.find('a', {'class': 'a-link-normal'})['href'] if product.find('a', {'class': 'a-link-normal'}) else 'N/A',
            "Product Name": product.find('span', {'class': 'a-text-normal'}).text if product.find('span', {'class': 'a-text-normal'}) else 'N/A',
            "Product Price": product.find('span', {'class': 'a-price'}).text if product.find('span', {'class': 'a-price'}) else 'N/A',
            "Rating": product.find('span', {'class': 'a-icon-alt'}).text if product.find('span', {'class': 'a-icon-alt'}) else 'N/A',
            "Number of Reviews": product.find('span', {'class': 'a-size-base'}).text if product.find('span', {'class': 'a-size-base'}) else 'N/A',
        }
        data.append(product_data)

# Save the data to a CSV file
csv_filename = 'amazon_product.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Scraped data from {len(data)} products and saved to {csv_filename}")
