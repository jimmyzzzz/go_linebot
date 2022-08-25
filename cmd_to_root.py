import importlib

def load_env_module(first_line):
	first_line=first_line.replace('%', ' % ')
	first_line_list=first_line.split()
	
	env=first_line_list[1]
	env_module=importlib.import_module(env)
	return env_module

def is_command(cmd_str):
	if cmd_str[0]!='%': return False
	
	finded_percentage=False
	for c in cmd_str[1:]:
		if finded_percentage:
			# c should be '\n' or ' '
			if c=='\n': return True
			if c!=' ': return False
			
		else:
			# c should not be '\n'
			# if not finded '%'
			if c=='\n': return False
			if c=='%':
				finded_percentage=True
				continue 
			
	return False

def file_to_root(path):
	with open(path,'r') as f:
		first_line = f.readline()

		if not is_command(first_line): return

		env_module = load_env_module(first_line)

		root_cmd = first_line
		main_cmds = f.readlines()
		root=env_module.root_blk(
			env_module=env_module,
			root_cmd=root_cmd,
			main_cmds=main_cmds
		)

		print(root.run())

def str_to_root(cmd_str):
	if not is_command(cmd_str): return

	cmds=cmd_str.split('\n')
	root_cmd=cmds[0]
	main_cmds=cmds[1:]
	
	env_module=load_env_module(root_cmd)
	root=env_module.root_blk(
		env_module=env_module,
		root_cmd=root_cmd,
		main_cmds=main_cmds
	)

	return root.run()

def cmds_portal(cmd_str):
	try:
		return_str=str_to_root(cmd_str)
		if return_str: return (True, return_str)
		return (False, return_str)

	except Exception as er:
		error_message='='*2+'\n'
		error_message+=f"Error[-1] at ROOT_BLK:\n{er}"
		return (True, error_message)
	
def file_portal(path):
	with open(path,'r') as f:
		cmd_str=f.read()
		return cmds_portal(cmd_str)