#!/usr/bin/env python3
"""Building a simple paginator"""
import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
            This function retrieves a paginated list
            of baby names from a CSV file.

        Args:
            page: The desired page number (default: 1).
            page_size: The number of items per page (default: 10).

        Returns:
            A list containing the requested page of baby name data.
        """
        assert isinstance(page, int) and page > 0,\
            "page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0,\
            "page_size must be a positive integer"
        data = []
        with open(self.DATA_FILE, "r") as file:
            for line in file:
                data.append(line.strip().split(","))
        total_row = len(data)
        if page * page_size > total_row:
            return []

        start_index, end_index = index_range(page, page_size)
        return data[start_index:end_index]


def index_range(page: int, page_size: int) -> tuple():
    """
    This function calculates the start and end
    index for a given page and page size.

    Args:
        page: The current page number (1-indexed).
        page_size: The number of items per page.

    Returns:
        A tuple of two integers representing the
        start and end index for the current page.
    """
    if page <= 0:
        raise ValueError("page must be a positive integer")
    if page_size <= 0:
        raise ValueError("page_size must be a positive integer")
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
