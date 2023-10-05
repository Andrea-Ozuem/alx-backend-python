#!/usr/bin/env python3

'a type-annotated function sum_mixed_list whichi'

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    '''sums and returns val'''
    summ = 0
    for item in mxd_lst:
        summ += item
    return summ
