from datetime import datetime

from src.restapi import db_controller


class Offer:
    def __init__(self,
                 offer_id: int,
                 name: str,
                 source: str,
                 location: str,
                 people_count: int,
                 description: str,
                 food_info: str,
                 night_count: int,
                 start_date: datetime,
                 end_date: datetime,
                 transport_info: str,
                 price: int,
                 img_links: [str]
                 ):
        self._offer_id = offer_id
        self._name = name
        self._source = source
        self._location = location
        self._people_count = people_count
        self._description = description
        self._food_info = food_info
        self._night_count = night_count
        self._start_date = start_date
        self._end_date = end_date
        self._transport_info = transport_info
        self._price = price
        self._img_links = img_links

    def print_info(self):
        print(f'Offer ID: {self._offer_id}',
              f'Offer name: {self._name}',
              f'Offer source: {self._source}',
              f'Location: {self._location}',
              f'Tourists count: {self._people_count}',
              f'Description: {self._description}',
              f'Food info: {self._food_info}',
              f'Nights count: {self._night_count}',
              f'Start Date: {self._start_date.strftime("%d.%m.%Y")}',
              f'End Date: {self._end_date.strftime("%d.%m.%Y")}',
              f'Transport: {self._transport_info}',
              f'Price: {self._price}',

              f'Images:',
              sep='\n')

        print('\t')
        for e in self._img_links:
            print(e)
        print()

    def add_to_db(self, db: db_controller.DbController):
        db.add_data(
            offer_id=self._offer_id,
            offer_name=self._name,
            offer_source=self._source,
            location=self._location,
            people_count=self._people_count,
            description=self._description,
            food_info=self._food_info,
            night_count=self._night_count,
            start_date=self._start_date,
            end_date=self._end_date,
            transport_info=self._transport_info,
            price=self._price,
            links=self._img_links)
