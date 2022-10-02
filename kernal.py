
import traceback


class KERNAL:

	def __init__(self, sub_kernals=[]):
		self.sub_kernals = sub_kernals
		self.root_dict = {}

	def run(self, CMD):

		if self.is_run_by_self(CMD):
			is_cmd = True
			try:
				return_str = self.run_command(CMD)

			except Exception as error:
				return (is_cmd, traceback.format_exc())
			return (is_cmd, return_str)

		for sub_kernal in self.sub_kernals:
			(is_cmd, return_str) = self.sub_kernal_run(sub_kernal, CMD)
			if is_cmd: return (is_cmd, return_str)

		(is_cmd, return_str) = (False, None)
		return (is_cmd, return_str)

	def is_run_by_self(self, CMD):
		return False

	def run_command(CMD):
		return "this is return str"

	def sub_kernal_run(self, sub_kernal, CMD):
		(is_cmd, return_str) = sub_kernal.run(CMD)
		return (is_cmd, return_str)