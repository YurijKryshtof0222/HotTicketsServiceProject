from DataBaseController import DbController

if __name__ == '__main__':
    db_controller = DbController("my_database.db")
    # db_controller.add_data(
    #     offer_id=5555,
    #     offer_name="Paris",
    #     offer_source="www//htkfnlvdn",
    #     location="France",
    #     people_count=2,
    #     description="Lorem ipsu...",
    #     food_info="All inclusive",
    #     night_count="5",
    #     start_date="28.09.2023",
    #    end_date="15.10.2023",
    #     links=["link1", "link2", "link2"],
    # )
    json_records = db_controller.get_all_records_as_json(5, 1)
    print(json_records)