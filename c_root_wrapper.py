
import traceback
from ctypes import CDLL
from ctypes import c_char_p
import os


class sample_c_root_wapper:

	def __init__(self, root_name, root_path):
		self.root_name = root_name
		self.so_module = CDLL(os.path.join(root_path, f"{root_name}.so"))

	def run(self, user_id, root_cmd, user_cmds):

		run_order = [
			("get_user_id", user_id),
			("get_root_cmd", root_cmd),
			("get_user_cmds", user_cmds)
		]
		for fn_name, input_str in run_order:
			success, return_info = self.fn_call(fn_name, input_str)
			if success: continue
			if fn_name in {"get_user_id", "get_root_cmd", "get_user_cmds"}:
				continue
			return f"ERROR[{self.root_name}]: {fn_name} not find"

		success, return_info = self.fn_call("root_return", " ")
		return return_info

	def fn_call(self, fn_name, input_str):
		try:
			fn = getattr(self.so_module, fn_name)
		except AttributeError as error:
			success = False
			return (success, error)

		fn.argtypes = [c_char_p]
		fn.restype = c_char_p

		return_str = fn(bytes(input_str, 'utf-8'))
		return_str = return_str.decode("utf-8")
		success = True
		return (success, return_str)

class c_root_wapper(sample_c_root_wapper):

	def run(self, user_id, root_cmd, user_cmds):
		pass