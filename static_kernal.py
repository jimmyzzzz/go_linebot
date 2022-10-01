
from run_call import RunCall
import importlib
import traceback
import sys
import os


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

	def run(self, CMD):
		try:
			return super().run(CMD)
		except Exception as error:
			return traceback.format_exc()

class PythonKernal(KERNAL):

	def __init__(self):
		super().__init__()
		now_path = os.path.dirname(os.path.realpath(__file__))
		self.root_dir_path = os.path.join(now_path, "PythonKernal_root")
		sys.path.append(self.root_dir_path)

	def run(self, CMD):
		cmd_str = CMD.message.text
		if cmd_str[0] != '%': return (False, None)
		return super().run(CMD)

	def python_file_is_exist(self, title_str):
		title_str = title_str.replace("%", " ")
		title_str = title_str.replace(":", " ")
		root_name = title_str.split()[0]

		root_path = os.path.join(self.root_dir_path, f"{root_name}.py")
		if os.path.isfile(root_path):
			return True
		return False

	def is_run_by_self(self, CMD):

		cmd_str = CMD.message.text
		if cmd_str[0]!='%': return False

		finded_percentage=False
		title_str = ""
		for c in cmd_str[1:]:
			title_str += c

			if finded_percentage:
				# 確定是合法語法
				if c=='\n':
					# 要確認是否存在該py檔
					if self.python_file_is_exist(title_str): return True
					return False

				if c!=' ': return False
			else:
				if c=='\n': return False
				if c=='%': finded_percentage=True; continue

		# 確定是合法語法
		if finded_percentage:
			# 要確認是否存在該py檔
			if self.python_file_is_exist(title_str): return True
			return False

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

		path_head = os.path.join(self.root_dir_path, root_name)
		fp_list = []

		class IoRunCall(RunCall):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)

				if self.exists(path_head): return
				self.makedirs(path_head)

			def open_file(self, path, mode='r'):
				fp = open(os.path.join(path_head, path), mode=mode)
				fp_list.append(fp)
				return fp

			def listdir(self, path):
				return os.listdir(os.path.join(path_head, path))

			def isfile(self, path):
				return os.path.isfile(os.path.join(path_head, path))

			def exists(self, path):
				return os.path.exists(os.path.join(path_head, path))

			def makedirs(self, path):
				os.makedirs(os.path.join(path_head, path))

			def close(self):
				for fp in fp_list:
					fp.close()
				fp_list.clear()


		run_call = IoRunCall(root, user_id, root_cmds, user_cmds)
		return_str = root.run(run_call, user_id, root_cmds, user_cmds)
		run_call.close()
		return return_str
