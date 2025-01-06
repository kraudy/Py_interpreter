from tiny_interpreter import Interpreter

"""
It is important to note that these well formated instructions should be the result of the compiler,
the interpreter is the last phase
"""

"""
This dictionary has 2 arrays corresponding to (instruction, argument) and data.
Can be viewd as variables in the data segment of the memory
"""

# Test 1: 7 + 5

what_to_excecute = {
  # This is basically an array of tuples
  "instructions": [
                  # Instruction | arguments
                  ("LOAD_VALUE", 0), 
                  ("LOAD_VALUE", 1), 
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  # Array of data
  "numbers": [7, 5]
}

interpreter = Interpreter()

interpreter.run_code(what_to_excecute)

# Test 2: (7 + 5) + 8

what_to_excecute = {
  "instructions": [
                  # Instruction | arguments
                  ("LOAD_VALUE", 0), 
                  ("LOAD_VALUE", 1), 
                  ("ADD_TWO_VALUES", None),
                  ("LOAD_VALUE", 2), 
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  # Array of data
  "numbers": [7, 5, 8]
}

interpreter = Interpreter()
interpreter.run_code(what_to_excecute)

# Test 3: a + b | a = 1, b = 2

"""
Notice that now we are introducing new OPCODES: STORE_NAME and LOAD_NAME so the arguments can point to
to differents arrays of data
On this program, the data is loaded into the stack, transfer to a variable, then moved back from the variables
to the stack and then and operation is performed 
"""
what_to_excecute = {
  "instructions": [
                  # Instruction | arguments
                  ("LOAD_VALUE", 0), 
                  ("STORE_NAME", 0), 
                  ("LOAD_VALUE", 1),
                  ("STORE_NAME", 1), 
                  ("LOAD_NAME", 0),
                  ("LOAD_NAME", 1),
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  # Array of data
  "numbers": [1, 2],
  "names": ["a", "b"]
}

interpreter = Interpreter()
interpreter.run_code(what_to_excecute)