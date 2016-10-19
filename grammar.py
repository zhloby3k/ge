class FnNode:
    def __init__(self, fn, children, name = ""):
        self.fn = fn
        self.children = children
        self.name = name

    def evaluate(self, i):
        args = [child.evaluate(i) for child in self.children]
        return self.fn(*args, i = i)

    def disp(self, indent = 0):
        print("  "*indent + self.name)
        for ch in self.children:
            ch.disp(indent + 1)

class IfNode:
    def __init__(self, cond_expr, true_expr, false_expr):
        self.cond_expr = cond_expr
        self.true_expr = true_expr
        self.false_expr = false_expr

    def evaluate(self, i):
        cond_value = self.cond_expr.evaluate(i)
        if cond_value:
            return self.true_expr.evaluate(i)
        else:
            return self.false_expr.evaluate(i)

    def disp(self, indent = 0):
        print("  "*indent + "if")
        self.cond_expr.disp(indent + 1)
        self.true_expr.disp(indent + 1)
        self.false_expr.disp(indent + 1)

class OffsetNode:
    def __init__(self, expr, offset_expr):
        self.expr = expr
        self.offset_expr = offset_expr

    def evaluate(self, i):
        offset = self.offset_expr.evaluate(i)
        if i - offset < 0:
            raise IndexError
        return self.expr.evaluate(i - offset)

    def disp(self, indent = 0):
        print("  "*indent + "offset")
        self.expr.disp(indent + 1)
        self.offset_expr.disp(indent + 1)

class LiteralNode:
    def __init__(self, value):
        self.value = value

    def evaluate(self, i):
        return self.value

    def disp(self, indent = 0):
        print("  "*indent + str(self.value))

class Grammar:
    def __init__(self, rules, functions, max_level, start):
        self.rules = rules
        self.functions = functions
        self.non_terminals = rules.keys()
        self.max_level = max_level
        self.start = start    

    def translate(self, rna):
        translation, rest_rna = self.translate_rec(rna, self.start, 0)
        return translation

    def build_exec_tree(self, translation):
        return self.build_exec_tree_rec(translation, False)

    def translate_rec(self, rna, tree, level):
        if level >= self.max_level:
            raise TreeLevelError

        if isinstance(tree, list):
            res = []
            for term in tree:
                sub_tree, rna = self.translate_term(term, rna, level)
                res.append(sub_tree)
        else:
            res, rna = self.translate_term(tree, rna, level)
        return res, rna
                
    def build_exec_tree_rec(self, translation, literal):
        if literal:
            if isinstance(translation, list):
                children = self.build_children(translation[1:], literal)
                return translation[0] + ''.join(children)
            else:
                return translation
        else:
            if isinstance(translation, list):
                head = translation[0]
                if head in self.functions:
                    children = self.build_children(translation[1:], literal)
                    return FnNode(self.functions[head], children, head)
                elif head == 'if':
                    children = self.build_children(translation[1:], literal)
                    return IfNode(*children)
                elif head == 'offset':
                    children = self.build_children(translation[1:], literal)
                    return OffsetNode(*children)
                else:
                    children = self.build_children(translation[1:], True)
                    return LiteralNode(eval(head + ''.join(children)))                    
            else:
                return LiteralNode(eval(translation))
                    
    def build_children(self, children, literal):
        res = []
        for child in children:
            res.append(self.build_exec_tree_rec(child, literal))
        return res

    def translate_term(self, term, rna, level):
        if self.is_nonterminal(term):
            expression = self.get_expression(term, rna[0])
            translation, rna = self.translate_rec(rna[1:], expression, level + 1)
        else:
            translation = term
        
        return translation, rna

    def is_function(self, term):
        return term in self.functions

    def is_nonterminal(self, term):
        return term in self.non_terminals

    def get_expression(self, term, value):
        expressions = self.rules[term]
        size = len(expressions)
        return expressions[value % size]
        

class TranslationError(Exception):
    pass

class TreeLevelError(TranslationError):
    pass
