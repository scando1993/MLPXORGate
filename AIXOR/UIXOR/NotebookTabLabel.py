import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NotebookTabLabel(Gtk.HBox):
    def __init__(self, title, notebook, page_num):
        super(Gtk.HBox,self)
        self.label = Gtk.Label(title)
        self.close_button = Gtk.Button()
        self.close_image = Gtk.Image()
        self.page_num = page_num
        self.notebook = notebook

        self.close_image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)

        self.close_button.set_image(self.close_image)
        self.close_button.set_relief(Gtk.ReliefStyle.NONE)
        self.close_button.connect('clicked',self.close_cb)

        self.pack_start(self.label, expand=True, fill=True, padding=0)
        self.pack_end(self.close_button, expand=False, fill=False, padding=0)
        self.show_all()

    def close_cb(self, button):
        self.notebook.remove_page(self.page_num)
