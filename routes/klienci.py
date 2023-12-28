from flask import Blueprint, request, Response, abort, jsonify, render_template, g, flash, redirect, url_for
from connection.database import Database
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from lib.config import app_config
klienci_route = Blueprint('klienci_route', __name__)
klienci_route.config = app_config()['secret']
class NowyKlient(FlaskForm):
    imie = StringField('Imie')
    nazwisko = StringField('Nazwisko')
    nr_telefonu = StringField('Nr telefonu')
    adres = StringField('Adres')
    kod_pocztowy = StringField('Kod Pocztowy')
    miasto = StringField('Miasto')
    mail = StringField('Email')
    submit = SubmitField("Submit")
@klienci_route.route("/klienci", methods=['POST', 'GET', 'UPDATE', 'DELETE'])
def lista_klientow():
    """
    Route do obslugi tabeli klientow. W zaleznosci od metody sa wykonywane rozne akcje:
    - UPDATE: zaktualizuj klienta w bazie
    """
    t = request.values
    form = NowyKlient()
    edit_form = NowyKlient()
    current_url = request.path
    if "edit" in t.keys():
        print("jestem w edit")
        print(t['edit'])
        if t['edit'] == 'True':
            if edit_form.validate_on_submit():
                return "teraz jestem w edit"
        else:
            if form.validate_on_submit():
                if form.data:
                    dane_klienta = form.data
                    query = "insert into klienci(imie,nazwisko,nr_telefonu,adres,kod_pocztowy,miasto,email) values('{}','{}','{}','{}','{}','{}','{}')".format(
                        dane_klienta['imie'],
                        dane_klienta['nazwisko'],
                        dane_klienta['nr_telefonu'],
                        dane_klienta['adres'],
                        dane_klienta['kod_pocztowy'],
                        dane_klienta['miasto'],
                        dane_klienta['mail']
                    )
                    db_ = Database()
                    db = getattr(g,"db",None)
                    result = db_.exec_query(query=query,type="insert", cnx=db)
                    if result:
                        flash("Klient został zapisany", "success")
                    else:
                        flash("Klient nie został zapisany", "error")
                return redirect(url_for("klienci_route.lista_klientow"))
    if request.method == "GET":
        db_ = Database()
        db = getattr(g, 'db', None)
        # db.connect_to_database()
        query = "SELECT * FROM klienci"
        result = db_.exec_query(query, "select", db)
        # dicts_from_result = [{row[0]: row[1:]} for row in result.fetchall()]
        result_fetch = result.fetchall()
        kolumny = ['id', 'Imie', 'Nazwisko', 'Nr telefonu', 'Adres', 'Kod pocztowy', 'Miasto', 'Email', 'Akcje']
        return render_template("klienci.html", current_url=current_url, kolumny=kolumny,
                               klienci=result_fetch, form=form, edit_form=edit_form)



@klienci_route.route("/usun_klienta", methods=['GET','POST'])
def usun_klienta():
    t = request.values
    if t:
        db_ = Database()
        db = getattr(g, 'db', None)
        query = "delete from klienci where id={}".format(t['id'])
        result = db_.exec_query(cnx=db, query=query, type="delete")
        if result:
            flash("Klient został usuniety", "success")
        else:
            flash("Klient nie został usuniety", "error")
    return redirect(url_for("klienci_route.lista_klientow"))

# @klienci_route.route("/edytuj_klienta", methods=['GET,POST'])
# def edytuj_klienta():
#     # pobierz dane po id
#     if method
#     # wygeneruj modal
#     # zapisz do bazy

    # return "dupa"
@klienci_route.route("/pokaz_zamowienia_dla_klienta")
def zamowienia_per_klient():
    pass
