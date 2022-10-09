
import traceback


class BASE_ROOT:

    def __init__(self, root_module):
        self.root_module = root_module

    def run(self, run_call):

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
