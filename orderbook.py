## Author: Sharif Afandi
## Year  : 2024

import logging
import sys
import numpy as np
import pandas as pd
import time
from avl import *
import matplotlib.pyplot as plt
import ast

BIDS_STR = "BIDS"
ASKS_STR = "ASKS"

class Orderbook:
    def __init__(self):
        logging.debug(f"{self.__class__.__name__} initialized.")
        self.bids = AVL()
        self.asks = AVL()
    
    def _is_quantity_zero(self, order):
        return abs(order[1]) <= eps

    # Update (add/remove) orders to/from orderbook on given @side
    def update(self, orders, side):
        order_tree = None
        if side == BIDS_STR:
            order_tree = self.bids
        elif side == ASKS_STR:
            order_tree = self.asks

        for order in orders:
            order[0] = float(order[0])
            order[1] = float(order[1])
            if self._is_quantity_zero(order):
                order_tree.remove(order[0])
            else:
                order_tree.insert(order[0], order[1])

    # Calculate the total quantity ahead of a given price on the bid or ask side
    def amount_ahead(self, side, price):
        if side == BIDS_STR:
            return self.bids.get_sum_between_keys_LR(price, float('inf')) # from price and better
        elif side == ASKS_STR:
            return self.asks.get_sum_between_keys_LR(float('-inf'), price) # better up to price
        return 0

    # Find the nearest worst price (higher for bids, lower for asks)
    def nearest_worse_price(self, side, price):
        if side == BIDS_STR:
            node = self.bids.floor_node(price)
            return None if not node else node.key
        elif side == ASKS_STR:
            node = self.asks.ceil_node(price)
            return None if not node else node.key
        else:
            return None

    def get_top10(self):  # Return top 10 orders for both bids and asks
        result = {BIDS_STR: [], ASKS_STR: []}

        # BIDS
        if not self.bids.is_empty():
            max_node = self.bids.get_max_node()
            result[BIDS_STR].append([max_node.key, max_node.value])
            while len(result[BIDS_STR]) < 10:
                last_price = result[BIDS_STR][-1][0]
                next_price_node = self.bids.floor_node(last_price)
                if not next_price_node:
                    break
                result[BIDS_STR].append([next_price_node.key, next_price_node.value])
        
        # ASKS
        if not self.asks.is_empty():
            min_node = self.asks.get_min_node()
            result[ASKS_STR].append([min_node.key, min_node.value])
            while len(result[ASKS_STR]) < 10:
                last_price = result[ASKS_STR][-1][0]
                next_price_node = self.asks.ceil_node(last_price)
                if not next_price_node:
                    break
                result[ASKS_STR].append([next_price_node.key, next_price_node.value])
        
        return result

orderbook = Orderbook()

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

# Returns current orderbook instance
def get_orderbook():
    return orderbook


# Returns top 10 bids and asks up until the given timestamp for a symbol
def get_top_10_bids_and_asks(ls, timestamp, symbol):
    global orderbook
    orderbook = Orderbook()
    exec_times.clear()

    for i in range(0, len(ls)):
        start_time = time.time()
        cur_timestamp = ls[i][0]
        cur_symbol = ls[i][1]

        if cur_symbol != symbol:
            continue

        # start_time = time.time()
        # try:
        bids = ls[i][2]
        asks = ls[i][3]
            # execution_time_ms = ((time.time() - start_time)*1000.0)
            # exec_times.append((execution_time_ms, len(bids)+len(asks)))
        # except Exception as e:
            # print(f"Error parsing bids/asks at index {i}: {e}")
            # sys.exit(1)

        start_time = time.time()
        orderbook.update(bids, BIDS_STR)
        orderbook.update(asks, ASKS_STR)

        execution_time_ms = ((time.time() - start_time)*1000.0)
        exec_times.append((execution_time_ms, len(bids)+len(asks)))
        
        if cur_timestamp >= timestamp:
            break
    
    return orderbook.get_top10()

def main(filename, timestamp, symbol):
    # Read CSV data
    csv_data = read_csv(filename)

    total_exec_time = time.time()

    # Get and print top 10 bids/asks
    top_10 = get_top_10_bids_and_asks(csv_data, timestamp, symbol)
    print(f"Top 10 bids/asks for {symbol} at {timestamp}: {top_10}")

    total_exec_time = ((time.time() - total_exec_time)*1000.0)

    print(f"mean exectime(ms) {np.mean(np.array(exec_times)[:, 0])}")
    print(f"min exectime(ms)  {np.min(np.array(exec_times)[:, 0])}")
    print(f"max exectime(ms)  {np.max(np.array(exec_times)[:, 0])}")

    print(f"total execution time: {total_exec_time}")

    # # plot exec times
    # # Plot the results
    # plt.plot(np.array(exec_times)[:, 1], np.array(exec_times)[:, 0], marker='o')
    # plt.xlabel("Input Size")
    # plt.ylabel("Execution Time (milliseconds)")
    # plt.title("Execution Time vs. Input Size")
    # plt.grid()
    # plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python orderbook.py <datafilename> <timestamp> <symbol>")
        sys.exit(1)
    
    filename = sys.argv[1]
    timestamp = np.int64(sys.argv[2])
    symbol = sys.argv[3]

    main(filename, timestamp, symbol)
