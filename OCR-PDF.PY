import pdfplumber
import pandas as pd 

def extract_invoice_data(invoice_file):
    """Extracts invoice data from a PDF file.

    Args:   
        invoice_file: The path to the PDF file.

    Returns:
        A Pandas DataFrame containing the extracted invoice data.
    """

    with pdfplumber.open(invoice_file) as pdf:
        first_page = pdf.pages[0]

        # Extract the brand name.
        brand_name = first_page.extract_text()[first_page.extract_text().find("Brand:") + 6:]

        # Extract the address.
        address = first_page.extract_text()[first_page.extract_text().find("Address:") + 8:]

        # Extract the customer name.
        customer_name = first_page.extract_text()[first_page.extract_text().find("Customer Name:") + 13:]

        # Extract the customer address.
        customer_address = first_page.extract_text()[first_page.extract_text().find("Customer Address:") + 17:]

        # Extract the product descriptions and prices.
        product_descriptions = []
        prices = []

        for table in first_page.extract_tables():
            for row in table:
                if len(row) >= 2:
                    product_descriptions.append(row[0])
                    prices.append(row[1])

        # Calculate the grand total.
        grand_total = sum(prices)

        # Ensure the product descriptions and prices have the same length.
        min_length = min(len(product_descriptions), len(prices))
        product_descriptions = product_descriptions[:min_length]
        prices = prices[:min_length]

        # Create a Pandas DataFrame containing the extracted invoice data.
        invoice_data = pd.DataFrame({
            "Brand": [brand_name],
            "Address": [address],
            "Customer Name": [customer_name],
            "Customer Address": [customer_address],
            "Description of Product": product_descriptions,
            "Price": prices
        })

        return invoice_data


def save_invoice_data_to_excel(invoice_data, excel_file):
    # Save the Pandas DataFrame to an Excel file.
    invoice_data.to_excel(excel_file, index=False)

# Example usage:
invoice_file = "Test.pdf"
excel_file = "invoice.xlsx"

invoice_data = extract_invoice_data(invoice_file)
save_invoice_data_to_excel(invoice_data, excel_file)
