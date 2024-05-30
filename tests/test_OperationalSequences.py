import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Sequences import Operational_Sequences

x = Operational_Sequences.NumericalSequence()
y = Operational_Sequences.IntSequence()
x += (5, 5, 5)

print(x)
