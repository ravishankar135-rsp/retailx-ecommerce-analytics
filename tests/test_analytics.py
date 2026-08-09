import sys
from pathlib import Path

import pandas as pd

# Allow importing modules from src/
SRC_PATH = Path(__file__).resolve().parents[1] / "src"

sys.path.insert(0, str(SRC_PATH))

from analytics import calculate_kpis


def test_calculate_kpis():
    df = pd.DataFrame({
        "net_revenue": [1000, 1500, 500],
        "profit": [200, 300, 100],
        "order_id": [1, 2, 3],
        "customer_id": [101, 102, 101],
        "quantity": [2, 3, 1],
    })

    result = calculate_kpis(df)

    # Core KPI validation
    assert result["total_revenue"] == 3000.00
    assert result["total_profit"] == 600.00
    assert result["total_orders"] == 3
    assert result["total_customers"] == 2
    assert result["total_units_sold"] == 6

    # AOV = Revenue / Orders
    assert result["average_order_value"] == 1000.00

    # Profit Margin = Profit / Revenue * 100
    assert result["profit_margin_pct"] == 20.00