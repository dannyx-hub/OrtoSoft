from flask import Flask, render_template, Blueprint, request
from routes import userroute
from routes import klienci
app = Flask(__name__)
app.register_blueprint(userroute.user_route)
app.register_blueprint(klienci.klienci_route)

@app.route('/')
def index():
    current_url = request.path
    return render_template("index.html", current_url=current_url)

@app.route('/zamowienia')
def zamowienia():  # put application's code here
    current_url = request.path
    return render_template("zamowienia.html", current_url=current_url)



@app.route('/serwis')
def serwis():  # put application's code here
    current_url = request.path
    return render_template("serwis.html", current_url=current_url)

@app.route('/szyny')
def szyny():  # put application's code here
    current_url = request.path
    return render_template("szyny.html", current_url=current_url)



if __name__ == '__main__':
    app.run()
