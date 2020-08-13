import asyncio

on_message_func_dict = {}
login_func = {}

def register_on_message_func(func):
    on_message_func_dict[func.__name__] = func
    return func

def start_registered_function_call(*args):
    asyncio.run(call_registered_function_non_blocking(*args))

async def call_registered_function_non_blocking(*args):
    for _, func in on_message_func_dict.items():
        func(*args)


        