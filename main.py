from interpreter import Interpreter

inp = Interpreter()
while True:
    torun = input("\033[94;1m> \033[0;90m")
    error = inp.run_line_wrapped(torun)
    if error: print(error)
    print(inp.out_stream, end='')
    inp.out_stream = ""