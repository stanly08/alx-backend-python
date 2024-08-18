#!/usr/bin/env python3
"""
Tasks
"""

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Regular function that takes an integer max_delay and returns an asyncio.Task.

    Args:
        max_delay (int): The maximum delay in seconds for wait_random.

    Returns:
        asyncio.Task: An asyncio task representing the execution of wait_random.
    """
    return asyncio.create_task(wait_random(max_delay))
