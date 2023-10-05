#!/usr/bin/env python3

'a type-annotated function sum_mixed_list whichi'

from typing import List, Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''sums and returns val'''
    res: Tuple[str, float] = (k, v**2)
    return res
