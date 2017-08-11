import gi,sys,os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from NotebookTabLabel import NotebookTabLabel
from Constants import UI_FILE


class MLPNotebook(Gtk.Notebook):
    def __new__(cls, *args, **kwargs):
        file_path = os.path.dirname(__file__)
        try:
            builder = Gtk.Builder()
            builder.add_from_file(os.path.join(file_path, UI_FILE))
        except:
            print "Failed to load XML GUI file" + UI_FILE
            sys.exit(1)

        new_object = builder.get_object('MLPNotebook')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        builder = Gtk.Builder.new_from_file(UI_FILE)
        builder.connect_signals(self)

    def add_tab(self, content):
        pages = self.notebook.get_n_pages()
        label = "MLP #" + str(pages + 1)
        tab = NotebookTabLabel(label, self.notebook, pages + 1)
        self.notebook.append_page(content, tab.header)

    def on_btn_add_tab_clicked(self, button):
        self.add_tab(Gtk.Label(label= "test"))

