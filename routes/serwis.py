from flask import Blueprint, request, Response, abort, jsonify, render_template, g, flash, redirect, url_for
from connection.database import Database
from wtforms import StringField, SubmitField, SelectField, DateField
from flask_wtf import FlaskForm


serwisy_route = Blueprint("serwisy_route", __name__)



class NowySerwis(FlaskForm):
    urzadzenie = SelectField("Urządzenie")
    data_serwisu = DateField("Data Serwisu")
    rodzaj_serwisu = StringField("Rodzaj serwisu")
    submit = SubmitField("Submit")




@serwisy_route.route("/serwisy", methods=['POST', 'GET'])
def lista_serwisu():
    t = request.values
    current_url = request.path
    form = NowySerwis()
    db_ = Database()
    db = getattr(g, 'db', None)
    query_urzadzenia = "select id, numer from urzadzenia"
    result_lista = db_.exec_query(query_urzadzenia, "select", db)
    form.urzadzenie.choices = result_lista.fetchall()
    if form.validate_on_submit():
        if form.data:
            serwis_data = form.data
            query = "insert into serwis(id_urzadzenia,data_serwisu,rodzaj_serwisu) values ('{}','{}','{}')".format(
                int(serwis_data['urzadzenie']),
                serwis_data['data_serwisu'],
                serwis_data['rodzaj_serwisu']
            )
            ins = db_.exec_query(query,"insert",db)
            if ins:
                flash("Serwis został zapisany", "success")
            else:
                flash("Serwis nie został zapisany", "error")
            return redirect(url_for("serwisy_route.lista_serwisu"))
    query = "select serwis.id, urzadzenia.numer, serwis.data_serwisu, serwis.rodzaj_serwisu from serwis join urzadzenia on serwis.id_urzadzenia=urzadzenia.id"
    result = db_.exec_query(query,"select",db)
    kolumny = ['id', "Urządzenie", "Data serwisu", "Rodzaj serwisu", "Akcje"]
    return render_template("serwis.html", form=form, current_url=current_url, serwisy=result.fetchall(), kolumny=kolumny)

@serwisy_route.route("/usun_serwis",methods=['GET','POST'])
def usun_serwis():
    t = request.values
    if t:
        db_ = Database()
        db = getattr(g, 'db', None)
        query = "delete from serwis where id={}".format(t['id'])
        result = db_.exec_query(cnx=db, query=query, type="delete")
        if result:
            flash("Serwis został usuniety", "success")
        else:
            flash("Serwis nie został usuniety", "error")
        return redirect(url_for("serwisy_route.lista_serwisu"))