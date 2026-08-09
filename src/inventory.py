"""
RetailX - Inventory Analytics Engine

Purpose:
    Analyze inventory health, stock levels, reorder requirements,
    warehouse performance and category-level inventory exposure.
"""

from pathlib import Path
import logging

import pandas as pd


# ============================================================
# Configuration
# ============================================================

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "product_id",
    "product",
    "category",
    "warehouse",
    "stock_quantity",
    "reorder_level",
    "reorder_quantity",
    "unit_cost",
    "inventory_value",
    "lead_time_days",
    "safety_stock",
    "stock_status",
}


# ============================================================
# Data Loading
# ============================================================

def load_inventory(filepath: str | Path) -> pd.DataFrame:
    """
    Load inventory master data and validate its schema.
    """

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(
            f"Inventory file not found: {filepath}"
        )

    df = pd.read_csv(filepath)

    missing_columns = (
        REQUIRED_COLUMNS - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing inventory columns: "
            f"{sorted(missing_columns)}"
        )

    logger.info(
        "Inventory loaded: %d rows, %d columns",
        df.shape[0],
        df.shape[1],
    )

    return df


# ============================================================
# Inventory KPIs
# ============================================================

def calculate_inventory_kpis(
    df: pd.DataFrame
) -> dict:
    """
    Calculate core inventory KPIs.
    """

    total_units = int(
        df["stock_quantity"].sum()
    )

    total_inventory_value = (
        df["inventory_value"].sum()
    )

    total_products = (
        df["product_id"].nunique()
    )

    total_warehouses = (
        df["warehouse"].nunique()
    )

    low_stock_items = int(
        (df["stock_status"] == "Low Stock").sum()
    )

    out_of_stock_items = int(
        (df["stock_status"] == "Out of Stock").sum()
    )

    healthy_items = int(
        (df["stock_status"] == "Healthy").sum()
    )

    return {
        "total_stock_units": total_units,
        "total_inventory_value": round(
            total_inventory_value,
            2
        ),
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "healthy_items": healthy_items,
        "low_stock_items": low_stock_items,
        "out_of_stock_items": out_of_stock_items,
    }


# ============================================================
# Stock Health Analysis
# ============================================================

