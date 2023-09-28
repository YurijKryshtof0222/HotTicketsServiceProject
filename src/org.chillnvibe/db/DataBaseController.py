import sqlite3
class DbController:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Створюємо таблицю, якщо вона не існує
        create_table_offer_variation = '''
            CREATE TABLE IF NOT EXISTS offer_variation (
                variation_id INTEGER,
                offer_id INTEGER,
                night_count INTEGER,
                start_date DATE,
                end_date DATE
            );
        '''
        create_table_offer = '''
                    CREATE TABLE IF NOT EXISTS offer (
                        offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        offer_name STRING,
                        offer_source STRING,
                        location STRING,
                        description STRING,
                        food_info STRING
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
        self.cursor.execute(create_table_offer_variation)
        self.cursor.execute(create_table_offer_links)
        self.conn.commit()

    def add_data(self, uniq_id, offer_name, offer_source, location, description, food_info, night_count, start_date, end_date, links):
        # Insert data into the "offer" and "offer_variation" tables
        insert_to_offer_sql = '''
                            INSERT INTO offer (offer_id, offer_name, offer_source, location, description, food_info)
                            VALUES (?, ?, ?, ?, ?, ?);
                        '''
        self.cursor.execute(insert_to_offer_sql, (None, offer_name, offer_source, location, description, food_info))
        self.conn.commit()

        # Get the last inserted row ID (offer_id)
        offer_id = self.cursor.lastrowid
        insert_to_offer_variation_sql = '''
                               INSERT INTO offer_variation (variation_id, offer_id, night_count, start_date, end_date)
                               VALUES (?, ?, ?, ?, ?);
                           '''
        self.cursor.execute(insert_to_offer_variation_sql, (uniq_id, offer_id, night_count, start_date, end_date))
        self.conn.commit()
        for link in links:
            insert_to_offer_links_sql = '''
                           INSERT INTO offer_links (link_id, offer_id, link)
                           VALUES (?, ?, ?);
                       '''
            self.cursor.execute(insert_to_offer_links_sql, (None, offer_id, link))
            self.conn.commit()

    def delete_data(self, variation_id):
        # Видаляємо дані з таблиці за ідентифікатором
        delete_data_sql = '''
            DELETE FROM my_table
            WHERE id = ?;
        '''
        self.cursor.execute(delete_data_sql, (data_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()