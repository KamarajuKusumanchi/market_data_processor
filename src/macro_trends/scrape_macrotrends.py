import requests
from bs4 import BeautifulSoup
import csv


def scrape_macrotrends_to_csv(url, output_filename):
    """
    Scrapes financial data from a Macrotrends URL by directly parsing the HTML table
    using tbody tags for data rows (excluding headers and th tags in tbody),
    and saves it to a CSV file.
    It specifically processes the net income column by removing '$' and keeping it in millions.

    Args:
        url (str): The URL of the Macrotrends page containing the data.
        output_filename (str): The name of the CSV file to save the data to.
    """
    print(f"Fetching data from: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # net_income_mm is 'net income in millions of dollars'
    data_rows = [['year', 'net_income_mm']]

    # Find the main data table
    table = soup.find('table', {'class': 'table'})
    if not table:
        print(
            "Could not find the main data table with class 'table'. Please inspect the page's HTML structure."
        )
        return

    # Extract table rows from tbody
    table_body = table.find('tbody')
    if not table_body:
        print("Could not find the <tbody> tag in the table.")
        return

    for tr in table_body.find_all('tr'):
        row_data = []
        cells = tr.find_all('td')

        # Ensure there are at least two data cells to process 'year' and 'net_income'
        if cells and len(cells) >= 2:
            # The first cell is assumed to be the year
            year = cells[0].get_text(strip=True).replace('\n', ' ').replace('\r', ' ')
            row_data.append(year)

            # Process the second cell (net income)
            net_income_text = cells[1].get_text(strip=True)

            # Remove dollar signs and commas
            cleaned_income = net_income_text.replace('$', '').replace(',', '')

            # Handle negative numbers typically enclosed in parentheses, e.g., (123) -> -123
            if cleaned_income.startswith('(') and cleaned_income.endswith(')'):
                cleaned_income = '-' + cleaned_income[1:-1]

            try:
                # Convert to float (removed multiplication by 1e6 as requested)
                net_income_value = float(cleaned_income)
                row_data.append(net_income_value)
            except ValueError:
                # If parsing fails, append the original text for inspection
                print(
                    f"Warning: Could not parse net income value '{net_income_text}'. Appending as string."
                )
                row_data.append(net_income_text)
            data_rows.append(row_data)

    if len(data_rows) == 1:  # Only contains the header row, no actual data
        print("No data rows found in the <tbody> besides the custom header.")

    # Write data to CSV
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data_rows)
        print(f"Data successfully dumped to {output_filename}")
    except IOError as e:
        print(f"Error writing to CSV file {output_filename}: {e}")


if __name__ == "__main__":
    url = "https://macrotrends.net/stocks/charts/NET/cloudflare/net-income"
    scrape_macrotrends_to_csv(url, "cloudflare_net_income.csv")
