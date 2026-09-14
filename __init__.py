import os
import webbrowser
import tempfile
from pathlib import Path
from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

class Command:
	def __init__(self):
		return

	def run(self):
		fn = Path(tempfile.mkdtemp()) / os.path.basename(ed.get_filename() + '.txt')
		if not fn:
			msg_box(_('Cannot preview untitled tab'), MB_OK)
			return

		text = ed.get_text_sel() if ed.get_text_sel() else ed.get_text_all()
		code = ''
		i = 0
		for line in text.splitlines():
			i = i + 1
			code += '[' + str(i) + ']' + "\t" + line + "\n"
		with open(fn, 'w') as f:
			f.write(code)

		if not os.path.isfile(fn):
			msg_status(_('Cannot open file: ')+fn)
			return

		webbrowser.open_new_tab(str(fn))
		msg_box(_("This code is open in the browser.\nPress Ctrl+P there to print."), MB_OK)
