
from static_root import BASE_ROOT


class root(BASE_ROOT):

	def run_start(self, call):
		if call.root_cmd:
			call.push_str(f"{call.root_cmd}")


def help(call, cmd):
	if cmd == "help":
		call.push_str("[幫助] echo:輸入什麼就會回傳什麼")
		return

	call.push_str("[幫助] 請輸入help")