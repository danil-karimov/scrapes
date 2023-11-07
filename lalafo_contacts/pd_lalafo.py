import pandas as pd

# df = pd.read_excel('/Users/danil/Yandex.Disk.localized/Big data education/scrape_practice/lalafo_contacts/lalafo_contacts.xlsx', )
# df.to_csv('csv_lalafo_contacts.csv', index=False)

df = pd.read_csv('csv_lalafo_contacts.csv')
df.drop_duplicates(subset=['mobile_phone', 'email'], inplace=True)
df['mobile_phone'] = df['mobile_phone'].astype(str).apply(lambda x: x.split('.')[0])
df.to_excel('unique_contacts.xlsx', index=False)
