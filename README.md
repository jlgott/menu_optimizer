
# Menu Optimizer (Super Simple Demo)

This is a tiny Python script that picks the best restaurant order based on:
- how many people you need to feed
- how many vegan servings you need
- how many halal servings you need
- your total budget

The solver checks each restaurant’s menu and figures out how many of each item to order.
If a restaurant cannot meet the rules (too expensive, not enough vegan, etc.) it is skipped.
In the end the script prints the cheapest restaurant that satisfies all your requirements.

---
### How to run:
1. pip install pulp
2. python menu_solver.py

---
### Inputs
- TOTAL_PEOPLE = 10
- VEGAN_REQ = 2
- HALAL_REQ = 1
- BUDGET = 120
- MAX_REPEATS = 1

---
### Constraints
Adding more rules is very easy:
```python
model += x[i] <= 3  # no more than 3 of any item
model += x[i] >= 1  # must include at least one of this item
model += total_cost <= 90   # adjust budget or add new limits
```
---
### MILP 
This example uses a tiny MILP (Mixed-Integer Linear Program) to pick the best
restaurant order. MILP just means:

- we choose integer quantities (0, 1, 2, …) of each menu item
- we add simple linear rules (budget, servings, vegan/halal requirements)
- the solver finds the cheapest combination that satisfies all rules

You can keep adding constraints the same way—MILP handles them automatically.

**Basically a modified Knapsack Problem**

Source:  https://en.wikipedia.org/wiki/Knapsack_problem
