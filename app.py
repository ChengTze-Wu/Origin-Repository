from flask import *
import controller
app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
app.register_blueprint(controller.pages)
# api
app.register_blueprint(controller.attraction, url_prefix="/api")
app.register_blueprint(controller.user, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True, port=3000)