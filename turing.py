#!/usr/bin/env python3
from functools import reduce
from typing import Dict, Set, Tuple


def or_function(v1: bool, v2: bool) -> bool:
    return v1 or v2


def turing_machine(sigma: Set[chr],
                   gamma: Set[chr],
                   b: chr,
                   delta: Dict[Tuple[str, chr], Tuple[str, chr, int]],
                   f: Set[str],
                   s: str,
                   max_iter: int = 10000):

    def delta_fn(state: str, char: chr) -> Tuple[str, str, int]:
        print(f'{state}, {char} : {delta.get((state, char), "_")}')
        return delta.get((state, char), ("q_i", char, 0))

    def evaluate_word(word: str):
        return evaluate(b+word+b, 1, s, 1)

    def evaluate(word: str,
                 head_position: int,
                 state: chr,
                 iter_num: int) -> str:
        if word[0] != b or head_position < 0:
            evaluate(b + word, head_position + 1, state, iter_num)
        if word[-1] != b or head_position >= len(word):
            evaluate(word + b, head_position, state, iter_num)
        print(f'w: {word[:head_position]}|{word[head_position]}|{word[head_position+1:]}')
        (new_state, new_char, direction) = delta_fn(state, word[head_position])
        if new_state == "q_i" or iter_num > max_iter:
            return "Rejected"
        if new_state in f and direction == 0:
            return "Accepted"
        return evaluate(word[:head_position] + new_char + word[head_position+1:],
                        head_position + direction,
                        new_state,
                        iter_num + 1)

    if reduce(or_function, (v not in gamma for k, v in delta.keys())):
        raise Exception(f'char in delta is not in gamma {[v for k, v in delta.keys()]}')
    return evaluate_word


if __name__ == "__main__":

    delta = {
          ('s', 'a'): ('s', 'a', 1),
          ('s', 'b'): ('s', 'b', 1),
          ('s', '@'): ('t', '@', -1),
          ('t', 'b'): ('Si', 'b', 0),
          }

    stri = 'ababaaabab'
    sigma = {'a', 'b'}
    b = '@'
    gamma = {b} | sigma
    f = {'Si'}
    s = 's'

    # tm = turing_machine(sigma, gamma, b, delta, f, s)
    # print(tm(stri))
    # a^nb^n
    delta2 = {
        ('q_0', 'a'): ('q_1', 'A', 1),
        ('q_0', 'b'): ('q_x', 'b', 0),
        ('q_0', '&'): ('q_x', '&', 0),
        ('q_0', 'A'): ('q_x', 'A', 0),
        ('q_0', 'B'): ('q_3', 'B', 0),
        ('q_1', 'a'): ('q_1', 'a', 1),
        ('q_1', 'b'): ('q_2', 'B', -1),
        ('q_1', '&'): ('q_x', '&', 0),
        ('q_1', 'A'): ('q_x', 'A', 0),
        ('q_1', 'B'): ('q_1', 'B', 1),
        ('q_2', 'a'): ('q_2', 'a', -1),
        ('q_2', 'b'): ('q_x', 'b', 0),
        ('q_2', '&'): ('q_x', '&', 0),
        ('q_2', 'A'): ('q_0', 'A', 1),
        ('q_2', 'B'): ('q_2', 'B', -1),
        ('q_3', 'a'): ('q_x', 'a', 0),
        ('q_3', 'b'): ('q_x', 'b', 0),
        ('q_3', '&'): ('q_f', '&', 0),
        ('q_3', 'A'): ('q_x', 'A', 0),
        ('q_3', 'B'): ('q_3', 'B', 1),
    }

    stri = 'aaaaaabbbbbb'
    sigma = {'a', 'b'}
    b = '&'
    gamma = {b, 'A', 'B'} | sigma
    f = {'q_f'}
    s = 'q_0'

    tm = turing_machine(sigma, gamma, b, delta2, f, s)
    print(tm(stri))
