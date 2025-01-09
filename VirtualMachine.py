"""
This is a more complete implementation than tiny_interpreter, closer to Cpython
"""

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
    self.run_frame(frame)

"""
A Frame is like the context of execution of the bytecode
"""
class Frame(object):
  def __init__(self, code_obj, global_names, local_names, prev_frame):
    self.code_obj = code_obj
    self.global_names = global_names
    self.local_names = local_names
    self.prev_frame = prev_frame
    self.stack = []
    if prev_frame:
      self.builtin_names = prev_frame.builtin_names
    else:
      self.builtin_names = local_names['__builtins__']
      if hasattr(self.builtin_names, '__builtins__'):
        self.builtin_names = self.builtin_names.__dict__
    
    self.last_instruction = 0
    self.block_stack = []