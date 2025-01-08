"""
This interpreter works as a stack machine.Take into account this is not an optimized implementation,
which should not be a problem since it is done for learning sake
"""

class Interpreter:
  def __init__(self):
    self.stack = [] # This is the data stack (similar to data segment)
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

      bytecode_method = getattr(self, instruction)

      if argument_value is None:
        bytecode_method()
      else:
        bytecode_method(argument_value)
 
    print("=" * 20)
