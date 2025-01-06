"""
This interpreter works as a stack machine.Take into account this is not an optimized implementation,
which should not be a problem since it is done for learning sake
"""

class Interpreter:
  def __init__(self):
    self.stack = [] # Remember this stack is only a list, not the actual memory page segment assigned to the thread

  # Add data to the stack
  def LOAD_VALUE(self, number):
    self.stack.append(number)
    print(self.stack)

  def PRINT_ANSWER(self):
    answer = self.stack.pop() # We get the last value in the stack
    print(answer)
  
  def ADD_TWO_VALUES(self):
    # Note that there are not parameters given, the data is fetch directly from the stack
    first_num = self.stack.pop() 
    second_num = self.stack.pop() 
    total = first_num + second_num
    self.stack.append(total) # Add the output of the operation back to the stack
    print(self.stack)

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

# Testing

"""
This dictionary has 2 arrays corresponding to (instruction, argument) and data.
Can be viewd as variables in the data segment of the memory
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

interpreter.run_code(what_to_excecute)
