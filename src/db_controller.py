import sqlite3
import sys

from flask import jsonify
from src.offer import Offer


class DbController:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not DbController.__instance:
            DbController.__instance = super().__new__(cls)
        return DbController.__instance

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    # using for init database
    def create_table(self):
        # Створюємо таблицю, якщо вона не існує
        create_table_offer = '''
                    CREATE TABLE IF NOT EXISTS offer (
                        uniq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        offer_id INTEGER,
                        offer_name STRING,
                        offer_source STRING,
                        location STRING,
                        people_count INTEGER,
                        description STRING,
                        food_info STRING,
                        night_count INTEGER,
                        start_date DATE,
                        end_date DATE,
                        transport_info STRING,
                        price INTEGER
                    );
                '''
        create_table_offer_links = '''
                            CREATE TABLE IF NOT EXISTS offer_links (
                                link_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                offer_id INTEGER,
                                link STRING
                            );
                        '''
        self.cursor.execute(create_table_offer)
        self.cursor.execute(create_table_offer_links)
        self.conn.commit()

    def __convert_to_json(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        records = []

        for row in rows:
            offer_id = row[1]
            query_links = '''
                                   SELECT * FROM offer_links WHERE offer_id = ?;
                               '''
            self.cursor.execute(query_links, (offer_id,))
            links_row = self.cursor.fetchall()
            links = []
            for link in links_row:
                links.append(link[2])

            record = {
                "uniq_id" : row[0],
                "offer_id": row[1],
                "offer_name": row[2],
                "offer_source": row[3],
                "location": row[4],
                "people_count": row[5],
                "description": row[6],
                "food_info": row[7],
                "night_count": row[8],
                "start_date": row[9],
                "end_date": row[10],
                "transport_info": row[11],
                "price": row[12],
                "links": links
            }
            # print(record)

            records.append(record)

        return jsonify({'offer': records})

    # add record (tour) to database
    def add_offer(self, offer):
        # Insert data into the "offer" and "offer_variation" tables
        insert_to_offer_sql = '''
                            INSERT INTO offer (
                            uniq_id, 
                            offer_id, 
                            offer_name, 
                            offer_source, 
                            location, 
                            people_count, 
                            description, 
                            food_info, 
                            night_count, 
                            start_date, 
                            end_date,
                            transport_info,
                            price)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        '''
        self.cursor.execute(insert_to_offer_sql, (
            None,
            offer.offer_id,
            offer.name,
            offer.source,
            offer.location,
            offer.people_count,
            offer.description,
            offer.food_info,
            offer.night_count,
            offer.start_date,
            offer.end_date,
            offer.transport_info,
            offer.price
        ))
        self.conn.commit()
        for link in offer.img_links:
            insert_to_offer_links_sql = '''
                           INSERT INTO offer_links (link_id, offer_id, link)
                           VALUES (?, ?, ?);
                       '''
            self.cursor.execute(insert_to_offer_links_sql, (None, offer.offer_id, link))
            self.conn.commit()

    # select all record with pagination
    def get_all_offers_as_json(self,
                               page,
                               limit,
                               min_uniq_id,
                               max_uniq_id,
                               min_offer_id,
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
                               max_price):
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        query = f"""
               SELECT * FROM offer
               WHERE offer_name LIKE '%{name}%'
                 AND location LIKE '%{location}%'
                 AND people_count BETWEEN {min_people_count} AND {max_people_count}
                 AND food_info LIKE '%{food_info}%'
                 AND night_count BETWEEN {min_night_count} AND {max_night_count}
                 AND transport_info LIKE '%{transport_info}%'
                 AND price BETWEEN {min_price} AND {max_price}
           """

        if min_offer_id >= 0:
            query += f" AND offer_id >= {min_offer_id}"
        if max_offer_id >= 0:
            query += f" AND offer_id <= {max_offer_id}"

        if min_uniq_id >= 0:
            query += f" AND uniq_id >= {min_uniq_id}"
        if max_uniq_id >= 0:
            query += f" AND uniq_id <= {max_uniq_id}"

        if start_date and start_date.split():
            query += f" AND start_date LIKE '{start_date}%'"
        if end_date and end_date.split():
            query += f" AND end_date LIKE '{end_date}%'"

        query += f" ORDER BY uniq_id LIMIT {limit} OFFSET {offset}"

        return self.__convert_to_json(query)

    def get_offer_as_json(self, offer_id):
        query = f'''
            SELECT * FROM offer 
            WHERE offer_id = {offer_id}
            ORDER BY uniq_id DESC 
        '''

        return self.__convert_to_json(query)

    def get_offer(self, uniq_id):
        query = """
            SELECT * FROM offer WHERE uniq_id = ?
        """

        self.cursor.execute(query, (uniq_id,))
        row = self.cursor.fetchone()

        query_to_select_id = f"""
                    SELECT offer_id FROM offer
                    WHERE uniq_id={uniq_id}
                """
        self.cursor.execute(query_to_select_id)
        offer_id = self.cursor.fetchone()
        print(offer_id)

        query_links = '''
                        SELECT * FROM offer_links WHERE offer_id = ?;
                      '''
        self.cursor.execute(query_links, (offer_id[0],))
        links_cols = self.cursor.fetchall()
        links = []
        for link in links_cols:
            links.append(link[2])

        return Offer(
            offer_id=row[1],
            name=row[2],
            source=row[3],
            location=row[4],
            people_count=row[5],
            description=row[6],
            food_info=row[7],
            night_count=row[8],
            start_date=row[9],
            end_date=row[10],
            transport_info=row[11],
            price=row[12],
            img_links=links
        )

    def delete_offers(self,
                      min_uniq_id=None,
                      max_uniq_id=None,
                      min_offer_id=None,
                      max_offer_id=None,
                      name=None,
                      location=None,
                      min_people_count=None,
                      max_people_count=None,
                      food_info=None,
                      min_night_count=None,
                      max_night_count=None,
                      min_start_date=None,
                      max_start_date=None,
                      min_end_date=None,
                      max_end_date=None,
                      transport_info=None,
                      min_price=None,
                      max_price=None
                      ):

        where_conditions = ""

        if min_offer_id is not None:
            where_conditions += f" AND uniq_id >= {min_uniq_id}"
        if max_offer_id is not None:
            where_conditions += f" AND uniq_id <= {max_uniq_id}"
        if min_offer_id is not None:
            where_conditions += f" AND offer_id >= {min_offer_id}"
        if max_offer_id is not None:
            where_conditions += f" AND offer_id <= {max_offer_id}"
        if name is not None:
            where_conditions += f" AND offer_name LIKE {name}%"
        if location is not None:
            where_conditions += f" AND location LIKE {location}% "
        if min_people_count is not None:
            where_conditions += f" AND people_count >= {min_people_count}"
        if max_people_count is not None:
            where_conditions += f" AND people_count <= {max_people_count}"
        if food_info is not None:
            where_conditions += f" AND food_info LIKE {food_info}%"
        if min_night_count is not None:
            where_conditions += f" AND night_count >= {min_night_count}"
        if max_night_count is not None:
            where_conditions += f" AND night_count <= {max_night_count}"
        if transport_info is not None:
            where_conditions += f" AND transport_info LIKE {transport_info}%"
        if min_price is not None:
            where_conditions += f" AND price >= {min_price}"
        if max_price is not None:
            where_conditions += f" AND price <= {max_price}"
        if min_start_date is not None and min_start_date.strip():
            where_conditions += f" AND start_date >= '{min_start_date}' "
        if max_start_date is not None and max_start_date.strip():
            where_conditions += f" AND start_date <= '{max_start_date}' "
        if min_end_date is not None and min_start_date.strip():
            where_conditions += f" AND end_date >= '{min_end_date}' "
        if max_end_date is not None and max_start_date.strip():
            where_conditions += f" AND end_date <= '{max_end_date}' "

        query_to_select_id = """
            SELECT offer_id FROM offer
            WHERE 1=1
        """
        query_to_select_id += where_conditions
        self.cursor.execute(query_to_select_id)

        offer_link_list = self.cursor.fetchall()

        for offer_link in offer_link_list:
            query_links = "DELETE FROM offer_links WHERE offer_id = ?"
            self.cursor.execute(query_links, (offer_link[0],))

        query_to_delete_offers = """
            DELETE FROM offer
            WHERE 1=1
        """
        query_to_delete_offers += where_conditions
        print(query_to_delete_offers)
        self.cursor.execute(query_to_delete_offers)



    def update_offer(self, offer_id, offer):
        query = """
            UPDATE offer
            SET offer_name = ?,
                offer_source = ?,
                location = ?,
                people_count = ?,
                description = ?,
                food_info = ?,
                night_count = ?,
                start_date = ?,
                end_date = ?,
                transport_info = ?,
                price = ?
            WHERE offer_id = ?
        """
        self.cursor.execute(query, (
            offer.name,
            offer.source,
            offer.location,
            offer.people_count,
            offer.description,
            offer.food_info,
            offer.night_count,
            offer.start_date,
            offer.end_date,
            offer.transport_info,
            offer.price,

            offer_id))

    def delete_offer(self, offer_id):
        query = """
                    DELETE FROM offer
                    WHERE offer_id = ?
                """
        self.cursor.execute(query, (offer_id,))

        query = """
                    DELETE FROM offer_links
                    WHERE offer_id = ?
                """
        self.cursor.execute(query, (offer_id,))

    def close_connection(self):
        self.conn.close()
