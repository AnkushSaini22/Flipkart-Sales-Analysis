import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    """Load the dataset from a CSV file."""
    df = pd.read_csv(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

def get_unique_categories(df):
    """Return the unique categories available in the dataset."""
    return df['Category'].unique()

def filter_by_category(df, category):
    """Filter the dataset for a selected category."""
    return df[df['Category'] == category]

def total_revenue(category_df):
    """Calculate total revenue for the selected category."""
    return category_df['Total Sales (INR)'].sum()

def top_selling_products(category_df, top_n=5):
    """Get the top N best-selling products by quantity sold."""
    return category_df.groupby('Product Name')['Quantity Sold'].sum().nlargest(top_n)

def average_price_of_top_sold_products(category_df, top_n=5):
    """Calculate the average price of the top N most sold products."""
    top_products = category_df.groupby('Product Name')['Quantity Sold'].sum().nlargest(top_n).index
    return category_df[category_df['Product Name'].isin(top_products)]['Price (INR)'].mean()


def highest_rated_product(category_df):
    """Find the highest-rated product in the category."""
    return category_df.loc[category_df['Customer Rating'].idxmax(), ['Product Name', 'Customer Rating']]

def payment_method_distribution(category_df):
    """Calculate the distribution of payment methods in percentage."""
    return category_df['Payment Method'].value_counts(normalize=True) * 100





def month_with_highest_sales(category_df):
    """Determine the month with the highest sales for the category."""
    return category_df.groupby(category_df['Order Date'].dt.strftime('%B'))['Total Sales (INR)'].sum().idxmax()

def average_customer_rating(category_df):
    """Calculate the average customer rating for the category."""
    return category_df['Customer Rating'].mean()



def price_range_distribution(category_df):
    """Categorize products into price ranges and calculate their distribution."""
    bins = [0, 5000, 10000, 20000, 50000, 100000]
    labels = ['0-5K', '5K-10K', '10K-20K', '20K-50K', '50K+']
    category_df['Price Range'] = pd.cut(category_df['Price (INR)'], bins=bins, labels=labels)
    return category_df['Price Range'].value_counts()

def highest_revenue_low_sales_product(category_df):
    """Find the highest revenue-generating product despite having low sales."""
    return category_df.sort_values(by=['Total Sales (INR)'], ascending=False).head(1)[['Product Name', 'Total Sales (INR)']]

def get_category_data(category_name):
    """Main function to get category data with more analysis instead of plots."""
    file_path = os.path.join(os.path.dirname(__file__), '../flipkart_sales.csv')
    df = load_data(file_path)
    category_df = filter_by_category(df, category_name)

    if category_df.empty:
        return {"error": "No data found for the selected category!"}

    # Get detailed insights
    revenue = total_revenue(category_df)
    top_products = top_selling_products(category_df).to_dict()
    avg_price_value = average_price_of_top_sold_products(category_df)  # Changed logic here
    highest_rated = highest_rated_product(category_df).to_dict()
    avg_rating_value = average_customer_rating(category_df)
    highest_sales_month = month_with_highest_sales(category_df)
    price_distribution = price_range_distribution(category_df).to_dict()
    high_revenue_low_sales = highest_revenue_low_sales_product(category_df).to_dict(orient='records')[0]

    # Compare sales across categories (text format)
    category_sales = df.groupby('Category')['Total Sales (INR)'].sum().sort_values(ascending=False)
    category_sales_text = category_sales.to_dict()

    return {
        "total_revenue": revenue,
        "top_products": top_products,
        "average_price_of_top_sold_products": avg_price_value,  # Now based on high sold products
        "highest_rated_product": highest_rated,
        "avg_rating": avg_rating_value,
        "highest_sales_month": highest_sales_month,
        "price_range_distribution": price_distribution,
        "highest_revenue_low_sales_product": high_revenue_low_sales,
        "category_sales_comparison": category_sales_text
    }
