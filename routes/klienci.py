from flask import Blueprint, request, Response, abort, jsonify, render_template
from connection.database import Database

klienci_route = Blueprint('klienci_route', __name__)


@klienci_route.route("/klienci", methods=['POST', 'GET', 'UPDATE', 'DELETE'])
def lista_klientow():
    """
    Route do obslugi tabeli klientow. W zaleznosci od metody sa wykonywane rozne akcje:
    - POST: Dodanie nowego klienta
    - GET: Pokaz liste klientow
    - UPDATE: zaktualizuj klienta w bazie
    - DELETE: usun klienta
    """
    current_url = request.path
    if request.method == "GET":
        db = Database()
        db.connect_to_database()
        query = "SELECT * FROM klienci"
        result = db.exec_query(query, "select")
        kolumny = ['id', 'Imie', 'Nazwisko', 'Nr telefonu', 'Adres', 'Kod pocztowy', 'Miasto', 'Email', 'Akcje']
        if result:
            print(f"Result {result}")
        return render_template("klienci.html", current_url=current_url, kolumny=kolumny,
                               klienci=result)

@klienci_route.route("/pokaz_zamowienia_dla_klienta")
def zamowienia_per_klient():
    pass
