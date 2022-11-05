

from kernal import HalfKernal

too_many_key_error = "[提示] 太多指令！"

class ShortCallKernal(HalfKernal):

	def get_self_root_names(self):
		return ['uid', 'gid', 'py']

	def uid(self, CMD, CmdData):
		(user_id, group_id, root_cmd, user_cmds) = CmdData
		if root_cmd.strip(): return too_many_key_error
		return user_id

	def gid(self, CMD, CmdData):
		(user_id, group_id, root_cmd, user_cmds) = CmdData
		if root_cmd.strip(): return too_many_key_error
		return user_id

	def py(self, CMD, CmdData):
		(user_id, group_id, root_cmd, user_cmds) = CmdData
		return str(eval(root_cmd))
