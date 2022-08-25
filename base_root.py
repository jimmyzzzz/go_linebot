
def root_cmd_preprocess(root_cmd):
	root_cmd=root_cmd.strip()
	root_cmd=root_cmd.split()
	return root_cmd[2:-1]

def main_cmds_preprocess(main_cmds):
	return [
		tuple(c.strip() for c in cmd.split(':'))
		for cmd in main_cmds if ':' in cmd
	]

class root_call:
	def __init__(self, root_ref):
		self.__root_ref=root_ref

	@property
	def var(self):
		return self.__root_ref.var_dict

	@property
	def mail(self):
		return self.__root_ref.mail_dict

	@property
	def index(self): return self.__root_ref.run_index

	@index.setter
	def index(self, n):
		self.__root_ref.run_index=n

class ROOT_BLK:
	def __init__(self, env_module, root_cmd, main_cmds):
		self.env_module=env_module
		self.root_cmd=root_cmd_preprocess(root_cmd)
		self.main_cmds=main_cmds_preprocess(main_cmds)
		self.run_index=0
		self.var_dict={}
		self.mail_dict={}
		self.call=root_call(self)

	def run(self):
		ret_str=''
		cmds_size=len(self.main_cmds)

		while self.run_index<cmds_size:
			real_idx=self.run_index
			(fn, cmd)=self.main_cmds[self.run_index]
			
			try:
				fc=getattr(self.env_module, fn)
				ret=fc(self.call, cmd)
			except Exception as err:
				error_message='='*20+'\n'
				error_message+=f'Error[{real_idx}] at {fn}:{cmd}\n{err}'
				ret_str+=error_message
				break
			else:
				if ret: ret_str+=ret

			self.run_index+=1

		return ret_str

class IO_call(root_call):
	def get_file_fp(self, path, mode='r'):
		full_path=self.__root_ref.path_head+path
		f_pointer=open(full_path, mode=mode)
		self.__root_ref.f_pointer_list.append(f_pointer)
		return f_pointer

class IO_ROOT(ROOT_BLK):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		env_name=self.env_module.__name__
		self.path_head=f'./data/{env_name}/'
		self.f_pointer_list=[]
		
		self.call=IO_call(self)
		
	def run(self):
		ret=super().run()
		[fp.close() for fp in self.f_pointer_list]
		return ret