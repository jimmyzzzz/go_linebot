

from kernal import HalfKernal

too_many_key_error = "[提示] 太多指令！"

class ShortCallKernal(HalfKernal):

    def get_self_root_names(self):
        return ['lid', 'uid', 'gid', 'py']

    def lid(self, CMD, CmdData):
        (user_id, group_id, root_cmd, user_cmds) = CmdData
        if root_cmd is not None: return too_many_key_error
        return user_id

    def uid(self, CMD, CmdData):
        (user_id, group_id, root_cmd, user_cmds) = CmdData
        if root_cmd is not None: return too_many_key_error

        success, uid = self.init_kernal_ref.pipe("get_uid", line_id=user_id)
        if success:
            return uid
        return "UNKNOW"

    def gid(self, CMD, CmdData):
        (user_id, group_id, root_cmd, user_cmds) = CmdData
        if root_cmd is not None: return too_many_key_error
        return group_id

    def py(self, CMD, CmdData):
        (user_id, group_id, root_cmd, user_cmds) = CmdData

        def run_CMD(root_cmd):
            HalfKernal = "HalfKernal"
            return str(eval(root_cmd))

        return run_CMD(root_cmd)
