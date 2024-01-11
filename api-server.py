from flask import Flask, request, render_template, url_for, session, redirect, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
app.secret_key = "masuperclef"
CORS(app)

@app.route("/projects/bazaar-tracker/items/<item>/api")
def return_api_data(item):
    sample_data = {
    "graphAmount": 1,
    "graphBottomData": [
    items[item].rt_times_getter()
    ],
    "graphDatas": [
        [
        items[item].rt_buy_price_getter(),
        items[item].rt_sell_price_getter(),
        [items[item].get_avg_buy_price()]*len(items[item].rt_times_getter())
        ]
    ],
    "graphObjects": [
        document.querySelector("#graph")
    ]
    }
    return jsonify(sample_data)

if __name__ == "__main__":
    if os.path.exists("save/save.save"):
        items = pickle.load(open("save/save.save", "rb"))
        print(items)
    else:
        print("NO DATA")
        exit()

    app.run(debug=False, port=80, host="0.0.0.0")
