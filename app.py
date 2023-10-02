from flask import Flask, render_template, Blueprint


app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/zamowienia')
def zamowienia():  # put application's code here
    return render_template("zamowienia.html")

@app.route('/klienci')
def klienci():  # put application's code here
    return render_template("klienci.html")

@app.route('/serwis')
def serwis():  # put application's code here
    return render_template("serwis.html")

@app.route('/szyny')
def szyny():  # put application's code here
    return render_template("szyny.html")



if __name__ == '__main__':
    app.run()
