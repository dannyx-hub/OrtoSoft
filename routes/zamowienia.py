from flask import Blueprint, request, g, flash, redirect, url_for, render_template, send_file

import umowa_gen
from connection.database import Database
from wtforms import StringField, SubmitField, SelectField, DateField
from flask_wtf import FlaskForm

zamowienia_route = Blueprint("zamowienia_route", __name__)


class NoweZamowienie(FlaskForm):
    klient = SelectField("Klient")
    urzadzenie = SelectField("Urządzenie")
    dostawa = SelectField("Rodzaj dostawy", choices=[('kurier', 'Kurier'), ('odbiór osobisty', 'Odbiór osobisty')])
    data_rozpoczenia_wypozyczenia = DateField("Data rozpoczęcia wypożyczenia", format='%Y-%m-%d')
    data_zakonczenia_wypozyczenia = DateField("Data zakończenia wypożyczenia", format='%Y-%m-%d')
    rodzaj_platnosci = SelectField("Rodzaj płatności", choices=[("gotowka", "Gotówka"), ("przelew", "Przelew")])
    submit = SubmitField("Submit")


@zamowienia_route.route("/zamowienie", methods=['POST', 'GET'])
def lista_zamowien():
    form = NoweZamowienie()
    current_url = request.path
    db_ = Database()
    db = getattr(g, 'db', None)

    query_urzadzenia = "select id, numer from urzadzenia"
    result_lista_urzadzenia = db_.exec_query(query_urzadzenia, "select", db)

    query_klient = "select id, nazwisko from klienci"
    result_lista_klient = db_.exec_query(query_klient, "select", db)

    form.urzadzenie.choices = result_lista_urzadzenia.fetchall()
    form.klient.choices = result_lista_klient.fetchall()

    query = "SELECT wypozyczenia.id,nazwisko,numer,dostawa,data_rozpoczecia_wypozyczenia,data_zakonczenia_wypozyczenia, rodzaj_platnosci FROM wypozyczenia join klienci on wypozyczenia.id_klienta=klienci.id join urzadzenia on wypozyczenia.id_urzadzenia=urzadzenia.id"
    kolumny = ['id', 'Klient', 'Urządzenie', 'Rodzaj dostawy', "Data rozpoczęcia wypożyczenia",
               "Data zakończenia wypożyczenia", "Rodzaj płatności", "Akcje"]
    result_zamowienia = db_.exec_query(query, "select", db)

    if form.validate_on_submit():
        zamowienie_data = form.data
        insert_query = "insert into wypozyczenia(id_klienta, id_urzadzenia, dostawa, data_rozpoczecia_wypozyczenia, data_zakonczenia_wypozyczenia, rodzaj_platnosci) values('{}','{}','{}','{}','{}','{}')".format(
            zamowienie_data['klient'],
            zamowienie_data['urzadzenie'],
            zamowienie_data['dostawa'],
            zamowienie_data['data_rozpoczenia_wypozyczenia'],
            zamowienie_data['data_zakonczenia_wypozyczenia'],
            zamowienie_data['rodzaj_platnosci']
        )
        ins = db_.exec_query(insert_query, "insert", db)

        if ins:
            flash("Zamówienie zostało zapisane", "success")
        else:
            flash("Zamówienie nie zostało zapisane", "error")

        return redirect(url_for("zamowienia_route.lista_zamowien"))

    return render_template("zamowienia.html", form=form, current_url=current_url,
                           zamowienia=result_zamowienia.fetchall(),
                           kolumny=kolumny)

@zamowienia_route.route("/usun_zamowienie", methods=['POST', 'GET'])
def usun_zamowienie():
    t = request.values
    if t:
        db_ = Database()
        db = getattr(g, 'db', None)
        query = "delete from wypozyczenia where id={}".format(t['id'])
        result = db_.exec_query(cnx=db, query=query, type="delete")
        if result:
            flash("Zamówienie zostało usunietę", "success")
        else:
            flash("Zamówienie zostało usunietę", "error")
        return redirect(url_for("zamowienia_route.lista_zamowien"))

@zamowienia_route.route("/wygeneruj_umowe", methods=['POST', 'GET'])
def wygeneruj_umowe():
    # from lib.umowa_gen import
    t = request.values
    s = umowa_gen.GeneratorUmowy(t['id'])
    s.open_template()
    dataclient = s.create_data_set()
    data = s.find_variable()
    return data[1]
