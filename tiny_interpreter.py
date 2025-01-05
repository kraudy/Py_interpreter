"""
This dictionary has 2 arrays that are viewd as 2 stack. This interpreter is considered a stack machine
"""
what_to_excecute = {
  "instructions": [
                  # Instruction | data
                  ("LOAD_VALUE", 0), # 0 = First elemnt of the array
                  ("LOAD_VALUE", 1), # 1 = Second element of the array
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  "numbers": [7, 5]
}

"""
Take into account this is not a fast interpreter, which should not be a problem since it is done for learning
sake
"""

class Interpreter:
  def __init__(self):
    self.stack = [] # Remember this stack is only a list, not the actual memory page segment assigned to the thread

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
