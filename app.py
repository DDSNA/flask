import json
import logging
import os
import os.path
from datetime import datetime

import requests
from flask import Flask, render_template, current_app, redirect, jsonify
import flask_caching
from sqlalchemy import create_engine, insert, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

from flaskr.database_callers import historical_call

# security import

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

# config

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 900
}

app.config.from_mapping(config)
cache = flask_caching.Cache(app)


# only creating this here because of security reasons
connection_string = "mysql+mysqldb://pythonapp:BadPass2023@containers-us-west-174.railway.app:7822/railway"
engine = create_engine(connection_string, pool_recycle=360, echo=True)

# logging
logging.basicConfig()


# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)


@app.route('/', methods=['GET'])
@cache.cached(timeout=1000)
def index():
    try:
        render_template('index.html')

    except Exception as e:
        print('There was an error: %s', e)
    return render_template('index.html')


@app.route('/secret')
def secret_key():
    __secret_key = app.config.get("SECRET KEY")
    return f"The configured secret key is {__secret_key}."


@app.route('/call-fuzz')
@cache.cached(timeout=600)
def call_fuzz():

    api_url = (
        "https://market.fuzzwork.co.uk/aggregates/?region=60008494&types=2268,2305,2267,2288,2287,2307,2272,2309,2073,2310,2270,2306,2286,2311,2308,2393,2396,3779,2401,2390,2397,2392,3683,2389,2399,2395,2398,9828,2400,3645,2329,3828,9836,9832,44,3693,15317,3725,3689,2327,9842,2463,2317,2321,3695,9830,3697,9838,2312,3691,2319,9840,3775,2328,2358,2345,2344,2367,17392,2348,9834,2366,2361,17898,2360,2354,2352,9846,9848,2351,2349,2346,12836,17136,28974,2867,2868,2869,2870,2871,2872,2875,2876%22")
    response = requests.get(api_url)
    print(response.url)
    print(response.status_code)
    response.json()
    data = response.text
    print(data)
    thedata = json.loads(data)
    print(thedata)
    return thedata


@app.route('/call-to-db')
@cache.cached(timeout=200)
def call_db_and_fuzz():
    api_url = (
        "https://market.fuzzwork.co.uk/aggregates/?region=60008494&types=2268,2305,2267,2288,2287,2307,2272,2309,2073,2310,2270,2306,2286,2311,2308,2393,2396,3779,2401,2390,2397,2392,3683,2389,2399,2395,2398,9828,2400,3645,2329,3828,9836,9832,44,3693,15317,3725,3689,2327,9842,2463,2317,2321,3695,9830,3697,9838,2312,3691,2319,9840,3775,2328,2358,2345,2344,2367,17392,2348,9834,2366,2361,17898,2360,2354,2352,9846,9848,2351,2349,2346,12836,17136,28974,2867,2868,2869,2870,2871,2872,2875,2876")
    response = requests.get(api_url)

    data = response.text
    # noinspection SpellCheckingInspection
    thedata = json.loads(data)
    print(response.status_code)

    def save_folder_location_printer():
        local_folder = os.path.join(current_app.root_path)
        print(local_folder)
        return local_folder

    save_folder_location_printer()
    current_time = datetime.utcnow()
    file_name = r"%s/flaskr/temp-data/jsons/" % save_folder_location_printer() + current_time.strftime(
        '%d-%m-%Y-%H-%M-%S.json')
    with open(file_name, 'w') as fp:
        fp.write(data)
        print('created', file_name)
    with open(file_name, "r") as fr:
        read_test = fr.read()
        print(read_test)
        print('reading: ', file_name)

    # PHIND
    meta = MetaData()

    # Reflect your table
    my_table = Table('TEST_EVE_DATA', meta, autoload_with=engine)

    with engine.connect() as conn:
        upload_json = insert(my_table).values(JSON_File=thedata)
        try:
            conn.execute(upload_json)
            conn.commit()
            print(read_test)
        except Exception as e:
            print("An error occurred during database insertion: ", e)
            import traceback
            traceback.print_exc()

    # PHIND

    conn.close()

    return thedata


@app.route('/historical_table', methods=['GET'])
@cache.cached(timeout=600)
def show_historical_jsons():
    try:
        historical_data = historical_call()
        print(historical_data)
        return render_template('historical_datapage.html', data=historical_data)
    except Exception as e:
        print('Got this error lol:', e)



# redirect for mismatch between / and /static
@app.route('/static/')
def static_redirect():
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
