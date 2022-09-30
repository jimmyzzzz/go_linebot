
from template_root import BASE_ROOT

class root(BASE_ROOT):
    def run_start(self):
        self.push_return_str(f"hello {self.user_id}\n")

    def run_end(self):
        self.push_return_str(f"bye {self.user_id}\n")
        print(list(self.return_str()))

    def run_error(self):
        self.push_return_str(f"sorry {self.user_id}\n")

def insert_var(fn):
    def wrap(call, cmd):
        new_cmd = ''
        var_name = ''
        inserting = False
        for c in cmd:
            if inserting:
                if not c == '}': var_name += c; continue
                new_cmd += call.var[var_name]
                (var_name, inserting) = ('', False)

            else:
                if not c == '{': new_cmd += c; continue
                if new_cmd[-1] == '\\':
                    new_cmd = new_cmd[:-1] + c; continue
                inserting = True

        return fn(call, new_cmd)
    return wrap

@insert_var
def say(call, cmd):
    call.push_return(cmd)

@insert_var
def sayl(call, cmd):
    call.push_return(cmd+'\n')

@insert_var
def let(call, cmd):
    wlist = cmd.split()
    for w in wlist:
        k, v = w.split('=')
        call.var[k] = v
