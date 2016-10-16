from grammar import Grammar
import random

functions = {
    'and'  : lambda x, y: x and y,
    'or'   : lambda x, y: x or y,
    'xor'  : lambda x, y: (x or y) and (not (x and y)),
    'nand' : lambda x, y: not (x and y),
    'not'  : lambda x: not x
}

Rules = {
    'S' : ['expr'],
    'expr' : [['tri_op', 'expr', 'expr', 'expr'],
              ['bi_op', 'expr', 'expr'],
              ['u_op', 'expr'],
              'bool','bool'],
    'tri_op' : ['if'],
    'bi_op' : ['and', 'or', 'xor', 'nand'],
    'u_op' : ['not'],
    'bool' : ['True', 'False']
}

grammar1 = Grammar(Rules, functions, 10, 'S')
tree = grammar1.build_exec_tree(['if', 'False', ['xor', 'False', ['not', 'True']], ['not', ['if', ['nand', 'False', 'False'], 'False', 'False']]])
print('test')
print(tree.evaluate())

#rna = [random.randint(0,256) for x in range(1,10000)]
#translation = grammar1.translate(rna)
#print(translation)
#tree = grammar1.build_exec_tree(translation)
#print(tree.evaluate())

#Rules2 = {
#    'S' : ['expr'],
#    'expr' : ['d', ['d', 'expr']],
#    'd' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#}

#grammar2 = Grammar(Rules2, functions, 10, 'S')
#translation = grammar2.translate(rna)
#print(translation)
#tree = grammar2.build_exec_tree(translation)
#print(tree.evaluate() + 10)
