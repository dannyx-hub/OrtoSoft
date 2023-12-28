from flask import Flask, render_template, Blueprint, request, g
from routes import userroute, klienci, urzadzenia, zamowienia, serwis
from datetime import datetime, timedelta
from connection.database import Database
from lib.config import app_config

app = Flask(__name__)
app.config['SECRET_KEY'] = app_config()['secret']
db = Database()


@app.before_request
def before_first_request():
    g.db = db.connect_to_database()


app.register_blueprint(userroute.user_route)
app.register_blueprint(klienci.klienci_route)
app.register_blueprint(urzadzenia.urzadzenia_route)
app.register_blueprint(zamowienia.zamowienia_route)
app.register_blueprint(serwis.serwisy_route)


@app.route('/')
def index():
    current_url = request.path
    def range_date():
        first_day = datetime(datetime.now().year, datetime.now().month, 1)
        next_month_first_day = datetime(datetime.now().year, datetime.now().month + 1, 1) if datetime.now().month < 12 else datetime(datetime.now().year + 1, 1, 1)
        last_day = next_month_first_day - timedelta(days=1)
        return first_day,last_day
    start_date, end_date = range_date()
    start_date.strftime('%Y-%m-%d')
    end_date.strftime('%Y-%m-%d')
    #zapytanie do serwisow o serwis w tym miesiacu
    wydarzenia = []
    db_ = Database()
    db = getattr(g, 'db', None)
    query_serwis = "select urzadzenia.numer, serwis.data_serwisu, serwis.rodzaj_serwisu from serwis join urzadzenia on serwis.id_urzadzenia=urzadzenia.id WHERE serwis.data_serwisu BETWEEN '{}' AND '{}'".format(
            start_date,
            end_date
    )
    serwis_result = db_.exec_query(query_serwis,"select",db)

    zamowienia_query = "SELECT nazwisko,numer,dostawa,data_rozpoczecia_wypozyczenia,data_zakonczenia_wypozyczenia FROM wypozyczenia join klienci on wypozyczenia.id_klienta=klienci.id join urzadzenia on wypozyczenia.id_urzadzenia=urzadzenia.id WHERE data_rozpoczecia_wypozyczenia BETWEEN '{}' AND '{}'".format(
        start_date,
        end_date
    )
    zamowienia_result = db_.exec_query(zamowienia_query,"select", db)
    if zamowienia_result:
        for x in zamowienia_result.fetchall():
            wydarzenia.append({"title":f"Zamowienie {x[0]} {x[1]}", "start":x[3],"end":x[4]})
    if serwis_result:
        for x in serwis_result.fetchall():
            wydarzenia.append({"title":"Serwis: "+x[0]+f" {x[2]}", "start":x[1]})



    #zapytanie do zamowien o zamowienia w tym miesiacu
    return render_template("index.html", current_url=current_url, wydarzenia=wydarzenia)


if __name__ == '__main__':
    app.run(port=5001)
