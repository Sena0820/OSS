
class SearchNodeValueOrdered(SearchNode):
    def __init__(self, *args, **kwargs):
        super(SearchNodeValueOrdered, self).__init__(*args, **kwargs)
        self.value = self.problem.value(self.state)
        #自分が設定したvalueがここで登場している

    def __lt__(self, other):
        # value must work inverted, because heapq sorts 1-9
        # and we need 9-1 sorting
        return -self.value < -other.value


class InverseTransformSampler(object):
    def __init__(self, weights, objects):
        assert weights and objects and len(weights) == len(objects)#条件のテストなので無視
        self.objects = objects
        tot = float(sum(weights))
        if tot == 0:
            tot = len(weights)
            weights = [1 for x in weights]
        accumulated = 0
        self.probs = []
        for w, x in izip(weights, objects):
            p = w / tot
            accumulated += p
            self.probs.append(accumulated)

    def sample(self):
        target = random.random()
        i = 0
        while i + 1 != len(self.probs) and target > self.probs[i]:
            i += 1
        return self.objects[i]

def expand(self, local_search=False):
    '''Create successors.'''
    new_nodes = []
    for action in self.problem.actions(self.state):
        new_state = self.problem.result(self.state, action)
        cost = self.problem.cost(self.state,
                                 action,
                                 new_state)
        nodefactory = self.__class__
        new_nodes.append(nodefactory(state=new_state,
                                     parent=None if local_search else self,#ヒントになるかも
                                     problem=self.problem,
                                     action=action,
                                     cost=self.cost + cost,
                                     depth=self.depth + 1))
    return new_nodes

def _all_expander(fringe, iteration, viewer):
    '''
    Expander that expands all nodes on the fringe.
    '''
    expanded_neighbors = [node.expand(local_search=True)
                          for node in fringe]
#   fringeをnodeに格納してstateやactionを駆使してnewnodeを返してexpanded_neighborsというリストに格納している
    if viewer:
        viewer.event('expanded', list(fringe), expanded_neighbors)

    list(map(fringe.extend, expanded_neighbors))
    #expanded_neighborsというリストにextendという関数を適応させているだけ
    #もう一度考え直す
def _create_genetic_expander(problem, mutation_chance):
    '''
    Creates an expander that expands the bests nodes of the population,
    crossing over them.
    '''
    def _expander(fringe, iteration, viewer):
        fitness = [x.value for x in fringe] # fringeの値をfitnessというリストに格納
        sampler = InverseTransformSampler(fitness, fringe)
        # 良く分からないがprobという値が蓄積していっている
        new_generation = []

        expanded_nodes = []
        expanded_neighbors = []

        for _ in fringe:# fringeの要素の数だけ繰り返すという無駄な変数を使わない書きかた
            node1 = sampler.sample()#引数のオブジェクトをほぼランダムで返すだけ
            node2 = sampler.sample()
            child = problem.crossover(node1.state, node2.state)
            action = 'crossover'
            if random.random() < mutation_chance:
                # Noooouuu! she is... he is... *IT* is a mutant!
                child = problem.mutate(child)
                action += '+mutation'

            child_node = SearchNodeValueOrdered(state=child, problem=problem, action=action)
            # これさへ分かれば理解できそう
            new_generation.append(child_node)

            expanded_nodes.append(node1)
            expanded_neighbors.append([child_node])
            expanded_nodes.append(node2)
            expanded_neighbors.append([child_node])

        if viewer:
            viewer.event('expanded', expanded_nodes, expanded_neighbors)

        fringe.clear()
        for node in new_generation:
            fringe.append(node)

    return _expander


def genetic(problem, population_size=100, mutation_chance=0.1,
            iterations_limit=0, viewer=None):
    '''
    Genetic search.

    population_size specifies the size of the population (ORLY).
    mutation_chance specifies the probability of a mutation on a child,
    varying from 0 to 1.
    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: SearchProblem.generate_random_state, SearchProblem.crossover,
    SearchProblem.mutate and SearchProblem.value.
    '''
    return _local_search(problem,
                         _create_genetic_expander(problem, mutation_chance),
                         iterations_limit=iterations_limit,
                         fringe_size=population_size,
                         random_initial_states=True,
                         stop_when_no_better=iterations_limit==0,
                         viewer=viewer)


def _local_search(problem, fringe_expander, iterations_limit=0, fringe_size=1,
                  random_initial_states=False, stop_when_no_better=True,
                  viewer=None):
    '''
    Basic algorithm for all local search algorithms.
    '''
    if viewer:
        viewer.event('started')

    fringe = BoundedPriorityQueue(fringe_size)
    # このコードでキューという先に入れたものが先に取り出されるデータ構造のリストにfringeをしている（__init__)
    # 取り出すときは普通のリストのように取り出せる
    if random_initial_states:
        for _ in range(fringe_size):
            s = problem.generate_random_state()
            fringe.append(SearchNodeValueOrdered(state=s, problem=problem))
    else:
        fringe.append(SearchNodeValueOrdered(state=problem.initial_state,
                                             problem=problem))

    finish_reason = ''
    iteration = 0
    run = True
    best = None
    word_list = []
    while run:
        # if viewer:
            # viewer.event('new_iteration', list(fringe))

        old_best = fringe[0]
        # print(f"old:{fringe[0]}")
        fringe_expander(fringe, iteration, viewer)
        #　これが良く分からん、でもこれでfringeを操作して新たな値に変えているのは確か
        best = fringe[0]
        word_list.append(fringe[0])
        # print(f"new:{fringe[0]}")
        # print(f"fringe:{fringe[1]}")

        iteration += 1
        print(f"↑{iteration}回目")
        print("                        ")
        if iterations_limit and iteration >= iterations_limit:
            run = False
            finish_reason = 'reaching iteration limit'
        elif old_best.value >= best.value and stop_when_no_better:
            run = False
            finish_reason = 'not being able to improve solution'
    double_list = []
    for i in word_list:
        if i not in double_list:
            double_list.append(i)
    print(f"探索に掛かった単語数：{len(double_list)}")
    print(f"探索過程：{double_list}")
    if viewer:
        viewer.event('finished', fringe, best, 'returned after %s' % finish_reason)

    return best
