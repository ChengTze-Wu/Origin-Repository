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
        status = 0 # 未付款狀態
        req_data = request.get_json()
        prime = req_data["prime"]
        amount = req_data["order"]["price"]
        phone_number = req_data["order"]["contact"]["phone"]
        name = req_data["order"]["contact"]["name"]
        email = req_data["order"]["contact"]["email"]
       
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(encoded_token, secret_key, algorithms=["HS256"])
            email = decoded_token["email"]
            user = model.get_current_user(email)
            user_id = user["data"]["id"]
            booking = model.get_booking_by_user_id(user_id)[0]
            
            resp = send_to_tappay(prime, amount, phone_number ,name ,email)
    
            resp_data = {
                "data": {
                    "number": resp["order_number"],
                    "payment": {
                    "status": resp["status"],
                    "message": "付款成功"
                    }
                }
            }

            model.create_order(resp["order_number"], status, booking["booking_id"])
            
            return make_response((resp_data, 200, api_header))
        else:
            resp = make_response(({"error":True, "message":"未登入系統"}, 403, api_header))
            
    except Exception as e:
        error_message = {"error":True, "message":str(e)}
        resp = make_response((error_message, 500, api_header))
        


@order.route("/order/<orderNumber>", methods=["GET"])
def get_order(orderNumber):
    resp_data = model.get_order_by_booking_id(orderNumber)
    return make_response(resp_data, 200)