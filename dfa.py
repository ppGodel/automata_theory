#!/usr/bin/env python3.7
from functools import reduce
from typing import Callable, Iterable, Dict, Set, Tuple, Any


def compose_functions(f: Callable, g: Callable) -> Callable:
    def fog(x:Any) -> Any:
        return g(f(x))
    return fog

def or_function(v1: bool, v2: bool)-> bool:
    return v1 or v2

def deterministic_automate(sigma: Set[chr],
                           delta: Dict[Tuple[chr,str], str],
                           f: Set[str],
                           s: str):
    def delta_fn(char: chr, state: str) -> str:
        #print(f'{char} , {state} : {delta.get((char,state), "_")}')
        return delta.get((char,state), "_")

    def delta_curr(char:chr) -> Callable[[str],str]:
        def delta_eval(state:str) -> str:
            return delta_fn(char, state)
        return delta_eval

    def compose_delta_transitions(functions: Iterable[Callable]) -> Callable:
        return reduce(compose_functions, functions)

    def create_delta_transitions(word: str) -> Iterable[Callable[[str],str]]:
        return (delta_curr(char) for char in word)

    def evaluate(word: str) -> bool:
        return compose_delta_transitions(
            create_delta_transitions(word))(s) in F

    if reduce(or_function ,(k not in sigma for k,v in delta.keys())):
        raise Exception('char in delta is not in sigma')
    return evaluate


if __name__ == '__main__':
    # a*b
    delta_dict = { ('a',"q0"): "q0",
                   ('b',"q0"): "q1",
                   ('a',"q1"): "qx",
                   ('b',"q1"): "qx",
                   ('a',"qx"): "qx",
                   ('b',"qx"): "qx"}
    sigma = {'a','b'}
    F = {"q1"}
    s = "q0"
    da = deterministic_automate(sigma, delta_dict, F, s)
    print(da("aaaaaaabbbbb"))
