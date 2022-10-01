
from static_root import BASE_ROOT


class root(BASE_ROOT):

	def run_start(self, call):
		call.push_str(f"To: {call.user_id}\n")

		if call.root_cmds:
			root_args = ' '.join(call.root_cmds[0])
			call.push_str(f"{root_args}\n")

		call.push_str("--------------------\n")


def hello(call, cmd):
	call.push_str(f"hello {cmd}\n")