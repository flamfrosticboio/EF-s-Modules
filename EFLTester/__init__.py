from time import time as get_time, sleep
from threading import Thread
from typing import TypedDict

class Data(TypedDict): ...
class ArgsDict(TypedDict): ...
class TestDataContents(TypedDict): ...

_time_offset = get_time()

def _print_warning(type, message):
    print("\033[93m" + type + ": " + message + "\033[0m")

def execute_commands(commands, globals=None, locals=None, command_format_args=(), command_format_kwargs={},):
    for command in commands:
        formatted_command = str(command).format(*command_format_args, **command_format_kwargs)
        exec(formatted_command, globals, locals)

def _unpack_args(_d: dict):
    if _d is None: return (), {}
    ba, bk = _d.get("args", ()), _d.get("kwargs", {})
    if callable(ba): ba = ba()
    if callable(bk): bk = bk()
    return tuple(ba), bk

def _print_test(test_name):
    cstr = "|  Now executing test: " + test_name + "  |"
    rpr = "#" + "-" * (len(cstr) - 2) + "#"
    print(rpr)
    print(cstr)
    print(rpr)
 
def execute_test(test_name, contents):
    _print_test(test_name)

    btimeit = contents.get("timeit", False)
    main_commands = contents.get("commands")

    _globals = None if contents.get("disable_globals") else globals()

    if btimeit == True:
        start_time = get_time() - _time_offset
        print(f">> Test started at {round(start_time, 2)} sec after module initialization")
        print("")

    if cmd := contents.get("setup_commands", None):
        _locals = None if contents.get("disable_locals") else locals()
        _args = _unpack_args(contents.get("setup_args"))
        execute_commands(
            cmd, _globals, _locals, _args[0], _args[1]
        )

    interval = contents.get("interval", 0)
    for data in contents["data"]:
        _locals = None if contents.get("disable_locals") else locals()
        args = (data,) if isinstance(data, str) else tuple(data) if hasattr(data, "__iter__") else ()
        kwargs = data if isinstance(data, dict) else {}
        
        if contents.get("printout_current_data", False):
            print(">", data) 

        execute_commands(main_commands, _globals, _locals, args, kwargs)    # type: ignore
        if interval > 0: sleep(interval)

    print("--------------------------------------------------------")
    print(f"Executing '{test_name}' finished!")

    if cmd := contents.get("exit_commands", None):
        _locals = None if contents.get("disable_locals") else locals()
        _args = _unpack_args(contents.get("exit_args"))
        execute_commands(
            cmd, _globals, _locals, _args[0], _args[1]
        )

    if btimeit == True:
        end_time = get_time() - _time_offset
        elapsed_time = end_time - start_time
        print(f">> Time ended at {round(end_time, 2)} sec after module initialization")
        print(f">> Test took {round(elapsed_time, 2)} seconds to finish!")

    print("\n")

def _main(test_data: dict[str, dict], async_mode=False):
    print("#-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#")
    print("| /// Tester Module version 1.1 [Made by EF] /// |")
    print("#-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#")

    if not async_mode:
        _print_warning("[EFLTester] Warning", "Testing is in synchronous mode. Any time based"
                        " features will affect the main thread.")
        
    print("")

    for test_name, contents in test_data.items():
        execute_test(test_name, contents)

def main(test_data): _main(test_data)
def async_main(test_data):
    thread = Thread(daemon=True, target=_main, args=(test_data,), kwargs={"async_mode": True})
    thread.start()
    return thread
