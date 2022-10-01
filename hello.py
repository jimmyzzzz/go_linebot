
from template_root import BASE_ROOT
# from env_tool import *


class root(BASE_ROOT):

    def run_start(self):
        cmd = self.root_cmds[0][0]
        self.push_return_str(f"{cmd}\n")

def name(call, cmd):
    call.push_return(f"你好!{cmd}\n")

# @insert_var
# def show(call, cmd):
#     call.push_return(f"{cmd}\n")