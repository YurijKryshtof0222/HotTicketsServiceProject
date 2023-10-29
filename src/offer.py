from datetime import datetime
from dataclasses import dataclass


@dataclass
class Offer:
    offer_id: int
    name: str
    source: str
    location: str
    people_count: int
    description: str
    food_info: str
    night_count: int
    start_date: datetime
    end_date: datetime
    transport_info: str
    price: int
    img_links: [str]

    def print_info(self):
        print(f'Offer ID: {self.offer_id}',
              f'Offer name: {self.name}',
              f'Offer source: {self.source}',
              f'Location: {self.location}',
              f'Tourists count: {self.people_count}',
              f'Description: {self.description}',
              f'Food info: {self.food_info}',
              f'Nights count: {self.night_count}',
              f'Start Date: {self.start_date.strftime("%d.%m.%Y")}',
              f'End Date: {self.end_date.strftime("%d.%m.%Y")}',
              f'Transport: {self.transport_info}',
              f'Price: {self.price}',
              'Images: ',
              *self.img_links,
              sep='\n')