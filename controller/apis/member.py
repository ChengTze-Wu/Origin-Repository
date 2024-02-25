import os
from flask import Blueprint, request, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import model
import jwt

member = Blueprint('member', __name__)

secret_key = os.environ['USER_TOKEN_SECRET_KEY']

api_header = {("Content-Type", "application/json; charset=utf-8")}


@member.route("/user", methods=["GET"])
def get_current_user():
    try:
        email = None
        encoded_token = request.cookies.get("token")
        if encoded_token:
            decoded_token = jwt.decode(
                encoded_token, secret_key, algorithms=["HS256"])
            email = decoded_token["email"]
        data = model.get_current_user(email)
        resp = make_response((data, 200, api_header))
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error": True, "message": "Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp


@member.route("/user", methods=["POST"])
def signup_user():
    try:
        req = request.get_json()
        name = req["name"]
        email = req["email"]
        password = generate_password_hash(req["password"])

        signup_pass = model.signup_user(name, email, password)
        if(signup_pass):
            message = {"ok": True}
            status = 200
        else:
            message = {"error": True, "message": "註冊失敗，email已被註冊"}
            status = 400
        resp = make_response((message, status, api_header))
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error": True, "message": "Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp


@member.route("/user", methods=["PATCH"])
def signin_user():
    try:
        req = request.get_json()
        email = req["email"]
        password = req["password"]
        data = model.signin_user(email)
        if data and check_password_hash(data["password"], password):
            success_message = {"ok": True}
            resp = make_response((success_message, 200, api_header))
            encoded_token = jwt.encode(
                {"email": data["email"]}, secret_key, algorithm="HS256")
            resp.set_cookie("token", encoded_token)
        else:
            error_message = {"error": True, "message": "帳號或密碼錯誤"}
            resp = make_response((error_message, 400, api_header))
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error": True, "message": "Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp


@member.route("/user", methods=["DELETE"])
def signout_user():
    try:
        success_message = {"ok": True}
        resp = make_response((success_message, 200, api_header))
        resp.delete_cookie("token")
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        error_message = {"error": True, "message": "Internal Server Error"}
        resp = make_response((error_message, 500, api_header))
    return resp
