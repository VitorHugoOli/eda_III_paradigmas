from dataclasses import dataclass
from typing import Tuple, List, NamedTuple
import time
from prettytable import PrettyTable


class Item(NamedTuple):
    value: int
    weight: int
    index: int = 0


@dataclass
class KnapsackEvaluation:
    name: str
    best_value = 0
    best_subset = []
    count = 0
    time = 0


class KnapsackEvaluator:
    def __init__(self):
        self.evaluations: List[KnapsackEvaluation] = []

    def add_evaluation(self, evaluation: KnapsackEvaluation) -> None:
        """Add an evaluation to the list of evaluations."""
        self.evaluations.append(evaluation)

    @staticmethod
    def evaluate(method):
        def _evaluate(*args, **kw):
            _eval = args[0].eval

            ts = time.time()
            result = method(*args, **kw)
            te = time.time()

            _eval.time = te - ts
            _eval.best_value, _eval.best_subset = result
            return result

        return _evaluate

    def __repr__(self):
        """Return a string representation of the evaluator."""
        table = PrettyTable()
        table.field_names = ["Name", "Best value", "Best subset", "Count", "Time"]
        for ev in sorted(self.evaluations, key=lambda x: x.count):
            table.add_row([ev.name, ev.best_value, ev.best_subset, ev.count, "{:0.6f} seconds".format(ev.time)])
        return str(table)


class KnapsackBase(KnapsackEvaluator):
    def __init__(self, items: List[Item], capacity: int):
        self.items = items
        self.capacity = capacity
        self.eval = None
        for idx, item in enumerate(self.items):
            self.items[idx] = item._replace(index=idx)
        super().__init__()

    def __repr__(self):
        """Return a string representation of the problem."""
        items_table = PrettyTable()
        items_table.field_names = ["Item Index", "Value", "Weight"]
        for idx, item in enumerate(self.items):
            items_table.add_row([idx, item.value, item.weight])

        problem_info = PrettyTable()
        problem_info.field_names = ["Total Capacity"]
        problem_info.add_row([self.capacity])

        return f"{items_table}\n{problem_info}\n{super().__repr__()}"


class KnapsackExhaustiveSearch(KnapsackBase):
    def __init__(self, items: List[Item], capacity: int):
        super().__init__(items, capacity)
        self.best_value = 0
        self.best_subset = []

    def exhaustive_search(self) -> Tuple[int, List[int]]:
        self.eval = KnapsackEvaluation("Exhaustive Search")
        self.evaluations.append(self.eval)
        return self._exhaustive_search()

    @KnapsackEvaluator.evaluate
    def _exhaustive_search(self) -> Tuple[int, List[int]]:
        visited = [False] * len(self.items)  # Initialize visited array
        self._exhaustive_search_set([], 0, 0, visited)
        return self.best_value, self.best_subset

    def _exhaustive_search_set(self, subset: List[int], value: int, weight: int, visited: List[bool]):
        if weight <= self.capacity and value > self.eval.best_value:
            self.best_value = value
            self.best_subset = subset[:]
        elif weight > self.capacity:
            return

        for i in range(len(self.items)):
            self.eval.count += 1
            if not visited[i]:
                visited[i] = True
                self._exhaustive_search_set(subset + [i], value + self.items[i].value, weight + self.items[i].weight,
                                            visited)
                visited[i] = False


class KnapsackDynamicProgramming(KnapsackBase):
    def __init__(self, items: List[Item], capacity: int):
        super().__init__(items, capacity)

    def dynamic_programming(self) -> Tuple[int, List[int]]:
        self.eval = KnapsackEvaluation("Dynamic Programming")
        self.add_evaluation(self.eval)
        return self._dynamic_programming()

    @KnapsackEvaluator.evaluate
    def _dynamic_programming(self) -> Tuple[int, List[int]]:
        n = len(self.items)
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]
        for i in range(1, n + 1):
            i_dx = i - 1
            for j in range(self.capacity + 1):
                self.eval.count += 1
                if self.items[i_dx].weight <= j:
                    dp[i][j] = max(dp[i_dx][j], dp[i_dx][j - self.items[i_dx].weight] + self.items[i_dx].value)
                else:
                    dp[i][j] = dp[i_dx][j]
        return dp[n][self.capacity], self._get_subset(dp)

    def _get_subset(self, dp: List[List[int]]) -> List[int]:
        subset = []
        n = len(self.items)
        j = self.capacity
        for i in range(n, 0, -1):
            self.eval.count += 1
            if dp[i][j] != dp[i - 1][j]:
                subset.append(i - 1)
                j -= self.items[i - 1].weight
        return subset[::-1]


