import pandas as pd
import os

# Function to load the dataset
def load_data(file_path):
    """Load the dataset from a CSV file."""
    df = pd.read_csv(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

# Function to compute total revenue, total orders, and total quantity sold
def get_sales_summary(df):
    total_revenue = float(df['Total Sales (INR)'].sum())
    total_orders = int(df['Order ID'].nunique())
    total_quantity = int(df['Quantity Sold'].sum())
    return {
        'Total Revenue': total_revenue,
        'Total Orders': total_orders,
        'Total Quantity Sold': total_quantity
    }

# Function to analyze sales over time
def get_sales_trends(df):
    daily_sales = df.groupby(df['Order Date'].dt.date)['Total Sales (INR)'].sum().astype(float).to_dict()
    weekly_sales = df.groupby(df['Order Date'].dt.to_period('W'))['Total Sales (INR)'].sum().astype(float).to_dict()
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Total Sales (INR)'].sum().astype(float).to_dict()
    
    highest_month = max(monthly_sales, key=monthly_sales.get)
    lowest_month = min(monthly_sales, key=monthly_sales.get)
    
    return {
        #'Daily Sales': daily_sales,
        #'Weekly Sales': weekly_sales,
        'Monthly Sales': monthly_sales,
        'Highest Sales Month': highest_month,
        'Lowest Sales Month': lowest_month
    }

# Function to find top-selling and least-selling products
def get_product_sales(df, top_n=10):
    top_products = df.groupby('Product Name')['Quantity Sold'].sum().nlargest(top_n).astype(int).to_dict()
    least_products = df.groupby('Product Name')['Quantity Sold'].sum().nsmallest(top_n).astype(int).to_dict()
    return {
        'Top Selling Products': top_products,
        'Least Selling Products': least_products
    }

# Function to calculate average selling price
def get_avg_selling_price(df):
    return float(df['Price (INR)'].mean())

# Function to analyze revenue distribution by category
def get_revenue_by_category(df):
    return df.groupby('Category')['Total Sales (INR)'].sum().astype(float).to_dict()

# Function to analyze customer rating distribution
def get_customer_rating_distribution(df):
    return df['Customer Rating'].value_counts(normalize=True).mul(100).astype(float).to_dict()

# Function to find correlation between ratings and sales
def get_rating_sales_correlation(df):
    return df[['Customer Rating', 'Total Sales (INR)']].corr().to_dict()

# Function to analyze price distribution
def get_price_distribution(df):
    return df['Price (INR)'].describe().to_dict()

# Function to check if lower-priced products sell more
def get_price_vs_sales(df):
    return df.groupby(pd.qcut(df['Price (INR)'], q=4))['Quantity Sold'].sum().astype(int).to_dict()

# Function to get common payment methods
def get_payment_methods(df):
    return df['Payment Method'].value_counts().to_dict()

# Function to find highest return rate categories
def get_highest_return_categories(df):
    if 'Return Status' in df.columns:
        return df[df['Return Status'] == 'Returned'].groupby('Category').size().nlargest(5).astype(int).to_dict()
    return "Return data not available"

# Function to flatten nested dictionaries
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Main function to analyze the dataset
def analyze_sales_data():
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    file_path = os.path.join(os.path.dirname(__file__), '../flipkart_sales.csv')
    
    try:
        df = load_data(file_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"error": "Failed to load data"}

    analysis = {}
    
    try:
        analysis['Sales Summary'] = get_sales_summary(df)
        analysis['Sales Trends'] = get_sales_trends(df)
        analysis['Product Sales'] = get_product_sales(df)
        analysis['Average Selling Price'] = get_avg_selling_price(df)
        analysis['Revenue by Category'] = get_revenue_by_category(df)
        #analysis['Customer Rating Distribution'] = get_customer_rating_distribution(df)
        #analysis['Rating vs Sales Correlation'] = get_rating_sales_correlation(df)
        #analysis['Average Quantity Per Order'] = get_avg_quantity_per_order(df)
        analysis['Price Distribution'] = get_price_distribution(df)
        #analysis['Price vs Sales'] = get_price_vs_sales(df)
        analysis['Payment Methods'] = get_payment_methods(df)
        #analysis['Highest Return Categories'] = get_highest_return_categories(df)
    except Exception as e:
        print(f"Error during analysis: {e}")
        return {"error": "Failed to perform analysis"}

    flattened_analysis = flatten_dict(analysis)
    
    return flattened_analysis

# Example usage
if __name__ == "__main__":
    result = analyze_sales_data()
    print(result)