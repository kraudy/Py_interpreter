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

Is compiled to bytecode, which look like this on raw hexadecimal values. As you may tell, 2 bytes are used
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

# Useful commands

```py
# To disassemble in human readable form
dis.dis(function)
```

```py
# To show bytecode in raw hexadecimal 
function.__code__.co_code
```

```py
# To show bytecode in deciaml value 
list(function.__code__.co_code)
```

```py
# To show bytecode name
[dis.opname[i] for i in list(function.__code__.co_code)]
```

# Examples

## While loop 

```py
def loop():
  x = 1
  while x < 5:
    x = x + 1
    return x
```

```asm
  2           0 LOAD_CONST               1 (1)
              2 STORE_FAST               0 (x)

  3           4 LOAD_FAST                0 (x)
              6 LOAD_CONST               2 (5)
              8 COMPARE_OP               0 (<)
             10 POP_JUMP_IF_FALSE       12 (to 24)

  4          12 LOAD_FAST                0 (x)
             14 LOAD_CONST               1 (1)
             16 BINARY_ADD
             18 STORE_FAST               0 (x)

  5          20 LOAD_FAST                0 (x)
             22 RETURN_VALUE

  3     >>   24 LOAD_CONST               0 (None)
             26 RETURN_VALUE
```

## For loop 

```py
def myfor():
  for i in range(5):
          x += i
```

```asm
  2           0 LOAD_GLOBAL              0 (range)
              2 LOAD_CONST               1 (5)
              4 CALL_FUNCTION            1
              6 GET_ITER
        >>    8 FOR_ITER                 6 (to 22)
             10 STORE_FAST               0 (i)

  3          12 LOAD_FAST                1 (x)
             14 LOAD_FAST                0 (i)
             16 INPLACE_ADD
             18 STORE_FAST               1 (x)
             20 JUMP_ABSOLUTE            4 (to 8)

  2     >>   22 LOAD_CONST               0 (None)
             24 RETURN_VALUE
```

## List comprehension 

```py
def gen():
  x = [i for i in range(5)]
  return x
```

```asm
  2           0 LOAD_CONST               1 (<code object <listcomp> at 0x7f53cc04d790, file "<stdin>", line 2>)
              2 LOAD_CONST               2 ('gen.<locals>.<listcomp>')
              4 MAKE_FUNCTION            0
              6 LOAD_GLOBAL              0 (range)
              8 LOAD_CONST               3 (5)
             10 CALL_FUNCTION            1
             12 GET_ITER
             14 CALL_FUNCTION            1
             16 STORE_FAST               0 (x)

  3          18 LOAD_FAST                0 (x)
             20 RETURN_VALUE

Disassembly of <code object <listcomp> at 0x7f53cc04d790, file "<stdin>", line 2>:
  2           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                 4 (to 14)
              6 STORE_FAST               1 (i)
              8 LOAD_FAST                1 (i)
             10 LIST_APPEND              2
             12 JUMP_ABSOLUTE            2 (to 4)
        >>   14 RETURN_VALUE
```

# References
