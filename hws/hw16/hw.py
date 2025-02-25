from typing import List, Any, Dict, Set, Generator

class StaticArray:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.capacity = [None] * capacity

    def set(self, index: int, value: int) -> None:
        """
        Set the value at a particular index.
        """
        if 0 <= index < len(self.capacity):
            self.array[index] = value
        else:
            raise IndexError("вне диапазоне")


    def get(self, index: int) -> int:
        """
        Retrieve the value at a particular index.
        """
        if 0 <= index < len(self.capacity):
            return self.array[index]
        else: 
            raise IndexError("вне диапазоне")


class DynamicArray:
    def __init__(self):
        """
        Initialize an empty dynamic array.
        """
        self.array = []

    def append(self, value: int) -> None:
        """
        Add a value to the end of the dynamic array.
        """
        self.array.append (value)

    def insert(self, index: int, value: int) -> None:
        """
        Insert a value at a particular index.
        """
        if 0 <= index < len(self.array): 
            self.array.append(index, value)
        else:
            raise IndexError("вне диапазоне")
        
    def delete(self, index: int) -> None:
        """
        Delete the value at a particular index.
        """
        if 0 <= index < len(self.array): 
            del self.array(index)
        else:
            raise IndexError("вне диапазоне")

    def get(self, index: int) -> int:
        """
        Retrieve the value at a particular index.
        """
        if 0 <= index < len(self.array): 
            return self.array(index)
        else:
            raise IndexError("вне диапазоне")
        
class Node:
    def __init__(self, value: int):
        """
        Initialize a node.
        """
        self.value =value
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        """
        Initialize an empty singly linked list.
        """
        self.head = None

    def append(self, value: int) -> None:
        """
        Add a node with a value to the end of the linked list.
        """
        new_node = Node(value)
        if not self.head: 
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def insert(self, position: int, value: int) -> None:
        """
        Insert a node with a value at a particular position.
        """
        new_node = Node(value)
        if position == 0:
            new_node.next = self.head
            self.head = new_node 
            return
        current = self.head 
        for _ in range (position -1):
            if not current:
                IndexError("вне диапазоне")
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def delete(self, value: int) -> None:
        """
        Delete the first node with a specific value.
        """ 
        if not self.head:
            return
        if self.head.value == value:
            self.head = self.head.next
            return
        current = self.head 
        while current.next and current.next.value != value:
            current = current.next
        if current.next:
            current.next = current.next.next

    def find(self, value: int) -> Node:
        """
        Find a node with a specific value.
        """
        current = self.head 
        while current: 
            if current.value == current:
                return
            current = current.next 
        return None
    
    def size(self) -> int:
        """
        Returns the number of elements in the linked list.
        """
        count = 0 
        current = self.head
        while current:
            count +=1 
            current = current.next
        return count
    
    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty.
        """
        return self.head is None
    
    def print_list(self) -> None:
        """
        Prints all elements in the linked list.
        """
        current = self.head
        while current:
            print (current.value, end=" -> ")
            current = current.next
        print (None)

    def reverse(self) -> None:
        """
        Reverse the linked list in-place.
        """
        prev = None 
        current = self.head 
        while current: 
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev 
    
    def get_head(self) -> Node:
        """
        Returns the head node of the linked list.
        """
        return self.head 
    
    def get_tail(self) -> Node:
        """
        Returns the tail node of the linked list.
        """
        current = self.head
        if current and current.next:
            current =current.next
        return current 

class DoubleNode:
    def __init__(self, value: int, next_node = None, prev_node = None):
        """
        Initialize a double node with value, next, and previous.
        """
        self.value = value 
        self.next = next_node
        self.prev = prev_node

class DoublyLinkedList:
    def __init__(self):
        """
        Initialize an empty doubly linked list.
        """
        self.head = None
        self.tail = None
    def append(self, value: int) -> None:
        """
        Add a node with a value to the end of the linked list.
        """
        new_node = DoubleNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next =new_node
            new_node.prev = self.tail
            self.tail = new_node
         
    def insert(self, position: int, value: int) -> None:
        """
        Insert a node with a value at a particular position.
        """
        if position == 0:
            new_node = DoubleNode(value, self.head)
            if self.head:
                self.head.prev = new_node
            self.head = new_node
            if not self.tail:
                self.tail = new_node
            return
        current = self.head
        for _ in range (position - 1 ): 
            if not current:
                raise IndexError ("вне диапозоне")
            current = current.next
        new_node = DoubleNode (value, current.next, current)
        if current.next:
            current.next.prev = new_node
        current.next = new_node
        if new_node.next is None:
            self.tail = new_node

    def delete(self, value: int) -> None:
        """
        Delete the first node with a specific value.
        """
        current = self.head
        while current:
            if current.value == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return
            current = current.next


    def find(self, value: int) -> DoubleNode:
        """
        Find a node with a specific value.
        """
        current = self.headx
        while current:
            if current.value == value:
                return current
            current = current.next
        return None
        
    def size(self) -> int:
        """
        Returns the number of elements in the linked list.
        """
        count = 0
        current = self.head
        while current: 
            count +=1
            current = current.next
        return count 

    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty.
        """
        return self.head is None

    def print_list(self) -> None:
        """
        Prints all elements in the linked list.
        """
        current = self.head
        while current:
            print(current.value, end=" <-> ")
            current = current.next
        print("None")

    def reverse(self) -> None:
        """
        Reverse the linked list in-place.
        """
        current = self.head 
        while current:
            current.prev , current.next = current.next, current.prev
            current = current.prev
        self.head, self.tail = self.tail, self.head
        

    def get_head(self) -> DoubleNode:
        """
        Returns the head node of the linked list.
        """
        return self.head
    
    def get_tail(self) -> DoubleNode:
        """
        Returns the tail node of the linked list.
        """
        return self.tail 

