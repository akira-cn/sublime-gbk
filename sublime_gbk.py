#coding: utf8

import sublime, sublime_plugin
import os, re

def gbk2utf8(view):
    try:
        reg_all = sublime.Region(0, view.size())
        gbk = view.substr(reg_all).encode('gbk')
    except:
        gbk = file(view.file_name()).read()
        text = gbk.decode('gbk')

        tmp_file = u"%s.dump"%view.file_name()
        f = file(tmp_file, 'w')
        f.write(text.encode('utf8'))
        f.close()

        window = sublime.active_window()
        
        tmp_view = window.open_file(tmp_file)

        if not tmp_view:
            tmp_view = window.open_file(tmp_file)
        
        tmp_view.set_syntax_file(view.settings().get('syntax'))
        window.focus_view(view)
        window.run_command('close')
        window.focus_view(tmp_view)
        sublime.status_message('gbk encoding detected, open with utf8.')

def saveWithEncoding(view, file_name = None, encoding = 'gbk'):
    if not file_name:
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
        if ".dump" in view.file_name():
            file_name = view.file_name()[:-5]
            saveWithEncoding(view, file_name)

    def on_close(self,view):
        if ".dump" in view.file_name():
            os.remove(view.file_name())


class SaveWithGbkCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
    def run(self, edit):
        file_name = self.view.file_name()

        if(not file_name):
            return

        if ".dump" not in self.view.file_name():
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

        if ".dump" in self.view.file_name():
            file_name = self.view.file_name()[:-5]
            saveWithEncoding(self.view, file_name, 'utf-8')
            sublime.active_window().run_command('close')
            sublime.active_window().open_file(file_name)
        else:
            sublime.active_window().run_command('save')