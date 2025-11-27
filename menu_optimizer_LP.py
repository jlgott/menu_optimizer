import time
import pulp

# dummy restaraunt **pre-filtered** menus
#* NOTE: PuLP can NOT have spaces in namespaces, need underscore or .

restaurants = {
    "Thai_House": [
        {"name": "Veggie_Stir_Fry", "serves": 2, "price": 18, "vegan": 1, "halal": 0},
        {"name": "Green_Curry", "serves": 3, "price": 28, "vegan": 1, "halal": 0},
        {"name": "Chicken_Satay", "serves": 2, "price": 22, "vegan": 0, "halal": 1},
        {"name": "Pad_Thai", "serves": 2, "price": 20, "vegan": 0, "halal": 0},
        {"name": "Fried_Rice", "serves": 3, "price": 24, "vegan": 0, "halal": 0},
        {"name": "Mango_Sticky_Rice", "serves": 2, "price": 15, "vegan": 1, "halal": 0},
    ],
    "Lebanese_Grill": [
        {"name": "Falafel_Plate", "serves": 3, "price": 25, "vegan": 1, "halal": 1},
        {"name": "Shawarma_Platter", "serves": 4, "price": 45, "vegan": 0, "halal": 1},
        {"name": "Tabbouleh", "serves": 2, "price": 18, "vegan": 1, "halal": 1},
        {"name": "Mixed_Grill", "serves": 4, "price": 55, "vegan": 0, "halal": 1},
        {"name": "Baklava_Tray", "serves": 3, "price": 20, "vegan": 0, "halal": 1},
        {"name": "Hummus_Bowl", "serves": 2, "price": 15, "vegan": 1, "halal": 1},
    ],
    "Greek_Taverna": [
        {"name": "Spanakopita", "serves": 2, "price": 22, "vegan": 0, "halal": 0},
        {"name": "Greek_Salad", "serves": 3, "price": 20, "vegan": 1, "halal": 0},
        {"name": "Lamb_Gyro", "serves": 3, "price": 35, "vegan": 0, "halal": 1},
        {"name": "Dolmades", "serves": 2, "price": 18, "vegan": 1, "halal": 0},
        {"name": "Moussaka", "serves": 4, "price": 40, "vegan": 0, "halal": 0},
        {"name": "Baklava", "serves": 3, "price": 18, "vegan": 0, "halal": 0},
    ],
    "Chinese_Kitchen": [
        {"name": "Wonton_Soup", "serves": 2, "price": 12, "vegan": 0, "halal": 0},
        {"name": "Mapo_Tofu", "serves": 2, "price": 22, "vegan": 1, "halal": 0},
        {"name": "Sweet_&_Sour_Chicken", "serves": 3, "price": 28, "vegan": 0, "halal": 0},
        {"name": "Vegetable_Dumplings", "serves": 2, "price": 16, "vegan": 1, "halal": 0},
        {"name": "Beef_Stir_Fry", "serves": 3, "price": 30, "vegan": 0, "halal": 0},
        {"name": "Fried_Rice", "serves": 3, "price": 20, "vegan": 0, "halal": 0},
    ]
}





# LP for one rest
def solve_restaurant(
    name: str,
    menu: dict,
    total_people: int,
    budget: float,
    vegan_req: int,
    halal_req: int,
    max_repeats: int
):
    
    # setup LP problem
    model = pulp.LpProblem(name, pulp.LpMinimize)

    # order count for each item
    x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in range(len(menu))}

    # Objective Fn: min cost
    model += pulp.lpSum(menu[i]["price"] * x[i] for i in range(len(menu)))

    #* ***Constraints
    # total people
    model += pulp.lpSum(menu[i]["serves"] * x[i] for i in range(len(menu))) >= total_people

    # vegans
    model += pulp.lpSum(menu[i]["serves"] * menu[i]["vegan"] * x[i] for i in range(len(menu))) >= vegan_req

    # halals
    model += pulp.lpSum(menu[i]["serves"] * menu[i]["halal"] * x[i] for i in range(len(menu))) >= halal_req

    # budget total
    model += pulp.lpSum(menu[i]["price"] * x[i] for i in range(len(menu))) <= budget

    # maximum item repeats of 2, as an example.
    for i in range(len(menu)):
        model += x[i] <= max_repeats

    # RUN MODEL
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # check for optimal solutions, if there are no optimal solutions don't return one.
    if pulp.LpStatus[model.status] != "Optimal":
        return None


    # calc some key metrics for faster processing later
    total_cost = sum(menu[i]["price"] * x[i].value() for i in range(len(menu)))
    chosen = [(menu[i]["name"], int(x[i].value())) for i in range(len(menu)) if x[i].value() > 0]


    return {
        "restaurant": name,
        "cost": total_cost,
        "items": chosen
    }



# GLOBALS for testing
TOTAL_PEOPLE = 10
VEGAN_REQ = 2
HALAL_REQ = 1
BUDGET = 120
MAX_REPEATS = 1

# solve all restaurants
def main_loop(total_people, vegan_req, halal_req, budget, max_repeats):
    solutions = []
    for rname, rmenu in restaurants.items():
        sol = solve_restaurant(rname, rmenu, total_people, budget, vegan_req, halal_req, max_repeats)
        if sol:
            solutions.append(sol)
    
    if not solutions:
        return None, []
    
    cheapest = min(solutions, key=lambda s: s["cost"])
    return cheapest, solutions




if __name__ == "__main__":

    s = time.perf_counter()
    
    cheapest, all_solutions = main_loop(TOTAL_PEOPLE, VEGAN_REQ, HALAL_REQ, BUDGET, MAX_REPEATS)
    
    e = time.perf_counter()

    print(f"\n*** RUN TIME ***\n   {(e-s)*1000:.3f} ms\n")

    print("*** Constraints ***")
    print(f'People: {TOTAL_PEOPLE}')
    print(f'Vegans: {VEGAN_REQ}')
    print(f'Halals: {HALAL_REQ}')
    print(f'BUDGET: ${BUDGET}')
    print(f'REPEATS: {MAX_REPEATS}')

    print("\nBest option:")
    print(cheapest["restaurant"])
    print("\tCost:", cheapest["cost"])
    
    for item, qty in cheapest["items"]:
        print(f"\t\t{qty}x {item}")

    print("\n*** ALL SOLUTIONS ***")
    for sol in all_solutions:
        print(f"\n{sol['restaurant']}")
        print(f"\tT_Cost: {sol['cost']}")
        
        for item, qty in sol["items"]:
            print(f"\t\t{qty}x {item}")

