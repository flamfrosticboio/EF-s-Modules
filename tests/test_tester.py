import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import EFLTester


test_data: dict[str, EFLTester.TestDataContents] = {
    "Simple Print Test": {
        "data": [
            "Hello World!",
            "EFLTester Print Test good",
            "",
            "Random Text: fmchtuoc*#3y8q@0%83mySvyu"
        ],
        "commands": [
            "print('{}')"
        ]
    },
    "Advanced Print Test": {
        "data": [
            {'mes': "Hello World!", "HELLO": "FW"},
        ],
        "commands": [
            'print("{mes}")',
        ],
        'setup_commands': (
            'print("Setting up things!")',
            'print("[Some Value {} {mes}]")',
        ),
        'setup_args': {
            "args": (10,),
            "kwargs": {"mes": True},
        },
        'exit_commands': [
            'print("OK SELF EXITING YEE")',
            "print('{}', '{ar}')",
        ],
        'exit_args': {
            'args': (10,),
            'kwargs': {'ar': "MINECRAFT"}
        }
    },
    "Some test": {
        "data": [
            "1",
            "2",
            "3",
            "4",
            "5",
        ],
        "commands": [
            'print({})',
        ],
        "interval": 0.5,
        'timeit': True
    },
    "ATE": {
        "data": [
            "(10, 20)"
        ],
        "commands": [
            'x = {}',
            'print(x)'
        ],
        'setup_commands': [
            "print({})",
        ],
        'setup_args': {
            "args": lambda: (10, 20, 30)
        },
        'printout_current_data': True
    },
}

# EFLTester.main(test_data)
EFLTester.async_main(test_data).join()
