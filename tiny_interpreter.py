"""
This interpreter works as a stack machine.Take into account this is not an optimized implementation,
which should not be a problem since it is done for learning sake
"""

class Interpreter:
  def __init__(self):
    self.stack = [] # Remember this stack is only a list, not the actual memory page segment assigned to the thread
    self.environment = {} # Used for storing variables
  
  def show_stack(self, function):
    print(f"Stack state: {self.stack} | Function: {function}")
  
  def show_variables(self):
    print(f"Variables: {self.environment}")

  # Simulates creating a variable and assigning a value
  def STORE_NAME(self, name):
    self.environment[name] = self.stack.pop()
    self.show_stack("STORE_NAME")
    self.show_variables()

  # Add value of variable to the stack
  def LOAD_NAME(self, name):
    self.stack.append(self.environment[name]) 
    self.show_stack("LOAD_NAME")
    self.show_variables()

  # Add data to the stack
  def LOAD_VALUE(self, number):
    self.stack.append(number)
    self.show_stack("LOAD_VALUE")

  def PRINT_ANSWER(self):
    print(self.stack.pop())
  
  def ADD_TWO_VALUES(self):
    # Note that there are not parameters given, the data is fetch directly from the stack
    first_num = self.stack.pop() 
    second_num = self.stack.pop() 
    total = first_num + second_num
    self.stack.append(total) # Add the output of the operation back to the stack
    self.show_stack("ADD_TWO_VALUES")

  def parse_argument(self, instruction, argument, what_to_execute):
    """ Takes the Opcode and the arguments and returns the corresponding value"""
    numbers = ["LOAD_VALUE"]
    names = ["LOAD_NAME", "STORE_NAME"]

    if instruction in numbers:
      argument_value = what_to_execute["numbers"][argument]
    elif instruction in names:
      argument_value = what_to_execute["names"][argument]
    else:
      argument_value = None
    
    return argument_value

  def run_code(self, what_to_execute):
    # Get the instruction values from the dictionary to be interpreted
    instructions = what_to_execute["instructions"] 

    """ 
      The instruction is mapped to the corresponding function and is also used to determine the
      argument value from what_to_execute on each step
    """
    for each_step in instructions:
      instruction, argument = each_step
      argument_value = self.parse_argument(instruction, argument, what_to_execute)

      if instruction == "LOAD_VALUE":
        self.LOAD_VALUE(argument_value) 
      elif instruction == "ADD_TWO_VALUES":
        self.ADD_TWO_VALUES()
      elif instruction == "PRINT_ANSWER":
        self.PRINT_ANSWER()
      elif instruction == "STORE_NAME":
        self.STORE_NAME(argument_value)
      elif instruction == "LOAD_NAME":
        self.LOAD_NAME(argument_value)
    
    print("=" * 20)

# Testing

"""
This dictionary has 2 arrays corresponding to (instruction, argument) and data.
Can be viewd as variables in the data segment of the memory
It is important to note that these well formated instructions should be the result of the compiler,
the interpreter is the last phase
"""
what_to_excecute = {
  # This is basically an array of tuples
  "instructions": [
                  # Instruction | arguments
                  ("LOAD_VALUE", 0), # 0 = First elemnt of the array
                  ("LOAD_VALUE", 1), # 1 = Second element of the array
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  # Array of data
  "numbers": [7, 5]
}

interpreter = Interpreter()

interpreter.run_code(what_to_excecute)

what_to_excecute = {
  "instructions": [
                  # Instruction | arguments
                  ("LOAD_VALUE", 0), # 0 = First elemnt of the array
                  ("LOAD_VALUE", 1), # 1 = Second element of the array
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