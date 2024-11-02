## Precise & Real-Time Orderbook
### How to use orderbook.py?

To start using orderbook run the following commands in your terminal:
```
> pip insatll requirements.txt
> python orderbook.py <datafilename> <timestamp> <symbol>
```
Example:
```
> py orderbook.py orderbooks.csv 1727684922792 USTCUSDT
```
Expected output:
```
Top 10 bids/asks for USTCUSDT at 1727684922792: {'BIDS': [[0.02237, 107105.0], [0.02236, 228631.0], [0.02235, 277308.0], [0.02234, 572724.0], [0.02233, 918842.0], [0.02232, 1316929.0], [0.02231, 1214516.0], [0.0223, 1317778.0], [0.02229, 492031.0], [0.02228, 1028896.0]], 'ASKS': [[0.02239, 9686.0], [0.0224, 89962.0], [0.02241, 418015.0], [0.02242, 600831.0], [0.02243, 196310.0], [0.02244, 1892841.0], [0.02245, 655180.0], [0.02246, 812377.0], [0.02247, 525265.0], [0.02248, 207719.0]]}
mean exectime(ms) 0.050686687403331605
min exectime(ms)  0.004291534423828125
max exectime(ms)  88.44232559204102
total execution time: 1044.8498725891113
```

### My Solution
I implemented AVL Tree in avl.py to keep the copy of orderbook, because the AVL Tree has **O(log n)** time complexity for insertion and deletion operations. So, it is required to keep two separate trees for bids and asks. In the tree we assign prices to keys and quantities to values. Every time when we receive orders for update, we just insert new quantity for a given key or delete the key if quantity is zero.

My AVL Tree implementation accounts for floating point imprecision and performs required checks to avoid imprecision.

To support **AmountAhead** function I added sum queries with **O(log n)** time complexity to AVL Tree. To achieve this it is required to keep additional sum info in every node, where sum is the sum of all subtree node values and update this value whenever required.

Because AVL Tree is actually a Balanced Binary Search Tree we can support **NearestWorsePrice** function in **O(log n)** time complexity as well.

Finally, to get best 10 bids and asks we can do in-order traversal and get result in **O(log n)** as well.

### Testing & Performance Measurements
#### Accuracy Testing
I implemented naive naiveorderbook.py that runs really slow in comparison to the optimal AVL Tree implementation to compare final orderbooks. Given the *orderbooks.csv* datafile, I implemented test_orderbook_biginput.py and compared results of naive and optimal orderbooks for many different inputs, it showed 100% accuracy in all test cases. You can run tests by yourself by running the following command inside of Case Study 1 folder:
```
python -m unittest .\test_orderbook_biginput.py  
```
It can potentialy run for several minutes because of slowness of naive implementation.
#### Performance Tests
The orderbook.py internally measures all the orderbook update command execution times and prints it on screen. Here is the example of output for the following command that runs all the updates in given csv:
```
py .\orderbook.py orderbooks.csv 1727696628512 HMSTRUSDT
```
Output:
```
Top 10 bids/asks for HMSTRUSDT at 1727696628512: {'BIDS': [[0.005753, 454109.0], [0.005752, 591495.0], [0.005751, 1040846.0], [0.00575, 442682.0], [0.005749, 1878746.0], [0.005748, 529459.0], [0.005747, 3262150.0], [0.005746, 1603925.0], [0.005745, 2585369.0], [0.005744, 903663.0]], 'ASKS': [[0.005754, 2601.0], [0.005755, 177997.0], [0.005756, 105215.0], [0.005757, 152665.0], [0.005758, 110770.0], [0.005759, 910729.0], [0.00576, 322839.0], [0.005761, 616940.0], [0.005762, 1030053.0], [0.005763, 571910.0]]}
mean exectime(ms) 0.07388673710549912
min exectime(ms)  0.00286102294921875
max exectime(ms)  93.36185455322266
total execution time: 9021.116495132446
```