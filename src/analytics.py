"""
RetailX - Business Analytics Module

Provides:
- Sales KPIs
- Profit KPIs
- Category analysis
- Regional analysis
- Customer analysis
- Product analysis
- Monthly trends
- Payment analysis
"""

from pathlib import Path
import logging

import pandas as pd


logger = logging.getLogger(__name__)


# ============================================================
# KPI ANALYSIS
# ============================================================

def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate core business KPIs.
    """

    total_revenue = df["net_revenue"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    total_units = df["quantity"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    profit_margin = (
        total_profit / total_revenue * 100
        if total_revenue > 0
        else 0
    )

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_units_sold": int(total_units),
        "average_order_value": round(
            average_order_value,
            2
        ),
        "profit_margin_pct": round(
            profit_margin,
            2
        ),
    }


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

def category_performance(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze sales and profit by category.
    """

    result = (
        df.groupby("category")
        .agg(
            orders=("order_id", "nunique"),
            units_sold=("quantity", "sum"),
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["profit_margin_pct"] = (
        result["profit"]
        / result["revenue"]
        * 100
    ).round(2)

    result = result.sort_values(
        "revenue",
        ascending=False
    )

    return result


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

def product_performance(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze product-level performance.
    """

    result = (
        df.groupby(
            ["product_id", "product", "category"]
        )
        .agg(
            orders=("order_id", "nunique"),
            units_sold=("quantity", "sum"),
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["profit_margin_pct"] = (
        result["profit"]
        / result["revenue"]
        * 100
    ).round(2)

    return result.sort_values(
        "revenue",
        ascending=False
    )


# ============================================================
# REGIONAL ANALYSIS
# ============================================================

def regional_performance(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze business performance by region.
    """

    result = (
        df.groupby(
            ["region", "state"]
        )
        .agg(
            orders=("order_id", "nunique"),
            customers=("customer_id", "nunique"),
            units_sold=("quantity", "sum"),
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["profit_margin_pct"] = (
        result["profit"]
        / result["revenue"]
        * 100
    ).round(2)

    return result.sort_values(
        "revenue",
        ascending=False
    )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

def customer_performance(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze customer purchasing behavior.
    """

    result = (
        df.groupby(
            ["customer_id", "customer_name"]
        )
        .agg(
            orders=("order_id", "nunique"),
            units_purchased=("quantity", "sum"),
            total_spend=("net_revenue", "sum"),
            total_profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["average_order_value"] = (
        result["total_spend"]
        / result["orders"]
    ).round(2)

    result["profit_margin_pct"] = (
        result["total_profit"]
        / result["total_spend"]
        * 100
    ).round(2)

    return result.sort_values(
        "total_spend",
        ascending=False
    )


# ============================================================
# MONTHLY SALES TREND
# ============================================================

def monthly_sales_trend(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate monthly revenue and profit trends.
    """

    result = (
        df.groupby(
            ["year", "month"]
        )
        .agg(
            orders=("order_id", "nunique"),
            units_sold=("quantity", "sum"),
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["profit_margin_pct"] = (
        result["profit"]
        / result["revenue"]
        * 100
    ).round(2)

    result["period"] = (
        result["year"].astype(str)
        + "-"
        + result["month"].astype(str).str.zfill(2)
    )

    return result.sort_values(
        ["year", "month"]
    )


# ============================================================
# PAYMENT ANALYSIS
# ============================================================

def payment_method_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze revenue by payment method.
    """

    result = (
        df.groupby("payment_mode")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["revenue_share_pct"] = (
        result["revenue"]
        / result["revenue"].sum()
        * 100
    ).round(2)

    return result.sort_values(
        "revenue",
        ascending=False
    )


# ============================================================
# ORDER STATUS ANALYSIS
# ============================================================

def order_status_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze order status distribution.
    """

    result = (
        df.groupby("status")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("net_revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )

    result["order_share_pct"] = (
        result["orders"]
        / result["orders"].sum()
        * 100
    ).round(2)

    return result.sort_values(
        "orders",
        ascending=False
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

def top_products(
    df: pd.DataFrame,
    n: int = 10
) -> pd.DataFrame:
    """
    Return top N products by revenue.
    """

    product_df = product_performance(df)

    return product_df.head(n)


# ============================================================
# TOP CUSTOMERS
# ============================================================

def top_customers(
    df: pd.DataFrame,
    n: int = 10
) -> pd.DataFrame:
    """
    Return top N customers by spending.
    """

    customer_df = customer_performance(df)

    return customer_df.head(n)


# ============================================================
# ANALYTICS SUMMARY
# ============================================================

def generate_summary(
    df: pd.DataFrame
) -> dict:
    """
    Generate a complete analytics summary.
    """

    kpis = calculate_kpis(df)

    summary = {
        "kpis": kpis,
        "top_category": (
            category_performance(df)
            .iloc[0]["category"]
        ),
        "top_product": (
            product_performance(df)
            .iloc[0]["product"]
        ),
        "top_region": (
            regional_performance(df)
            .iloc[0]["region"]
        ),
    }

    return summary


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    from data_loader import load_orders
    from data_cleaning import clean_orders

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    raw_path = (
        project_root
        / "data"
        / "raw"
        / "orders.csv"
    )

    orders = load_orders(raw_path)

    cleaned_orders = clean_orders(
        orders
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    kpis = calculate_kpis(
        cleaned_orders
    )

    print("\n")
    print("=" * 70)
    print("RETAILX BUSINESS ANALYTICS")
    print("=" * 70)

    print("\nCORE KPIs")
    print("-" * 70)

    print(
        f"Total Revenue       : ₹{kpis['total_revenue']:,.2f}"
    )

    print(
        f"Total Profit        : ₹{kpis['total_profit']:,.2f}"
    )

    print(
        f"Total Orders        : {kpis['total_orders']:,}"
    )

    print(
        f"Total Customers     : {kpis['total_customers']:,}"
    )

    print(
        f"Units Sold          : {kpis['total_units_sold']:,}"
    )

    print(
        f"Average Order Value : ₹{kpis['average_order_value']:,.2f}"
    )

    print(
        f"Profit Margin       : {kpis['profit_margin_pct']:.2f}%"
    )

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    print("\nTOP CATEGORIES")
    print("-" * 70)

    print(
        category_performance(
            cleaned_orders
        ).head(10).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Regional
    # --------------------------------------------------------

    print("\nREGIONAL PERFORMANCE")
    print("-" * 70)

    print(
        regional_performance(
            cleaned_orders
        ).head(10).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Top Products
    # --------------------------------------------------------

    print("\nTOP 10 PRODUCTS")
    print("-" * 70)

    print(
        top_products(
            cleaned_orders
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Top Customers
    # --------------------------------------------------------

    print("\nTOP 10 CUSTOMERS")
    print("-" * 70)

    print(
        top_customers(
            cleaned_orders
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Payment
    # --------------------------------------------------------

    print("\nPAYMENT METHOD ANALYSIS")
    print("-" * 70)

    print(
        payment_method_analysis(
            cleaned_orders
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Order Status
    # --------------------------------------------------------

    print("\nORDER STATUS ANALYSIS")
    print("-" * 70)

    print(
        order_status_analysis(
            cleaned_orders
        ).to_string(
            index=False
        )
    )

    print("\n" + "=" * 70)
    print("ANALYTICS COMPLETED SUCCESSFULLY")
    print("=" * 70)
