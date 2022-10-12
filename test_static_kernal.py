
from init_kernal import InitKernal
import sys
import time

class fake_event:

	def __init__(self, user_id, group_id, txt):
		self.user_id = user_id
		self.group_id = group_id
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
		user_id = self.user_id
		group_id = self.group_id

		class fake_source: pass

		s = fake_source()
		s.__dict__['user_id'] = user_id

		if group_id:
			s.__dict__['type'] = "group"
			s.__dict__['group_id'] = group_id
		else:
			s.__dict__['type'] = "user"

		return s

def file_to_events(file_path):
	with open(file_path, 'r') as f:
		total_block_str = f.read()
		block_list = total_block_str.split('#')

		user_block_list = []
		for block in block_list[1:]:
			cmd_list = block.split('\n')

			info_list = cmd_list[0].split()
			if len(info_list)==1:
				user_id = info_list[0]
				group_id = None
			else:
				user_id = info_list[0]
				group_id = info_list[1]

			cmds = '\n'.join(cmd_list[1:])
			user_block_list.append((user_id, group_id, cmds))

		return [
			fake_event(user_id, group_id, cmds)
			for user_id, group_id, cmds in user_block_list
		]

def run_kernal(kernal, event_list):
	total_return_str = ''
	for event in event_list:
		time_start = time.time()
		is_cmd, kernal_return_str = kernal.run(event)
		time_cost = time.time() - time_start

		run_info = f" user:'{event.source.user_id}' "
		if "group_id" in event.source.__dict__:
			run_info += f" group:'{event.source.group_id}' "
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