class KnapsackMemoized(KnapsackBase):
    def __init__(self, items: List[Item], capacity: int):
        super().__init__(items, capacity)
        self.dp = [[None for _ in range(self.capacity + 1)] for _ in range(len(self.items) + 1)]

    def memoized(self) -> Tuple[int, List[int]]:
        self.eval = KnapsackEvaluation("Memoized")
        self.add_evaluation(self.eval)
        return self._memoized()

    @KnapsackEvaluator.evaluate
    def _memoized(self):
        best_value = self.__memoized(len(self.items), self.capacity)
        best_subset = self.__get_subset()
        return best_value, best_subset

    def __memoized(self, i: int, j: int) -> int:
        if self.dp[i][j] is not None:
            return self.dp[i][j]

        if i == 0 or j == 0:
            result = 0
        elif self.items[i - 1].weight > j:
            result = self.__memoized(i - 1, j)
        else:
            tmp1 = self.items[i - 1].value + self.__memoized(i - 1, j - self.items[i - 1].weight)
            tmp2 = self.__memoized(i - 1, j)
            result = max(tmp1, tmp2)

        self.dp[i][j] = result
        return result

    def __get_subset(self) -> List[int]:
        subset = []
        i, j = len(self.items), self.capacity
        while i > 0 and j > 0:
            self.eval.count += 1
            if self.dp[i][j] != self.dp[i - 1][j]:
                subset.append(i - 1)
                j -= self.items[i - 1].weight
            i -= 1
        return subset[::-1]


class KnapsackGreedy(KnapsackBase):
    def __init__(self, items: List[Item], capacity: int):
        super().__init__(items, capacity)

    def greedy(self) -> Tuple[int, List[int]]:
        self.eval = KnapsackEvaluation("Greedy")
        self.add_evaluation(self.eval)
        return self._greedy()

    @KnapsackEvaluator.evaluate
    def _greedy(self) -> Tuple[int, List[int]]:
        n = len(self.items)
        items = sorted(self.items, key=lambda x: x.weight == 0 and (x.value * 1000) or x.value / x.weight, reverse=True)
        subset = []
        value = 0
        weight = 0
        for i in range(n):
            self.eval.count += 1
            if weight + items[i].weight <= self.capacity:
                subset.append(items[i].index)
                value += items[i].value
                weight += items[i].weight
        return value, subset


class KnapsackBruteForce(KnapsackBase):
    def __init__(self, items: List[Item], capacity: int):
        super().__init__(items, capacity)

    def brute_force(self) -> Tuple[int, List[int]]:
        self.eval = KnapsackEvaluation("Brute Force")
        self.add_evaluation(self.eval)
        return self._brute_force()

    @KnapsackEvaluator.evaluate
    def _brute_force(self) -> Tuple[int, List[int]]:
        n = len(self.items)
        return self.calc_dp_pos(n, self.capacity), []

    def calc_dp_pos(self, i, j):
        if i == 0 or j == 0:
            return 0
        self.eval.count += 1

        return max(self.calc_dp_pos(i - 1, j),
                   self.calc_dp_pos(i - 1, j - self.items[i - 1].weight) + self.items[i - 1].value if
                   j - self.items[i - 1].weight >= 0 else 0)


class Knapsack(KnapsackExhaustiveSearch, KnapsackDynamicProgramming, KnapsackGreedy, KnapsackBruteForce,
               KnapsackMemoized):
    def __init__(self, items: List[Item], capacity: int):
        super().__init__(items, capacity)
