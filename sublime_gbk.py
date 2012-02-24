#coding: utf8

import sublime, sublime_plugin
import os, re
import urllib

TEMP_PATH = os.path.join(os.getcwd(), 'tmp')
SEPERATOR = '                '

def gbk2utf8(view):
	try:
		reg_all = sublime.Region(0, view.size())
		gbk = view.substr(reg_all).encode('gbk')
	except:
		gbk = file(view.file_name()).read()
		text = gbk.decode('gbk')
		
		file_name = view.file_name().encode('utf-8')

		tmp_file_name = urllib.quote_plus(os.path.basename(file_name))  + SEPERATOR + urllib.quote_plus(file_name)
		tmp_file = os.path.join(TEMP_PATH, tmp_file_name)

		f = file(tmp_file, 'w')
		f.write(text.encode('utf8'))
		f.close()

		window = sublime.active_window()
		
		v = window.find_open_file(tmp_file)

		if(not v):
			window.open_file(tmp_file)

		window.focus_view(view)
		window.run_command('close')
		window.focus_view(v)

		sublime.status_message('gbk encoding detected, open with utf8.')

def saveWithEncoding(view, file_name = None, encoding = 'gbk'):
	if(not file_name):
		file_name = view.file_name()
	reg_all = sublime.Region(0, view.size())
	text = view.substr(reg_all).encode(encoding)
	gbk = file(file_name, 'w')
	gbk.write(text)
	gbk.close()	

class EventListener(sublime_plugin.EventListener):
	def on_load(self, view):
		gbk2utf8(view)
	def on_post_save(self, view):
		parts = view.file_name().split(SEPERATOR)
		if(view.file_name().startswith(TEMP_PATH) and len(parts) > 1):
			file_name = urllib.unquote_plus(parts[1].encode('utf-8')).decode('utf-8')
			saveWithEncoding(view, file_name)

class SaveWithGbkCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		file_name = self.view.file_name()

		if(not file_name):
			return

		parts = file_name.split(SEPERATOR)
		if(not file_name.startswith(TEMP_PATH) and len(parts) <= 1):
			saveWithEncoding(self.view)
			sublime.active_window().run_command('close')
			sublime.active_window().open_file(self.view.file_name())
		else:
			sublime.active_window().run_command('save')

class SaveWithUtf8Command(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
	def run(self, edit):
		file_name = self.view.file_name()

		if(not file_name):
			return

		parts = file_name.split(SEPERATOR)

		if(file_name.startswith(TEMP_PATH) and len(parts) > 1):
			file_name = urllib.unquote_plus(parts[1].encode('utf-8')).decode('utf-8')
			saveWithEncoding(self.view, file_name, 'utf-8')
			sublime.active_window().run_command('close')
			sublime.active_window().open_file(file_name)
		else:
			sublime.active_window().run_command('save')