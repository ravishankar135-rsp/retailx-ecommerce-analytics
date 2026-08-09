from pathlib import Path

import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "orders.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "inventory_master.csv"
)


# Load orders
orders = pd.read_csv(RAW_DATA)


# Product-level demand and cost
product_summary = (
    orders
    .groupby(
        ["product_id", "product", "category"]
    )
    .agg(
        total_units_sold=("quantity", "sum"),
        avg_unit_cost=("cost_price", "mean")
    )
    .reset_index()
)


rng = np.random.default_rng(42)

warehouses = [
    "WH-North",
    "WH-West",
    "WH-South",
    "WH-East"
]


inventory_records = []


# Create inventory records
for _, product in product_summary.iterrows():

    number_of_warehouses = int(
        rng.integers(1, 4)
    )

    selected_warehouses = rng.choice(
        warehouses,
        size=number_of_warehouses,
        replace=False
    )

    for warehouse in selected_warehouses:

        daily_demand = max(
            product["total_units_sold"] / 365,
            1
        )

        lead_time_days = int(
            rng.integers(2, 11)
        )

        safety_stock = int(
            np.ceil(
                daily_demand *
                rng.uniform(2, 7)
            )
        )

        reorder_level = int(
            np.ceil(
                daily_demand *
                lead_time_days
                + safety_stock
            )
        )

        stock_quantity = max(
            0,
            int(
                np.ceil(
                    reorder_level *
                    rng.uniform(0.5, 2.5)
                )
            )
        )

        reorder_quantity = max(
            10,
            int(
                np.ceil(
                    daily_demand *
                    rng.uniform(15, 35)
                )
            )
        )

        unit_cost = round(
            float(product["avg_unit_cost"]),
            2
        )

        inventory_value = round(
            stock_quantity * unit_cost,
            2
        )

        # Stock classification
        if stock_quantity == 0:

            stock_status = "Out of Stock"

        elif stock_quantity <= reorder_level:

            stock_status = "Low Stock"

        else:

            stock_status = "Healthy"


        inventory_records.append({

            "product_id":
                product["product_id"],

            "product":
                product["product"],

            "category":
                product["category"],

            "warehouse":
                warehouse,

            "stock_quantity":
                stock_quantity,

            "reorder_level":
                reorder_level,

            "reorder_quantity":
                reorder_quantity,

            "unit_cost":
                unit_cost,

            "inventory_value":
                inventory_value,

            "lead_time_days":
                lead_time_days,

            "safety_stock":
                safety_stock,

            "stock_status":
                stock_status
        })


# Create DataFrame
inventory = pd.DataFrame(
    inventory_records
)


# Sort data
inventory = inventory.sort_values(
    [
        "warehouse",
        "category",
        "product_id"
    ]
).reset_index(drop=True)


# Save dataset
inventory.to_csv(
    OUTPUT_FILE,
    index=False
)


# Display result
print()
print("=" * 60)
print("RETAILX INVENTORY MASTER")
print("=" * 60)

print(
    f"Rows       : {len(inventory):,}"
)

print(
    f"Products   : "
    f"{inventory['product_id'].nunique():,}"
)

print(
    f"Warehouses : "
    f"{inventory['warehouse'].nunique()}"
)

print()
print("STOCK STATUS")
print("-" * 60)

print(
    inventory["stock_status"]
    .value_counts()
    .to_string()
)

print()
print("OUTPUT FILE")
print("-" * 60)

print(OUTPUT_FILE)

print("=" * 60)