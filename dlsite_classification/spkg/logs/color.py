
def Blue(log_func, text):
    log_func(f'\u001b[34;1m{text}\u001b[0m')


def Green(log_func, text):
    log_func(f'\u001b[32m{text}\u001b[0m')


def Yellow(log_func, text):
    log_func(f'\u001b[33m{text}\u001b[0m')


def Cyan(log_func, text):
    log_func(f'\u001b[36m{text}\u001b[0m')


def Red(log_func, text, stack_info=True):
    log_func(f'\u001b[31m{text}\u001b[0m', stack_info=stack_info)