def stock_health(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze inventory health status.
    """

    result = (
        df.groupby("stock_status")
        .agg(
            items=("product_id", "count"),
            stock_units=("stock_quantity", "sum"),
            inventory_value=("inventory_value", "sum"),
        )
        .reset_index()
    )

    result["item_share_pct"] = (
        result["items"]
        / result["items"].sum()
        * 100
    ).round(2)

    return result.sort_values(
        "items",
        ascending=False
    )


# ============================================================
# Reorder Analysis
# ============================================================

def reorder_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Identify products requiring replenishment.
    """

    result = df.copy()

    result["stock_gap"] = (
        result["reorder_level"]
        - result["stock_quantity"]
    )

    result["reorder_required"] = (
        result["stock_quantity"]
        <= result["reorder_level"]
    )

    result["recommended_order_qty"] = (
        result["reorder_quantity"]
    )

    result["recommended_action"] = "No Action"

    result.loc[
        result["stock_status"] == "Low Stock",
        "recommended_action"
    ] = "Reorder"

    result.loc[
        result["stock_status"] == "Out of Stock",
        "recommended_action"
    ] = "Urgent Reorder"

    return result[
        result["reorder_required"]
    ].sort_values(
        ["stock_status", "stock_gap"],
        ascending=[True, False]
    )


# ============================================================
# Warehouse Performance
# ============================================================

def warehouse_performance(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze inventory performance by warehouse.
    """

    result = (
        df.groupby("warehouse")
        .agg(
            products=("product_id", "nunique"),
            stock_units=("stock_quantity", "sum"),
            inventory_value=("inventory_value", "sum"),
            low_stock_items=(
                "stock_status",
                lambda x: (x == "Low Stock").sum()
            ),
            out_of_stock_items=(
                "stock_status",
                lambda x: (x == "Out of Stock").sum()
            ),
        )
        .reset_index()
    )

    result["risk_items"] = (
        result["low_stock_items"]
        + result["out_of_stock_items"]
    )

    result["inventory_share_pct"] = (
        result["inventory_value"]
        / result["inventory_value"].sum()
        * 100
    ).round(2)

    return result.sort_values(
        "inventory_value",
        ascending=False
    )


# ============================================================
# Category Inventory Analysis
# ============================================================

def category_inventory(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze inventory exposure by product category.
    """

    result = (
        df.groupby("category")
        .agg(
            products=("product_id", "nunique"),
            stock_units=("stock_quantity", "sum"),
            inventory_value=("inventory_value", "sum"),
            low_stock_items=(
                "stock_status",
                lambda x: (x == "Low Stock").sum()
            ),
            out_of_stock_items=(
                "stock_status",
                lambda x: (x == "Out of Stock").sum()
            ),
        )
        .reset_index()
    )

    result["risk_items"] = (
        result["low_stock_items"]
        + result["out_of_stock_items"]
    )

    result["inventory_share_pct"] = (
        result["inventory_value"]
        / result["inventory_value"].sum()
        * 100
    ).round(2)

    return result.sort_values(
        "inventory_value",
        ascending=False
    )


# ============================================================
# Product Inventory Analysis
# ============================================================

def product_inventory(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze inventory at product level.
    """

    result = (
        df.groupby(
            ["product_id", "product", "category"]
        )
        .agg(
            warehouses=("warehouse", "nunique"),
            stock_units=("stock_quantity", "sum"),
            inventory_value=("inventory_value", "sum"),
            reorder_level=("reorder_level", "sum"),
            safety_stock=("safety_stock", "sum"),
        )
        .reset_index()
    )

    result["stock_gap"] = (
        result["reorder_level"]
        - result["stock_units"]
    )

    result["needs_reorder"] = (
        result["stock_units"]
        <= result["reorder_level"]
    )

    return result.sort_values(
        "inventory_value",
        ascending=False
    )


# ============================================================
# Inventory Risk
# ============================================================

def inventory_risk(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Rank inventory records by replenishment risk.
    """

    result = df.copy()

    result["risk_score"] = 0

    result.loc[
        result["stock_status"] == "Low Stock",
        "risk_score"
    ] = 1

    result.loc[
        result["stock_status"] == "Out of Stock",
        "risk_score"
    ] = 2

    # Higher score = higher inventory risk
    result["stock_coverage_ratio"] = (
        result["stock_quantity"]
        / result["reorder_level"]
    ).round(2)

    return result.sort_values(
        ["risk_score", "stock_coverage_ratio"],
        ascending=[False, True]
    )


# ============================================================
# Business Insights
# ============================================================

def generate_inventory_insights(
    df: pd.DataFrame
) -> list[str]:
    """
    Generate high-level business insights.
    """

    kpis = calculate_inventory_kpis(df)

    warehouse_df = warehouse_performance(df)
    category_df = category_inventory(df)

    insights = []

    if kpis["out_of_stock_items"] > 0:

        insights.append(
            f"{kpis['out_of_stock_items']} inventory "
            "items are currently out of stock."
        )

    if kpis["low_stock_items"] > 0:

        insights.append(
            f"{kpis['low_stock_items']} inventory "
            "items require replenishment."
        )

    if not warehouse_df.empty:

        top_warehouse = (
            warehouse_df.iloc[0]["warehouse"]
        )

        insights.append(
            f"{top_warehouse} has the highest "
            "inventory value exposure."
        )

    if not category_df.empty:

        top_category = (
            category_df.iloc[0]["category"]
        )

        insights.append(
            f"{top_category} has the highest "
            "inventory value."
        )

    return insights


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    inventory_path = (
        project_root
        / "data"
        / "raw"
        / "inventory_master.csv"
    )

    inventory = load_inventory(
        inventory_path
    )

    # ========================================================
    # KPIs
    # ========================================================

    kpis = calculate_inventory_kpis(
        inventory
    )

    print()
    print("=" * 70)
    print("RETAILX INVENTORY ANALYTICS")
    print("=" * 70)

    print()
    print("INVENTORY KPIs")
    print("-" * 70)

    print(
        f"Total Stock Units       : "
        f"{kpis['total_stock_units']:,}"
    )

    print(
        f"Inventory Value         : "
        f"₹{kpis['total_inventory_value']:,.2f}"
    )

    print(
        f"Total Products          : "
        f"{kpis['total_products']:,}"
    )

    print(
        f"Total Warehouses        : "
        f"{kpis['total_warehouses']}"
    )

    print(
        f"Healthy Items           : "
        f"{kpis['healthy_items']:,}"
    )

    print(
        f"Low Stock Items         : "
        f"{kpis['low_stock_items']:,}"
    )

    print(
        f"Out of Stock Items      : "
        f"{kpis['out_of_stock_items']:,}"
    )

    # ========================================================
    # Stock Health
    # ========================================================

    print()
    print("STOCK HEALTH")
    print("-" * 70)

    print(
        stock_health(
            inventory
        ).to_string(index=False)
    )

    # ========================================================
    # Reorder
    # ========================================================

    print()
    print("REORDER ANALYSIS")
    print("-" * 70)

    reorder_df = reorder_analysis(
        inventory
    )

    print(
        reorder_df[
            [
                "product",
                "category",
                "warehouse",
                "stock_quantity",
                "reorder_level",
                "reorder_quantity",
                "recommended_action",
            ]
        ]
        .head(15)
        .to_string(index=False)
    )

    # ========================================================
    # Warehouse
    # ========================================================

    print()
    print("WAREHOUSE PERFORMANCE")
    print("-" * 70)

    print(
        warehouse_performance(
            inventory
        ).to_string(index=False)
    )

    # ========================================================
    # Category
    # ========================================================

    print()
    print("CATEGORY INVENTORY")
    print("-" * 70)

    print(
        category_inventory(
            inventory
        ).to_string(index=False)
    )

    # ========================================================
    # Top Inventory Risk
    # ========================================================

    print()
    print("TOP INVENTORY RISKS")
    print("-" * 70)

    risk_df = inventory_risk(
        inventory
    )

    print(
        risk_df[
            [
                "product",
                "warehouse",
                "stock_quantity",
                "reorder_level",
                "stock_status",
                "risk_score",
                "stock_coverage_ratio",
            ]
        ]
        .head(15)
        .to_string(index=False)
    )

    # ========================================================
    # Business Insights
    # ========================================================

    print()
    print("BUSINESS INSIGHTS")
    print("-" * 70)

    insights = generate_inventory_insights(
        inventory
    )

    for number, insight in enumerate(
        insights,
        start=1
    ):
        print(
            f"{number}. {insight}"
        )

    print()
    print("=" * 70)
    print("INVENTORY ANALYTICS COMPLETED")
    print("=" * 70)