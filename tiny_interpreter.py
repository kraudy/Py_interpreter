"""
This dictionary has 2 arrays that are viewd as 2 stack. The interpreter is considered a stack machine
"""
what_to_excecute = {
  "instructions": [
                  # Instruction | data
                  ("LOAD_VALUE", 0), # 0 = First elemnt of the array
                  ("LOAD_VALUE", 1), # 1 = Second element of the array
                  ("ADD_TWO_VALUES", None),
                  ("PRINT_ANSWER", None)
                  ],
  "number": [7, 5]
}

