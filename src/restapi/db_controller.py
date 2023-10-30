import sqlite3

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

    def __convert_to_json(self, query, limit, offset):
        self.cursor.execute(query, (limit, offset))
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
                "links": links
            }

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
    def get_all_records_as_json(self, page, limit, where=''):
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        query = '''
               SELECT * FROM offer 
           '''

        if where and where.strip():
            where_args = where.split('&')
            length = len(where_args)

            query += "WHERE "
            for i in range(length):
                query += where_args[i]
                if i != length - 1:
                    query += " AND "

        query += """
            \nORDER BY uniq_id DESC LIMIT ? OFFSET ?
        """
        return self.__convert_to_json(query, limit, offset)

    def close_connection(self):
        self.conn.close()

    def get_offer(self, offer_id):
        query = """
            SELECT * FROM offer WHERE offer_id = ?
        """

        self.cursor.execute(query, (offer_id,))
        row = self.cursor.fetchone()

        query_links = '''
                                           SELECT * FROM offer_links WHERE offer_id = ?;
                                       '''
        self.cursor.execute(query_links, (offer_id,))
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

    def update_offer(self, offer, id):
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

            offer.offer_id))
