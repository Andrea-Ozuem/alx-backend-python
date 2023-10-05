#!/usr/bin/env python3

'a type-annotated function sum_mixed_list whichi'

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''sums and returns val'''
    def multiplier_function(x: float) -> float:
        '''multiplier func'''
        return x * multiplier

    return multiplier_function
