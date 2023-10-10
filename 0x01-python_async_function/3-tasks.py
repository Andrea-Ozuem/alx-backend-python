#!/usr/bin/env python3

'Concurrent coroutines'

import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    '''random, n times'''
    return sorted(results)
