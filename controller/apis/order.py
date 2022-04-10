import os
from flask import Blueprint, request, make_response
import jwt
from dotenv import load_dotenv
import requests
from datetime import datetime

order =  Blueprint('order', __name__)

PARTNER_KEY = "partner_Dqd7KLJ0xaWhm0vx2sC0qfFX3fV0aDSJmXLx5ZuhN2FIpMyZ8G569Uva"

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
def bulid_order():
    status = 0 # 未付款狀態
    req_data = request.get_json()
    prime = req_data["prime"]
    amount = req_data["order"]["price"]
    phone_number = req_data["order"]["contact"]["phone"]
    name = req_data["order"]["contact"]["name"]
    email = req_data["order"]["contact"]["email"]
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
    
    return make_response(resp_data, 200)

@order.route("/order/<orderNumber>", methods=["GET"])
def get_order():
    return ""