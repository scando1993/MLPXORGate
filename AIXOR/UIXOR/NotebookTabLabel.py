import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NotebookTabLabel:
    def __init__(self, title, notebook, child):
        self.content = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
        self.label = Gtk.Label(title)
        close_button = Gtk.Button()
        close_image = Gtk.Image()
        self.notebook = notebook
        self.notebook_child = child

        close_image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)

        close_button.set_image(close_image)
        close_button.set_relief(Gtk.ReliefStyle.NONE)
        close_button.connect('clicked',self.close_cb)

        self.content.pack_start(self.label, expand=True, fill=True, padding=0)
        self.content.pack_end(close_button, expand=False, fill=False, padding=0)
        self.content.show_all()

    def close_cb(self, button):
        index = self.notebook.page_num(self.notebook_child)
        self.notebook.remove_page(index)
        self.notebook.queue_draw()
