#!/usr/bin/env python3

'type-annotated function sum_list which takes a list input_list'


from typing import List


def sum_list(input_list: List[float]) -> float:
    '''sums alll floats in a list'''
    summ = 0
    for item in input_list:
        summ += item
    return summ
