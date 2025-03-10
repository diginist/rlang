class Unit:
    def __init__(self, utype: str, udict=None):
        self.type = utype
        self.dict = {} if udict is None else udict
    def __getitem__(self, item):
        return self.dict.__getitem__(item)
    def __setitem__(self, key, value):
        self.dict.__setitem__(key, value)
    def __repr__(self):
        return f"<{self.type} unit {self.dict}>"

class Expression:
    def __init__(self, units):
        self.units = units

class Parser:
    type_statements = [
        "number", "bit", "string"
    ]
    statements = type_statements + [
        "loop:", "jump:",
        "get", "send", "pass", "stop", "exit"
    ]
    def parse_expression(self, code):
        out = []
        string_mode = False
        for i in code:
            if string_mode:
                if i.endswith('"'):
                    string_mode = False
                    out[-1]["value"] += f" {i[:-1]}"
                else:
                    out[-1]["value"] += f" {i}"
            else:
                if i.startswith('"'):
                    if i.endswith('"'):
                        out.append(Unit("string", {"value": i[1:-1]}))
                    else:
                        string_mode = True
                        out.append(Unit("string", {"value": i[1:]}))
                else:
                    out.append(Unit("var", {"var": i}))
        if string_mode:
            raise SyntaxError("error: unclosed string")
        return Expression(out)
    def parse(self, code):
        tree = []
        tokens = code.split(" ")
        statement = tokens[0]
        expr_token = 1 #which token does the expression start at
        if statement in self.statements:
            if statement in self.type_statements:
                if tokens[1].endswith(":"):
                    var = tokens[1][:-1]
                    tree.append(Unit("type", {'type': statement}))
                    tree.append(Unit("newvar", {'var': var}))
                    expr_token = 2
                else:
                    raise SyntaxError("error: bad declaration")
            else:
                tree.append(Unit(statement))
        else:
            if len(statement) == 0:
                tree.append(Unit("empty_statement", {}))
            elif statement.endswith(":"):
                tree.append(Unit("oldvar", {'var': statement[:-1]}))
            else:
                raise SyntaxError("error: bad statement")
        if len(tokens) > expr_token:
            expr = self.parse_expression(tokens[expr_token:])
            tree.append(expr)
        return tree