from dotenv import load_dotenv
load_dotenv()
from flask import Flask
import controller

app = Flask(__name__)

# config
app.config.from_object("config.ProConfig")
# pages
app.register_blueprint(controller.pages)
# api
app.register_blueprint(controller.apis.attraction, url_prefix="/api")
app.register_blueprint(controller.apis.member, url_prefix="/api")
app.register_blueprint(controller.apis.booking, url_prefix="/api")
app.register_blueprint(controller.apis.order, url_prefix="/api")

if __name__ == '__main__':
    app.run()
