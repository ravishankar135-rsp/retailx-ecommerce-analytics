"""
RetailX - Data Cleaning Module

Responsibilities:
- Handle missing values
- Remove duplicate records
- Validate business rules
- Detect invalid values
- Create derived metrics
- Save cleaned data
"""

from pathlib import Path
import logging

import pandas as pd


logger = logging.getLogger(__name__)


# ============================================================
# Missing Value Report
# ============================================================

def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a column-wise missing value report.
    """

    report = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percentage": (
            df.isna().mean() * 100
        ).round(2)
    })

    report = report[
        report["missing_count"] > 0
    ].sort_values(
        "missing_count",
        ascending=False
    )

    return report


# ============================================================
# Duplicate Handling
# ============================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate order records.
    """

    before = len(df)

    df = df.drop_duplicates(
        subset=["order_id"]
    ).copy()

    removed = before - len(df)

    logger.info(
        "Duplicate orders removed: %d",
        removed
    )

    return df


# ============================================================
# Missing Value Handling
# ============================================================

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values according to business logic.

    delivery_days can legitimately be missing for orders
    that have not yet been delivered.
    """

    df = df.copy()

    # Text fields
    text_columns = [
        "customer_name",
        "city",
        "state",
        "region",
        "product",
        "category",
        "payment_mode",
        "status",
        "warehouse",
    ]

    for column in text_columns:

        if column in df.columns:
            df[column] = df[column].fillna(
                "Unknown"
            )

    # Numeric fields where zero is meaningful
    numeric_zero_columns = [
        "discount_pct",
        "discount_amount",
        "shipping_cost",
    ]

    for column in numeric_zero_columns:

        if column in df.columns:
            df[column] = df[column].fillna(0)

    # Delivery days:
    # Keep NaN because non-delivered orders do not have
    # a completed delivery duration.
    logger.info(
        "Missing delivery_days values retained "
        "where delivery is not completed."
    )

    return df


# ============================================================
# Business Rule Validation
# ============================================================

def validate_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and remove records that violate core
    business rules.
    """

    df = df.copy()

    initial_rows = len(df)

    # Quantity must be positive
    df = df[
        df["quantity"] > 0
    ]

    # Prices cannot be negative
    df = df[
        df["unit_price"] >= 0
    ]

    df = df[
        df["cost_price"] >= 0
    ]

    # Discount percentage must be 0-100
    df = df[
        df["discount_pct"].between(
            0,
            100
        )
    ]

    # Revenue cannot be negative
    df = df[
        df["gross_revenue"] >= 0
    ]

    # Profit margin should be reasonable
    df = df[
        df["profit_margin_pct"].between(
            -1000,
            1000
        )
    ]

    removed = initial_rows - len(df)

    logger.info(
        "Business-invalid records removed: %d",
        removed
    )

    return df


# ============================================================
# Derived Metrics
# ============================================================

def create_derived_metrics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create additional business metrics.
    """

    df = df.copy()

    # Average selling price per unit
    df["average_selling_price"] = (
        df["net_revenue"] /
        df["quantity"]
    ).round(2)

    # Revenue per order
    df["revenue_per_order"] = (
        df["net_revenue"]
    ).round(2)

    # Profit per order
    df["profit_per_order"] = (
        df["profit"]
    ).round(2)

    # Year
    df["year"] = (
        df["order_date"]
        .dt.year
    )

    # Month
    df["month"] = (
        df["order_date"]
        .dt.month
    )

    # Month name
    df["month_name"] = (
        df["order_date"]
        .dt.month_name()
    )

    # Quarter
    df["quarter"] = (
        "Q" +
        df["order_date"]
        .dt.quarter.astype(str)
    )

    # Day of week
    df["day_of_week"] = (
        df["order_date"]
        .dt.day_name()
    )

    return df


# ============================================================
# Complete Cleaning Pipeline
# ============================================================

def clean_orders(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Execute complete RetailX data-cleaning pipeline.
    """

    logger.info(
        "Starting data cleaning pipeline."
    )

    # 1. Duplicate handling
    df = remove_duplicates(df)

    # 2. Missing values
    df = handle_missing_values(df)

    # 3. Business validation
    df = validate_business_rules(df)

    # 4. Derived metrics
    df = create_derived_metrics(df)

    # Sort by order date
    df = df.sort_values(
        "order_date"
    ).reset_index(drop=True)

    logger.info(
        "Data cleaning completed: %d rows, %d columns",
        df.shape[0],
        df.shape[1]
    )

    return df


# ============================================================
# Save Cleaned Dataset
# ============================================================

def save_cleaned_data(
    df: pd.DataFrame,
    output_path: str | Path
) -> None:
    """
    Save cleaned dataset as CSV.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    logger.info(
        "Cleaned dataset saved to %s",
        output_path
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    # Import loader from same project
    from data_loader import load_orders

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    raw_path = (
        project_root
        / "data"
        / "raw"
        / "orders.csv"
    )

    processed_path = (
        project_root
        / "data"
        / "processed"
        / "orders_cleaned.csv"
    )

    try:

        # Load raw data
        orders_df = load_orders(
            raw_path
        )

        print("\n" + "=" * 60)
        print("BEFORE CLEANING")
        print("=" * 60)

        print(
            f"Rows          : {len(orders_df):,}"
        )

        print(
            f"Columns       : {len(orders_df.columns)}"
        )

        print(
            f"Missing Values: "
            f"{orders_df.isna().sum().sum():,}"
        )

        print(
            f"Duplicates    : "
            f"{orders_df.duplicated().sum():,}"
        )

        # Missing-value report
        report = missing_value_report(
            orders_df
        )

        print("\nMissing Value Report:")
        print(report)

        # Cleaning
        cleaned_df = clean_orders(
            orders_df
        )

        print("\n" + "=" * 60)
        print("AFTER CLEANING")
        print("=" * 60)

        print(
            f"Rows          : {len(cleaned_df):,}"
        )

        print(
            f"Columns       : {len(cleaned_df.columns)}"
        )

        print(
            f"Missing Values: "
            f"{cleaned_df.isna().sum().sum():,}"
        )

        print(
            f"Duplicates    : "
            f"{cleaned_df.duplicated().sum():,}"
        )

        # Save processed dataset
        save_cleaned_data(
            cleaned_df,
            processed_path
        )

        print(
            f"\nCleaned dataset saved at:\n"
            f"{processed_path}"
        )

    except Exception as exc:

        logger.exception(
            "Data cleaning pipeline failed: %s",
            exc
        )
