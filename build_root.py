
import importlib
import template_root
import os

def read_build_cmd(user_id, build_cmd, root_cmds, user_cmds):

	build_cmd_list = build_cmd.split()
	(env_name, options) = (build_cmd_list[0], build_cmd_list[1:])

	env_module = importlib.import_module(env_name)

	if options: raise ValueError('尚未開放 build options')

	if issubclass(env_module.root, template_root.IO_ROOT):
		path_head = os.path.join('data', env_name)
		fp_list = []

		class io_call:
			def open_file(self, path, mode='r'):
				fp = open(os.path.join(path_head, path))
				fp_list.append(fp)
				return fp

			def listdir(self, path):
				return os.listdir(os.path.join(path_head, path))

			def isfile(self, path):
				return os.path.isfile(os.path.join(path_head, path))

			def exists(path):
				return os.path.exists(os.path.join(path_head, path))

			def makedirs(self, path):
				os.makedirs(os.path.join(path_head, path))

			def close(self):
				for i in range(len(fp_list)):
					fp_list.pop().close()

		return env_module.root(
			kernal_call=io_call(),
			user_id=user_id,
			env_module=env_module,
			root_cmds=root_cmds,
			user_cmds=user_cmds
		)

	return env_module.root(
		user_id=user_id,
		env_module=env_module,
		root_cmds=root_cmds,
		user_cmds=user_cmds
	)