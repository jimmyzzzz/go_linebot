
import traceback
from ctypes import CDLL
from ctypes import c_char_p
import os


class sample_c_root_wapper:

    def __init__(self, root_name, root_path):
        self.root_name = root_name
        self.so_module = CDLL(root_path)

    def run(self, user_id, group_id, uid, root_cmd, user_cmds):

        if root_cmd is None:
            root_cmd_str = ""
        elif root_cmd.strip() == "":
            root_cmd_str = " "
        else:
            root_cmd_str = root_cmd.strip()

        user_cmds = '\n'.join(user_cmds)
        run_order = [
            ("get_user_id", user_id),
            ("get_group_id", group_id if group_id else "PERSON_ROOM"),
            ("get_uid", uid if uid else ""),
            ("get_root_cmd", root_cmd_str),
            ("get_user_cmds", user_cmds)
        ]

        ignore_set = {"get_user_id", "get_group_id", "get_uid", "get_root_cmd", "get_user_cmds"}

        (success, return_str) = self.run_cmd_list(run_order, ignore_set)
        return return_str

    def run_cmd_list(self, cmd_list, ignore_set):
        for fn_name, input_str in cmd_list:
            success, return_info = self.fn_call(fn_name, input_str)

            if success: continue
            if fn_name in ignore_set:
                continue
            return (success, f"ERROR[{self.root_name}]: {fn_name} not find")

        (success, return_info) = self.fn_call("root_return", " ")
        return (success, return_info)

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

    def run(self, user_id, group_id, uid, root_cmd, user_cmds):

        if root_cmd is None:
            root_cmd_str = ""
        elif root_cmd.strip() == "":
            root_cmd_str = " "
        else:
            root_cmd_str = root_cmd.strip()

        user_cmds = [
            tuple(c.strip() for c in cmd.split(':', 1))
            for cmd in user_cmds if ':' in cmd
        ]

        run_order = [
            ("get_user_id", user_id),
            ("get_group_id", group_id if group_id else "PERSON_ROOM"),
            ("get_uid", uid if uid else ""),
            ("get_root_cmd", root_cmd_str),
            ("run_start", " "),
            *user_cmds,
            ("run_end", " "),
        ]

        ignore_set = {"get_user_id", "get_group_id", "get_uid", "get_root_cmd", "run_start", "run_end"}

        (success, return_str) = self.run_cmd_list(run_order, ignore_set)
        return return_str