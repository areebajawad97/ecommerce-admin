import pymysql


conn = pymysql.connect(
        host='localhost',
        user='root',
        password="",
        db='ecommerce_db',
    )