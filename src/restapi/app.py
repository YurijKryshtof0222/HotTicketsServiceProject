from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_controller import DbController

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db = DbController("../my_database.db")


@app.route('/')
def index():
    return 'Hello'


@app.route('/records', methods=['GET'])
def get_records():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    return db.get_all_records_as_json(page, limit)


@app.route('/records/filter', methods=['GET'])
def get_filtered_records():
    # Отримання параметрів з URL-запиту та обробка їх
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offer_name = request.args.get('offer_name', '')
    country = request.args.get('country', '')
    # Додайте обробку інших параметрів

    return db.get_filtered_records_as_json(page, limit, offer_name, country)


if __name__ == '__main__':
    app.run()
