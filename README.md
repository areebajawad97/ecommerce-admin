# ecommerce-admin

Dependencies:
1.	Python: 
Make sure you have Python installed. 

2.	FastAPI: 
Install FastAPI and Uvicorn for serving the application:
python -m pip install fastapi uvicorn[standard]

3.	Mysql-connector-python: 
Install the MySQL connector to interact with the MySQL database:
pip install mysql-connector-python
pip install pymysql

4. Execute ecommerce_db.sql

API Endpoints:
•	Sales Data by Date Range, Product, and Category:
The view_all_sales_date_range API endpoint is designed to retrieve and return sales-related data for orders placed within a specified date range. 
Here is a brief description of this API endpoint:
Endpoint URL: /view_all_sales_date_range/
HTTP Method: POST
Input: date_from (string): The starting date of the date range.
date_to (string): The ending date of the date range.

The view_all_sales_product API endpoint is designed to retrieve and return sales data for a specific product based on its product_id. It returns a list of dates and the total quantity of that product sold on each date.
Here is a brief description of this API endpoint:
Endpoint URL: /view_all_sales_product/
HTTP Method: POST
Input: product_id (integer)

The view_all_sales_category API endpoint is designed to retrieve and return sales data for a specific product category based on its category_id. It returns a list of products (from that specific category) dates and the total quantity of that product sold on each date.
Here is a brief description of this API endpoint:
Endpoint URL: /view_all_sales_category/
HTTP Method: POST
Input: category_id(integer)


•	Revenue Analysis:
The analyze_revenue API endpoint is designed to calculate and analyze revenue data based on different time periods (daily, weekly, monthly, or yearly) for both total revenue and product-specific revenue. 
Here is a brief description of this API endpoint:
Endpoint URL: /analyze_revenue/
HTTP Method: POST
Input: type (string): The type of revenue analysis to perform. It can be one of the following values: "DAILY," "WEEKLY," "MONTHLY," or "YEARLY."
 
•	Compare Revenue:
The compare_revenue API endpoint is designed to compare revenue and profit data for products within a specified category and date range. 
Here is a brief description of this API endpoint:
Endpoint URL: /compare_revenue/
HTTP Method: POST
Purpose: This API calculates and returns revenue and profit information for each product within the specified criteria.
Input: category_id (integer)
start_date (string)
end_date (string)

•	Inventory Status with Low Stock Alerts:
The view_current_inventory_status API endpoint is designed to provide information about the current inventory status of products, including stock levels, alert thresholds, and whether products are in low stock. 
Here is a brief description of this API endpoint:
Endpoint URL: /view_current_inventory_status/
HTTP Method: GET
Purpose: This API endpoint allows you to retrieve and view the current inventory status of products in your inventory system. It provides details about each product, including its name, current stock level, alert threshold, and whether it is in low stock.

•	Update Inventory Levels:
The update_inventory_levels API endpoint is designed to update the stock levels of a product in the inventory system and record the change in inventory history. 
Here is a brief description of this API endpoint:
Endpoint URL: /update_inventory_levels/
HTTP Method: POST
Input: product_id (integer)
stock_level (integer)

•	View Inventory History:
The view_inventory_history API endpoint is designed to provide a history of changes in inventory levels for products, including details about stock level updates and status changes. 
Here is a brief description of this API endpoint:
Endpoint URL: /view_inventory_history/
HTTP Method: GET

•	Inserting New Products:
The add_new_product API endpoint is designed to add a new product to your inventory system. It allows you to specify details about the product, such as its category, name, initial stock level, and alert threshold. 
Here is a brief description of this API endpoint:
Endpoint URL: /add_new_product/
HTTP Method: POST
Input: category_id (integer)
product_name (string)
stock_level (integer)
alert_threshold (integer)
