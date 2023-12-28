from flask import Blueprint, request, render_template, g, flash, redirect, url_for
from connection.database import Database
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

urzadzenia_route = Blueprint("urzadzenia_route", __name__)


class NoweUrzadzenie(FlaskForm):
    producent = StringField("Producent")
    model = StringField("Model")
    numer = StringField("Numer")
    submit = SubmitField("Submit")


@urzadzenia_route.route("/urzadzenia",methods=['POST', 'GET', 'UPDATE', 'DELETE'])
def lista_urzadzen():
    form = NoweUrzadzenie()
    current_url = request.path
    db_ = Database()
    db = getattr(g, 'db', None)
    query = "SELECT * FROM urzadzenia"
    result = db_.exec_query(query,"select",db)
    if form.validate_on_submit():
        dane_urzadzenia = form.data
        query= "insert into urzadzenia(producent,model,numer) values('{}','{}','{}')".format(
            dane_urzadzenia['producent'],
            dane_urzadzenia['model'],
            dane_urzadzenia['numer']
        )
        result = db_.exec_query(query,"insert",db)
        if result:
            flash("Urządzenie zostało zapisane", "success")
        else:
            flash("Urządzenie nie zostało zapisane", "error")
        return redirect(url_for("urzadzenia_route.lista_urzadzen"))
    kolumny = ['id','Producent','Model','Numer', 'Akcje']
    return render_template("szyny.html", current_url=current_url,urzadzenia=result.fetchall(), kolumny=kolumny,form=form)

@urzadzenia_route.route("/usun_urzadzenie", methods=['GET','POST'])
def usun_urzadzenie():
    t = request.values
    if t:
        db_ = Database()
        db = getattr(g, 'db', None)
        query = "delete from urzadzenia where id={}".format(t['id'])
        result = db_.exec_query(cnx=db, query=query, type="delete")
        if result:
            flash("Urządzenie zostało usuniętę", "success")
        else:
            flash("Urządzenie nie zostało usuniętę", "error")
    return redirect(url_for("urzadzenia_route.lista_urzadzen"))