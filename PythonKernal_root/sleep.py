
from static_root import BASE_ROOT
from datetime import datetime
from time import sleep

class root(BASE_ROOT):

    def run_start(self, call):

        uid = call.uid
        group_id = call.group_id

        if call.root_cmd:
            sleep_time = int(call.root_cmd)

            call.push_str(f"> {uid}\n")
            if group_id: call.push_str(f"group: {group_id}\n")

            call.push_str('*' * 20 + '\n')

            run_start = datetime.now().strftime('%m/%d %H:%M:%S')
            sleep(sleep_time)
            run_end = datetime.now().strftime('%m/%d %H:%M:%S')

            call.push_str(f"start: {run_start}\n")
            call.push_str(f"end: {run_end}\n")

            call.push_str('*' * 20 )

def help(call, cmd):
    if cmd == "help":
        call.push_str("[幫助] 輸入多少就會暫停多少秒")
        return

    call.push_str("[幫助] 請輸入help")