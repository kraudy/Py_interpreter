"""
This is a more complete implementation than tiny_interpreter, closer to Cpython
"""
import types
import inspect
import dis
import sys
import collections
import operator

class VirtualMachineError(Exception):
  pass

Block = collections.namedtuple("Block", "type, handler, stack_height")

class VirtualMachine(object):
  def __init__(self):
    self.frames = []  # The call stack of frames, this is like a memory map
    self.frame = None # The current frame
    self.return_value = None
    self.last_exception = None

  def run_code(self, code, global_names=None, local_names=None):
    """Entry point of bytecode execution"""
    # Creation of initial frame on which the code will start executing
    frame = self.make_frame(code, global_names=global_names, local_names=local_names)
    # The execution of the code is done inside the frame
    self.run_frame(frame)

  def make_frame(self, code, callargs={}, global_names=None, local_names=None):
    if global_names is not None and local_names is not None:
      local_names = global_names
    elif self.frames:
      global_names = self.frame.global_names
      local_names = {}
    else:
      global_names = local_names = {
        '__builtins__': __builtins__,
        '__name__': __name__,
        '__doc__': None,
        '__package__': None
      }
    local_names.update(callargs)
    frame = Frame(code, global_names, local_names, self.frame)
    return frame

  # Frame stack manipulation
  def push_frame(self, frame):
    self.frames.append(frame)
    self.frame = frame
  
  def pop_frame(self):
    self.frames.pop()
    if self.frames:
      self.frame = self.frames[-1]
    else:
      self.frame = None

  def run_frame(self):
    pass

  # Data stack manipulation
  def top(self):
    return self.frame.stack[-1]
  
  def pop(self):
    return self.frame.stack.pop()

  def push(self, *vals):
    self.frame.stack.extend(vals)
  
  def popn(self, n):
    """Pop n values from the stack"""
    if n:
      ret = self.frame.stack[-n:]
      self.frame.stack[-n:] = []
      return ret
    else:
      return []
    
  # Block stack manipulation
  def push_block(self, b_type, handler=None):
    stack_height = len(self.frame.stack)
    self.frame.block_stack.append(Block(b_type, handler, stack_height))

  def pop_block(self):
    return self.frame.block_stack.pop()

  def unwind_block(self, block):
    """Unwind value of data stack corresponding to a block"""
    if block.type == 'except-handler':
      # The exception is on the stack as type, value, and traceback.
      offset = 3
    else:
      offset = 0
    
    while len(self.frame.stack) > block.level + offset:
      self.pop()

    if block.type == 'except-handler':
      traceback, value, exctype = self.popn(3)
      self.last_exception = exctype, value, traceback

  def manage_block_stack(self, why):
    """"""
    frame = self.frame
    block = frame.block_stack[-1]
    if block.type == 'loop' and why == 'continue':
      self.jump(self.return_value)
      why = None
      return why
    
    self.pop_block()
    self.unwind_block(block)

    if block.type == 'loop' and why == 'break':
      why = None
      self.jump(block.handler)
      return why

    if (block.type in ['setup-except', 'finally'] and why == 'exception'):
      self.push_block('except-handler')
      exctype, value, tb = self.last_exception
      self.push(tb, value, exctype)
      self.push(tb, value, exctype) # yes, twice
      why = None
      self.jump(block.handler)
      return why
    
    elif block.type == 'finally':
      if why in ('return', 'continue'):
        self.push(self.return_value)
      
      self.push(why)

      why = None
      self.jump(block.handler)
      return why
    
    return why

  # Stack manipulation
  def byte_LOAD_CONST(self, const):
    self.push(const)

  def byte_POP_TOP(self):
    self.pop()

  # Names
  def byte_LOAD_NAME(self, name):
    frame = self.frame
    if name in frame.f_locals:
      val = frame.f_locals[name]
    elif name in frame.f_globals:
      val = frame.f_globals[name]
    elif name in frame.f_builtins:
      val = frame.f_builtins[name]
    else:
      raise NameError("name '%s' is not defined" % name)
    
    self.push(val)
  
  def byte_STORE_NAME(self, name):
    self.frame.f_locals[name] = self.pop()
  
  def byte_LOAD_FAST(self, name):
    if name in self.frame.f_locals:
      val = self.frame.f_locals[name]
    else:
      raise UnboundLocalError(
        "local variable '%s' referenced before assignment" %name
      )
    self.push(val)

  def byte_STORE_FAST(self, name):
    self.frame.f_locals[name] = self.pop()
  
  def byte_LOAD_GLOBAL(self, name):
    f = self.frame
    if name in f.f_globals:
      val = f.f_globals[name]
    elif name in f.f_builtins:
      val = f.f_builtins[name]
    else:
      raise NameError("global name '%s' is not defined" % name)
    self.push(val)
  
  # Operators
  BINARY_OPERATORS = {
    'POWER': pow,
    'MULTIPLY': operator.mul,
    'FLOOR_DIVIDE': operator.floordiv,
    'TRUE_DIVIDE': operator.truediv,
    'MODULO': operator.mod,
    'ADD':    operator.add,
    'SUBSTRACT': operator.sub,
    'SUBSCR': operator.getitem,
    'LSHIFT': operator.lshift,
    'RSHIFT': operator.rshift,
    'AND':    operator.and_,
    'XOR':    operator.xor,
    'OR':     operator.or_
  }

  def binaryOperator(self, op):
    x, y = self.popn(2)
    self.push(self.BINARY_OPERATORS[op](x, y))
  
  COMPARE_OPERATORS = [
    operator.lt,
    operator.le,
    operator.eq,
    operator.ne,
    operator.gt,
    operator.ge,
    lambda x, y: x in y,
    lambda x, y: x not in y,
    lambda x, y: x is y,
    lambda x, y: x is not y,
    lambda x, y: issubclass(x, Exception) and issubclass(x, y)
  ]

  def byte_COMPARE_OP(self, opnum):
    x, y = self.popn(2)
    self.push(self.COMPARE_OPERATORS[opnum](x, y))
  
  # Attributes and indexing
  def byte_LOAD_ATTR(self, attr):
    obj = self.pop()
    val = getattr(obj, attr)
    self.push(val)
  
  def byte_STORE_ATTR(self, name):
    val, obj = self.popn(2)
    setattr(obj, name, val)

  # Building
  def byte_BUILD_LIST(self, count):
    elts = self.popn(count)
    self.push(elts)
  
  def byte_BUILD_MAP(self, size):
    self.push({}) # ?
  
  def byte_STORE_MAP(self):
    the_map, val, key = self.popn(3)
    the_map[key] = val
    self.push(the_map)
  
  def byte_LIST_APPEND(self, count):
    val = self.pop()
    the_list = self.frame.stack(-count) # peek
    the_list.append(val)
  
  # Jumps
  def byte_JUMP_FORWARD(self, jump):
    self.jump(jump)

  def byte_JUMP_ABSOLUTE(self, jump):
    self.jump(jump)

  def byte_POP_JUMP_IF_TRUE(self, jump):
    val = self.pop()
    if val:
      self.jump(jump)

  def byte_POP_JUMP_IF_FALSE(self, jump):
    val = self.pop()
    if not val:
      self.jump(jump)
    
  # Blocks
  def byte_SETUP_LOOP(self, dest):
    self.push_block('loop', dest)

  def byte_GET_ITER(self):
    self.push(iter(self.pop()))
  
  def byte_FOR_ITER(self, jump):
    iterobj = self.top()
    try:
      v = next(iterobj)
      self.push(v)
    except StopIteration:
      self.pop()
      self.jump(jump)
    
  def byte_BREAK_LOOP(self):
    return 'break'
  
  def byte_POP_BLOCK(self):
    self.pop_block()
  
  # Functions
  def byte_MAKE_FUNCTION(self, argc):
    # Note the order
    name = self.pop()
    code = self.pop()
    defaults = self.popn(argc)
    globs = self.frame.f_globals
    fn = Function(name, code, globs, defaults, None, self)
    self.push(fn)
  
  def byte_CALL_FUNCTION(self, arg):
    lenKw, lenPos = divmod(arg, 256) # KWargs not supported hede | ?
    posargs = self.popn(lenPos)

    func = self.pop()
    frame = self.frame
    retval = func(*posargs)
    self.push(retval)
  
  def byte_RETURN_VALUE(self):
    self.return_value = self.pop()
    return "return"

  def parse_byte_and_args(self):
    f = self.frame
    opoffset = f.last_instruction
    byteCode = f.code_obj.co_code[opoffset]
    f.last_instruction += 1
    byte_name = dis.opname[byteCode]
    if byteCode >= dis.HAVE_ARGUMENT:
      # index into bytecode
      arg = f.code_obj.co_code[f.last_instruction : f.last_instruction + 2]
      f.last_instruction += 2 # Advance instruction pointer
      arg_val = arg[0] + (arg[1] * 256)
      if byteCode in dis.hasconst: # Look up a constant
        arg = f.code_obj.co_const[arg_val]
      elif byteCode in dis.hasname: # Look up name
        arg = f.code_obj.co_names[arg_val]
      elif byteCode in dis.haslocal: # Look up local name
        arg = f.code_obj.co_varnames[arg_val]
      elif byteCode in dis.hasjrel: # Calculate a relative jump
        arg = f.last_instruction + arg_val
      else:
        arg = arg_val
      argument = [arg]
    else:
      argument = []

    return byte_name, argument

  def dispatch(self, byte_name, argument):
    """Dispatch bytename to corresponding method.
    Exceptions are caught and set on the virtual machine"""

    # Reason to unwinding the stack
    why = None
    try:
      bytecode_fn = getattr(self, 'byte_%s' % byte_name, None)
      if bytecode_fn is None:
        if byte_name.startswith('UNARY_'):
          self.unaryOperator(byte_name[6:])
        elif byte_name.startswith('BINARY_'):
          self.binaryOperator(byte_name[7:])
        else:
          raise VirtualMachineError(
            "unsupported bytecode type: %s" % byte_name
          )
      else:
          why = bytecode_fn(*argument)
    except:
      # deals with exception encountered while executing the op
      self.last_exception = sys.exc_info()[:2] + (None,)
      why = 'exception'

  def run_frame(self, frame):
    """Run frame until it returns"""  
    self.push_frame(frame)
    while True:
      byte_name, arguments = self.parse_byte_and_args()

      why = self.dispatch(byte_name, arguments)

      # Deal with block management
      while why and frame.block_stack:
        why = self.manage_block_stack(why)
      
      if why:
        break
    
    self.pop_frame()

    if why == 'exception':
      exc, val, tb = self.last_exception
      e = exc(val)
      e.__traceback__ = tb
      raise e

    return self.return_value

