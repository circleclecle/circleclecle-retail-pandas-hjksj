import pandas as pd

try:
    df = pd.read_csv(r'E:\假期实习项目\archive\data.csv', encoding='ISO-8859-1')
except UnicodeDecodeError:
    df = pd.read_csv(r'E:\假期实习项目\archive\data.csv', encoding='utf-8')

print("--- 数据前 5 行 ---")
print(df.head())

print("\n--- 数据基本信息 ---")
print(df.info())

print(f"\n数据形状: {df.shape}")

print("\n--- 数值列统计描述 ---")
print(df.describe())

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df_clean = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]

df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['UnitPrice']

print(f"清洗前数据量: {df.shape[0]} 行")
print(f"清洗后数据量: {df_clean.shape[0]} 行")
print(f"被剔除的脏数据: {df.shape[0] - df_clean.shape[0]} 行")

monthly_sales = df_clean.groupby(df_clean['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
print("\n--- 每月总销售额 ---")
print(monthly_sales)

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

monthly_sales.plot(kind='line', title='Monthly Sales Trend (2010-2011)', figsize=(10, 5))
plt.xlabel('Month')
plt.ylabel('Total Sales (GBP)')
plt.grid(True)

plt.savefig('monthly_sales.png')
plt.show()

print("\n--- Top 10 热销产品 ---")
top_products = df_clean.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print(top_products)

plt.figure(figsize=(12, 6))
top_products.plot(kind='bar', color='skyblue')
plt.title('Top 10 Best-Selling Products by Revenue')
plt.xlabel('Product Description')
plt.ylabel('Total Revenue (GBP)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout() 
plt.savefig('top_products.png')
plt.show()

print("\n--- Top 10 购买大户 (CustomerID) ---")
top_customers = df_clean.dropna(subset=['CustomerID']).groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print(top_customers)

plt.figure(figsize=(10, 5))
top_customers.plot(kind='bar', color='coral')
plt.title('Top 10 Customers by Revenue')
plt.xlabel('Customer ID')
plt.ylabel('Total Spend (GBP)')
plt.xticks(rotation=0) 
plt.tight_layout()
plt.savefig('top_customers.png')
plt.show()
