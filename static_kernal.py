
import importlib
import traceback
import sys


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


class InitKernal(KERNAL):

	def __init__(self):
		super().__init__(sub_kernals=[
			PythonKernal(),
		])


class PythonKernal(KERNAL):

	def __init__(self):
		super().__init__()
		self.root_dir_path = "./PythonKernal_root"
		sys.path.append(self.root_dir_path)

	def run(self, CMD):
		cmd_str = CMD.message.text
		if cmd_str[0] != '%': return (False, None)
		return super().run(CMD)

	def is_run_by_self(self, CMD):

		cmd_str = CMD.message.text
		if cmd_str[0]!='%': return False

		finded_percentage=False
		for c in cmd_str[1:]:
			if finded_percentage:
				if c=='\n': return True
				if c!=' ': return False
			else:
				if c=='\n': return False
				if c=='%': finded_percentage=True; continue

		if finded_percentage: return True
		return False

	def deconstruct_CMD(self, CMD):
		cmd_str = CMD.message.text
		user_id = CMD.source.user_id

		cmd_line = cmd_str.split('\n')
		(first_cmd, user_cmds) = (cmd_line[0], cmd_line[1:])

		first_cmd = first_cmd.replace('%', '')
		first_cmd_list = first_cmd.split(':')
		(build_cmd, root_cmds) = (first_cmd_list[0], first_cmd_list[1:])

		return user_id, build_cmd, root_cmds, user_cmds

	def run_command(self, CMD):
		(user_id, build_cmd, root_cmds, user_cmds) = self.deconstruct_CMD(CMD)

		build_cmd_list = build_cmd.split()
		(root_name, options) = (build_cmd_list[0], build_cmd_list[1:])

		if root_name in self.root_dict:
			root = self.root_dict[root_name]
		else:
			root_module = importlib.import_module(root_name)
			root = root_module.root(root_module)
			self.root_dict[root_name] = root

		if options: raise ValueError('尚未開放 build options')

		return root.run(user_id, root_cmds, user_cmds)
