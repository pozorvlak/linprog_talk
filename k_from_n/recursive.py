#!/usr/bin/env python

import sys

def best(k, options):
    if k > len(options):
        return None
    if len(options) == 0:
        return []
    head, tail = options[0], options[1:]
    with_head = best(k - 1, [o for o in tail if o % head != 0])
    if with_head is not None:
        return [head] + with_head
    return best(k, tail)

answer = best(int(sys.argv[1]), range(1, int(sys.argv[2]) + 1))
print(answer)
print(len(answer))
print(sum(answer))

