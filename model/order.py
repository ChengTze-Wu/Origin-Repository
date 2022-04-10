import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_DATABASE']
}

cnx = mysql.connector.connect(pool_name = "order",
                              pool_size = 5,
                              **config)


def create_order(number, status, booking_id):
    try:
        cnx = mysql.connector.connect(pool_name = "order")
        cursor = cnx.cursor()
        
        query = ("INSERT INTO orders values (%s, %s, %s)")
        value = (number, status, booking_id)
            
        cursor.execute(query, value)
        cnx.commit()
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()

                        
def get_order_by_booking_id(order_number):
    try:
        cnx = mysql.connector.connect(pool_name = "order")
        cursor = cnx.cursor()
        
        query = ("SELECT orders.number, bookings.price, attractions.id, attractions.name, "
                 "attractions.address,  attractions.image, bookings.date, bookings.time, "
                 "users.name, user.email, orders.phone, orders.status "
                 "FROM(((orders INNER JOIN booking ON orders.booking_id = bookings.id) "
                 "INNER JOIN attractions ON bookings.attraction_id = attractions.id)) "
                 "INNER JOIN users ON bookings.user_id = users.id "
                 "WHERE orders.number = %s")
        value = (order_number,)
        
        cursor.execute(query, value)
        data = cursor.fetchone()
        if data:
            result = { "data": {
                "number": data[0],
                "price": data[1],
                "trip":{
                "attraction": {
                    "id": data[2],
                    "name": data[3],
                    "address": data[4],
                    "image": data[5].split(",")[0]
                },
                "date": str(data[6]),
                "time": data[7],
                },
                "contact": {
                    "name": data[8],
                    "email": data[9],
                    "phone": data[10]
                },
                "status": data[11]
            }}
        else:
            result = {"data":None}
        return result
    except Exception as e:
        raise e
    finally:
        if cnx.in_transaction:
            cnx.rollback()
        cursor.close()
        cnx.close()