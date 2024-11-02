## Author: Sharif Afandi
## Year  : 2024

import logging
import time
import numpy as np
import pandas as pd
import sys
import ast

from copy import deepcopy

from common import *

from orderbook import BIDS_STR, ASKS_STR

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class NaiveOrderbook:
    def __init__(self):
        logging.debug(f"{self.__class__.__name__} initialized.")
        self.bids = []  # List of [price, quantity] for bids
        self.asks = []  # List of [price, quantity] for asks
    
    def is_price_present(self, price):
        for i in self.bids:
            if compare(i[0], price) == 0:
                return True
        return False

    def update(self, orders, side):
        if side == BIDS_STR:
            self.update_bids(orders)
        elif side == ASKS_STR:
            self.update_asks(orders)
    
    def update_bids(self, bids):
        new_bids = deepcopy(self.bids)

        for bid in bids:
            bid[0] = float(bid[0])
            bid[1] = float(bid[1])
            flag = True
            for i in range(len(new_bids)):
                if compare(new_bids[i][0], bid[0]) == 0: # price already exists
                    if compare(bid[1], 0) == 0: # remove this price
                        del new_bids[i]
                    else:
                        new_bids[i][1] = bid[1] # update this price quantity
                    flag = False
                    break

            if flag and compare(bid[1], 0.0) == 1:
                new_bids.append(bid)
        
        self.bids = new_bids

    def update_asks(self, asks):
        new_asks = deepcopy(self.asks)

        for ask in asks:
            ask[0] = float(ask[0])
            ask[1] = float(ask[1])
            flag = True
            for i in range(len(new_asks)):
                if compare(new_asks[i][0], ask[0]) == 0: # price already exists
                    if compare(ask[1], 0) == 0: # remove this price
                        del new_asks[i]
                    else:
                        new_asks[i][1] = ask[1] # update this price quantity
                    flag = False
                    break

            if flag and compare(ask[1], 0.0) == 1:
                new_asks.append(ask)
        
        self.asks = new_asks

    # Calculate the total quantity ahead of a given price on the bid or ask side
    def amount_ahead(self, side, price):
        total_quantity = 0
        if side == BIDS_STR:
            for bid in self.bids:
                if bid[0] > price:  # Only consider bids above the given price
                    total_quantity += bid[1]
        elif side == ASKS_STR:
            for ask in self.asks:
                if ask[0] < price:  # Only consider asks below the given price
                    total_quantity += ask[1]
        return total_quantity

    # Find the nearest worst price (higher for bids, lower for asks)
    def nearest_worst_price(self, side, price):
        nearest_price = None
        if side == BIDS_STR:
            for bid in self.bids:
                if bid[0] <= price:  # Consider prices equal to or below the given bid price
                    if nearest_price is None or bid[0] < nearest_price:
                        nearest_price = bid[0]
        elif side == ASKS_STR:
            for ask in self.asks:
                if ask[0] >= price:  # Consider prices equal to or above the given ask price
                    if nearest_price is None or ask[0] > nearest_price:
                        nearest_price = ask[0]
        return nearest_price

    def get_top10(self):  # Return top 10 orders for both bids and asks
        sorted_bids = sorted(self.bids, key=lambda x: -x[0])  # Sort bids from highest to lowest
        sorted_asks = sorted(self.asks, key=lambda x: x[0])   # Sort asks from lowest to highest
        return {BIDS_STR: sorted_bids[:10], ASKS_STR: sorted_asks[:10]}


orderbook = NaiveOrderbook()

# Read CSV and return a numpy array
def read_csv(filename):
    try:
        df = pd.read_csv(filename)
        df_numpy = df.to_numpy()
        for i in range(0, len(df_numpy)):
            df_numpy[i][2] = ast.literal_eval(df_numpy[i][2])
            df_numpy[i][3] = ast.literal_eval(df_numpy[i][3])
        return df_numpy
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    return df_numpy
exec_times = []
total_exec_time = 0.0

# Returns current orderbook instance
def get_orderbook():
    return orderbook

# Returns top 10 bids and asks up until the given timestamp for a symbol
def naive_get_top_10_bids_and_asks(ls, timestamp, symbol):
    global orderbook
    orderbook = NaiveOrderbook()
    for i in range(0, len(ls)):
        start_time = time.time()
        cur_timestamp = ls[i][0]
        cur_symbol = ls[i][1]

        if cur_symbol != symbol:
            continue

        bids = ls[i][2]
        asks = ls[i][3]

        orderbook.update(bids, BIDS_STR)
        orderbook.update(asks, ASKS_STR)

        execution_time_ms = ((time.time() - start_time)*1000.0)

        exec_times.append(execution_time_ms)
        
        if cur_timestamp >= timestamp:
            break
    
    return orderbook.get_top10()

def main(filename, timestamp, symbol):
    # Read CSV data
    csv_data = read_csv(filename)
    
    total_exec_time = time.time()

    # Get and print top 10 bids/asks
    top_10 = naive_get_top_10_bids_and_asks(csv_data, timestamp, symbol)
    print(f"Top 10 bids/asks for {symbol} at {timestamp}: {top_10}")

    total_exec_time = ((time.time() - total_exec_time)*1000.0)

    print(f"mean exectime {np.array(exec_times).mean()}")
    print(f"min exectime {np.array(exec_times).min()}")
    print(f"max exectime {np.array(exec_times).max()}")

    print(f"total execution time: {total_exec_time}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python orderbook.py <datafilename> <timestamp> <symbol>")
        sys.exit(1)
    
    filename = sys.argv[1]
    timestamp = np.int64(sys.argv[2])
    symbol = sys.argv[3]

    main(filename, timestamp, symbol)
