#!/usr/bin/env python3

'a type-annotated function sum_mixed_list whichi'

from typing import Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    return [(i, len(i)) for i in lst]
