"""
This dictionary has 2 arrays corresponding to (instruction, argument) and data 
"""
what_to_excecute = {
  # This is basically an array of tuples
  "instructions": [
                  # Instruction | data
                  ("LOAD_VALUE", 0), # 0 = First elemnt of the array
                  ("LOAD_VALUE", 1), # 1 = Second element of the array
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  # This is a simple array
  "numbers": [7, 5]
}

"""
This interpreter is considered a stack machine.Take into account this is not a fast implementation,
which should not be a problem since it is done for learning sake
"""

class Interpreter:
  def __init__(self):
    self.stack = [] # Remember this stack is only a list, not the actual memory page segment assigned to the thread

  # Add data to the stack
  def LOAD_VALUE(self, number):
    self.stack.append(number)

  def PRINT_ANSWER(self):
    answer = self.stack.pop() # We get the last value in the stack
    print(answer)
  
  def ADD_TWO_VALUES(self):
    first_num = self.stack.pop() # Get the last value from the stack
    second_num = self.stack.pop() # Get the next value from the stack
    total = first_num + second_num
    self.stack.append(total) # Add the output of the operation back to the stack

  def run_code(self, what_to_excecute):
    # Get the instruction values from the dictionary to be interpreted
    instructions = what_to_excecute["instructions"] 
    # Get the data stack array 
    numbers = what_to_excecute["numbers"] 
    # Now we need to interpret the instructions and apply them on the data
    for each_step in instructions:
      instruction, argument = each_step
      if instruction == "LOAD_VALUE":
        number = numbers[argument] # Get the data from the array
        self.LOAD_VALUE(number) # Call the corresponding function
      elif instruction == "ADD_TWO_VALUES":
        self.ADD_TWO_VALUES()
      elif instruction == "PRINT_ANSWER":
        self.PRINT_ANSWER()