# RetailX — E-Commerce Sales & Inventory Analytics Platform

> An end-to-end, modular Python analytics platform for e-commerce sales, profitability, inventory health, warehouse performance, and business intelligence.

## 📌 Project Overview

RetailX is a modular e-commerce analytics platform built with Python, Pandas, NumPy, Matplotlib, and Pytest.

The platform transforms raw sales and inventory data into structured business analytics and actionable insights across:

- Sales performance
- Revenue and profitability
- Product performance
- Customer analysis
- Regional performance
- Payment methods
- Order status
- Inventory health
- Reorder requirements
- Warehouse performance
- Category-level inventory exposure

## 🎯 Business Problem

E-commerce businesses generate large volumes of transactional and inventory data. Without structured analytics, it becomes difficult to identify revenue trends, profitable products, customer performance, inventory shortages, reorder requirements, and warehouse-level risks.

RetailX addresses this problem by converting raw operational data into reusable analytics, visualizations, and business insights.

## 🚀 Project Objectives

1. Clean and prepare e-commerce transaction data.
2. Calculate core business KPIs.
3. Analyze product, category, customer, and regional performance.
4. Analyze monthly sales trends.
5. Analyze payment methods and order status.
6. Build an inventory master dataset.
7. Identify low-stock products.
8. Perform inventory risk and reorder analysis.
9. Analyze warehouse inventory exposure.
10. Generate automated business visualizations.
11. Implement automated testing using Pytest.
12. Provide a modular end-to-end analytics pipeline.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data manipulation and analytics |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Pytest | Automated testing |
| CSV | Data storage |
| Git | Version control |
| GitHub | Repository and project hosting |

## 📊 Dataset

### Sales Dataset

- 20,000 orders
- Customer information
- Product information
- Category
- Geography
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

Inventory analysis includes:

- Stock quantity
- Reorder level
- Reorder quantity
- Inventory value
- Stock status
- Safety stock
- Lead time
- Warehouse exposure

## 📈 Business Analytics

RetailX provides analytics functions for:

### Sales & Profitability
- Total revenue
- Total profit
- Total orders
- Total customers
- Units sold
- Average Order Value
- Profit margin

### Product Analytics
- Top products
- Product revenue
- Product profitability
- Product performance

### Category Analytics
- Category revenue
- Category profit
- Category performance

### Customer Analytics
- Customer performance
- High-value customers
- Customer revenue contribution

### Regional Analytics
- Regional revenue
- Regional performance

### Time-Series Analytics
- Monthly revenue trends

### Payment Analytics
- Revenue by payment method

### Order Analytics
- Order status analysis

## 📦 Inventory Analytics

RetailX generates an inventory master and performs:

- Stock health analysis
- Low-stock detection
- Reorder analysis
- Inventory risk scoring
- Stock coverage analysis
- Warehouse performance analysis
- Category inventory exposure

### Inventory KPIs

| KPI | Result |
|---|---:|
| Total Stock Units | 4,383 |
| Inventory Value | ₹32,112,380.43 |
| Total Products | 132 |
| Total Warehouses | 4 |
| Healthy Items | 182 |
| Low Stock Items | 71 |
| Out of Stock Items | 0 |

## 🔎 Key Business Insights

Based on the generated analytics:

1. 71 inventory items require replenishment.
2. WH-West has the highest inventory value exposure.
3. Electronics has the highest inventory value exposure.
4. Inventory risk analysis identifies products requiring reorder action.
5. Warehouse-level analysis highlights areas with higher stock-risk exposure.

## 📊 Visualizations

The project automatically generates:

- Monthly Revenue Trend
- Category Revenue
- Category Profit
- Payment Method Revenue
- Warehouse Inventory
- Stock Health
- Warehouse Inventory Risk
- Top 10 Products

Visual reports are available in:

`reports/figures/`

## 🧪 Testing

RetailX uses Pytest for automated testing.

Current test result:

```text
7 passed in 1.19s
