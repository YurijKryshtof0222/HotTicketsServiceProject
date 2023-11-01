from datetime import datetime
from re import split

from flask import Flask, request, jsonify

from db_controller import DbController
from src.offer import Offer

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
db = DbController("../my_database.db")


@app.route('/')
def index():
    return 'Hello'


@app.route('/offers', methods=['GET'])
def get_offers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    name = str(request.args.get('name', ''))
    location = str(request.args.get('location', ''))
    min_people_count = int(request.args.get('min_people_count', 1))
    max_people_count = int(request.args.get('max_people_count', 10))
    food_info = str(request.args.get('food_info', ''))
    min_night_count = int(request.args.get('min_night_count', 1))
    max_night_count = int(request.args.get('max_night_count', 12))
    start_date = str(request.args.get('start_date', ''))
    end_date = str(request.args.get('end_date', ''))
    transport_info = request.args.get('transport_info', '')
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 9999999))

    return db.get_all_offers_as_json(page,
                                     limit,
                                     name,
                                     location,
                                     min_people_count,
                                     max_people_count,
                                     food_info,
                                     min_night_count,
                                     max_night_count,
                                     start_date,
                                     end_date,
                                     transport_info,
                                     min_price,
                                     max_price)


@app.route('/offer/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    return db.get_offer_as_json(offer_id)


@app.route('/offers', methods=['POST'])
def create_offer():
    # Отримуємо дані з тіла POST-запиту у форматі JSON
    data = request.form

    comma_and_blank_regex = ' *, *'

    offer = Offer(
        offer_id=int(data['offer_id']),
        name=data['name'],
        source=data['source'],
        location=data['location'],
        people_count=int(data['people_count']),
        description=data['description'],
        food_info=data['food_info'],
        night_count=int(data['night_count']),
        start_date=datetime.strptime(data['start_date'], '%d.%m.%Y'),
        end_date=datetime.strptime(data['end_date'], '%d.%m.%Y'),
        transport_info=data['transport_info'],
        price=int(data['price']),
        img_links=split(comma_and_blank_regex, data['img_links'])
    )

    db.add_offer(offer)

    return jsonify({'message': 'Selected Offers created successfully'}), 201


@app.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    data = request.form
    offer = db.get_offer(offer_id)

    if offer is None:
        return jsonify({'error': 'Offer not found'}), 404

    # Оновлюємо дані об'єкта "offer" на основі даних з запиту
    offer.name = data.get('name', offer.name)
    offer.source = data.get('source', offer.source)
    offer.location = data.get('location', offer.location)
    offer.people_count = data.get('people_count', offer.people_count)
    offer.description = data.get('description', offer.description)
    offer.food_info = data.get('food_info', offer.food_info)
    offer.night_count = data.get('night_count', offer.night_count)
    offer.start_date = data.get('start_date', offer.start_date)
    offer.end_date = data.get('end_date', offer.end_date)
    offer.transport_info = data.get('transport_info', offer.transport_info)
    offer.price = data.get('price', offer.price)
    offer.img_links = data.get('img_links', offer.img_links)

    db.update_offer(offer, id)  # Зберігаємо оновлений запис "offer" в базі даних

    return jsonify({'message': 'Selected Offers updated successfully'}), 200


@app.route('/offer/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    db.delete_offer(offer_id)

    return jsonify({'message': 'Selected Offer deleted successfully'}), 200


@app.route('/offers', methods=['DELETE'])
def delete_offers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    name = str(request.args.get('name', ''))
    location = str(request.args.get('location', ''))
    min_people_count = int(request.args.get('limit', 1))
    max_people_count = int(request.args.get('limit', 10))
    food_info = str(request.args.get('food_info', ''))
    min_night_count = int(request.args.get('min_night_count', 1))
    max_night_count = int(request.args.get('max_night_count', 12))
    start_date = str(request.args.get('start_date', ''))
    end_date = str(request.args.get('end_date', ''))
    transport_info = request.args.get('transport_info', '')
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 9999999))

    delete_offers(name,
                  location,
                  min_people_count,
                  max_people_count,
                  food_info,
                  min_night_count,
                  max_night_count,
                  start_date,
                  end_date,
                  transport_info,
                  min_price,
                  max_price)

    return jsonify({'message': 'Selected offers deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
