# Py_interpreter
Simple Python interpreter written in Python. Based on the CPython virtual stack machine implementation

# Rationale for the project

This python function

```py
def cond():
  x = 3
  if x < 5:
      return 'yes'
  else:
      return 'no'
```

Is compiled to bytecode, which look like this on raw hexadecimal values. At you may tell, 2 bytes are used
per bytecode instruction.

```asm
b'd\x01}\x00|\x00d\x02k\x00r\x08d\x03S\x00d\x04S\x00'
```

Converted to decimal

```py
[100, 1, 125, 0, 124, 0, 100, 2, 107, 0, 114, 8, 100, 3, 83, 0, 100, 4, 83, 0]
```

Converted to operations

```py
['LOAD_CONST', 'POP_TOP', 'STORE_FAST', '<0>', 'LOAD_FAST', '<0>', 'LOAD_CONST', 'ROT_TWO', 'COMPARE_OP', '<0>', 'POP_JUMP_IF_FALSE', '<8>', 'LOAD_CONST', 'ROT_THREE', 'RETURN_VALUE', '<0>', 'LOAD_CONST', 'DUP_TOP', 'RETURN_VALUE', '<0>']
```

Converted to human readable form

```asm
  2           0 LOAD_CONST               1 (3)
              2 STORE_FAST               0 (x)

  3           4 LOAD_FAST                0 (x)
              6 LOAD_CONST               2 (5)
              8 COMPARE_OP               0 (<)
             10 POP_JUMP_IF_FALSE        8 (to 16)

  4          12 LOAD_CONST               3 ('yes')
             14 RETURN_VALUE

  6     >>   16 LOAD_CONST               4 ('no')
             18 RETURN_VALUE
```

The first column is the source line number. Second column is the bytecode index. Third column 
is the instruction. Fourth column is the the argument to the instruction. Fifth column is the
argument value. Based on this syntax is our interpreter written (implemented with less scope).

Our tiny interpreter takes this last representation and executes it implementing a stack machine.
