from collections.abc import Callable
from typing import Any


LogFunc = Callable[..., Any]


def Blue(log_func: LogFunc, text: str) -> None:
    log_func(f"\u001b[34;1m{text}\u001b[0m")


def Green(log_func: LogFunc, text: str) -> None:
    log_func(f"\u001b[32m{text}\u001b[0m")


def Yellow(log_func: LogFunc, text: str) -> None:
    log_func(f"\u001b[33m{text}\u001b[0m")


def Cyan(log_func: LogFunc, text: str) -> None:
    log_func(f"\u001b[36m{text}\u001b[0m")


def Red(log_func: LogFunc, text: str, *, stack_info: bool = True) -> None:
    log_func(f"\u001b[31m{text}\u001b[0m", stack_info=stack_info)
