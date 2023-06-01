from knapsack import KnapsackBase, KnapsackExastiveSearch, Knapsack

knap_1 = Knapsack(
    items=[(10, 60), (20, 100), (30, 120), (40, 200), (50, 240), (60, 300), (70, 350), (80, 400), (90, 450),
           (100, 500)],
    capacity=200
)

knap_2 = Knapsack(
    items=[(5, 10), (10, 20), (6, 15), (7, 7), (3, 8), (9, 25)],
    capacity=15
)

knap_1.exastive_search()
print(knap_1)
