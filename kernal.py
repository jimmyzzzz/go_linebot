
import traceback
import build_root

def is_command(event):
	
	cmd_str = event.message.text
	if cmd_str[0]!='%': return False
	
	finded_percentage=False
	for c in cmd_str[1:]:
		if finded_percentage:
			if c=='\n': return True
			if c!=' ': return False
		else:
			if c=='\n': return False
			if c=='%': finded_percentage=True; continue
	
	if finded_percentage: return True
	return False


def get_root(event):
	
	cmd_str = event.message.text
	user_id = event.source.user_id
	
	cmd_line = cmd_str.split('\n')
	(first_cmd, user_cmds) = (cmd_line[0], cmd_line[1:])
	
	first_cmd = first_cmd.replace('%', '')
	first_cmd_list = first_cmd.split(':')
	(build_cmd, root_cmds) = (first_cmd_list[0], first_cmd_list[1:])
	
	root = build_root.read_build_cmd(
		user_id=user_id,
		build_cmd=build_cmd,
		root_cmds=root_cmds,
		user_cmds=user_cmds
	)
	return root

def read_cmd(event):
	try:
		if not is_command(event):
			return (False, None)
		
		root = get_root(event)
		print_str = root.run()
		root.close()
		return (True, print_str)
	
	except Exception:
		error_message = traceback.format_exc()
		return (True, error_message)

class fake_event:
	def __init__(self, txt):
		self.txt = txt
		self.user_id = 123
	
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
	
def read_file(path):
	with open(path,'r') as f:
		cmd_str = f.read()
		event = fake_event(cmd_str)
		return read_cmd(event)
