"""
This is a more complete implementation than tiny_interpreter, closer to Cpython
"""
import types
import inspect

class VirtualMachineError(Exception):
  pass

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
