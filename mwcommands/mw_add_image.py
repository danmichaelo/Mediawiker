#!/usr/bin/env python\n
# -*- coding: utf-8 -*-

import sys

import sublime
import sublime_plugin

pythonver = sys.version_info[0]
if pythonver >= 3:
    from . import mw_utils as utils
else:
    import mw_utils as utils


class MediawikerInsertImageCommand(sublime_plugin.WindowCommand):
    ''' alias to Add image command '''

    def run(self):
        if utils.props.get_setting('offline_mode'):
            return

        self.window.run_command(utils.cmd('page'), {"action": utils.cmd('add_image')})


class MediawikerAddImageCommand(sublime_plugin.TextCommand):
    image_prefix_min_lenght = 4
    images_names = []

    def run(self, edit):
        if utils.props.get_setting('offline_mode'):
            return

        self.image_prefix_min_lenght = utils.props.get_setting('image_prefix_min_length', 4)
        sublime.active_window().show_input_panel('Wiki image prefix (min %s):' % self.image_prefix_min_lenght, '', self.show_list, None, None)

    def show_list(self, image_prefix):
        if len(image_prefix) >= self.image_prefix_min_lenght:
            images = utils.api.call('get_pages', prefix=image_prefix, namespace=utils.api.IMAGE_NAMESPACE)  # images list by prefix
            self.images_names = [utils.api.page_attr(x, 'page_title') for x in images]
            sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(self.images_names, self.on_done), 1)
        else:
            sublime.message_dialog('Image prefix length must be more than %s. Operation canceled.' % self.image_prefix_min_lenght)

    def on_done(self, idx):
        if idx >= 0:
            index_of_cursor = self.view.sel()[0].begin()
            self.view.run_command(utils.cmd('insert_text'), {'position': index_of_cursor, 'text': '[[Image:%s]]' % self.images_names[idx]})
