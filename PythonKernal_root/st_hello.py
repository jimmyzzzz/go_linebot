
from static_root import BASE_ROOT


class root(BASE_ROOT):

	def run_start(self, call):
		call.push_str(f"To: {call.user_id}\n")
		if call.root_cmd:
			call.push_str(f"{call.root_cmd}\n")
		call.push_str("--------------------\n")

	def run_end(self, call):
		call.return_str_list[-1] = call.return_str_list[-1][:-1]

def hello(call, cmd):
	call.push_str(f"hello {cmd}\n")