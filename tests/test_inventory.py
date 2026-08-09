import sys
from pathlib import Path

import pandas as pd

# Allow importing modules from src/
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_PATH))

from inventory import (
    calculate_inventory_kpis,
    stock_health,
    reorder_analysis,
    warehouse_performance,
    category_inventory,
    inventory_risk,
)


def sample_inventory():
    """Create a small test dataset."""

    return pd.DataFrame({
        "product_id": ["P1", "P2", "P3"],
        "product": ["Laptop", "Mouse", "Keyboard"],
        "category": ["Electronics", "Electronics", "Electronics"],
        "warehouse": ["WH-North", "WH-West", "WH-North"],
        "stock_quantity": [100, 5, 0],
        "reorder_level": [20, 10, 15],
        "reorder_quantity": [50, 30, 25],
        "unit_cost": [50000, 500, 1000],
        "inventory_value": [5000000, 2500, 0],
        "lead_time_days": [5, 3, 4],
        "safety_stock": [10, 5, 5],
        "stock_status": [
            "Healthy",
            "Low Stock",
            "Out of Stock",
        ],
    })


def test_calculate_inventory_kpis():

    df = sample_inventory()

    result = calculate_inventory_kpis(df)

    assert result["total_stock_units"] == 105
    assert result["total_inventory_value"] == 5002500
    assert result["total_products"] == 3
    assert result["total_warehouses"] == 2

    assert result["healthy_items"] == 1
    assert result["low_stock_items"] == 1
    assert result["out_of_stock_items"] == 1


def test_stock_health():

    df = sample_inventory()

    result = stock_health(df)

    assert set(
        result["stock_status"]
    ) == {
        "Healthy",
        "Low Stock",
        "Out of Stock",
    }

    assert result["items"].sum() == 3


def test_reorder_analysis():

    df = sample_inventory()

    result = reorder_analysis(df)

    # P2 and P3 should require reorder
    assert len(result) == 2

    assert set(
        result["product_id"]
    ) == {"P2", "P3"}

    # Out of stock should be urgent
    out_of_stock = result[
        result["stock_status"] == "Out of Stock"
    ]

    assert (
        out_of_stock.iloc[0]["recommended_action"]
        == "Urgent Reorder"
    )


def test_warehouse_performance():

    df = sample_inventory()

    result = warehouse_performance(df)

    assert len(result) == 2

    assert (
        result["stock_units"].sum()
        == 105
    )

    assert (
        result["inventory_value"].sum()
        == 5002500
    )


def test_category_inventory():

    df = sample_inventory()

    result = category_inventory(df)

    assert len(result) == 1

    assert (
        result.iloc[0]["category"]
        == "Electronics"
    )

    assert (
        result.iloc[0]["stock_units"]
        == 105
    )


def test_inventory_risk():

    df = sample_inventory()

    result = inventory_risk(df)

    # Highest risk should be Out of Stock
    assert (
        result.iloc[0]["stock_status"]
        == "Out of Stock"
    )

    assert (
        result.iloc[0]["risk_score"]
        == 2
    )

    # Lowest stock coverage should be highest risk
    assert (
        result.iloc[0]["stock_coverage_ratio"]
        == 0.0
    )