class System:
    def __init__(self, exec_tree, interpreter):
        self.exec_tree = exec_tree
        self.interpreter = interpreter

    def get_signal(self, index):
        try:
            return self.interpreter(self.exec_tree.evaluate(index))
        except IndexError:
            return 'do_nothing'

def test_system(system, data, start, end):
    state = {'results' : []}
    for i in range(end - start - 1):
        idx = start + i
        signal = system.get_signal(idx)
        if signal == 'do_nothing':
            res = 0
        elif signal == 'buy':
            res = data['close'][idx] - data['open'][idx]
        elif signal == 'sell':
            res = data['open'][idx] - data['close'][idx]
        state['results'].append(res)

    return state
