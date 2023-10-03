from fastapi import FastAPI, Request
from dbcon import  conn as connection
import json
from datetime import date


app = FastAPI()

@app.post("/view_all_sales_date_range/")
async def view_all_sales_date_range(request: Request):
    formatted_results = []
    result = 0
    cur = connection.cursor()

    try:
        params =  await request.json()
        date_from = params.get('date_from')
        date_to = params.get("date_to")

        cur.execute("SELECT id, order_ID, date, total_sale, total_quantity, total_profit FROM orders "
                        "WHERE date BETWEEN %s and %s ", (date_from, date_to))
        order_result = cur.fetchall()

        for row in order_result:
            id, order_ID,date,total_sale,total_quantity,total_profit = row

            order_details_list = []
            cur.execute(
                "SELECT "
                "products.product_name, order_details.sale, order_details.quantity, order_details.profit "
                "FROM `order_details` INNER JOIN products ON order_details.product_id = products.id "
                "WHERE order_details.order_id = %s",(id))
            order_detail_query = cur.fetchall()
            for order_detail_row in order_detail_query:
                product_name, sale, quantity, profit = order_detail_row
                order_details_list.append({
                    "product_name": product_name,
                    "sale": sale,
                    "quantity": quantity,
                    "profit": profit
                })

            formatted_results.append({
                'order_ID': order_ID,
                'date': date.strftime('%Y-%m-%d'),  # Convert date to string in the desired format
                "total_sale":total_sale,
                "total_quantity":total_quantity,
                "total_profit":total_profit,
                "order_details": order_details_list
            })
        result = 1

    except Exception as e:
        result = 0
        formatted_results = str(e)

    json_string = json.dumps({"result": result, "data": formatted_results})

    return json.loads(json_string)



@app.post("/analyze_revenue/")
async def analyze_revenue(request: Request):
    formatted_results = []
    result = 0
    cur = connection.cursor()

    try:
        params = await request.json()
        type = params.get('type')

        query_main_total_revenue = (
            "SELECT ROUND(SUM(total_sale), 2) as daily_revenue FROM `orders` %s"
        )
        query_main_products_revenue = (
            "SELECT ROUND(SUM(order_details.sale), 2) as total_product_revenue, products.product_name "
            "FROM `orders` "
            "INNER JOIN order_details ON orders.id = order_details.order_id "
            "INNER JOIN products ON order_details.product_id = products.id "
            "%s GROUP BY products.product_name"
        )
        if type == "DAILY":
            date_condition = "WHERE orders.date = CURRENT_DATE"

            daily_revenue_query = query_main_total_revenue % date_condition
            cur.execute(daily_revenue_query)
            daily_revenue = cur.fetchone()

            total_products_revenue = query_main_products_revenue % date_condition
            cur.execute(total_products_revenue)
            daily_product_revenue = cur.fetchall()
            daily_product_revenue_list = []
            for order_detail_row in daily_product_revenue:
                total_product_revenue, product_name = order_detail_row
                daily_product_revenue_list.append({
                    "total_product_revenue": total_product_revenue,
                    "product_name": product_name
                })

            return { "type": type ,"today_revenue": daily_revenue[0], "today_products_revenue": daily_product_revenue_list}
        if type == "WEEKLY":
            date_condition = "WHERE YEARWEEK(orders.date) = YEARWEEK(CURRENT_DATE)"

            weekly_revenue_query = query_main_total_revenue % date_condition
            cur.execute(weekly_revenue_query)
            weekly_revenue = cur.fetchone()

            total_products_revenue = query_main_products_revenue % date_condition
            cur.execute(total_products_revenue)
            weekly_product_revenue = cur.fetchall()
            weekly_product_revenue_list = []
            for order_detail_row in weekly_product_revenue:
                total_product_revenue, product_name = order_detail_row
                weekly_product_revenue_list.append({
                    "total_product_revenue": total_product_revenue,
                    "product_name": product_name
                })

            return { "type": type ,"weekly_revenue": weekly_revenue[0], "weekly_products_revenue": weekly_product_revenue_list}

        if type == "MONTHLY":
            date_condition = "WHERE DATE_FORMAT(orders.date, '%Y-%m') = DATE_FORMAT(CURRENT_DATE, '%Y-%m')"

            monthly_revenue_query = query_main_total_revenue % date_condition
            cur.execute(monthly_revenue_query)
            monthly_revenue = cur.fetchone()

            total_products_revenue = query_main_products_revenue % date_condition
            cur.execute(total_products_revenue)
            monthly_product_revenue = cur.fetchall()
            monthly_product_revenue_list = []
            for order_detail_row in monthly_product_revenue:
                total_product_revenue, product_name = order_detail_row
                monthly_product_revenue_list.append({
                    "total_product_revenue": total_product_revenue,
                    "product_name": product_name
                })

            return { "type": type ,"monthly_revenue": monthly_revenue[0], "monthly_products_revenue": monthly_product_revenue_list}

        if type == "YEARLY":
            date_condition = "WHERE YEAR(orders.date) = YEAR(CURRENT_DATE)"

            yearly_revenue_query = query_main_total_revenue % date_condition
            cur.execute(yearly_revenue_query)
            yearly_revenue = cur.fetchone()

            total_products_revenue = query_main_products_revenue % date_condition
            cur.execute(total_products_revenue)
            yearly_product_revenue = cur.fetchall()
            yearly_product_revenue_list = []
            for order_detail_row in yearly_product_revenue:
                total_product_revenue, product_name = order_detail_row
                yearly_product_revenue_list.append({
                    "total_product_revenue": total_product_revenue,
                    "product_name": product_name
                })

            return { "type": type ,"yearly_revenue": yearly_revenue[0], "yearly_products_revenue": yearly_product_revenue_list}
    except Exception as e:
        print(e)
        result = 0
        return {"result": result, "error": str(e)}



