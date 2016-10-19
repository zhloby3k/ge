import trade
import tester
from grammar import TreeLevelError

class GE:
    def __init__(self, data):
        self.grammar = trade.get_grammar(data)
        self.data = data

    def calculate_fitness(self, element):
        res = {'total' : 0,
               'results' : []}
        try:
            translation = self.grammar.translate(element)            
        except TreeLevelError:
            res['total'] = -1000000
            return res
        tree = self.grammar.build_exec_tree(translation)
        system = tester.System(tree, lambda x: x)
        result = tester.test_system(system, self.data, 0, self.data['N'])
        
        res['total'] = sum(result['results'])
        res['results'] = result['results']

        return res
