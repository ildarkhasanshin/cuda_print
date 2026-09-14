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
		text = ed.get_text_sel() if ed.get_text_sel() else ed.get_text_all()

		suffix_txt = '.txt'
		if ed.get_filename().endswith(suffix_txt):
			text_print = text
			fn_ = os.path.basename(ed.get_filename())
		else:
			text_ = ''
			i = 0
			for line in text.splitlines():
				i = i + 1
				text_ += '[' + str(i) + ']' + "\t" + line + "\n"
			text_print = text_
			fn_ = os.path.basename(ed.get_filename() + suffix_txt)

		fn = Path(tempfile.mkdtemp()) / fn_
		if not fn:
			msg_box(_('Cannot preview untitled tab'), MB_OK)
			return

		with open(fn, 'w') as f:
			f.write(text_print)

		if not os.path.isfile(fn):
			msg_status(_('Cannot open file: ')+fn)
			return

		webbrowser.open_new_tab(str(fn))
		msg_box(_("Text is open via the browser.\nPress Ctrl+P there to print."), MB_OK)
