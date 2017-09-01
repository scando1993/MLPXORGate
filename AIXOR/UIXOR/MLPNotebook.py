import gi,sys,os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio
from NotebookTabLabel import NotebookTabLabel
from .MLPNotebookContent import MLPNotebookContent
from Constants import MLPNOTEBOOK_FILE
from ..Utils import GtkTemplate

mlp_content_array = {}

class MLPNotebook:

    def __init__(self):
        file_path = os.path.dirname(__file__)
        try:
            builder = Gtk.Builder()
            builder.add_from_file(os.path.join(file_path, MLPNOTEBOOK_FILE))

        except Exception as e:
            print e
            sys.exit(1)

        builder.connect_signals(self)

        self.content = builder.get_object("MLPNotebook")

        self.pop_over_menu_tabs = builder.get_object("popOverTabs")

        self.btn_select_tabs = builder.get_object("btnSelectTabs")
        self.btn_add_tab = builder.get_object("btnAddTab")

        self.initial_radio_button = None

        self.page_counter = 0
        self.tabs = []
        self.mlp_content_array = []

        self.content.show_all()

    def add_notebook_content(self):
        self.page_counter += 1

        label = "Untitled #" + str(self.page_counter)

        content = MLPNotebookContent()
        self.mlp_content_array.append(content)

        widget = content.contents
        self.add_notebook_page(label=label,widget=widget)

    def add_notebook_page(self, widget, label):
        tab = NotebookTabLabel(label, self.content, widget)

        self.content.append_page(widget, tab.content)

        self.tabs.append(tab)

        self.content.queue_draw()

    def on_MLPNotebook_page_added(self, notebook, child, pag_num):
        # string = "Page " + str(pag_num + 1)
        # # self.pop_over_g_menu.append(string, None)
        # self.pop_over_g_menu.insert(pag_num,string,None)
        pass

    def on_MLPNotebook_page_removed(self, notebook, child, page_num):
        if self.content.get_n_pages() == 1:
            self.content.set_show_tabs(False)

        del self.mlp_content_array[page_num]

    def on_btnSelectTabs_toggled(self, button):
        if len(self.pop_over_menu_tabs.get_children()) > 0:
            self.pop_over_menu_tabs.remove(self.pop_over_menu_tabs.get_children()[0])

        box = Gtk.Box().new(Gtk.Orientation.VERTICAL, 0)
        self.pop_over_menu_tabs.add(box)

        tab = self.content.get_tab_label(self.content.get_nth_page(0))
        label = get_label_from_tab(tab)
        radio = Gtk.RadioButton().new_with_label(None, label.get_text())
        radio.connect('toggled',self.on_radio_btn_clicked,0)
        box.pack_start(radio, True, False, 0)

        for i in range(1, self.content.get_n_pages()):
            tab = self.content.get_tab_label(self.content.get_nth_page(i))
            label = get_label_from_tab(tab)
            rad = Gtk.RadioButton().new_with_label(None, label.get_text())
            rad.join_group(radio)
            rad.connect('toggled',self.on_radio_btn_clicked, i)
            box.pack_start(rad,True,False,0)

        box.show_all()

    def on_radio_btn_clicked(self, button, page_num):
        self.content.set_current_page(page_num)

    def on_btn_add_tab_clicked(self, button):
        self.add_notebook_content()

    def get_mlp_content_at_current_page(self):
        index = self.content.get_current_page()
        return self.mlp_content_array[index]


def get_label_from_tab(notebook_tab):
    childrens = notebook_tab.get_children()

    for widget in childrens:
        if isinstance(widget,Gtk.Label):
            return widget