class Queue:
    def __init__(self):
        """
        Initialize an empty queue.
        """
        self.items = []

    def enqueue(self, value: int) -> None:
        """
        Add a value to the end of the queue.
        """
        self.items.append(value)

    def dequeue(self) -> int:
        """
        Remove a value from the front of the queue and return it.
        """
        if self.is_empty():
            raise IndexError("error")
        return self.items.pop(0)

    def peek(self) -> int:
        """
        Peek at the value at the front of the queue without removing it.
        """
        if self.is_empty():
            raise IndexError("error")
        return self.items.pop(0)

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        """
        return len(self.items) == 0
    
from typing import List, Optional, Generator

class TreeNode:
    def __init__(self, value: int):
        self.value = value
        self.left = None  
        self.right = None  

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value: int) -> None:
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node: TreeNode, value: int) -> None:
        if value < node.value:
            if node.left:
                self._insert(node.left, value)
            else:
                node.left = TreeNode(value)
        else:
            if node.right:
                self._insert(node.right, value)
            else:
                node.right = TreeNode(value)

    def delete(self, value: int) -> None:
        self.root = self._delete(self.root, value)

    def _delete(self, node: Optional[TreeNode], value: int) -> Optional[TreeNode]:
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_larger_node = self._find_min(node.right)
                node.value = min_larger_node.value
                node.right = self._delete(node.right, min_larger_node.value)
        return node

    def _find_min(self, node: TreeNode) -> TreeNode:
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, value: int) -> Optional[TreeNode]:
        return self._search(self.root, value)

    def _search(self, node: Optional[TreeNode], value: int) -> Optional[TreeNode]:
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def inorder_traversal(self) -> List[int]:
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Optional[TreeNode], result: List[int]) -> None:
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)

    def preorder_traversal(self) -> List[int]:
        result = []
        self._preorder_traversal(self.root, result)
        return result

    def _preorder_traversal(self, node: Optional[TreeNode], result: List[int]) -> None:
        if node:
            result.append(node.value)
            self._preorder_traversal(node.left, result)
            self._preorder_traversal(node.right, result)

    def postorder_traversal(self) -> List[int]:
        result = []
        self._postorder_traversal(self.root, result)
        return result

    def _postorder_traversal(self, node: Optional[TreeNode], result: List[int]) -> None:
        if node:
            self._postorder_traversal(node.left, result)
            self._postorder_traversal(node.right, result)
            result.append(node.value)

    def level_order_traversal(self) -> List[int]:
        if not self.root:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        return result

    def size(self) -> int:
        return self._size(self.root)

    def _size(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def is_empty(self) -> bool:
        return self.root is None

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Optional[TreeNode]) -> int:
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def minimum(self) -> Optional[TreeNode]:
        return self._find_min(self.root) if self.root else None

    def maximum(self) -> Optional[TreeNode]:
        current = self.root
        while current and current.right:
            current = current.right
        return current

    def is_valid_bst(self) -> bool:
        return self._is_valid_bst(self.root, float('-inf'), float('inf'))
    
    def _is_valid_bst(self, node: Optional[TreeNode], min_val: int, max_val: int) -> bool:
        if not node:
            return True
        if not (min_val < node.value < max_val):
            return False
        return self._is_valid_bst(node.left, min_val, node.value) and \
               self._is_valid_bst(node.right, node.value, max_val)

def insertion_sort(lst: List[int]) -> List[int]:
    for i in range(1, len(lst)):
        key = lst[i]
        j = i -1
        while j >= 0 and lst[j] > key:
            lst[j+1] = lst [j]
            j -= 1
        lst[j+1] = key
    return lst

def selection_sort(lst: List[int]) -> List[int]:
    for i in range(len(lst))  :
        min_idx = i
        for j in range(i+1,len(lst)):
            if lst[j] < lst[min_idx]:
                min_idx = j 
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst

def bubble_sort(lst: List[int]) -> List[int]:
    for i in range (len(lst)):
        for j in range (0, len(lst) - i - 1 ):
            if lst[j] > lst[j+1]:
                 lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

def shell_sort(lst: List[int]) -> List[int]:
    gap = len(lst) // 2
    while gap > 0:
        for i in range (gap, len(lst)):
            j = i
            while j >= gap and lst(j - gap) > lst[i]:
                lst[j] = lst[j - gap]
                j -= gap
            lst[j] = lst[i]
        gap //= 2
    return lst

def merge_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    
    return merge(left, right)
def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1:
        return lst
    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)