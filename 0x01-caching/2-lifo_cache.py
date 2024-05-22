#!usr/bin/python3
"""2-lifo_cache.py"""
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """Fifo Cache class"""
    def __init__(self):
        super().__init__();
        self.stack = []
        
    def put(self, key, item):
        """
        Add an item in the cache.
        If the number of items in the cache exceeds MAX_ITEMS, remove the last item put in the cache (LIFO).
        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Remove the old key from the stack
            self.stack.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Evict the last item in LIFO order
            last_key = self.stack.pop()
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

        # Add the new item to the cache and stack
        self.cache_data[key] = item
        self.stack.append(key)
        
    def get(self, key):
        """
        Get an item by key.
        If key is None or if the key doesn’t exist in self.cache_data, return None.
        """
        return self.cache_data.get(key, None)
