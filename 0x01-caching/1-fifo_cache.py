#!usr/bin/python3
"""1-fifo_cache.py"""
BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """Fifo Cache class"""
    def __init__(self):
        super().__init__();
        self.order = []
        
    def put(self, key, item):
        """
        Add an item in the cache.
        If the number of items in the cache exceeds MAX_ITEMS,
        remove the first item put in the cache (FIFO).
        If key or item is None, this method should not do anything.
        """
        if key is not None and item is not None:
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                first_key = self.order.pop(0)
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")
            self.cache_data[key] = item
            self.order.append(key)
        
    def get(self, key):
        """
        Get an item by key.
        If key is None or if the key doesn’t exist in self.cache_data, return None.
        """
        return self.cache_data.get(key, None)
