"""
RetailX - Data Loader

Purpose:
    Load and validate raw e-commerce order data.

Responsibilities:
    1. Read CSV data
    2. Validate schema
    3. Validate data types
    4. Handle missing/invalid records
    5. Return a Pandas DataFrame
"""

from pathlib import Path
import logging

import pandas as pd


# ============================================================
# Logging Configuration
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# Custom Exceptions
# ============================================================

class DataLoaderError(Exception):
    """Base exception for data loader errors."""
    pass


class DataFileNotFoundError(DataLoaderError):
    """Raised when the input data file does not exist."""
    pass


class InvalidSchemaError(DataLoaderError):
    """Raised when the dataset schema is invalid."""
    pass


# ============================================================
# Required Columns
# ============================================================

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "city",
    "state",
    "region",
    "product_id",
    "product",
    "category",
    "quantity",
    "unit_price",
    "cost_price",
    "discount_pct",
    "discount_amount",
    "shipping_cost",
    "gross_revenue",
    "net_revenue",
    "total_cost",
    "profit",
    "profit_margin_pct",
    "payment_mode",
    "status",
    "delivery_days",
    "warehouse",
}


# ============================================================
# Data Type Configuration
# ============================================================

NUMERIC_COLUMNS = [
    "quantity",
    "unit_price",
    "cost_price",
    "discount_pct",
    "discount_amount",
    "shipping_cost",
    "gross_revenue",
    "net_revenue",
    "total_cost",
    "profit",
    "profit_margin_pct",
    "delivery_days",
]


# ============================================================
# Schema Validation
# ============================================================

def validate_schema(df: pd.DataFrame) -> None:
    """
    Validate whether the dataset contains all required columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    Raises
    ------
    InvalidSchemaError
        If required columns are missing.
    """

    actual_columns = set(df.columns)

    missing_columns = REQUIRED_COLUMNS - actual_columns

    if missing_columns:
        raise InvalidSchemaError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    logger.info("Dataset schema validation successful.")


# ============================================================
# Data Type Conversion
# ============================================================

def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dataset columns into appropriate data types.
    """

    df = df.copy()

    # Date conversion
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Numeric conversion
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# ============================================================
# Data Validation
# ============================================================

def validate_data(df: pd.DataFrame) -> None:
    """
    Perform basic business-level data validation.
    """

    if (df["quantity"] <= 0).any():
        raise DataLoaderError(
            "Invalid quantity detected. Quantity must be greater than 0."
        )

    if (df["unit_price"] < 0).any():
        raise DataLoaderError(
            "Invalid unit price detected."
        )

    if (df["cost_price"] < 0).any():
        raise DataLoaderError(
            "Invalid cost price detected."
        )

    if ((df["discount_pct"] < 0) | (df["discount_pct"] > 100)).any():
        raise DataLoaderError(
            "Discount percentage must be between 0 and 100."
        )

    logger.info("Business validation successful.")


# ============================================================
# Load Orders
# ============================================================

def load_orders(filepath: str | Path) -> pd.DataFrame:
    """
    Load and validate RetailX order data.

    Parameters
    ----------
    filepath : str | Path
        Path to orders.csv.

    Returns
    -------
    pd.DataFrame
        Validated order dataset.
    """

    filepath = Path(filepath)

    # Check file existence
    if not filepath.exists():
        raise DataFileNotFoundError(
            f"Data file not found: {filepath}"
        )

    logger.info("Loading dataset from %s", filepath)

    try:
        df = pd.read_csv(filepath)

    except Exception as exc:
        raise DataLoaderError(
            f"Unable to read CSV file: {exc}"
        ) from exc

    # Basic check
    if df.empty:
        raise DataLoaderError(
            "Dataset is empty."
        )

    # Validate schema
    validate_schema(df)

    # Convert types
    df = convert_data_types(df)

    # Validate data
    validate_data(df)

    logger.info(
        "Dataset loaded successfully: %d rows, %d columns",
        df.shape[0],
        df.shape[1],
    )

    return df


# ============================================================
# Dataset Summary
# ============================================================

def get_dataset_summary(df: pd.DataFrame) -> dict:
    """
    Generate a basic dataset summary.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_revenue": round(
            df["net_revenue"].sum(),
            2
        ),
        "total_profit": round(
            df["profit"].sum(),
            2
        ),
    }


# ============================================================
# Main Execution
# ============================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    project_root = Path(__file__).resolve().parents[1]

    data_path = (
        project_root
        / "data"
        / "raw"
        / "orders.csv"
    )

    try:

        orders_df = load_orders(data_path)

        summary = get_dataset_summary(
            orders_df
        )

        print("\n" + "=" * 60)
        print("RETAILX DATA LOADER")
        print("=" * 60)

        print(
            f"Rows              : {summary['rows']:,}"
        )

        print(
            f"Columns           : {summary['columns']}"
        )

        print(
            f"Missing Values    : {summary['missing_values']:,}"
        )

        print(
            f"Duplicate Rows    : {summary['duplicate_rows']:,}"
        )

        print(
            f"Total Revenue     : ₹{summary['total_revenue']:,.2f}"
        )

        print(
            f"Total Profit      : ₹{summary['total_profit']:,.2f}"
        )

        print("=" * 60)

    except DataLoaderError as exc:

        logger.error("Data loading failed: %s", exc)
