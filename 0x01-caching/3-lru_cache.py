#!usr/bin/python3
"""3-lru_cache.py"""
from collections import OrderedDict
BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """LRU Cache class that inherits from BaseCaching"""

    def __init__(self):
        """Initialize the LRU cache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache

        Args:
            key (str): Key for the item to be added
            item (any): Value of the item to be added

        If the number of items in the cache exceeds MAX_ITEMS,
        discard the least recently used item (LRU algorithm)
        and print the key of the discarded item.
        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discard_key, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {discard_key}")

        self.cache_data[key] = item

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
        return self.cache_data[key]
