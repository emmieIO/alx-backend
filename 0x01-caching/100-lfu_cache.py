#!usr/bin/python3
"""2-lifo_cache.py"""
from collections import OrderedDict
BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """LFU Cache class that inherits from BaseCaching"""

    def __init__(self):
        """Initialize the LFU cache"""
        super().__init__()
        self.cache_data = OrderedDict()
        self.frequencies = {}

    def put(self, key, item):
        """Add an item in the cache

        Args:
            key (str): Key for the item to be added
            item (any): Value of the item to be added

        If the number of items in the cache exceeds MAX_ITEMS,
        discard the least frequently used item (LFU algorithm).
        If there are multiple items with the same least frequency,
        discard the least recently used item among them (LRU algorithm).
        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data.move_to_end(key)
            self.frequencies[key] += 1
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            min_freq = min(self.frequencies.values())
            lfu_keys = \
                [k for k, v in self.frequencies.items() if v == min_freq]
            discard_key = \
                next((k for k in self.cache_data if k in lfu_keys), None)
            print(f"DISCARD: {discard_key}")
            del self.cache_data[discard_key]
            del self.frequencies[discard_key]

        self.cache_data[key] = item
        self.frequencies[key] = 1

    def get(self, key):
        """Get an item by key

        Args:
            key (str): Key of the item to be retrieved

        Returns:
            The value of the item if key exists in the cache,
            otherwise None is returned.
        """
        if key is None or key not in self.cache_data:
            return None

        self.cache_data.move_to_end(key)
        self.frequencies[key] += 1
        return self.cache_data[key]
