import os
from flask import Blueprint, request, make_response
import jwt
import model
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()


PARTNER_KEY = "partner_Dqd7KLJ0xaWhm0vx2sC0qfFX3fV0aDSJmXLx5ZuhN2FIpMyZ8G569Uva"
secret_key = os.environ['USER_TOKEN_SECRET_KEY']

api_header = {("Content-Type","application/json; charset=utf-8"),
              ('Access-Control-Allow-Origin', '*')}

order =  Blueprint('order', __name__)


# serial_generate
index_num = 1
last_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
def serial_generator():
    global index_num
    serial_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    serial = "{}{:03}".format(serial_datetime, index_num)
    index_num += 1
    return serial

def send_to_tappay(prime, amount, phone_number ,name ,email):
    # guarantee unique serial
    global last_datetime
    global index_num
    if last_datetime != datetime.now().strftime("%Y%m%d%H%M%S"):
        index_num = 1
    current_serial = serial_generator()
    last_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {'Content-Type': 'application/json',
               'x-api-key':PARTNER_KEY}

    j_data = {
        "prime": prime,
        "partner_key": PARTNER_KEY,
        "merchant_id": "yaoop3050777_NCCC",
        "details":"TapPay Test",
        "order_number": current_serial,
        "amount": amount,
        "cardholder": {
            "phone_number": phone_number,
            "name": name,
            "email": email,
        },
    }
    
    r = requests.post(url, headers=headers, json=j_data)
    
    return r.json()


@order.route("/orders", methods=["POST"])
def create_order():
    try:   
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(encoded_token, secret_key, algorithms=["HS256"])
            email = decoded_token["email"]
            user = model.get_current_user(email)
            user_id = user["data"]["id"]
            
            req_data = request.get_json()
            if req_data:
                prime = req_data["prime"]
                amount = req_data["order"]["price"]
                phone_number = req_data["order"]["contact"]["phone"]
                name = req_data["order"]["contact"]["name"]
                contact_email = req_data["order"]["contact"]["email"]
                attraction_id = req_data["order"]["trip"]["attraction"]["id"]
                date =  req_data["order"]["trip"]["date"]
                time =  req_data["order"]["trip"]["time"]
            else:
                return make_response(({"error":True, "message":"資料輸入錯誤"}, 400, api_header))
                        
            resp_tappay = send_to_tappay(prime, amount, phone_number ,name ,contact_email)
            booking_status = 0
            if resp_tappay["status"] == 0:
                resp_data = {
                    "data": {
                        "number": resp_tappay["order_number"],
                        "payment": {
                        "status": resp_tappay["status"],
                        "message": "付款成功"
                        }
                    }
                }
                booking_status = 1
                model.create_order(resp_tappay["order_number"], booking_status, phone_number, date, time, amount, attraction_id, user_id)
            else:
                resp_data = {
                    "data": {
                        "number": resp_tappay["order_number"],
                        "payment": {
                        "status": resp_tappay["status"],
                        "message": "付款失敗"
                        }
                    }
                }
                model.create_order(resp_tappay["order_number"], booking_status, phone_number, date, time, amount, attraction_id, user_id)
            model.delete_booking_by_user(user_id)
            resp = make_response((resp_data, 200, api_header))
        else:
            resp = make_response(({"error":True, "message":"未登入系統"}, 403, api_header))
    except Exception as e:
        error_message = {"error":True, "message":str(e)}
        resp = make_response((error_message, 500, api_header))
    return resp

@order.route("/order/<orderNumber>", methods=["GET"])
def get_order(orderNumber):
    try:  
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(encoded_token, secret_key, algorithms=["HS256"])
            resp_data = model.get_order_by_booking_id(orderNumber)
            resp = make_response(resp_data, 200)
        else:
            resp = make_response(({"error":True, "message":"未登入系統"}, 403, api_header))
    except Exception as e:
        error_message = {"error":True, "message":str(e)}
        resp = make_response((error_message, 500, api_header))
    return resp