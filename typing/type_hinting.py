from typing import TypeVar, Sequence

T = TypeVar("T")

def my_func(x: Sequence[T]) -> T:
    return "ss"
    # return x[0]

# my_lst = [2,3,4]
my_lst = ["item1","item"]

my_func(my_lst)

