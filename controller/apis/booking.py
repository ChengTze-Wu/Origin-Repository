import os
from flask import Blueprint, request, make_response, current_app
import model
import jwt

secret_key = os.environ['USER_TOKEN_SECRET_KEY']

api_header = {("Content-Type","application/json; charset=utf-8")}

booking = Blueprint('booking', __name__)

@booking.route('/booking', methods=["GET"])
def get_booking_with_cookie():
    try:
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(encoded_token, secret_key, algorithms=["HS256"])
            email = decoded_token["email"]
            user = model.get_current_user(email)
            user_id = user["data"]["id"]
            booking = model.get_booking_by_user_id(user_id)[0]
            resp = make_response((booking, 200, api_header))
        else:
            resp = make_response(({"error":True, "message":"未登入系統"}, 403, api_header))
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error":True, "message":"Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp

@booking.route('/booking', methods=["POST"])
def create_booking():
    try:
        resq = request.get_json()
        attraction_id = resq["attractionId"]
        date = resq["date"]
        time = resq["time"]
        price = resq["price"]
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(encoded_token, secret_key, algorithms=["HS256"])
            email = decoded_token["email"]
            user = model.get_current_user(email)
            user_id = user["data"]["id"]
            model.create_booking(date, time, price, attraction_id, user_id)
            resp = make_response(({"ok":True}, 200, api_header))
        elif encoded_token == None:
            resp = make_response(({"error":True, "message":"未登入系統"}, 403, api_header))
        else:
            resp = make_response(({"error":True, "message":"建立失敗，輸入不正確或其他原因"}, 400, api_header))
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error":True, "message":"Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp

@booking.route('/booking', methods=["DELETE"])
def delete_booking():
    try:
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(encoded_token, secret_key, algorithms=["HS256"])
            email = decoded_token["email"]
            user = model.get_current_user(email)
            user_id = user["data"]["id"]
            model.delete_booking_by_user(user_id)
            resp = make_response(({"ok":True}, 200, api_header))
        else:
            resp = make_response(({"error":True, "message":"未登入系統"}, 403, api_header))
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error":True, "message":"Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp