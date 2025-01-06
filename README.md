# Py_interpreter
Simple Python interpreter written in Python

# Explanation

This python function

```py
def cond():
  x = 3
  if x < 5:
      return 'yes'
  else:
      return 'no'
```

Is compiled to bytecode

```text
b'd\x01}\x00|\x00d\x02k\x00r\x08d\x03S\x00d\x04S\x00'
```

Which looks like this

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

Based on this syntax is our interpreter written (implemented with less scope)
