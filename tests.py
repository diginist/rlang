import unittest
from interpreter import Interpreter

class TestVariableDefinitions(unittest.TestCase):
    inp = Interpreter()

    def test_define_str(self):
        self.inp.run_line("string hewo: \"Hello, world!\"")

    def test_read_str(self):
        self.inp.run_line("send hewo")
        self.assertEqual(self.inp.out_stream, "Hello, world!\n")
        self.inp.out_stream = ""
        
    def test_type_mismatch_at_definition(self):  
        self.assertRaises(RuntimeError, self.inp.run_line, "number realnumber: \"not a number\"")
        self.inp = Interpreter()

if __name__ == '__main__':
    unittest.main()
