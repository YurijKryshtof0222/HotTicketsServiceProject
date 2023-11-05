from datetime import datetime

from flask import Flask, request, jsonify

from src.db_controller import DbController
from src.offer import Offer

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
db = DbController("../my_database.db")


@app.route('/')
def index():
    return '<h1>Hello</h1>'


@app.route('/offer/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    return db.get_offer_as_json(offer_id)


@app.route('/offers', methods=['GET'])
def get_offers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    #...
    min_offer_id = int(request.args.get('min_offer_id', 0))
    max_offer_id = int(request.args.get('max_offer_id', 9999999999))
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
    max_price = int(request.args.get('max_price', 999999999))

    return db.get_all_offers_as_json(page,
                                     limit=limit,
                                     name=name,
                                     min_offer_id=min_offer_id,
                                     max_offer_id=max_offer_id,
                                     location=location,
                                     min_people_count=min_people_count,
                                     max_people_count=max_people_count,
                                     food_info=food_info,
                                     min_night_count=min_night_count,
                                     max_night_count=max_night_count,
                                     start_date=start_date,
                                     end_date=end_date,
                                     transport_info=transport_info,
                                     min_price=min_price,
                                     max_price=max_price)


@app.route('/offer', methods=['POST'])
def create_offer():
    # Отримуємо дані з тіла POST-запиту у форматі JSON
    data = request.get_json()
    #...
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
        img_links=data['img_links']
    )

    db.add_offer(offer)

    return jsonify({'message': 'Offer created successfully'}), 201


@app.route('/offers', methods=['POST'])
def create_offers():
    # Get data from the request body in JSON format
    data = request.get_json()
    comma_and_blank_regex = ' *, *'
    for entry in data:
        offer = Offer(
            offer_id=int(entry['offer_id']),
            name=entry['name'],
            source=entry['source'],
            location=entry['location'],
            people_count=int(entry['people_count']),
            description=entry['description'],
            food_info=entry['food_info'],
            night_count=int(entry['night_count']),
            start_date=datetime.strptime(entry['start_date'], '%d.%m.%Y'),
            end_date=datetime.strptime(entry['end_date'], '%d.%m.%Y'),
            transport_info=entry['transport_info'],
            price=int(entry['price']),
            img_links=entry['img_links']
        )
        db.add_offer(offer)
    return jsonify({'message': ' Offers created successfully'}), 201


@app.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    data = request.form
    offer = request.args.get(db.get_offer(offer_id))

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
    min_offer_id = int(request.args.get('min_offer_id')) if request.args.get('min_offer_id') else None
    max_offer_id = int(request.args.get('max_offer_id')) if request.args.get('max_offer_id') else None
    name = request.args.get('name')
    location = request.args.get('location')
    min_people_count = int(request.args.get('min_people_count')) if request.args.get('min_people_count') else None
    max_people_count = int(request.args.get('min_people_count')) if request.args.get('min_people_count') else None
    food_info = request.args.get('food_info')
    min_night_count = int(request.args.get('min_night_count')) if request.args.get('min_night_count') else None
    max_night_count = int(request.args.get('max_night_count')) if request.args.get('max_night_count') else None
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    transport_info = request.args.get('transport_info')
    min_price = int(request.args.get('min_price')) if request.args.get('min_price') else None
    max_price = int(request.args.get('max_price')) if request.args.get('max_price') else None

    db.delete_offers(min_offer_id,
                     max_offer_id,
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

    return jsonify({'message': 'Selected offers deleted successfully'}), 200


# if __name__ == '__main__':
#     app.run()
