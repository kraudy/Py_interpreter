"""
This is a more complete implementation than tiny_interpreter, closer to Cpython
"""

class VirtualMachineError(Exception):
  pass

class VirtualMachine(object):
  def __init__(self):
    self.frames = []  # The call stack of frames
    self.frame = None # The current frame
    self.return_value = None
    self.last_exception = None

  def run_code(self, code, global_names=None, local_names=None):
    """Entry point of bytecode execution"""
    # Creation of initial frame
    frame = self.make_frame(code, global_names=global_names, local_names=local_names)
    self.run_frame(frame)
