import importlib

def load_env_module(first_line):
	first_line_list=first_line.split()
	env=first_line_list[1]
	env_module=importlib.import_module(env)
	return env_module

def is_command(cmd_str):
	if cmd_str[0]!='%': return False
	for c in cmd_str[1:]:
		if c=='%': return True
		if c=='\n': return False
	return False

def file_to_root(path):
	with open(path,'r') as f:
		first_line = f.readline()

		if not is_command(first_line): return

		env_module = load_env_module(first_line)

		title_cmd = first_line
		main_cmds = f.readlines()
		root=env_module.root_blk(
			env_module=env_module,
			title_cmd=title_cmd,
			main_cmds=main_cmds
		)

		print(root.run())

def str_to_root(cmd_str):
	if not is_command(cmd_str): return

	cmds=cmd_str.split('\n')
	env_cmd=cmds[0]
	main_cmds=cmds[1:]

	env_module=load_env_module(env_cmd)
	root=env_module.root_blk(
		env_module=env_module,
		title_cmd=env_cmd,
		main_cmds=main_cmds
	)

	return root.run()

def cmds_portal(cmd_str):
	try:
		return_str=str_to_root(cmd_str)
		if return_str: return (True, return_str)
		return (False, return_str)

	except Exception as er:
		error_m=f"Error:\n{er}"
		return (True, error_m)