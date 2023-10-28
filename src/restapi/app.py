from flask import Flask, request
from db_controller import DbController

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db = DbController("../my_database.db")


@app.route('/')
def index():
    return 'Hello'


@app.route('/offers', methods=['GET'])
@app.route('/offers/<where_conditions>', methods=['GET'])
def get_offers(where_conditions=''):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    where_conditions = request.args.get('<where_conditions>', where_conditions)
    return db.get_all_records_as_json(page, limit, where_conditions)


if __name__ == '__main__':
    app.run(debug=True)
