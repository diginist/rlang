from interpreter import Interpreter

inp = Interpreter()
while True:
    torun = input(">")
    error = inp.run_line(torun)
    if error: print(error)
    print(inp.out_stream, end='')
    inp.out_stream = ""