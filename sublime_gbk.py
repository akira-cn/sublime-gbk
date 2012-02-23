import sublime, sublime_plugin

def gbk2utf8(view):
	try:
		reg_all = sublime.Region(0, view.size())
		gbk = view.substr(reg_all).encode('gbk')
	except:
		gbk = file(view.file_name()).read()
		text = gbk.decode('gbk')
		view.settings().set('encoding', 'gbk')
		edit = view.begin_edit()
		view.replace(edit, reg_all, text)
		view.end_edit(edit)
		view.set_encoding('utf-8')
		sublime.status_message('gbk encoding detected, open with utf8.')

def saveAsGbk(view):
	reg_all = sublime.Region(0, view.size())
	text = view.substr(reg_all).encode('gbk')
	gbk = file(view.file_name(), 'w')
	gbk.write(text)
	gbk.close()	

class EventListener(sublime_plugin.EventListener):
	def on_modified(self, view):
		if(view.settings().get('user_deactivated')):
			gbk2utf8(view)
	def on_deactivated(self, view):
		view.settings().set('user_deactivated', True)
	def on_load(self, view):
		gbk2utf8(view)
	def on_post_save(self, view):
		if(view.settings().get('encoding') == 'gbk'):
			saveAsGbk(view)


class SaveAsGbkCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		self.view.settings().set('encoding', 'gbk')
		sublime.active_window().run_command('save')

class SaveAsUtf8Command(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		self.view.settings().set('encoding', None)
		sublime.active_window().run_command('save')