@app.post("/view_all_sales_product/")
async def view_all_sales_date_range(request: Request):
    formatted_results = []
    result = 0
    cur = connection.cursor()

    try:
        params =  await request.json()
        product_id = params.get('product_id')
        if product_id:

            cur.execute("SELECT orders.date, SUM(order_details.quantity) as total_quantity_sold "
                        "FROM order_details inner join orders on order_details.order_id = orders.id "
                        "WHERE order_details.product_id = %s group by orders.date", (product_id))
            result = cur.fetchall()

            for row in result:
                date, total_quantity_sold,  = row

                formatted_results.append({
                    'date': date.strftime('%Y-%m-%d'),
                    "total_quantity_sold": int(total_quantity_sold)
                })
            result = 1
        else:
            result = 0
            formatted_results.append({
                'error': "product_id is required"
            })
    except Exception as e:
        result = 0
        formatted_results = str(e)

    json_string = json.dumps({"result": result, "data": formatted_results})

    return json.loads(json_string)


@app.post("/view_all_sales_category/")
async def view_all_sales_date_range(request: Request):
    formatted_results = []
    result = 0
    cur = connection.cursor()

    try:
        params =  await request.json()
        category_id = params.get('category_id')
        if category_id:

            cur.execute("SELECT products.product_name,orders.date, SUM(order_details.quantity) as total_quantity_sold "
                        "FROM order_details "
                        "inner join orders on order_details.order_id = orders.id "
                        "inner join products on order_details.product_id = products.id "
                        "where products.category_id = %s group by products.product_name, orders.date", (category_id))
            result = cur.fetchall()

            for row in result:
                product_name, date, total_quantity_sold,  = row

                formatted_results.append({
                    "product_name": product_name,
                    "date": date.strftime('%Y-%m-%d'),
                    "total_quantity_sold": int(total_quantity_sold)
                })
            result = 1
        else:
            result = 0
            formatted_results.append({
                'error': "category_id is required"
            })
    except Exception as e:
        result = 0
        formatted_results = str(e)

    json_string = json.dumps({"result": result, "data": formatted_results})

    return json.loads(json_string)


