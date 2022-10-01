
import traceback

def root_cmds_preprocess(root_cmds):
	return [cmd.strip().split() for cmd in root_cmds]

def user_cmds_preprocess(user_cmds):
	return [
		tuple(c.strip() for c in cmd.split(':'))
		for cmd in user_cmds if ':' in cmd
	]

class RunCall:

	def __init__(self, root_ref, user_id, root_cmds, user_cmds):
		self.root = root_ref
		self.run_index = 0
		self.return_str_list = []
		self.full_error = True

		self.user_id = user_id
		self.root_cmds = root_cmds_preprocess(root_cmds)
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

class BASE_ROOT:

	def __init__(self, root_module):
		self.root_module = root_module

	def run(self, user_id, root_cmds, user_cmds):
		run_call = RunCall(self, user_id, root_cmds, user_cmds)

		self.run_start(run_call)

		cmds_num = len(run_call.user_cmds)
		while run_call.run_index < cmds_num:
			real_index = run_call.run_index

			(fn_name, fn_cmd) = run_call.user_cmds[run_call.run_index]

			try:
				self.run_cmd(run_call, fn_name, fn_cmd)

			except Exception as error:

				error_message = '=' * 20 + '\n'
				error_message += f'Error[{real_index}] '
				error_message += f'at {fn_name}: {fn_cmd}\n'

				if run_call.full_error:
					error_message += traceback.format_exc()
				else:
					error_message += error

				error_message += '=' * 20 + '\n'
				run_call.push_str(error_message)

				self.run_error(run_call)
				return run_call.get_return()

			run_call.run_index += 1

		self.run_end(run_call)
		return run_call.get_return()

	def run_cmd(self, run_call, fn_name, fn_cmd):
		fn = getattr(self.root_module, fn_name)
		return fn(run_call, fn_cmd)

	def run_start(self, run_call): pass
	def run_end(self, run_call): pass
	def run_error(self, run_call): pass


class IO_ROOT(BASE_ROOT):
	pass