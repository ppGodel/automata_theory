#!/usr/bin/env python3.7
from functools import reduce
from typing import Callable, Dict, Set, Tuple, Any


def compose_functions(f: Callable, g: Callable) -> Callable:
    def fog(x:Any) -> Any:
        return g(f(x))
    return fog


def or_function(v1: bool, v2: bool)-> bool:
    return v1 or v2


def turing_machine(sigma: Set[chr],
                   gamma: Set[chr],
                   b: chr,
                   delta: Dict[Tuple[chr, str], Tuple[chr, str, int]],
                   f: Set[str],
                   s: str,
                   max_iter: int = 10000):

    def delta_fn(char: chr, state: str) -> str:
        print(f'{char} , {state} : {delta.get((char,state), "_")}')
        return delta.get((char,state), (char, "q_i", 0))

    def evaluate_word(word: str):
        return evaluate(b+word+b, 1, s, 1)

    def evaluate(word: str, head_position: int, state: chr, iter_num:int) -> str:
        if word[0] != b or head_position < 0:
            evaluate(b + word, head_position + 1, state, iter_num)
        if word[-1] != b or head_position >= len(word):
            evaluate(word + b, head_position, state, iter_num)
        print(f'w: {word[:head_position]}|{word[head_position]}|{word[head_position+1:]}')
        (new_char, new_state, direction) = delta_fn(word[head_position], state)
        if new_state == "q_i" or iter_num > max_iter:
            return "Rejected"
        if new_state in f:
            return "Accepted"
        return evaluate(word[:head_position] + new_char + word[head_position+1:],
                        head_position + direction,
                        new_state,
                        iter_num + 1)


    if reduce(or_function, (k not in gamma for k, v in delta.keys())):
        raise Exception('char in delta is not in sigma')
    return evaluate_word

if __name__ == "__main__":

    MT = {('0', 's') : ('0', 's', 1),
          ('1', 's') : ('1', 's', 1),
          ('@', 's') : ('@', 't', -1),
          ('0', 't') : ('0', 'Si', 0)
          }

    stri = '01111'
    sigma = {'1','0'}
    b = '@'
    gamma = {b} | sigma
    f = {'Si'}
    s = 's'

    tm = turing_machine(sigma,gamma,b,MT,f,s)
    result = tm(stri)
    print(result)
