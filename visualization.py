"""
RetailX - Visualization Module

Generates business and inventory charts for reporting.
"""

from pathlib import Path
import logging

import matplotlib.pyplot as plt
import pandas as pd


logger = logging.getLogger(__name__)


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "orders.csv"

INVENTORY_DATA = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "inventory_master.csv"
)

FIGURE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Load Data
# ============================================================

def load_data():

    orders = pd.read_csv(
        RAW_DATA,
        parse_dates=["order_date"]
    )

    inventory = pd.read_csv(
        INVENTORY_DATA
    )

    return orders, inventory


# ============================================================
# 1. Monthly Revenue Trend
# ============================================================

def monthly_revenue_chart(df):

    monthly = (
        df.groupby(
            df["order_date"].dt.to_period("M")
        )["net_revenue"]
        .sum()
        .reset_index()
    )

    monthly["order_date"] = (
        monthly["order_date"]
        .astype(str)
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly["order_date"],
        monthly["net_revenue"],
        marker="o"
    )

    plt.title(
        "RetailX Monthly Revenue Trend"
    )

    plt.xlabel("Month")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "monthly_revenue_trend.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()

    logger.info(
        "Created %s",
        output
    )


# ============================================================
# 2. Category Revenue
# ============================================================

def category_revenue_chart(df):

    category = (
        df.groupby("category")[
            "net_revenue"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    plt.figure(figsize=(10, 6))

    category.plot(
        kind="bar"
    )

    plt.title(
        "Revenue by Product Category"
    )

    plt.xlabel("Category")
    plt.ylabel("Revenue")

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "category_revenue.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# 3. Category Profit
# ============================================================

def category_profit_chart(df):

    category = (
        df.groupby("category")[
            "profit"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    plt.figure(figsize=(10, 6))

    category.plot(
        kind="bar"
    )

    plt.title(
        "Profit by Product Category"
    )

    plt.xlabel("Category")
    plt.ylabel("Profit")

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "category_profit.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# 4. Payment Method Revenue
# ============================================================

def payment_revenue_chart(df):

    payment = (
        df.groupby("payment_mode")[
            "net_revenue"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    plt.figure(figsize=(10, 6))

    payment.plot(
        kind="bar"
    )

    plt.title(
        "Revenue by Payment Method"
    )

    plt.xlabel("Payment Method")
    plt.ylabel("Revenue")

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "payment_method_revenue.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# 5. Warehouse Inventory Value
# ============================================================

def warehouse_inventory_chart(
    inventory
):

    warehouse = (
        inventory.groupby("warehouse")[
            "inventory_value"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    plt.figure(figsize=(10, 6))

    warehouse.plot(
        kind="bar"
    )

    plt.title(
        "Inventory Value by Warehouse"
    )

    plt.xlabel("Warehouse")
    plt.ylabel("Inventory Value")

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "warehouse_inventory_value.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# 6. Stock Health
# ============================================================

def stock_health_chart(
    inventory
):

    stock = (
        inventory["stock_status"]
        .value_counts()
    )

    plt.figure(figsize=(8, 6))

    stock.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        "Inventory Stock Health"
    )

    plt.ylabel("")

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "stock_health.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# 7. Warehouse Risk
# ============================================================

def warehouse_risk_chart(
    inventory
):

    risk = (
        inventory.groupby(
            "warehouse"
        )["stock_status"]
        .apply(
            lambda x:
            (x != "Healthy").sum()
        )
        .sort_values(
            ascending=False
        )
    )

    plt.figure(figsize=(10, 6))

    risk.plot(
        kind="bar"
    )

    plt.title(
        "Inventory Risk by Warehouse"
    )

    plt.xlabel("Warehouse")
    plt.ylabel("Risk Items")

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "warehouse_inventory_risk.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# 8. Top Products by Revenue
# ============================================================

def top_products_chart(df):

    products = (
        df.groupby("product")[
            "net_revenue"
        ]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 7))

    products.plot(
        kind="barh"
    )

    plt.title(
        "Top 10 Products by Revenue"
    )

    plt.xlabel("Revenue")
    plt.ylabel("Product")

    plt.tight_layout()

    output = (
        FIGURE_DIR
        / "top_10_products.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()


# ============================================================
# Generate All Charts
# ============================================================

def generate_all_charts():

    print()
    print("=" * 70)
    print("RETAILX VISUALIZATION ENGINE")
    print("=" * 70)

    orders, inventory = load_data()

    print(
        f"Orders loaded    : {len(orders):,}"
    )

    print(
        f"Inventory records: {len(inventory):,}"
    )

    print()
    print("Generating charts...")

    monthly_revenue_chart(
        orders
    )

    print(
        "✓ Monthly revenue trend"
    )

    category_revenue_chart(
        orders
    )

    print(
        "✓ Category revenue"
    )

    category_profit_chart(
        orders
    )

    print(
        "✓ Category profit"
    )

    payment_revenue_chart(
        orders
    )

    print(
        "✓ Payment method revenue"
    )

    warehouse_inventory_chart(
        inventory
    )

    print(
        "✓ Warehouse inventory"
    )

    stock_health_chart(
        inventory
    )

    print(
        "✓ Stock health"
    )

    warehouse_risk_chart(
        inventory
    )

    print(
        "✓ Warehouse risk"
    )

    top_products_chart(
        orders
    )

    print(
        "✓ Top 10 products"
    )

    print()
    print(
        f"Charts saved to:"
    )

    print(
        FIGURE_DIR
    )

    print()
    print("=" * 70)
    print(
        "VISUALIZATION COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    try:

        generate_all_charts()

    except Exception as exc:

        logger.exception(
            "Visualization failed: %s",
            exc
        )