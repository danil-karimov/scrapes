# Importing the required libraries
import pdfplumber
import pandas as pd


# Function to extract table from a specific page
def extract_table_from_page(pdf_path, page_number):
    # Open the PDF file
    pdf = pdfplumber.open(pdf_path)

    # Access the specific page
    page = pdf.pages[page_number]

    # Extract tables from the page
    tables = page.extract_tables()

    # Close the PDF file
    pdf.close()

    # Convert the first table to a DataFrame
    if tables:
        df = pd.DataFrame(tables[0])

        # Cleaning the DataFrame (replace None with NaN and remove any '\n')
        df.fillna(value=pd.NA, inplace=True)
        df.replace(r'\n', ' ', regex=True, inplace=True)

        return df
    else:
        return None


# PDF file path
pdf_path = 'MarketT_290923.pdf'  # Replace with the path to your PDF file

# Extract table from page number 3
df = extract_table_from_page(pdf_path, 3)

# Show the extracted table
print(df)
