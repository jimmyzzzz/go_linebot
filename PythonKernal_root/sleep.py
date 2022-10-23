
from static_root import BASE_ROOT
from datetime import datetime
from time import sleep

class root(BASE_ROOT):

	def run_start(self, call):

		user_id = call.user_id
		group_id = call.group_id
		sleep_time = int(call.root_cmd) if call.root_cmd else 0

		call.push_str(f"> {user_id}\n")
		if group_id: call.push_str(f"group: {group_id}\n")

		call.push_str('*' * 20 + '\n')

		run_start = datetime.now().strftime('%m/%d %H:%M:%S')
		sleep(sleep_time)
		run_end = datetime.now().strftime('%m/%d %H:%M:%S')

		call.push_str(f"start: {run_start}\n")
		call.push_str(f"end: {run_end}\n")

		call.push_str('*' * 20 )