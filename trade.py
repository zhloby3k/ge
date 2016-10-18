import grammar
import data_functions
import numpy as np
import pandas as pd

def get_grammar(data):
    rules = get_rules()
    functions = get_functions(data)
    return grammar.Grammar(rules, functions, 20, 'S')


def get_rules():
    return {        
        'S' : ['trade_expr'],
        'trade_expr' : [['if', 'bool_expr', '"buy"', 'sell_expr']],

        'sell_expr'  : [['if', 'bool_expr', '"sell"', '"do_nothing"']],
        
        'bool_expr'  : ['comb_bool', 'rel_bool'],

        'comb_bool'  : [['bi_op_bool', 'bool_expr', 'bool_expr'],
                        ['u_op_bool', 'bool_expr']],
        'rel_bool'   : [['greater', 'num_expr', 'num_expr'],
                        ['less', 'num_expr', 'num_expr']],

        'bi_op_bool' : ['and', 'or'],

        'u_op_bool'  : ['not'],

        'num_expr'   : [['bi_op', 'num_expr', 'num_expr'],
                        ['offset', 'num_expr', 'int'],
                        'int',
                        'float',
                        'indicator'],
        
        'bi_op'      : ['add',
                        'sustract',
                        'multiple'],
        
        'int'        : ['all',
                        ['non_zero', 'all']],
        
        'float'      : [['all', '.', 'int']],
    
        'non_zero'   : ['1', '2', '3', '4', '5', '6', '7', '8', '9'],

        'all'        : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
        
        'indicator' : [['ma', 'int']]
    
}

def ma(data, n):
    s = pd.Series(data['close'])
    return s.rolling(center=False,window=n).mean().values

def get_functions(data):
    return {
        'and'        : lambda x, y, *, i = 0: x and y,
        'or'         : lambda x, y, *, i = 0: x or y,
        'not'        : lambda x, *, i = 0: not x,
        
        'add'        : lambda x, y, *, i = 0: x + y,
        'sustract'   : lambda x, y, *, i = 0: x - y,
        'multiple'   : lambda x, y, *, i = 0: x * y,
        
        'greater'    : lambda x, y, *, i = 0: True if x > y else False,
        'less'       : lambda x, y, *, i = 0: True if x < y else False,
        'equal'      : lambda x, y, *, i = 0: True if x == y else False,
        
        'ma'         : data_functions.wrapper(ma, data)
}    
