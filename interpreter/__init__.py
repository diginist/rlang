from .parser import Parser, Unit


class Interpreter:
    def __init__(self):
        self.parser: Parser = Parser()

        self.line: int = 0
        self.next_line: int = 0
        self.out_stream: str = ""
        self.vars: dict = {}
        self.vartypes: dict = {}
        self.loops: dict = {}

    def ex_expr(self, expr: parser.Expression) -> Unit:
        if expr.units[0].type == "var":
            return self.vars[expr.units[0]["var"]]
        return expr.units[0]

    def execute(self, tree: list[Unit]):
        statement = tree[0]
        expr = tree[-1]
        match statement.type:
            case "empty_statement":
                pass
            case "type":
                vtype = tree[0]["type"]
                var = tree[1]["var"]
                assign = self.ex_expr(expr)
                if assign.type != vtype:
                    raise RuntimeError("error: wrong type for declaration")
                self.vars[var] = self.ex_expr(expr)
                self.vartypes[var] = vtype
            case "oldvar":
                var = ["var"]
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
                self.out_stream += self.ex_expr(expr)["value"] + "\n"
            case "pass":
                pass
            case "stop":
                pass
            case "exit":
                raise KeyboardInterrupt

    def run_line(self, line: str):
        self.next_line = self.line + 1
        parsed = self.parser.parse(line)
        self.execute(parsed)
        self.line = self.next_line

    def run_line_wrapped(self, line: str):
        try:
            self.run_line(line)
        except SyntaxError as e:
            return f"\033[91msyntax \033[0m@ \033[91m`\033[1m{line}\033[0;91m` (L{self.line})\033[0m | \033[91m{e}\033[0m"
        except RuntimeError as e:
            return f"\033[91minterpreter \033[0m@ \033[91m`\033[1m{line}\033[0;91m` (L{self.line})\033[0m | \033[91m{e}\033[0m"
        except KeyboardInterrupt:
            return " "

    def run(self, code: str):
        program = code.splitlines()
        while True:
            error = self.run_line(program[self.line])
            if error:
                return error
            else:
                if self.line >= len(program):
                    break
