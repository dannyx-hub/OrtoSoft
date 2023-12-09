from flask import Blueprint, request, Response, abort, jsonify, render_template
from connection.database import Database

user_route = Blueprint('userroute', __name__)

@user_route.route("/zamowienia", methods=['POST', 'GET', 'UPDATE', 'DELETE'])
def zamowienia():
    """
    Route do obslugi tabeli zamownien. W zaleznosci od metody sa wykonywane rozne akcje:
    - POST: Dodanie nowego zamowienia
    - GET: Pokaz liste zamowien
    - UPDATE: zaktualizuj zamowienie w bazie
    - DELETE: usun zamowienie
    :return:
    """
    current_url = request.path
    if request.method == "GET":
        return render_template("zamowienia.html", current_url=current_url)
