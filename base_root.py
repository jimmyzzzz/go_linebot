
def title_cmd_preprocess(title_cmd):
    title_cmd=title_cmd.strip()
    title_cmd=title_cmd.split()
    return title_cmd[2:-1]

def main_cmds_preprocess(main_cmds):
    return [
        tuple(c.strip() for c in cmd.split(':'))
        for cmd in main_cmds if ':' in cmd
    ]

class root_call:
    def __init__(self, root_ref):
        self.root_ref=root_ref
        
    @property
    def var(self):
        return self.root_ref.var_dict
    
    @property
    def index(self): return self.root_ref.run_index

    @index.setter
    def index(self, n):
        self.root_ref.run_index=n

class ROOT_BLK:
    def __init__(self, env_module, title_cmd, main_cmds):
        self.env_module=env_module
        self.title_cmd=title_cmd_preprocess(title_cmd)
        self.main_cmds=main_cmds_preprocess(main_cmds)
        self.run_index=0
        self.var_dict={}
        
    def run(self):
        ret_str=''
        cmds_size=len(self.main_cmds)
        call=root_call(self)
        
        while self.run_index<cmds_size:
            (fn, cmd)=self.main_cmds[self.run_index]
            
            fc=getattr(self.env_module, fn)
            ret=fc(call, cmd)
            if ret: ret_str+=ret
            
            self.run_index+=1
            
        return ret_str