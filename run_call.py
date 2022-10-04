
def root_cmds_preprocess(root_cmd):
	#return [cmd.strip().split() for cmd in root_cmds]
	return root_cmd.strip()

def user_cmds_preprocess(user_cmds):
	return [
		tuple(c.strip() for c in cmd.split(':', 1))
		for cmd in user_cmds if ':' in cmd
	]

class RunCall:

	def __init__(self, root_ref, user_id, root_cmd, user_cmds):
		self.root = root_ref
		self.run_index = 0
		self.return_str_list = []
		self.full_error = True

		self.user_id = user_id
		self.root_cmd = root_cmds_preprocess(root_cmd)
		self.user_cmds = user_cmds_preprocess(user_cmds)

	def __setattr__(self, k, v):
		static_vars = {"root", "return_str_list"}
		static_vars |= {"user_id", "root_cmds", "user_cmds"}
		static_vars |= {"push_str", "get_return"}
		if k == static_vars:
			raise ValueError(f"{k} cannot overloading")
		self.__dict__[k] = v

	def push_str(self, return_str):
		self.return_str_list.append(return_str)

	def get_return(self):
		join_str = ''.join(self.return_str_list)
		ret_str = ''
		backslash = False

		for c in join_str:
			if backslash:
				if c=='n': ret_str+='\n'
				elif c=='t': ret_str+='\t'
				elif c=='\\': ret_str+='\\'
				backslash=False
				continue
			if c=='\\':
				backslash=True
				continue
			ret_str += c

		return ret_str
