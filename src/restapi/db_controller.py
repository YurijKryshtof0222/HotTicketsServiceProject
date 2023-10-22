import sqlite3
import json


class DbController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
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

    def __execute_query(self, query, limit, offset):
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
        return json.dumps(records)

    # add record (tour) to database
    def add_data(self,
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
                 price,
                 links):
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
            price
        ))
        self.conn.commit()
        for link in links:
            insert_to_offer_links_sql = '''
                           INSERT INTO offer_links (link_id, offer_id, link)
                           VALUES (?, ?, ?);
                       '''
            self.cursor.execute(insert_to_offer_links_sql, (None, offer_id, link))
            self.conn.commit()

    # select all record with pagination
    def get_all_records_as_json(self, page, limit):
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        query = '''
               SELECT * FROM offer ORDER BY uniq_id DESC LIMIT ? OFFSET ?
           '''
        return self.__execute_query(query, limit, offset)

    def get_filtered_records_as_json(self,
                                     page,
                                     limit,
                                     offer_name='',
                                     country='',
                                     people_count_operation='',
                                     people_count_value=0,
                                     food_info='',
                                     night_count_operation='',
                                     night_count_value=0,
                                     start_date_operation='',
                                     start_date_value=0,
                                     end_date_operation='',
                                     end_date_value=0,
                                     price_operation='',
                                     price_value=0):
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit

        conditions_dict = list()

        conditions_dict.append(f'offer_name =  "{offer_name}"'
                               if offer_name and offer_name.strip() else '')
        conditions_dict.append(f'location LIKE "{country}"%'
                               if country and country.strip() else '')
        conditions_dict.append(f' people_count  {people_count_operation} {people_count_value}'
                               if (people_count_operation
                                   and people_count_operation.strip()
                                   and people_count_value > 0) else '')
        conditions_dict.append(f'food_info = "{food_info}"' if (food_info and food_info.strip()) else '')
        conditions_dict.append(f'night_count {night_count_operation} {night_count_value}'
                               if (night_count_operation
                                   and night_count_operation.strip()
                                   and night_count_value > 0) else '')
        conditions_dict.append(f'start_date {end_date_operation}, {end_date_value}'
                               if (end_date_operation
                                   and end_date_operation.strip()
                                   and end_date_value > 0) else '')
        conditions_dict.append(f'start_date {start_date_operation}, {start_date_value}'
                               if (start_date_operation
                                   and start_date_operation.strip()
                                   and start_date_value > 0) else '')
        conditions_dict.append(f'price {price_operation} {price_value}'
                               if (price_operation
                                   and price_operation.strip()
                                   and price_value > 0) else '')
        query = "SELECT * FROM offer WHERE "

        is_first_cond = True
        for condition in conditions_dict:
            if condition:
                if not is_first_cond:
                    query += 'AND ' + condition
                    is_first_cond = False
                else:
                    query += condition

        query += ' ORDER BY uniq_id DESC LIMIT ? OFFSET ?'
        return self.__execute_query(query, limit, offset)

    def close_connection(self):
        self.conn.close()
