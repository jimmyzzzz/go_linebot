
from kernal import KERNAL
from dollar_kernal import DollarKernal
from python_kernal import PythonKernal
from short_call_kernal import ShortCallKernal
from c_kernal import CKernal
import traceback


class InitKernal(KERNAL):

	def __init__(self):
		super().__init__(sub_kernals=[
			DollarKernal(
				dir_name='DollarKernal_data', file_name='user_data.json',
				sub_kernals=[
					PythonKernal(root_dir="PythonKernal_root"),
					CKernal(root_dir="CKernal_root"),
					ShortCallKernal()
				]
			),
		])

	def run(self, CMD):
		cmd_str = CMD.message.text
		if cmd_str[0] not in {'%', '$', '!', '?'}:
			return (False, None)

		try:
			return super().run(CMD)
		except Exception as error:
			return (True, traceback.format_exc())