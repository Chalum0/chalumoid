import pickle
import os
import datetime
import time

def at_the_end(list_, argument, length):
    list_.append(argument)
    if len(list_) > length:
        list_.pop(0)

class Obj:
    def __init__(self, item, data):
        self.data_amount = 20
        self._item = item

        # LIVE ORDERS TABLE
        self._buy_orders = []
        self._sell_offers = []

        self._buy_orders_amount = 0
        self._sell_offers_amount = 0

        # LIVE VIEW
        self._rt_buy_price = []
        self._rt_sell_price = []
        self._rt_times = []

        self._daily_average_buy_price = []
        self._daily_average_sell_price = []
        self._weekly_average_buy_price = []
        self._weekly_average_sell_price = []
        self._daily_buy_price = []
        self._daily_sell_price = []
        self._daily_times = []
        self._weekly_buy_price = []
        self._weekly_sell_price = []
        self._weekly_times = []
        self._last_daily_update = 0
        self._last_weekly_update = 0

        # WEEKLY OVERVIEW

        self.tt_price = 0.0
        self.amount_values = 0.0



        self.update_prices(data=data[self._item])


    def update_prices(self, data):
        try:
            buy_orders = data["sell_summary"]
            sell_offers = data["buy_summary"]

            self._buy_orders = buy_orders
            self._sell_offers = sell_offers

            self._buy_orders_amount = 0
            self._sell_offers_amount = 0

            for i in buy_orders:
                self._buy_orders_amount += i["orders"]
            for i in sell_offers:
                self._sell_offers_amount += i["orders"]


            buy_highest = buy_orders[0]["pricePerUnit"]
            sell_highest = sell_offers[0]["pricePerUnit"]

            buy_price = buy_highest + 0.1
            sell_price = sell_highest - 0.1

            self.tt_price += buy_price
            self.amount_values += 1

            # REAL TIME PRICES UPDATE
            at_the_end(self._rt_buy_price, round(buy_price, 1), self.data_amount)
            at_the_end(self._rt_sell_price, round(sell_price, 1), self.data_amount)
            at_the_end(self._rt_times, f"{datetime.datetime.now().hour}h:{datetime.datetime.now().minute}m:{datetime.datetime.now().second}s", self.data_amount)

            # DAILY PRICES UPDATE
            self._daily_average_buy_price.append(buy_price)
            self._daily_average_sell_price.append(sell_price)


            tme = time.time()
            if tme - self._last_daily_update >= (3600 * 24)/self.data_amount:
                at_the_end(self._daily_buy_price, sum(self._daily_average_buy_price)/len(self._daily_average_buy_price), self.data_amount)
                at_the_end(self._daily_sell_price, sum(self._daily_average_sell_price)/len(self._daily_average_sell_price), self.data_amount)
                self._daily_average_buy_price, self._daily_average_sell_price = ([], [])
                self._last_daily_update = tme
                at_the_end(self._daily_times, f"{datetime.datetime.now().day}/{datetime.datetime.now().month}:{datetime.datetime.now().hour}h", self.data_amount)

                # UPDATE WEEKLY PRICES
                self._weekly_average_buy_price.append(sum(self._daily_buy_price)/len(self._daily_buy_price))
                self._weekly_average_sell_price.append(sum(self._daily_sell_price)/len(self._daily_sell_price))


            if tme - self._last_weekly_update >= 604_800/self.data_amount:
                at_the_end(self._weekly_buy_price, sum(self._weekly_average_buy_price)/len(self._weekly_average_buy_price), self.data_amount)
                at_the_end(self._weekly_sell_price, sum(self._weekly_average_sell_price)/len(self._weekly_average_sell_price), self.data_amount)
                self._weekly_average_buy_price, self._weekly_average_sell_price = ([], [])
                self._last_weekly_update = tme
                at_the_end(self._weekly_times, f"{datetime.datetime.now().day}/{datetime.datetime.now().month}:{datetime.datetime.now().hour}h", self.data_amount)

        except IndexError:
            pass

    def rt_buy_price_getter(self):
        return self._rt_buy_price

    def rt_sell_price_getter(self):
        return self._rt_sell_price

    def rt_times_getter(self):
        return self._rt_times

    def daily_buy_getter(self):
        return self._daily_buy_price

    def daily_sell_getter(self):
        return self._daily_sell_price

    def daily_times_getter(self):
        return self._daily_times

    def weekly_buy_getter(self):
        return self._weekly_buy_price

    def weekly_sell_getter(self):
        return self._weekly_sell_price

    def weekly_times_getter(self):
        return self._weekly_times

    def buy_orders_getter(self):
        return self._buy_orders

    def sell_orders_getter(self):
        return self._sell_offers

    def buy_orders_amount_getter(self):
        return self._buy_orders_amount

    def sell_offers_amount_getter(self):
        return self._sell_offers_amount

    def get_avg_buy_price(self):
        return round(self.tt_price / self.amount_values, 1)
