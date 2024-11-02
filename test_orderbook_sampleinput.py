## Author: Sharif Afandi
## Year  : 2024

import unittest
from orderbook import *

# Test accurracy in simple small input
class TestOrderbookSampleInput(unittest.TestCase):

    # Simulated CSV data
    def setUp(self):
        self.csv_filename = "orderbooks_sampleinput.csv"

        # Converts CSV string to pandas DataFrame and then numpy array for testing
        self.csv_data_numpy = read_csv(self.csv_filename)

    def test_top_10_bids_asks_1(self):
        symbol = "BNBUSDT"
        timestamp = 1727682229009
        expected_bids = [[1.2, 0.3], [1.1, 0.3], [0.4, 0.1], [0.3, 0.1], [0.2, 0.2], [0.1, 0.2]] # descending order
        expected_asks = [[0.1, 0.2], [0.2, 0.2], [0.3, 0.1], [0.4, 0.1], [1.1, 0.3], [1.2, 0.3]] # ascending order

        # Test the get_top_10_bids_and_asks function
        top_10 = get_top_10_bids_and_asks(self.csv_data_numpy, timestamp, symbol)

        self.assertEqual(top_10[BIDS_STR], expected_bids)
        self.assertEqual(top_10[ASKS_STR], expected_asks)

    def test_amount_ahead(self):
        symbol = "BNBUSDT"
        timestamp = 1727682229009

        top_10 = get_top_10_bids_and_asks(self.csv_data_numpy, timestamp, symbol)
        # print(f"top10: {top_10}")

        expected_bids_amount_ahead = 0.7
        expected_asks_amount_ahead = 0.5
        bids_amount_ahead = get_orderbook().amount_ahead(BIDS_STR, 0.4)
        asks_amount_ahead = get_orderbook().amount_ahead(ASKS_STR, 0.3)
        self.assertEqual(compare(expected_bids_amount_ahead, bids_amount_ahead), 0)
        self.assertEqual(compare(expected_asks_amount_ahead, asks_amount_ahead), 0)

        expected_bids_amount_ahead = 0.0
        expected_asks_amount_ahead = 0.2
        bids_amount_ahead = get_orderbook().amount_ahead(BIDS_STR, 1.3)
        asks_amount_ahead = get_orderbook().amount_ahead(ASKS_STR, 0.1)
        self.assertEqual(compare(expected_bids_amount_ahead, bids_amount_ahead), 0)
        self.assertEqual(compare(expected_asks_amount_ahead, asks_amount_ahead), 0)

        expected_bids_amount_ahead = 1.2
        expected_asks_amount_ahead = 1.2
        bids_amount_ahead = get_orderbook().amount_ahead(BIDS_STR, 0.1)
        asks_amount_ahead = get_orderbook().amount_ahead(ASKS_STR, 1.2)
        self.assertEqual(compare(expected_bids_amount_ahead, bids_amount_ahead), 0)
        self.assertEqual(compare(expected_asks_amount_ahead, asks_amount_ahead), 0)

    def test_nearest_worse_price(self):
        symbol = "BNBUSDT"
        timestamp = 1727682229009

        top_10 = get_top_10_bids_and_asks(self.csv_data_numpy, timestamp, symbol)
        # print(f"top10: {top_10}")

        expected_bids_nearest_worse = 0.3
        expected_asks_nearest_worse = 0.4
        bids_nearest_worse = get_orderbook().nearest_worse_price(BIDS_STR, 0.4)
        asks_nearest_worse = get_orderbook().nearest_worse_price(ASKS_STR, 0.3)
        self.assertEqual(compare(expected_bids_nearest_worse, bids_nearest_worse), 0)
        self.assertEqual(compare(expected_asks_nearest_worse, asks_nearest_worse), 0)

        bids_nearest_worse = get_orderbook().nearest_worse_price(BIDS_STR, 0.1)
        asks_nearest_worse = get_orderbook().nearest_worse_price(ASKS_STR, 1.2)
        self.assertIsNone(bids_nearest_worse)
        self.assertIsNone(asks_nearest_worse)

        expected_bids_nearest_worse = 1.1
        expected_asks_nearest_worse = 1.2
        bids_nearest_worse = get_orderbook().nearest_worse_price(BIDS_STR, 1.2)
        asks_nearest_worse = get_orderbook().nearest_worse_price(ASKS_STR, 1.1)
        self.assertEqual(compare(expected_bids_nearest_worse, bids_nearest_worse), 0)
        self.assertEqual(compare(expected_asks_nearest_worse, asks_nearest_worse), 0)


    # def test_no_data_for_symbol(self):
    #     # Test with a symbol not in the dataset, should return empty top 10
    #     top_10 = get_top_10_bids_and_asks(self.csv_data_numpy, self.timestamp, "UNKNOWN")
    #     self.assertEqual(top_10["bids"], [])
    #     self.assertEqual(top_10["asks"], [])

    # def test_before_timestamp(self):
    #     # Test a timestamp earlier than any in the data; top 10 should be empty
    #     top_10 = get_top_10_bids_and_asks(self.csv_data_numpy, 1727682229005, self.symbol)
    #     self.assertEqual(top_10["bids"], [])
    #     self.assertEqual(top_10["asks"], [])

if __name__ == "__main__":
    unittest.main()
