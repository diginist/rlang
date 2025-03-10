import sys
from interpreter import Interpreter

rlang_ver = "0.0.1"

def run_file(filename, inp):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                error = inp.run_line_wrapped(line.strip())
                if error:
                    print(error)
                    sys.exit(1) 
                print(inp.out_stream, end='')
                inp.out_stream = ""
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

repl_notice = f"""R\033[90mlang

version \033[0m{rlang_ver}
\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-\033[0m+\033[90m-"""

def repl(inp):
    print(repl_notice)
    while True:
        try:
            torun = input("\033[94;1m> \033[0;90m")
            error = inp.run_line(torun)
            if error:
                print(error)
            print(inp.out_stream, end='')
            inp.out_stream = ""
        except (EOFError, KeyboardInterrupt):
            print("\nExiting REPL.")
            break

if __name__ == "__main__":
    inp = Interpreter()
    if len(sys.argv) > 1:
        run_file(sys.argv[1], inp)
    else:
        repl(inp)