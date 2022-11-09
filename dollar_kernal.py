
from kernal import HalfKernal
import os
import json
import traceback


class DollarKernal(HalfKernal):

	def __init__(self, dir_name, file_name, **kwargs):
		super().__init__(**kwargs)
		now_path = os.path.dirname(os.path.realpath(__file__))
		self.dir_path = os.path.join(now_path, dir_name)
		self.file_name = file_name
		self.user_data = self.read_user_json()

	def pipe(self, request, *args, **kwargs):
		
		if request=="get_uid":
			user_id = kwargs['line_id']
			if user_id not in self.user_data["USER"]:
				return super().pipe(request, *args, **kwargs)
			return (True, self.user_data["USER"][user_id]["UID"])

		return super().pipe(request, *args, **kwargs)

	def save_user_json(self):
		file_path = os.path.join(self.dir_path, self.file_name)
		with open(file_path, 'w') as f:
			data_str = json.dumps(self.user_data)
			f.write(data_str)

	def get_def_user_dict(self):
		return {
			"UID": "nick_name",
			"MOD": 'echo',
			"HELLO": True
		}

	def read_user_json(self):
		file_path = os.path.join(self.dir_path, self.file_name)

		if os.path.exists(file_path):
			with open(file_path, 'r') as f:
				return json.loads(f.read())

		if not os.path.exists(self.dir_path):
			os.makedirs(self.dir_path)

		self.user_data = {
			"META":{},
			"USER":{
				"line_id": self.get_def_user_dict()
			}
		}
		self.save_user_json()
		return self.user_data

	def uid_to_line_id(self, uid):
		for line_id, user_data in self.user_data["USER"].items():
			if user_data["UID"] == uid:
				return line_id
		return None

	def uid_to_mod(self, uid):
		line_id = self.uid_to_line_id(uid)
		if not line_id: return None
		return self.user_data["USER"][line_id]["MOD"]

	def uid_exists(self, uid):
		for line_id, user_data in self.user_data["USER"].items():
			if user_data["UID"] == uid:
				return True
		return False

	def get_self_root_names(self):
		return ['dk']

	def run(self, CMD):
		user_id = CMD.source.user_id
		cmd_str = CMD.message.text

		# 如果是新用戶就幫建立一個新uid
		if user_id not in self.user_data["USER"]:
			idx = 0
			while True:
				new_uid = f"new_user_{idx}"
				if not self.uid_exists(new_uid):
					def_user_dict = self.get_def_user_dict()
					def_user_dict["UID"] = new_uid
					self.user_data["USER"][user_id] = def_user_dict
					self.save_user_json()
					break

				idx += 1

		if "\n" in cmd_str:
			return super().run(CMD)

		if cmd_str[0] == "$" or cmd_str[0] == "＄":
			CMD.message.text = f"% dk : {cmd_str[1:]} %"

		if cmd_str[0] == "!" or cmd_str[0] == "！":
			user_mod = self.user_data["USER"][user_id]["MOD"]
			CMD.message.text = f"% {user_mod} : {cmd_str[1:]} %"

		if cmd_str[0] == "?" or cmd_str[0] == "？":
			user_mod = self.user_data["USER"][user_id]["MOD"]
			CMD.message.text = f"% {user_mod} %\n"
			CMD.message.text += f"help: {cmd_str[1:]}"

		return super().run(CMD)

	def run_sub(self, CMD):

		(is_cmd, return_str) = super().run_sub(CMD)

		# 加入歡迎語句
		user_id = CMD.source.user_id
		if is_cmd and self.user_data["USER"][user_id]["HELLO"]:
			uid = self.user_data["USER"][user_id]["UID"]
			mod = self.user_data["USER"][user_id]["MOD"]
			return_str = f"[{uid} in {mod}]:\n" + return_str

		return (is_cmd, return_str)

	def dk(self, CMD, CmdData):
		(user_id, group_id, root_cmd, user_cmds) = CmdData


		if not root_cmd: return "[提示]請輸入: help"

		root_cmd_list = root_cmd.split()
		main_key = root_cmd_list[0]
		other_keys = root_cmd_list[1:]

		if main_key == "help":
			if len(other_keys) != 0: return "[提示]只要輸入help就好"

			return_str = "[幫助] 加*號的是需要修改的key\n"
			return_str += "$ lid     ： 查看line_id\n"
			return_str += "$ uid *N  ： N=設定用戶名\n"
			return_str += "$ uid     ： 查看當前用戶名\n"
			return_str += "$ mod *M  ： M=要切換的應用\n"
			return_str += "$ mod     ： 查看當前所在應用\n"
			return_str += "$ ls      ： 查看可用應用列表\n"
			return_str += "$ hello   ： 開關歡迎語句\n"
			return_str += "$ upload  ： 上傳用戶資料表\n"
			return_str += "$ download： 更新用戶資料表"
			return return_str

		if main_key == "lid":
			if len(other_keys) != 0: return "[提示] 輸入太多key"
			return user_id

		if main_key == "uid":
			if len(other_keys) > 1: return "[提示] 輸入太多key"
			if len(other_keys) == 0:
				return self.user_data["USER"][user_id]["UID"]

			new_uid = other_keys[0]
			if self.uid_exists(new_uid):
				return f"[提示] uid:{new_uid} 已經存在"

			if user_id not in self.user_data["USER"]:
				return f"[提示] user_id:{user_id} 不存在"

			old_uid = self.user_data["USER"][user_id]["UID"]
			self.user_data["USER"][user_id]["UID"] = new_uid
			return f"[提示] 成功: {old_uid} -> {new_uid}"

		if main_key == "mod":
			if len(other_keys) > 1: return "[提示] 輸入太多key"
			if len(other_keys) == 0:
				return self.user_data["USER"][user_id]["MOD"]

			new_mod = other_keys[0]

			if user_id not in self.user_data["USER"]:
				return f"[提示] user_id:{user_id} 不存在"

			old_mod = self.user_data["USER"][user_id]["MOD"]
			self.user_data["USER"][user_id]["MOD"] = new_mod
			return f"[提示] 成功: {old_mod} -> {new_mod}"

		if main_key == "ls":
			if len(other_keys) != 0: return "[提示] 輸入太多key"
			return "\n".join(["[應用列表]"] + self.get_root_names())

		if main_key == "hello":
			if len(other_keys) != 0: return "[提示] 輸入太多key"
			try:
				old_hello = self.user_data["USER"][user_id]["HELLO"]
				new_hello = not old_hello
				self.user_data["USER"][user_id]["HELLO"] = new_hello
			except Exception:
				return "[提示] 更新失敗\n" + traceback.format_exc()
			return f"[提示] 更新成功: {old_hello} -> {new_hello}"

		if main_key == "upload":
			if len(other_keys) != 0: return "[提示] 輸入太多key"
			try:
				self.save_user_json()
			except Exception:
				return "[提示] 上傳失敗\n" + traceback.format_exc()
			return "[提示] 上傳成功"

		if main_key == "download":
			if len(other_keys) != 0: return "[提示] 輸入太多key"
			try:
				self.user_data = self.read_user_json()
			except Exception:
				return "[提示] 更新失敗\n" + traceback.format_exc()
			return "[提示] 更新成功"

		return "[提示] 未知指令"