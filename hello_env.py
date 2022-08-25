
from base_root import ROOT_BLK
from base_env import *

# 檔案中必須編寫一個叫root_blk的類
# 該類繼承 base_class.ROOT_BLK
class root_blk(ROOT_BLK):
	def __init__(self, *argc, **kwargc):
		super().__init__(*argc, **kwargc)

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

