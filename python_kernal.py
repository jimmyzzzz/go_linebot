
from run_call import RunCall
from kernal import PercentageKernal, DirKernal
import importlib
import sys
import os


class PythonKernal(PercentageKernal, DirKernal):

	def __init__(self, root_dir="PythonKernal_root", **kwargs):
		super().__init__(root_dir=root_dir, **kwargs)
		sys.path.append(self.root_dir_path)

	def get_self_root_names(self):
		return [
			file_name for file_name in os.listdir(self.root_dir_path)
			if file_name[-3:]==".py"
		]

	def target_file_is_exist(self, root_name):
		root_path = os.path.join(self.root_dir_path, f"{root_name}.py")
		if os.path.isfile(root_path):
			return True
		return False

	def import_root(self, root_name, option_list):
		root_module = importlib.import_module(root_name)
		root = root_module.root(root_module)
		return root

	def run_command(self, CMD):

		(RootOpt, CmdData) = self.get_RootOpt_CmdData(CMD)
		(root_name, root, option_list) = RootOpt
		(user_id, group_id, root_cmd, user_cmds) = CmdData

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

		run_call = IoRunCall(root, user_id, group_id, root_cmd, user_cmds)
		return_str = root.run(run_call)
		run_call.close()
		return return_str