"""
A Frame is like the context of execution of the bytecode
"""
class Frame(object):
  def __init__(self, code_obj, global_names, local_names, prev_frame):
    self.code_obj = code_obj
    self.global_names = global_names
    self.local_names = local_names
    self.prev_frame = prev_frame
    # Data stack of the frame
    self.stack = []
    if prev_frame:
      self.builtin_names = prev_frame.builtin_names
    else:
      self.builtin_names = local_names['__builtins__']
      if hasattr(self.builtin_names, '__builtins__'):
        self.builtin_names = self.builtin_names.__dict__
    
    self.last_instruction = 0
    self.block_stack = []

class Function(object):
  """
  Create a realistic function object 
  """
  # This is used for memory optimization, usually a Python class uses
  # a __dict__ to stores instance attributes which is dynamic, but __slots__
  # sets statically which attributes the class object has
  __slots__ = [
    'func_code', 'func_name', 'func_defaults', 'func_globals',
    'func_locals', 'func_dict', 'func_closure',
    '__name__', '__dict__', '__doc__',
    '_vm', '_func'
  ]

  def __init__(self, name, code, globs, defaults, closure, vm):
    self._vm = vm
    self.func_code = code 
    self.func_name = self.__name__ = name or code.co_name
    self.func_defaults = tuple(defaults)
    self.func_globals = globs
    self.func_locals = self._vm.frame.f_locals
    self.__dict__ = {}
    self.func_closure = closure
    self.__doc__ = code.co_consts[0] if code.co_consts else None

    kw = {
      'argdefs': self.func_defaults
    }
    if closure:
      kw['closure'] = tuple(make_cell(0) for _ in closure)
    self._func = types.FunctionType(code, globs, **kw)

    def __call__(self, *args, **kwargs):
      """When calling a function makes a new frame and run it"""
      callargs = inspect.getcallargs(self._func, *args, **kwargs)
      # callargs provides a mapping for the arguments to pass
      frame = self._vm.make_frame(
        self.func_code, callargs, self.func_globals, {}
      )
      return self._vm.run_frame(frame)
    
def make_cell(value):
  """Create real Python closure and grab a cell"""
  fn = (lambda x: lambda: x)(value)
  return fn.__closure__[0]
