## Author: Sharif Afandi
## Year  : 2024

from colorama import Fore, Style
from common import *


class Node:
    def __init__(self, key, value=0, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

        self.height = 1
        self.balance = 0

        self.sum = value # subtree sum including node itself

        self.low = key
        self.high = key
    
    def copy(self):
        new_node = Node(self.key, self.value, self.left, self.right)
        new_node.height = self.height
        new_node.balance = self.balance
        new_node.sum = self.sum
        new_node.low = self.low
        new_node.high = self.high
        return new_node

class AVL:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return not self.root

    def _calc_balance_factor(self, node):
        if not node:
            return 0
        l = 0 if not node.left else node.left.height
        r = 0 if not node.right else node.right.height
        return l-r
    
    def _update_balance_factor(self, node):
        node.balance = self._calc_balance_factor(node)
    def _update_height(self, node):
        node.height = 1 + max(0 if not node.left else node.left.height,
                          0 if not node.right else node.right.height)

    def insert(self, key, value=0):
        # if compare(key, 0.00102578)==0 and (compare(value, 1463.0) == 0 or compare(value, 24397.0) == 0):
        #         print(f"found0 {key} {value}")
        self.root = self._insert(self.root, key, value)  
    def _insert(self, node, key, value):
        if self.root is None: # if tree is empty
            self.root = Node(key, value)
            return self.root
        # print(f"insert {node.key}")
        
        # if compare(key, 0.00102578)==0:
        #         print(f"found1 {key, node.key} {value, node.value}")
        cmp = compare(key, node.key)
        if cmp == 0:    # we found node with given key, it is already present, just update value
            # if compare(key, 0.00102578)==0 and (compare(value, 1463.0) == 0 or compare(value, 24397.0) == 0):
            #     print(f"found1 {node.key, node.value} {key, value}")
            node.value = value
        elif cmp == -1: # key in left subtree
            if not node.left:
                node.left = Node(key, value)
                # if compare(key, 0.00102578)==0 and (compare(value, 1463.0) == 0 or compare(value, 24397.0) == 0):
                #     print(f"found4 {node.key, node.value} {key, value} {node.left.key, node.left.value}")
            else:
                node.left = self._insert(node.left, key, value)
        elif cmp == 1:  # key in right subtree
            if not node.right:
                # if compare(key, 0.00102578)==0 and (compare(value, 1463.0) == 0 or compare(value, 24397.0) == 0):
                    # print(f"found5 {node.key, key} {node.value, value}")
                node.right = Node(key, value)
            else:
                node.right = self._insert(node.right, key, value)

        # if compare(node.key, 0.00102578)==0:
        #         print(f"found35 {node.key, node.value} {key, value}")
        node = self._rebalance(node)
        node = self._update_sum(node)
        # if compare(node.key, 0.00102578)==0:
        #         print(f"found3 {node.key, node.value} {key, value}")
        return node
        
    def search_node(self, key):
        return self._search_node(self.root, key)   
    def _search_node(self, node, key): # will return either value or None
        if not node:
            return None
        
        cmp = compare(key, node.key)

        if cmp == 0: # it means that we found a node with the same key we search for
            return node
        elif cmp == -1: # it means that the key we search for is probably in left subtree
            return self._search_node(node.left, key)
        elif cmp == 1:
            return self._search_node(node.right, key)
    
    # returns node with min key in tree
    def get_min_node(self):
        min_node = self._get_min_node(self.root)
        if not min_node:
            return None
        return min_node
    # return min key in tree
    def get_min_key(self):
        min_node = self._get_min_node(self.root)
        if not min_node:
            return None
        return min_node.key
    def _get_min_node(self, node):
        if not node:
            return None
        if not node.left:
            return node
        return self._get_min_node(node.left)
    
    # returns node with max key in tree
    def get_max_node(self):
        max_node = self._get_max_node(self.root)
        if not max_node:
            return None
        return max_node
    # returns max key in tree
    def get_max_key(self):
        max_node = self._get_max_node(self.root)
        if not max_node:
            return None
        return max_node.key
    def _get_max_node(self, node):
        if not node:
            return node
        if not node.right:
            return node
        return self._get_max_node(node.right)

    # Returns closest key in tree strictly less than given key
    def floor_node(self, key):
        node = self._floor_node(self.root, key)
        if not node:
            return None
        return node
    def _floor_node(self, node, key):
        nearestNode = None
        while node:
            cmp = compare(node.key, key)
            if cmp < 0:
                nearestNode = node
                node = node.right
            else:
                node = node.left
        return nearestNode

    # Returns closest key in tree strictly greater than given key
    def ceil_node(self, key):
        node = self._ceil_node(self.root, key)
        if not node:
            return None
        return node
    def _ceil_node(self, node, key):
        nearestNode = None
        while node:
            cmp = compare(node.key, key)
            if cmp == -1 or cmp == 0:
                node = node.right
            else:
                nearestNode = node
                node = node.left
        return nearestNode

    def remove(self, key):
        # print(f"remove: {key}")
        self.root = self._remove(self.root, key)
    def _remove(self, node, key):
        # print(f"_remove: {None if not node else node.key}")
        if not node:
            return None
        
        cmp = compare(node.key, key)
        if cmp == 0: # key found
            if not node.left and not node.right:
                return None
            elif not node.right:
                return node.left
            elif not node.left:
                return node.right
            else: # both children present #TODO RISKY
                max_from_left = self._get_max_node(node.left).copy()
                max_from_left.left = node.left
                max_from_left.right = node.right

                node = max_from_left
                
                node.left = self._remove(node.left, max_from_left.key)
                # what is get max None?
        elif cmp == 1: # key in left subtree
            node.left = self._remove(node.left, key)
        elif cmp == -1: # key in right subtree
            node.right = self._remove(node.right, key)
        
        node = self._rebalance(node)
        self._update_sum(node)
        return node

    def printtree(self):
        if not self.root:
            print("Empty Tree")
        else:
            self._printtree(self.root, 0)
    def _printtree(self, node, depth):
        if node.right:
            self._printtree(node.right, depth+1)
        print(f"{" "*(0 if depth == 0 else depth*10)} {Fore.GREEN} {node.key} {Style.RESET_ALL} {Fore.RED} {node.value} {Style.RESET_ALL} [{node.sum}][{node.low}..{node.high}]")
        if node.left:
            self._printtree(node.left, depth+1)

    def _right_rotate(self, node):
        if not node:
            return None
        # print(f"_right_rotate {node.key}")

        if not node.left and not node.right:
            return node
        
        A = node
        B = node.left
        T2 = node.left.right

        A.left = T2
        B.right = A

        self._update_height(A)
        self._update_height(B)
        self._update_balance_factor(A)
        self._update_balance_factor(B)
        self._update_sum(A)
        self._update_sum(B)
        return B
    def _left_rotate(self, node):
        if not node:
            return None
        # print("_left_rotate")

        if not node.left and not node.right:
            return node
        
        A = node
        B = node.right
        T2 = node.right.left

        A.right = T2
        B.left = A

        self._update_height(A)
        self._update_height(B)
        self._update_balance_factor(A)
        self._update_balance_factor(B)
        self._update_sum(A)
        self._update_sum(B)
        
        return B

    def _rebalance(self, node):
        if not node:
            return node
        # print(f" rebalance {node.key}")
        
        self._update_height(node)
        self._update_balance_factor(node)
        # we assume that all the balance factors are calculated correctly for subtree

        if node.balance >= 2:
            if node.left.balance >= 0:    # LL case
                node = self._right_rotate(node)
            elif node.left.balance <= -1: # LR case
                node.left = self._left_rotate(node.left)
                node = self._right_rotate(node)

        elif node.balance <= -2:
            if node.right.balance <= 0:   # RR case
                node = self._left_rotate(node)
            elif node.right.balance >= 1:  # RL case
                node.right = self._right_rotate(node.right)
                node = self._left_rotate(node)

        return node
    def _update_low_high(self, node): 
        if not node:
            return node

        node.low  = node.key
        node.high = node.key

        if node.left:
            node.low  = min(node.low,  min(node.left.low, node.left.high))
            node.high = max(node.high, max(node.left.low, node.left.high))   
        if node.right:
            node.low  = min(node.low,  min(node.right.low, node.right.high))
            node.high = max(node.high, max(node.right.low, node.right.high))

        return node
    def _update_sum(self, node):
        if not node:
            return node
        left_sum = 0 if not node.left else node.left.sum
        right_sum = 0 if not node.right else node.right.sum
        node.sum = left_sum + right_sum + node.value
        return self._update_low_high(node)

    def get_sum_between_keys_LR(self, L, R):
        # print(f"get_sum_between_keys_LR {L, R, self.root.key}")
        return self._get_sum_between_keys_LR(self.root, L, R)
    def _get_sum_between_keys_LR(self, node, target_low, target_high) -> float:
        if not node:
            return 0
        
        node_low = node.low
        node_high = node.high
        
        # print(f"sumq {node.key} {node.sum, node.value} {node.low, node.high} {target_low, target_high}")
        
        cmp = compare(target_low, target_high)

        if cmp == 1: # node_low > node_high
            return 0
        
        cmp_low  = compare(node_low, target_low)
        cmp_high = compare(node_high, target_high)

        if cmp_low >= 0 and cmp_high <= 0: # node segment inside of target
            # print("return full sum")
            return node.sum

        sum = (node.value if compare(node.key, target_low) > -1 and compare(node.key, target_high) < 1 else 0) \
                + (0 if not node.left  else self._get_sum_between_keys_LR(node.left,  max(target_low, node.left.low),  min(target_high, node.left.high))) \
                + (0 if not node.right else self._get_sum_between_keys_LR(node.right, max(target_low, node.right.low), min(target_high, node.right.high)))

        # print(f" ret {node.key} sum {sum}")
        return sum


if __name__ == "__main__":
    avl = AVL()

    avl.insert(2.5)
    avl.insert(3.0)
    avl.insert(0.1)
    avl.insert(0.01)
    avl.insert(2.0)
    avl.insert(2.7)
    avl.insert(7.0)
    avl.insert(0.15)
    # avl.remove(0.15)

    # print(avl.get_sum_between_keys_LR(0.01, 1000))
    # print()

    # # Insert Rotations test
    # avl.insert(0.14) # triggers LL case at 2.0
    # avl.insert(2.4)
    # avl.insert(2.3)
    # avl.insert(0.0)
    # avl.insert(1.6)
    # avl.insert(1.7)
    # avl.insert(1.8)

    # avl.insert(7.1)
    # avl.insert(7.2)
    # avl.insert(7.3)
    # avl.insert(7.4)
    # avl.insert(7.5)


    # avl.remove(7.5)
    # avl.remove(2.0)
    # avl.remove(7.4)
    # avl.remove(7.3)
    # avl.remove(7.2)

    # avl.remove(2.4)
    # avl.remove(2.3)
    # avl.remove(1.8)
    # avl.remove(2.5)

    # avl.remove(0.0)
    # avl.remove(0.01)
    # avl.remove(0.1)
    # avl.remove(0.14)
    # avl.remove(0.15)

    # avl.remove(3.0)
    # avl.remove(2.7)

    # avl.remove(7.0)
    # avl.remove(7.1)
    # avl.remove(1.7)
    # avl.remove(1.6)

    # print(f"search node({2.0}) {bst.search_node(2.0).key}")
    # node = bst.search_node(2.0)
    
    # bst._right_rotate(node)

    avl.printtree()

    # max_node = bst._get_max_node(bst.root)
    # print(f"max key in tree {max_node.key}")

    # s = 0.15
    # print(f"floor({s}) = {avl.floor_node(s).key}")

    s = 0.15
    print(f"ceil({s}) = {avl.ceil_node(s).key}")


    # s = 0.1
    # print(f"search for {s}: found {bst.search(s)}")

    # s = 1.2
    # print(f"search for {s}: found {bst.search(s)}")
