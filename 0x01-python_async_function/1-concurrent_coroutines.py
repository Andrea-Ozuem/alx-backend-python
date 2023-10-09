#!/usr/bin/env python3

'Concurrent coroutines'

import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''random, n times'''
    return [await wait_random(max_delay) for val in range(n)]
