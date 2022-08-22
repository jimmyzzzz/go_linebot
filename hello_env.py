
from base_class import ROOT_BLK

# 檔案中必須編寫一個叫root_blk的類
# 該類繼承 base_class.ROOT_BLK
class root_blk(ROOT_BLK):
    def __init__(self, *argc, **kwargc):
        super().__init__(*argc, **kwargc)
        print('環境參數: ', self.title_cmd)

# 可以編寫自由編寫函數，回傳值會顯示出來
# call: 系統呼叫(設定變數or迴圈)
# cmd: 使用者傳入指令
def say(call, cmd):
    return '大聲說: ' + cmd + '\n'

# 不做事，可以用來作註釋
def note(call, cmd):
    pass

# 可以調整運行指針來達到goto的效果
def pass_n(call, cmd):
    n=int(cmd)
    call.index+=n 
    
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