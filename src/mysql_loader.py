import mysql.connector
import pandas as pd


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "ravi",
    "database": "retailx",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def load_inventory_risk():
    query = """
        SELECT *
        FROM inventory_risk_view
        ORDER BY risk_score DESC, units_sold DESC
    """

    connection = get_connection()

    try:
        return pd.read_sql(query, connection)
    finally:
        connection.close()


if __name__ == "__main__":
    df = load_inventory_risk()

    print("\n" + "=" * 70)
    print("RETAILX MYSQL INVENTORY RISK")
    print("=" * 70)

    print(f"Records loaded : {len(df)}")
    print(f"Columns        : {len(df.columns)}")

    print("\nTOP 10 INVENTORY RISKS\n")
    print(df.head(10).to_string(index=False))