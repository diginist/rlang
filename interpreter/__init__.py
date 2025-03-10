from .parser import Parser

class Interpreter:
    def __init__(self):
        self.parser = Parser()

        self.line = 0
        self.next_line = 0
        self.out_stream = ""
        self.vars = {}
        self.vartypes = {}
        self.loops = {}
    def ex_expr(self, expr):
        if expr.units[0].type == "var":
            return self.vars[expr.units[0]['var']]
        return expr.units[0]
    def execute(self, tree):
        statement = tree[0]
        expr = tree[-1]
        match statement.type:
            case "type":
                vtype = tree[0]['type']
                var = tree[1]['var']
                assign = self.ex_expr(expr)
                if assign.type != vtype:
                    raise RuntimeError("error: wrong type for declaration")
                self.vars[var] = self.ex_expr(expr)
                self.vartypes[var] = vtype
            case "oldvar":
                var = ['var']
                assign = self.ex_expr(expr)
                if assign.type != self.vartypes[var]:
                    raise RuntimeError("error: wrong type for assignment")
                self.vars[var] = assign
            case "loop:":
                pass
            case "jump:":
                pass
            case "get":
                pass
            case "send":
                self.out_stream += self.ex_expr(expr)['value'] + "\n"
            case "pass":
                pass
            case "stop":
                pass
            case "exit":
                raise KeyboardInterrupt

    def run_line(self, line):
        self.next_line = self.line + 1
        parsed = self.parser.parse(line)
        self.execute(parsed)
        self.line = self.next_line
    
    def run_line_wrapped(self, line):
        try:
            self.run_line(line)
        except SyntaxError as e:
            return f"\033[91msyntax \033[0m@ \033[91;1m{line}\033[0m | \033[91m{e}\033[0m"
        except RuntimeError as e:
            return f"\033[91minterpreter \033[0m@ \033[91;1m{line}\033[0m | \033[91m{e}\033[0m"
        except KeyboardInterrupt:
            return " "
        
    def run(self, code):
        program = code.splitlines()
        while True:
            error = self.run_line(program[self.line])
            if error:
                return error
            else:
                if self.line >= len(program):
                    break