@app.post("/compare_revenue/")
async def compare_revenue(request: Request):

    formatted_results = []
    result = 0
    cur = connection.cursor()

    try:
        params = await request.json()
        category_id = params.get('category_id')
        start_date = params.get('start_date')
        end_date = params.get('end_date')

        # Execute the query to compare revenue and profit for the specified category and date range
        cur.execute(
            "SELECT products.product_name, orders.date, ROUND(SUM(order_details.sale),2) as total_revenue, ROUND(SUM(order_details.profit),2) as total_profit "
            "FROM "
            "    orders "
            "INNER JOIN "
            "    order_details ON orders.id = order_details.order_id "
            "INNER JOIN "
            "    products ON order_details.product_id = products.id "
            "WHERE "
            "    products.category_id = %s "
            "    AND orders.date BETWEEN %s AND %s "
            "GROUP BY "
            "    products.product_name, date",
            (category_id, start_date, end_date)
        )
        result = cur.fetchall()

        for row in result:
            product_name, date, total_revenue, total_profit = row

            formatted_results.append({
                "product_name": product_name,
                "date": date.strftime('%Y-%m-%d'),
                "total_revenue": total_revenue,  # Round to 2 decimal places
                "total_profit": total_profit  # Round to 2 decimal places
            })
        result = 1
    except Exception as e:
        result = 0
        formatted_results = str(e)

    json_string = json.dumps({"result": result, "data": formatted_results})

    return json.loads(json_string)

@app.get("/view_current_inventory_status/")
def view_current_inventory_status():

    result = 0
    cur = connection.cursor()


    try:
        cur.execute("select products.product_name AS product_name, inventory.stock_level AS stock_level, "
                    "inventory.alert_threshold AS threshold_alert, "
                    "CASE WHEN inventory.stock_level < inventory.alert_threshold THEN true ELSE false END AS low_stock_alert "
                    "from inventory inner join products on products.id = inventory.product_id")

        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in cur.fetchall()]

        result = 1

    except Exception as e:
        result = 0
        data = str(e)

    json_string = json.dumps({"result": result, "data": data})

    return json.loads(json_string)

@app.get("/view_inventory_history/")
def view_inventory_history():
    formatted_results = []
    result = 0
    cur = connection.cursor()

    try:
        cur.execute("select products.product_name, inventory_history.stock_level, inventory_history.status, inventory_history.date from inventory_history inner join inventory on inventory_history.inventory_id = inventory.id inner join products on inventory.product_id = products.id order by inventory_history.date desc")

        data=cur.fetchall()

        for row in data:
            product_name,stock_level,status,date = row
            formatted_results.append({
                'product_name': product_name,
                'date': date.strftime('%Y-%m-%d'),  # Convert date to string in the desired format
                'stock_level': stock_level,
                'status': status
            })
        print(formatted_results)

        result = 1

    except Exception as e:
        result = 0
        formatted_results = str(e)

    json_string = json.dumps({"result": result, "data": formatted_results})

    return json.loads(json_string)

@app.post("/update_inventory_levels/")
async def update_inventory_levels(request: Request):
    cur = connection.cursor()

    try:
        params = await request.json()
        product_id = params.get('product_id')
        stock_level = params.get('stock_level')

        cur.execute("UPDATE inventory SET stock_level = stock_level + %s WHERE product_id = %s", (stock_level, product_id))
        connection.commit()

        cur.execute("SELECT inventory.id FROM inventory WHERE inventory.product_id = %s",(product_id))
        data=cur.fetchone()

        if data:
            inventory_id=data[0]
            today = date.today()
            status="STOCK_IN"

            cur.execute("INSERT INTO inventory_history (inventory_id,status,stock_level,date) VALUES (%s,%s,%s,%s)",(inventory_id,status,stock_level,today))
            connection.commit()
            result = 1

        else:
            result = "Product not found"
    except Exception as e:
        result = str(e)

    json_string = json.dumps({"result": result})

    return json.loads(json_string)

@app.post("/add_new_product/")
async def add_new_product(request: Request):
    cur = connection.cursor()

    try:
        params = await request.json()
        category_id= params.get('category_id')
        product_name = params.get('product_name')
        stock_level = params.get('stock_level')
        alert_threshold = params.get('alert_threshold')

        cur.execute("INSERT INTO products (category_id,product_name) VALUES (%s,%s)",(category_id, product_name))
        connection.commit()

        product_id = cur.lastrowid
        cur.execute("INSERT INTO inventory (product_id,stock_level,alert_threshold) VALUES (%s,%s,%s)",(product_id, stock_level,alert_threshold))
        connection.commit()

        inventory_id = cur.lastrowid
        today = date.today()
        status = "STOCK_IN"

        cur.execute("INSERT INTO inventory_history (inventory_id,status,stock_level,date) VALUES (%s,%s,%s,%s)",
                    (inventory_id, status, stock_level, today))
        connection.commit()


        result = 1


    except Exception as e:
        result = str(e)

    json_string = json.dumps({"result": result})

    return json.loads(json_string)