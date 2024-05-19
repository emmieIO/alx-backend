#!/usr/bin/env python3
"""Building the paginator helper"""
from typing import Tuple


def index_range(page: int, page_size: int) -> tuple() :
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