import pickle
import json
import os


if __name__ == "__main__":
    if os.path.exists("files/server-files/save.save"):
        items = pickle.load(open("files/server-files/save.save", "rb"))
        print(items)

        data = {
            "hello": 4
        }

        for item in items:
            print(item)
            try:

                buy_orders = items[item].buy_orders_getter()
                # print([[a, p] for a, p, oR in o for o in items[item].buy_orders_getter()])
                data[item] = {
                    "graph": {
                        "data":[
                        items[item].rt_buy_price_getter(),
                        items[item].rt_sell_price_getter(),
                        [items[item].get_avg_buy_price()] * len(items[item].rt_times_getter())
                    ],
                        "values": [
                            items[item].rt_times_getter()
                        ]
                    },
                    "table": [
                        [o["amount"], o["pricePerUnit"]] for o in buy_orders
                    ],
                    "avg": items[item].get_avg_buy_price()
                }
            except ZeroDivisionError:
                pass
        with open('files/server-files/save.json', 'w') as f:
            json.dump(data, f)


            # json_string = json.dumps(data)
            # print(json.loads(json_string))
        with open('files/server-files/save.json', 'r') as f:
            data = json.load(f)
        print(type(data))
    else:
        print("NO DATA")
        exit()