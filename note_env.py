
from template_root import IO_ROOT
from env_tool import *

class root(IO_ROOT):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = self.root_cmds[0][0]

        if not self.kernal_call.exists(self.path):
            print(f'mkdir: {self.path}')
            self.kernal_call.makedirs(self.path)

    def run(self):
        title_str = f'save to {self.path}\n'
        return title_str + super().run()


@insert_var
def fname(call, cmd):
    call.var['fname']=cmd

@insert_var
def note(call, cmd):
    my_path = call.root_ref.path
    file_path = my_path + '/' + call.var['fname']

    fp = call.io.open_file(file_path, mode='a+')

    if cmd[0] == '"': cmd = cmd[1:]
    if cmd[-1] == '"': cmd = cmd[:-1]

    print(cmd, file=fp)
