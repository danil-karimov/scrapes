import pandas as pd
import pdfplumber

pd.set_option('display.max_columns', None)


def extract_tables_from_pdf(pdf_path, start_page=3):
    # Initialize a list to store DataFrames for each table
    dfs = []

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through each page starting from 'start_page' to the end
        for page_number in range(start_page - 1, len(pdf.pages) -1):
            # Get the specific page
            page = pdf.pages[page_number]

            # Extract the table using 'vertical_strategy'
            table_settings = {
                # "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "text_x_tolerance": 2,
                "text_y_tolerance": 0,
                "intersection_tolerance": 0
            }

            # Extract tables; it's a list because one page might contain multiple tables
            tables = page.extract_tables(table_settings)

            for table in tables:
                # Convert the table to a DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])

                # Append the DataFrame to the list
                dfs.append(df)

    return dfs

# Define the PDF path
pdf_path = "MarketT_290923.pdf"

# Extract table from page 3
dfs = extract_tables_from_pdf(pdf_path)

# dfs.to_csv('extracted_tables.csv', index=False)
with pd.ExcelWriter('extracted_tables.xlsx') as writer:
    for i, df in enumerate(dfs):
        df.to_excel(writer, sheet_name=f'Table{i}', index=False)

# Чтение всех листов из исходного Excel-файла
xls = pd.ExcelFile('extracted_tables.xlsx')
sheet_names = xls.sheet_names  # Список всех листов

# Обработка каждого листа и сохранение результатов в словаре
cleaned_dfs = {}
for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = df.dropna()
    # df.reset_index(drop=True, inplace=True)
    cleaned_dfs[sheet] = df

# Запись всех обработанных DataFrame в новый Excel-файл
with pd.ExcelWriter('extracted_tables_cleaned.xlsx') as writer:
    for sheet, df in cleaned_dfs.items():
        df.to_excel(writer, sheet_name=sheet, index=False)

# Создание пустого DataFrame для хранения объединенных данных
combined_df = pd.DataFrame()

# Чтение всех листов и их объединение
with pd.ExcelFile('extracted_tables_cleaned.xlsx') as xls:
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        combined_df = pd.concat([combined_df, df])
# final_df = pd.concat(cleaned_dfs, ignore_index=True)

combined_df.to_excel('combined_extracted_tables.xlsx', index=False)
