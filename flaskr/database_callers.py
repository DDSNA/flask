from flask import jsonify
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
import json


def historical_call():
    connection_string_view = "mysql+mysqldb://frontend_tabledisplay:MareParolaMare98@containers-us-west-174.railway.app:7822/restricted_schema"
    engine_2 = create_engine(connection_string_view, echo=True)
    metadata = MetaData()
    Session = sessionmaker(bind=engine_2)
    session = Session()
    view_table = Table("json_table_backup", metadata, autoload_with=engine_2)
    with engine_2.connect() as conn_2:
        get_view_data = select(view_table)
        print(get_view_data)
        try:
            _results = session.execute(get_view_data)
            _rows = _results.fetchall()
            _results_dictionary = [{'data': json.dumps(row[1]), 'timestamp': row[2], 'index':row[0]} for row in _rows]
            conn_2.close()
            print(_results_dictionary)
        except Exception as e:
            print("Whoa! Error! This is th error itself: ", e)
            import traceback
            traceback.print_exc()
            conn_2.close()
        return _results_dictionary
