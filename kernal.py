
import traceback
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

			except Exception:
				return (is_cmd, traceback.format_exc())
			return (is_cmd, return_str)

		return self.run_sub(CMD)

	def run_sub(self, CMD):
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

	def get_self_root_names(self):
		'''請回傳該kernal的root名單'''
		return []

	def get_root_names(self):
		root_name_list = self.get_self_root_names()
		for sub_ker in self.sub_kernals:
			root_name_list += sub_ker.get_root_names()
		return root_name_list

class DirKernal(KERNAL):

	def __init__(self, root_dir, **kwargs):
		super().__init__(**kwargs)
		now_path = os.path.dirname(os.path.realpath(__file__))
		self.root_dir_path = os.path.join(now_path, root_dir)

class PercentageKernal(KERNAL):

	def title_to_root(self, title_str):
		title_str = title_str.replace("%", " ")
		title_str = title_str.replace(":", " ")
		root_name = title_str.split()[0]
		return root_name

	def target_file_is_exist(self, root_name):
		'''修改: 通過root_nmae確認是否存在root檔案'''
		return False

	def import_root(self, root_name, option_list):
		'''修改: 通過root_nmae import root'''
		return

	def is_run_by_self(self, CMD):
		cmd_str = CMD.message.text
		finded_percentage=False
		title_str = ""

		for c in cmd_str[1:]:
			title_str += c
			if finded_percentage:
				# 確定是合法語法
				if c=='\n':
					root_name = self.title_to_root(title_str)
					if self.target_file_is_exist(root_name):
						return True
					return False
				if c != ' ': return False

			else:
				if c=='\n': return False
				if c=='%': finded_percentage=True; continue

		if not finded_percentage: return False

		# 已經確定是合法語法
		root_name = self.title_to_root(title_str)
		if self.target_file_is_exist(root_name):
			return True
		return False

	def deconstruct_CMD(self, CMD):
		cmd_str = CMD.message.text

		cmd_line = cmd_str.split('\n')
		(first_cmd, user_cmds) = (cmd_line[0], cmd_line[1:])

		first_cmd = first_cmd.replace('%', '')
		if ":" not in first_cmd:
			(build_cmd, root_cmd) = (first_cmd, "")
			return build_cmd, root_cmd, user_cmds

		(build_cmd, root_cmd) = first_cmd.split(':', 1)
		return build_cmd, root_cmd, user_cmds

	def get_RootOpt_CmdData(self, CMD):
		source_type = CMD.source.type # "user" or "group"
		user_id = CMD.source.user_id
		group_id = CMD.source.group_id if source_type=="group" else None

		(build_cmd, root_cmd, user_cmds) = self.deconstruct_CMD(CMD)

		build_cmd_list = build_cmd.split()
		(root_name, option_list) = (build_cmd_list[0], build_cmd_list[1:])

		if root_name in self.root_dict:
			root = self.root_dict[root_name]
		else:
			root = self.import_root(root_name, option_list)
			self.root_dict[root_name] = root

		RootOpt = (root_name, root, option_list)
		CmdData = (user_id, group_id, root_cmd, user_cmds)
		return RootOpt, CmdData

	def run_command(self, CMD):
		'''
		修改: 通過CMD取得root並回傳結果
		提示; 可以通過 self.get_RootOpt_CmdData 取得 root,user_id 等
		'''
		return "this is return str"


class HalfKernal(PercentageKernal):

	def get_self_root_names(self):
		'''回傳虛擬root_names'''
		return []

	def target_file_is_exist(self, root_name):
		return root_name in self.get_self_root_names()

	def import_root(self, root_name, option_list):
		return getattr(self, root_name)

	def run_command(self, CMD):
		(RootOpt, CmdData) = self.get_RootOpt_CmdData(CMD)
		(root_name, virtual_root, option_list) = RootOpt

		return virtual_root(CMD, CmdData)