## Author: Sharif Afandi
## Year  : 2024

import unittest
from orderbook import *
import naiveorderbook

# Test accurracy in simple small input
class TestOrderbookBigInput(unittest.TestCase):
    def setUp(self):
        self.csv_filename = "orderbooks.csv"
        # Converts CSV string to pandas DataFrame and then numpy array for testing
        self.csv_data_numpy = read_csv(self.csv_filename)

    # def testOrderBookUpdatesToBeSub100ms(self):
    #     symbol = "SEIUSDT"
    #     timestamp = 1727696628512 # last timestamp in csv
    #     get_top_10_bids_and_asks(self.csv_data_numpy, timestamp, symbol)
    #     self.assertTrue(np.array(exec_times).max() <= 100)
        
    # TODO add ones for amount ahead and nearest worse
    # Attention: Runs for long time because of naive implementation comparison (several minutes)
    def testAccuracyBidsAsksVsNaiveOrderbook(self):
        inputs = [
            ("SEIUSDT", 1727682229112),
            ("NEIROUSDT", 1727682346770),
            ("NEIROUSDT", 1727682228771),
            ("TAOUSDT", 1727682228777),
            ("HMSTRUSDT", 1727682555292),
            ("DOGEUSDT", 1727682327575),
            ("BNBUSDT", 1727682327507),
            ("USTCUSDT", 1727682327492),
            ("WLDUSDT", 1727682327490),
            ("HMSTRUSDT", 1727682327483),
        ]
        for i in inputs:
            symbol = i[0]
            timestamp = i[1]
            top10 = get_top_10_bids_and_asks(self.csv_data_numpy, timestamp, symbol)
            naive_top10 = naiveorderbook.naive_get_top_10_bids_and_asks(self.csv_data_numpy, timestamp, symbol)
            self.assertEqual(top10[BIDS_STR], naive_top10[BIDS_STR])
            self.assertEqual(top10[ASKS_STR], naive_top10[ASKS_STR])
        

if __name__ == "__main__":
    unittest.main()