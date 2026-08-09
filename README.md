# RetailX — E-Commerce Sales & Inventory Analytics Platform

> End-to-end analytics platform for sales performance, profitability, inventory health, warehouse risk, and business intelligence using Python, SQL, Pandas, and MySQL.

## 🚀 Project Overview

RetailX is a modular, production-style analytics platform that transforms raw e-commerce transaction and inventory data into business insights.

The platform combines:

- Python
- Pandas
- NumPy
- Matplotlib
- MySQL
- SQL
- Pytest
- GitHub Actions

## 🎯 Business Problem

E-commerce companies generate large volumes of transactional and inventory data.

RetailX helps answer:

- How much revenue and profit are being generated?
- Which products and categories perform best?
- Which customers contribute the most revenue?
- Which regions perform best?
- Which payment methods generate the most revenue?
- Which products require replenishment?
- Which warehouses have higher inventory exposure?
- Which inventory items have higher business risk?

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │   Raw CSV Data   │
                    │ orders.csv       │
                    │ inventory.csv    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Data Cleaning    │
                    │ & Preparation    │
                    └────────┬─────────┘
                             │
                             ▼
             ┌────────────────────────────────┐
             │       Python Analytics         │
             │ Pandas • NumPy • Business KPI │
             └───────────────┬────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
       ┌─────────────────┐       ┌─────────────────┐
       │ Sales Analytics │       │ Inventory       │
       │ Revenue         │       │ Analytics       │
       │ Profit          │       │ Risk & Reorder  │
       └────────┬────────┘       └────────┬────────┘
                │                         │
                └────────────┬────────────┘
                             ▼
                    ┌──────────────────┐
                    │      MySQL       │
                    │ SQL Analytics    │
                    │ Views & Queries  │
                    └────────┬─────────┘
                             │
                             ▼

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and analytics |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Matplotlib | Business visualization |
| MySQL | Relational database |
| SQL | Business analytics |
| Pytest | Automated testing |
| GitHub Actions | Continuous Integration |
| CSV | Raw data storage |

## 📊 Dataset

### Sales Dataset

- 20,000 orders
- Customer information
- Product information
- Category
- Region
- Quantity
- Pricing
- Discounts
- Revenue
- Cost
- Profit
- Payment method
- Order status
- Delivery information

### Inventory Dataset

- 253 inventory records
- 132 products
- 4 warehouses

Key inventory fields:

- Stock quantity
- Reorder level
- Reorder quantity
- Unit cost
- Inventory value
- Lead time
- Safety stock
- Stock status

## 📈 Business Analytics

RetailX calculates important business KPIs including:

### Sales & Profitability

- Total Revenue
- Total Profit
- Total Orders
- Total Customers
- Units Sold
- Average Order Value
- Profit Margin

### Product Analytics

- Top products
- Product revenue
- Product profitability
- Product performance

### Customer Analytics

- Customer revenue
- Customer segmentation
- High-value customers
- Revenue contribution

### Regional Analytics

- Regional revenue
- Regional performance

### Time-Series Analytics

- Monthly revenue
- Month-over-month growth

### Payment Analytics

- Orders by payment method
- Revenue by payment method
- Average order value

## 📦 Inventory Analytics

RetailX performs:

- Stock health analysis
- Low-stock detection
- Reorder analysis
- Inventory risk scoring
- Warehouse inventory exposure
- Category inventory exposure
- Stock coverage analysis

### Inventory KPIs

| KPI | Result |
|---|---:|
| Total Stock Units | 4,383 |
| Inventory Value | ₹32,112,380.43 |
| Products | 132 |
| Warehouses | 4 |
| Healthy Items | 182 |
| Low Stock Items | 71 |
| Out of Stock Items | 0 |

## 🔎 Inventory Risk Analysis

RetailX identifies inventory items that require replenishment by analyzing:

- Current stock
- Reorder level
- Safety stock
- Inventory exposure
- Warehouse
- Product category

The system generates inventory risk information that can support business decisions related to:

- Reordering
- Stock monitoring
- Warehouse planning
- Inventory optimization

## 🗄️ MySQL & SQL Analytics

RetailX integrates Python analytics with MySQL for structured data storage and SQL-based business analysis.

MySQL analytics include:

- Revenue analysis
- Profit analysis
- Payment-method analysis
- Customer segmentation
- Monthly sales trends
- Inventory analytics
- Inventory risk analysis
- SQL views

Example KPI query:

```sql
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(net_revenue), 2) AS average_order_value
FROM orders;

## 🔗 Python + MySQL Integration

Python connects to MySQL using:

```text
mysql-connector-python

Database configuration is managed through environment variables.

The integration module is:

src/mysql_loader.py

Sensitive database credentials are excluded from GitHub using .gitignore.

📊 Visualizations

RetailX automatically generates:

Monthly Revenue Trend
Category Revenue
Category Profit
Payment Method Revenue
Stock Health
Top 10 Products
Warehouse Inventory Risk
Warehouse Inventory Value

Generated reports are stored in:

reports/figures/
🧪 Testing

RetailX uses Pytest for automated testing.

Current test result:

7 passed in 1.19s

Run tests:

py -m pytest
⚙️ GitHub Actions CI

RetailX includes a GitHub Actions CI pipeline.

The workflow automatically:

Installs dependencies
Runs Pytest
Validates the project

Workflow file:

.github/workflows/tests.yml
📁 Project Structure
retailx-ecommerce-analytics/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── data/
│   └── raw/
│       ├── orders.csv
│       └── inventory_master.csv
│
├── reports/
│   └── figures/
│
├── src/
│   ├── analytics.py
│   ├── data_cleaning.py
│   ├── data_loader.py
│   ├── inventory.py
│   ├── inventory_master.py
│   ├── main.py
│   ├── mysql_loader.py
│   └── visualization.py
│
├── tests/
│   ├── test_analytics.py
│   └── test_inventory.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
▶️ Installation

Clone the repository:

git clone https://github.com/ravishankar135-rsp/retailx-ecommerce-analytics.git

Move into the project:

cd retailx-ecommerce-analytics

Install dependencies:

py -m pip install -r requirements.txt
▶️ Run the Project

Run the complete pipeline:

py src/main.py

Run tests:

py -m pytest
💡 Key Business Insights

RetailX identifies:

Inventory items requiring replenishment.
Warehouse-level inventory exposure.
Category-level inventory exposure.
High-performing products and categories.
High-value customer segments.
Payment-method revenue distribution.
Monthly revenue trends.
Profitability trends.
🔮 Future Improvements
Power BI dashboard
Streamlit dashboard
FastAPI REST API
Docker deployment
Cloud database
Scheduled ETL pipelines
Demand forecasting
ML-based inventory prediction
🎤 MNC Interview Highlights
What is RetailX?

RetailX is an end-to-end e-commerce analytics platform combining Python, Pandas, SQL, MySQL, automated testing, visualization, and CI.

Why MySQL?

MySQL provides structured relational storage and enables SQL-based business analytics.

Why Pytest?

Pytest automatically validates core business logic and helps prevent regressions.

Why GitHub Actions?

GitHub Actions automatically runs tests whenever changes are pushed.

👨‍💻 Author

Ravishankar Prajapat

Data Science | Python | SQL | Machine Learning
                    ┌──────────────────┐
                    │ Visualizations   │
                    │ Reports & KPIs   │
                    └──────────────────┘
