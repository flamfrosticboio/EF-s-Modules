"""A module to test things using commands and data. Under the hood, this is a exec(cmd) like tester that cmd:str is formatted by parameter:data.
Notes: 
- Use only kwargs or args is allowed in formatting your commands. It is not possible to use both args and kwargs in data due to string.format() limitations.
- Pass globals and locals in main / async_main function if you intend to use them. 

Manual:
    TestDataContents (Dict):
    - [Required]: \n
        - data: (Iterable[Iterable[str] ] | dict[str, str] | str)
            - Data for repetitive testing.
            - Ex: {'data': [{"inst": "I will move right", "value": (10, 0)}], 'commands': ["print({inst}, "[Moving Relative Coordinate]", {value})"]}
        - commands: (Iterable[str])
            - Commands to be executed during repetitive testing.
            - Ex: {'data': ["(10, 20)", "(20, 10)"], 'commands': ['movement = {}', 'print(movement)']}
    - [Not Required]: \n
        - interval: (int | float)
            - Delay after next data execution
            - Note: interval yields the main thread. Use async_main().
            - Ex: {'data': [str(n) for n in range(1, 11)], 'commands': ['print({})'], "setup_commands": ['print("Printing numbers from:")'], 'interval': 1}  # counts from 1 to 10 at 1 second interval
        - timeit: (bool)
            - Enable to measure time in executing the test. Does not use timeit module.
            - Ex: {'data': ['yielder'], 'commands': ['print("{}")'], 'interval': 10, 'timeit': True}  # Prints out how long the test lasted.
        - setup_commands: (Iterable[str])
            - Commands executed prior to the main test.
            - Ex: look at the example of interval.
        - setup_args: (ArgsDict)
            - Args and kwargs to be executed in the setup_commands
            - Ex: {'data': ['milk', 'coffee', 'juice'], 'commands': ['print({})'], 'setup_commands': ['print("User {name} likes/prefers:")'], 'setup_args': {'kwargs': {'name': this_user.Name}}}
        - exit_commands: (Iterable[str])
            - Commands executed after the main test.
            - Ex: {'data': ['Something'], 'commands': ['print({})'], 'setup_commands': ['print("Starting")'], 'exit_commands': ['print("Finalizing")']}
        - exit_args: (ArgsDict)
            - Args and kwargs to be executed in the exit_commands
            - Ex: {'data': ['milk', 'coffee', 'juice'], 'commands': ['print({})'], 'exit_commands': ['print("Those are what User {name} likes/prefers.")'], 'exit_args': {'kwargs': {'name': this_user.Name}}}
        - disable_globals: (bool)
            - Whenever should the test use globals() or interact at global space
        - disable_locals: (bool)
            - Whenever should the thest use locals() or interact at local space (at <function > default)

    ArgsDict (Dict):
    -[Not Required]
        - args: (Iterable[Any] | Callable[[], Iterable[Any]])
            - Args for the command execution
        - kwargs: (Dict[str, Any] | Callable[[], Dict[str, Any]])
            - Kwargs for the command execution
"""

from typing import TypedDict, Required, NotRequired, Any, Callable, Dict, Iterable
from threading import Thread

class ArgsDict(TypedDict):
    args: NotRequired[Iterable[Any] | Callable[[], Iterable[Any]]]
    kwargs: NotRequired[Dict[str, Any] | Callable[[], Dict[str, Any]]]

class TestDataContents(TypedDict):
    data: Required[Iterable[Iterable[str] | dict[str, str] | str]]

    commands: Required[Iterable[str]]

    setup_commands: NotRequired[Iterable[str]]
    setup_args: NotRequired[ArgsDict]

    exit_commands: NotRequired[Iterable[str]]
    exit_args: NotRequired[ArgsDict]

    interval: NotRequired[int | float]
    timeit: NotRequired[bool]

    disable_globals: NotRequired[bool]
    disable_locals: NotRequired[bool]

    printout_current_data: NotRequired[bool]

def execute_test(test_name: str, contents: TestDataContents): ...
def main(test_data: dict[str, TestDataContents], globals: dict[str, Any] | None = None, locals: dict[str, Any] | None = None): ...
def async_main(test_data: dict[str, TestDataContents], globals: dict[str, Any] | None = None, locals: dict[str, Any] | None = None) -> Thread: ...
