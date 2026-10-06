import os
import webbrowser
import tempfile
from pathlib import Path
import plistlib
import subprocess
import sys
from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

class Command:
	def __init__(self):
		return

	def check_firefox(self):
		import subprocess
		try:
			output = subprocess.check_output(['firefox', '--version'])
		except:
			output = False

		return output

	def get_default_browser(self):
		system = sys.platform
		if system == "win32":
			try:
				import winreg
				path = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice"
				with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
					prog_id, _ = winreg.QueryValueEx(key, "ProgId")
				cmd_path = f"{prog_id}\\shell\\open\\command"
				with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, cmd_path) as command_key:
					command, _ = winreg.QueryValueEx(command_key, "")
				if command.startswith('"'):
					browser_exe = command.split('"')[1]
				else:
					browser_exe = command.split()[0]
				return os.path.basename(browser_exe).replace(".exe", "").lower()
			except Exception:
				return "unknown_windows_browser"
		elif system.startswith("linux"):
			try:
				result = subprocess.check_output(
					["xdg-settings", "get", "default-web-browser"],
					text=True,
					stderr=subprocess.DEVNULL,
				)
				browser = result.strip().split(".")[0]
				return browser.lower()
			except Exception:
				return os.environ.get("BROWSER", "unknown_linux_browser")
		elif system == "darwin":
			try:
				plist_path = os.path.expanduser(
					"~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist"
				)
				if os.path.exists(plist_path):
					with open(plist_path, "rb") as f:
						plist_data = plistlib.load(f)
					for handler in plist_data.get("LSHandlers", []):
						if handler.get("LSHandlerURLScheme") == "https":
							bundle_id = handler.get(
								"LSHandlerRoleAll", handler.get("LSHandlerRoleViewer")
							)
							if bundle_id:
								return bundle_id.split(".")[-1].lower()
				return "safari"
			except Exception:
				return "safari"

		return "unknown_os"

	def run(self):
		text = ed.get_text_sel() if ed.get_text_sel() else ed.get_text_all()

		suffix_txt = '.txt'
		edfn = ed.get_prop(PROP_FN)
		if edfn.endswith(suffix_txt):
			text_print = text
			fn_ = os.path.basename(edfn)
		else:
			text_ = ''
			i = 0
			for line in text.splitlines():
				i = i + 1
				text_ += '[' + str(i) + ']' + "\t" + line + "\n"
			text_print = text_
			fn_ = os.path.basename(edfn + suffix_txt)

		if 'firefox' in self.get_default_browser():
			fn = Path.home() / Path('cuda_print')
			fn.mkdir(parents=True, exist_ok=True)
			fn = fn / fn_
		else:
			fn = Path(tempfile.mkdtemp()) / fn_

		if not fn:
			msg_box(_('Cannot preview untitled tab'), MB_OK)
			return

		with open(fn, 'w', encoding='utf-8') as f:
			f.write(text_print)

		if not os.path.isfile(fn):
			msg_status(_('Cannot open file: ') + fn)
			return

		webbrowser.open_new_tab(str(fn))
		msg_box(_("Text is open via the browser.\nPress Ctrl+P there to print."), MB_OK)
