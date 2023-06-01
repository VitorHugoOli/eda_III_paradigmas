from typing import Tuple, List


class KnapsackEvaluation:
    def __init__(self, name: str):
        self.name = name
        self.best_value = 0
        self.best_subset = []
        self.count = 0
        self.time = 0


class KnapsackBase:
    def __init__(self, items: List[Tuple[int, int]], capacity: int):
        self.items = items
        self.capacity = capacity
        self.evals: List[KnapsackEvaluation] = []

    @classmethod
    def from_knapsack(cls, knapsack):
        return cls(knapsack.items, knapsack.capacity)

    def __str__(self):
        buffer = f"Items: {self.items}\nCapacity: {self.capacity}\n"
        buffer += f"{'Name':<20}{'Best value':<20}{'Best subset':<20}{'Count':<20}{'Time':<20}\n"
        for evall in self.evals:
            buffer += f"{evall.name:<20}{evall.best_value:<20}{str(evall.best_subset):<20}{evall.count:<20}{evall.time:<20}\n"
        return buffer


class KnapsackExastiveSearch(KnapsackBase):
    def __init__(self, items: List[Tuple[int, int]], capacity: int):
        super().__init__(items, capacity)
        self.ex_s_eval = KnapsackEvaluation("Exastive Search")
        self.evals.append(self.ex_s_eval)

    def exastive_search(self) -> Tuple[int, List[int]]:
        visited = [False] * len(self.items)  # Initialize visited array
        self._exastive_search([], 0, 0, visited)
        return self.ex_s_eval.best_value, self.ex_s_eval.best_subset

    def _exastive_search(self, subset: List[int], value: int, weight: int, visited: List[bool]):
        if weight > self.capacity:
            return
        if value > self.ex_s_eval.best_value:
            self.ex_s_eval.best_value = value
            self.ex_s_eval.best_subset = subset
        for i in range(len(self.items)):
            self.ex_s_eval.count += 1
            if not visited[i]:
                visited[i] = True
                self._exastive_search(subset + [i], value + self.items[i][0], weight + self.items[i][1], visited)
                visited[i] = False


class Knapsack(KnapsackExastiveSearch):
    def __init__(self, items: List[Tuple[int, int]], capacity: int):
        super().__init__(items, capacity)
