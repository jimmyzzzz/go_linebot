
from init_kernal import InitKernal
import pickle
import argparse
import os
import sys
import time

class fake_data:
    def __setattr__(self, k, v):
        self.__dict__[k] = v

class fake_event:

    def __init__(self, user_id, group_id, txt):
        self.message = fake_data()
        self.source = fake_data()

        self.message.text = txt

        self.source.user_id = user_id
        if group_id:
            self.source.type = "group"
            self.source.group_id = group_id
        else:
            self.source.type = "user"

def file_to_events(file_path):
    with open(file_path, 'r') as f:
        total_block_str = f.read()
        block_list = total_block_str.split('#')

        # 去除結尾的\n
        block_list = [
            b_str[:-1] for b_str in block_list[:-1]
        ] + [block_list[-1] if block_list[-1][-1]!="\n" else block_list[-1][-1:]]

        user_block_list = []
        for block in block_list[1:]:
            cmd_list = block.split('\n')

            info_list = cmd_list[0].split()
            if len(info_list)==1:
                user_id = info_list[0]
                group_id = None
            else:
                user_id = info_list[0]
                group_id = info_list[1]

            cmds = '\n'.join(cmd_list[1:])
            user_block_list.append((user_id, group_id, cmds))

        return [
            fake_event(user_id, group_id, cmds)
            for user_id, group_id, cmds in user_block_list
        ]

def run_kernal(kernal, event_list):
    for event in event_list:

        user_id = event.source.user_id
        run_info = f" user:'{user_id}' "
        if "group_id" in event.source.__dict__:
            run_info += f" group:'{event.source.group_id}' "

        time_start = time.time()
        is_cmd, kernal_return_str = kernal.run(event)
        time_cost = time.time() - time_start

        run_info += f"is_cmd:{is_cmd} "
        run_info += f"time:{time_cost:.6f}s\n"
        divider = "=" * len(run_info) + '\n'
        return_str = f"{divider}{run_info}{divider}{kernal_return_str}"
        print(return_str)

def run_file(file_path, kernal):
    event_list = file_to_events(file_path)
    run_kernal(kernal, event_list)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("file_path", nargs='+', type=str, help="測試腳本路徑(可以多個)")
    parser.add_argument("-k", type=str, default=None, help="保存與讀取kernal的檔案路徑")

    opt = parser.parse_args()

    if opt.k and os.path.exists(opt.k):
        with open(opt.k, 'rb') as f:
            kernal = pickle.load(f)
    else:
        kernal = InitKernal()

    file_path_list = [opt.file_path] if type(opt.file_path)==str else opt.file_path

    for file_path in file_path_list:
        run_file(file_path, kernal)

    if opt.k:
        with open(opt.k, 'wb') as f:
            pickle.dump(kernal, f)
