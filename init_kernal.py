
from kernal import KERNAL
from python_kernal import PythonKernal
from c_kernal import CKernal
import traceback


class InitKernal(KERNAL):

	def __init__(self):
		super().__init__(sub_kernals=[
			PythonKernal(root_dir="PythonKernal_root"),
			CKernal(root_dir="CKernal_root")
		])

	def run(self, CMD):
		try:
			return super().run(CMD)
		except Exception as error:
			return traceback.format_exc()