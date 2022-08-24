
def setv(call, cmd):
    s_list=cmd.split()
    for s in s_list:
        k,v=s.split('=')
        call.var[k]=v

def show(call, cmd):
    cmd=cmd.strip()
    cmd=cmd.replace('"','')
    
    ret_str=''
    var_str=''
    reading_var=False
    for c in cmd:
        if reading_var:
            if c=='}':
                ret_str+=str(call.var[var_str])
                reading_var=False
                var_str=''
            else:
                var_str+=c
        else:
            if c=='{': reading_var=True
            else: ret_str+=c
            
    return ret_str