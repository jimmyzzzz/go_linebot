
from kernal import PercentageKernal, DirKernal
from c_root_wrapper import sample_c_root_wapper
from c_root_wrapper import c_root_wapper
import os


class SampleCKernal(PercentageKernal, DirKernal):

	def __init__(self, root_dir="CKernal_root", **kwargs):
		super().__init__(root_dir=root_dir, **kwargs)

	def get_self_root_names(self):
		return [
			file_name for file_name in os.listdir(self.root_dir_path)
			if file_name[-3:]==".so"
		]

	def target_file_is_exist(self, root_name):
		root_path = os.path.join(self.root_dir_path, f"{root_name}.so")
		if os.path.isfile(root_path):
			return True
		return False

	def import_root(self, root_name, option_list):
		root_path = os.path.join(self.root_dir_path, f"{root_name}.so")
		root = sample_c_root_wapper(root_name=root_name, root_path=root_path)
		return root

	def run_command(self, CMD):
		(RootOpt, CmdData) = self.get_RootOpt_CmdData(CMD)
		(root_name, root, option_list) = RootOpt
		(user_id, group_id, root_cmd, user_cmds) = CmdData

		success, uid = self.init_kernal_ref.pipe("get_uid", line_id=user_id)

		return_str = root.run(user_id, group_id, uid, root_cmd, user_cmds)
		return return_str


class CKernal(SampleCKernal):

	def import_root(self, root_name, option_list):
		root_path = os.path.join(self.root_dir_path, f"{root_name}.so")
		root = c_root_wapper(root_name=root_name, root_path=root_path)
		return root