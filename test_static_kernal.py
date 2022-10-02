
from init_kernal import InitKernal
import sys
import time

class fake_event:

	def __init__(self, user_id, txt):
		self.user_id = user_id
		self.txt = txt

	@property
	def message(self):
		txt = self.txt

		class fake_message:
			def __init__(self):
				self.text = txt
		return fake_message()

	@property
	def source(self):
		user_id=self.user_id

		class fake_source:
			def __init__(self):
				self.user_id = user_id
		return fake_source()

def file_to_events(file_path):
	with open(file_path, 'r') as f:
		total_block_str = f.read()
		block_list = total_block_str.split('#')

		user_block_list = []
		for block in block_list[1:]:
			cmd_list = block.split('\n')
			user_id = cmd_list[0].strip()
			cmds = '\n'.join(cmd_list[1:])
			user_block_list.append((user_id, cmds))

		return [
			fake_event(user_id, cmds)
			for user_id, cmds in user_block_list
		]

def run_kernal(kernal, event_list):
	total_return_str = ''
	for event in event_list:
		time_start = time.time()
		is_cmd, kernal_return_str = kernal.run(event)
		time_cost = time.time() - time_start

		run_info = f" user:'{event.source.user_id}' "
		run_info += f"is_cmd:{is_cmd} "
		run_info += f"time:{time_cost:.6f}s\n"
		divider = "=" * len(run_info) + '\n'
		return_str = f"{divider}{run_info}{divider}{kernal_return_str}\n"
		total_return_str += return_str

	return total_return_str

def run_file(file_path):
	kernal = InitKernal()

	event_list = file_to_events(file_path)
	return run_kernal(kernal, event_list)

if __name__ == '__main__':
	for file_name in sys.argv[1:]:
		print(run_file(file_name))