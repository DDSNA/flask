from flask import jsonify
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import json

def historical_call(__frontend_key,__frontend_db,__url_db,__port_db):
    """This function is used to call the historical data from the database.
    It is used in the /historical route.
    :return: A list of dictionaries with the data and timestamp.
    """
    connection_string_view = f"mysql+mysqldb://frontend_user:{__frontend_key}@c{__url_db}:{__port_db}/{__frontend_db}"
    engine_2 = create_engine(connection_string_view, echo=True)
    metadata = MetaData()
    Session = sessionmaker(bind=engine_2)
    session = Session()
    view_table = Table("json_table", metadata, autoload_with=engine_2)
    with engine_2.connect() as conn_2:
        get_view_data = select(view_table)
        print(get_view_data)
        try:
            _results = session.execute(get_view_data)
            _rows = _results.fetchall()
            _results_dictionary = [{'data': json.dumps(row[1]), 'timestamp': row[2], 'index':row[0]} for row in _rows]
            conn_2.close()
        except Exception as e:
            print("Whoa! Error! This is th error itself: ", e)
            import traceback
            traceback.print_exc()
            conn_2.close()
        return _results_dictionary
