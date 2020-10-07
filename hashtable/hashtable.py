
class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many indexs
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    Implement this.
    """

    def __init__(self, capacity= 1000000):
        # Your code here
        self.capacity = capacity
        self.storage = [None] * self.capacity

    def get_num_indexs(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of indexs in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        # Your code here
        return len(self.storage)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        Implement this.
        """
        # Your code here
        return len([item for item in self.storage if item is not None]) / self.capacity

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        # Your code here
        return len(self.storage)

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.
        Based on https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function#FNV-1_hash
        """

        # Your code here
        

    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        for x in key:
            hash = ((hash << 5) + hash ) + ord(x)
        return hash & 0xFFFFFFFF

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        Implement this.
        """
        # Your code here

        index = self.hash_index(key)
        if self.storage[index] is None:
            self.storage[index] = HashTableEntry(key, value)
        else:  
            cur = self.storage[index]
            while cur.next is not None and cur.key != key:
                cur = cur.next
            if cur.key == key: 
                cur.value = value
            else:  
                cur.next = HashTableEntry(key, value)

        if self.get_load_factor() > .7:
            self.resize(self.capacity * 2)

        return self

    def delete(self, key):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        cur = self.storage[index]
        if cur is None:  
            print("nope")
        elif cur.key == key: 
            self.storage[index] = cur.next
        else:  
            while cur.next.key != key and cur.next is not None:
                cur = cur.next
            if cur.next.key == key:
                cur.next = cur.next.next
            else:
                print("Couldn't find that key!")

        if self.get_load_factor() < .2:
            if self.capacity > 16:
                self.resize(self.capacity//2)
            else:
                self.resize(8)

        return self

    def get(self, key):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Implement this.
        """
    
        index = self.hash_index(key)
        try:
            if self.storage[index] is not None:
                current = self.storage[index]

                while current.key != key:
                    current = current.next
                return current.value
        except:
            return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        Implement this.
        """
      
        table_items = [value for value in self.storage if value is not None]
        self.capacity = new_capacity
        self.storage = [None] * new_capacity
        while table_items:  
            current = table_items.pop()
            self.put(current.key, current.value)
            while current.next is not None:
                current = current.next
                self.put(current.key, current.value)

        return self


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_indexs()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_indexs()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")