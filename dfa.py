#!/usr/bin/env python3.7
from functools import reduce
from typing import Callable, Iterable, Dict, Set, Tuple, Any


def compose_functions(f: Callable, g: Callable) -> Callable:
    def fog(x: Any) -> Any:
        return g(f(x))

    return fog


def or_function(v1: bool, v2: bool) -> bool:
    return v1 or v2


def deterministic_automate(
    sigma: Set[chr], delta: Dict[Tuple[chr, str], str], f: Set[str], s: str
):
    def delta_fn(state: str, char: chr) -> str:
        print(f'{state} , {char} : {delta.get((state,char), "_")}')
        return delta.get((state, char), "_")

    def partial_delta(char: chr) -> Callable[[str], str]:
        def delta_eval(state: str) -> str:
            return delta_fn(state, char)

        return delta_eval

    # d(q,s) -> q_1 => d(q_1, s_1) ::  p(s, d) -> dp  :: dp(q) -> q_1 => dp(q_1) => ...
    # f(x) -> y => g(y) -> z : fog(x) -> z
    def compose_delta_transitions(functions: Iterable[Callable]) -> Callable:
        return reduce(compose_functions, functions)

    def create_delta_transitions(word: str) -> Iterable[Callable[[str], str]]:
        return map(partial_delta, word) if len(word) > 0 else (lambda x: x, lambda x: x)

    def evaluate(word: str) -> bool:
        return compose_delta_transitions(create_delta_transitions(word))(s) in F

    if reduce(or_function, (v not in sigma for k, v in delta.keys())):
        raise Exception("char in delta is not in sigma")
    return evaluate


if __name__ == "__main__":

    # a*b
    delta_dict = {
        ("q0", "a"): "qx",
        ("q0", "b"): "q1",
        ("q1", "a"): "q1",
        ("q1", "b"): "q2",
        ("q2", "a"): "q1",
        ("q2", "b"): "q2",
        ("qx", "a"): "qx",
        ("qx", "b"): "qx",
    }
    sigma = {"a", "b"}
    F = {"q2"}
    s = "q0"
    da = deterministic_automate(sigma, delta_dict, F, s)
    print(da("baab"))
    print(da("baaaab"))
    print(da("bbbbbbbbbbbbbb"))
    print(da("aaaaaba"))
    print(da(""))
    print(da("b"))
