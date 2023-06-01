from multiprocessing import Pool

from knap import Knapsack, KnapsackMemoized, Item, KnapsackGreedy, KnapsackExhaustiveSearch, KnapsackBruteForce, \
    KnapsackDynamicProgramming

approachs = {KnapsackBruteForce, KnapsackExhaustiveSearch, KnapsackDynamicProgramming, KnapsackMemoized, KnapsackGreedy}

knap_1 = Knapsack(
    items=[Item(10, 60), Item(20, 100), Item(30, 120), Item(40, 200), Item(50, 240), Item(60, 300), Item(70, 350),
           Item(80, 400), Item(90, 450),
           Item(100, 500)],
    capacity=200
)

for approach in approachs:
    knap_1.from_approach(approach)
    knap_1.solve()
print(knap_1)

knap_2 = Knapsack(
    items=[Item(5, 10), Item(10, 20), Item(6, 15), Item(7, 7), Item(3, 8), Item(9, 25)],
    capacity=15
)

for approach in approachs:
    knap_2.from_approach(approach)
    knap_2.solve()
print(knap_2)

knap = Knapsack([
    Item(360, 7),
    Item(83, 0),
    Item(59, 30),
    Item(130, 22),
    Item(431, 80),
    Item(67, 94),
    Item(230, 11),
    Item(52, 81),
    Item(93, 70),
    Item(125, 64),
    Item(670, 59),
    Item(892, 18),
    Item(600, 0),
    Item(38, 36),
    Item(48, 3),
    Item(147, 8),
    Item(78, 15),
    Item(256, 42),
    Item(63, 9),
    Item(17, 0),
    Item(120, 42),
    Item(164, 47),
    Item(432, 52),
    Item(35, 32),
    Item(92, 26),
    Item(110, 48),
    Item(22, 55),
    Item(42, 6),
    Item(50, 29),
    Item(323, 84),
    Item(514, 2),
    Item(28, 4),
    Item(87, 18),
    Item(73, 56),
    Item(78, 7),
    Item(15, 29),
    Item(26, 93),
    Item(78, 44),
    Item(210, 71),
    Item(36, 3),
    Item(85, 86),
    Item(189, 66),
    Item(274, 31),
    Item(43, 65),
    Item(33, 0),
    Item(10, 79),
    Item(19, 20),
    Item(389, 65),
    Item(276, 52),
    Item(312, 13),
], capacity=850)

for approach in approachs - {KnapsackBruteForce, KnapsackExhaustiveSearch}:
    knap.from_approach(approach)
    knap.solve()
print(knap)
