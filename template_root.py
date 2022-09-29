
import traceback

class base_root_call:
	def __init__(self, root_ref, self_index):
		self.root_ref=root_ref
		self.self_index=self_index

	@property
	def var(self):
		return self.root_ref.var_dict

	@property
	def run_index(self): return self.root_ref.run_index

	@run_index.setter
	def run_index(self, n):
		self.root_ref.run_index=n

	@property
	def cmds(self):
		return self.root_ref.user_cmds

	def push_mail(self, index, content):
		self.root_ref.mail_dict[index][self.self_index]=content

	def pull_mail(self):
		return self.root_ref.mail_dict[index]

	def push_return(self, new_str):
		self.root_ref.push_return_str(new_str)


class BASE_ROOT:

	@classmethod
	def root_cmds_preprocess(cls, root_cmds):
		# list: root_cmds
		return [cmd.strip().split() for cmd in root_cmds]

	@classmethod
	def user_cmds_preprocess(cls, user_cmds):
		return [
			tuple(c.strip() for c in cmd.split(':'))
			for cmd in user_cmds if ':' in cmd
		]

	def __init__(self, user_id, env_module, root_cmds, user_cmds):
		self.user_id=user_id
		self.env_module=env_module
		self.root_cmds=BASE_ROOT.root_cmds_preprocess(root_cmds)
		self.user_cmds=BASE_ROOT.user_cmds_preprocess(user_cmds)

		self.return_str_list=[]
		self.run_index=0
		self.var_dict={}
		self.mail_dict={}

	def run_start(self): pass
	def run_end(self): pass
	def run_error(self): pass
	def close(self): pass

	def new_call(self):
		return base_root_call(self, self.run_index)

	def run_cmd(self, call, fn_name, fn_cmd):
		fn = getattr(self.env_module, fn_name)
		return fn(call, fn_cmd)

	def push_return_str(self, new_str):
		self.return_str_list.append(new_str)

	def return_str(self):
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

	def run(self):

		run_start_ret = self.run_start()

		cmds_num=len(self.user_cmds)
		while self.run_index < cmds_num:
			real_index = self.run_index
			call = self.new_call()
			(fn_name, fn_cmd) = self.user_cmds[self.run_index]

			try:
				ret = self.run_cmd(call, fn_name, fn_cmd)

			except Exception as err:
				error_message = '='*20+'\n'
				error_message += f'Error[{real_index}] '
				error_message += f'at {fn_name}:{fn_cmd}\n'
				error_message += traceback.format_exc()
				error_message += '='*20+'\n'
				self.push_return_str(error_message)

				run_error_ret = self.run_error()
				return self.return_str()

			self.run_index+=1

		run_end_ret = self.run_end()
		return self.return_str()

class io_root_call(base_root_call):
	def __init__(self, io_call, root_ref, self_index):
		super().__init__(root_ref, self_index)
		self.io = io_call

class IO_ROOT(BASE_ROOT):

	def __init__(self, kernal_call, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.kernal_call=kernal_call

		if not self.kernal_call.exists(''):
			self.kernal_call.makedirs('')

	def new_call(self):
		return io_root_call(
			self.kernal_call, self, self.run_index
		)

	def close(self):
		self.kernal_call.close()

