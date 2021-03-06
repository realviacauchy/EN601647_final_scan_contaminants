# Install mmh3 and bitarray 3rd party module first
# pip install mmh3 -- murmur hash function
# pip install bitarray

import math
import mmh3
from bitarray import bitarray 

class BloomFilter(object):

    '''
    Class for bloom filter using murmur3 hash function
    '''
    def __init__(self, items_count, fp_prob):
        '''
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        '''
        # False posible probability in decimal
        self.fp_prob = fp_prob
         
        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)
 
        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)
                  
        # Bit array of given size
        self.bit_array = bitarray(self.size)
         
        # initialize all bits as 0
        self.bit_array.setall(0)

    def add(self, item):
        '''
        Add item to filter
        '''
        digests = []
        for i in range(self.hash_count):
            # create a digest for the given item
            # hash the item k times and use i as the seed
            digest = mmh3.hash(item,i) % self.size
            digests.append(digest)
            # set the bit at digest to 1 in the bit_array
            self.bit_array[digest] = True

    def check(self,item):
        '''
        Test item for membership in the set
        '''
        for i in range(self.hash_count):
            digest = mmh3.hash(item,i) % self.size
            if not self.bit_array[digest]:
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        '''
        Return size of bit array (m)
        Return the size of bit array(m) to used using
        following formula
                m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        '''
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)
    
    @classmethod
    def get_hash_count(self, m, n):
        '''
        Return the hash function(k) to be used using
        following formula
                k = (m/n) * lg(2)
                 
        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        '''
        k = (m/n) * math.log(2)
        return int(k)
