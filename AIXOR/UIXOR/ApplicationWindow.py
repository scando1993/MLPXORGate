import gi, sys, os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
from MLPNotebook import MLPNotebook, get_label_from_tab
from MLPNotebookContent import MLPNotebookContent
from Constants import UI_FILE
from NotebookTabLabel import NotebookTabLabel
from ..Utils.FileHandler import FileHandler


class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "ApplicationWindow"

    def __init__(self, *args, **kwargs):

        super(Gtk.ApplicationWindow,self).__init__(*args, **kwargs)

        file_path = os.path.dirname(__file__)
        try:
            builder = Gtk.Builder.new_from_file(os.path.join(file_path, UI_FILE))
        except:
            print "Failed to load XML GUI file" + UI_FILE
            sys.exit(1)

        builder.connect_signals(self)

        self.set_default_size(800,600)

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                           GLib.Variant.new_boolean(False))

        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                            lambda obj, pspec: max_action.set_state(
                                               GLib.Variant.new_boolean(obj.props.is_maximized)))

        self.main_window_content = builder.get_object("MainWindowContent")

        # self.notebook = builder.get_object("MLPNotebook")
        self.notebook = MLPNotebook()

        self.openActionContentRevealer = builder.get_object("OpenActionContentRevealer")

        self.closeActionContentRevealer = builder.get_object("CloseActionContentRevealer")

        self.analysisContent = builder.get_object("AnalysisContent")

        self.stackSwitcher = builder.get_object("stackContent")

        self.status_bar = builder.get_object("mainWindowStatusBar")

        self.notebook.add_notebook_content()

        self.analysisContent.remove(self.analysisContent.get_child1())
        self.analysisContent.pack1(self.notebook.content, True, False)

        self.add(self.main_window_content)
        self.show_all()

    def on_change_label_state(self, action, value):
        action.set_state(value)
        self.label.set_text(value.get_string())

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()

    def on_btnToolNew_clicked(self, button):
        self.notebook.content.set_show_tabs(True)
        self.notebook.add_notebook_content()

    def on_btn_add_tab_clicked(self, button):
        self.notebook.add_notebook_content()

    def on_btnToolSave_clicked(self, button):
        index = self.notebook.content.get_current_page()
        widget = self.notebook.content.get_nth_page(index)
        tab = self.notebook.content.get_tab_label(widget)
        label = get_label_from_tab(tab)
        # widget_obj = mlp_content_array[label.get_text()]

        widget_obj = self.notebook.get_mlp_content_at_current_page()

        dialog = Gtk.FileChooserDialog("Save File",
                                       self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
                                       )
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name(label.get_text())

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            File = FileHandler(file_name)
            File.save_object_in_file(widget_obj.save())
            label.set_text(File.name)
        dialog.destroy()

    def on_btnToolPreferences_clicked(self, button):
        pass

    def on_btnToolOpen_clicked(self, button):
        pass

    def on_btnToolStatistics_clicked(self, button):
        if button.get_active():
            self.stackSwitcher.set_visible_child_name("MLPStatistics")
        else:
            self.stackSwitcher.set_visible_child_name("MLPAnalysis")


    def on_btnToolCalculate_clicked(self, button):
        content = self.notebook.get_mlp_content_at_current_page()
        content.calculate()

    def on_btnToolCancel_clicked(self, button):
        pass

    def on_btnToolHelp_clicked(self, button):
        pass

    def on_btnCalculate_clicked(self, button):
        self.on_btnToolCalculate_clicked()

    def on_btnClose_clicked(self, button):
        pass

    def on_btnHelp_clicked(self, button):
        pass

    def on_btnCloseActionContent_clicked(self, button):
        self.closeActionContentRevealer.set_reveal_child(False)
        self.openActionContentRevealer.set_reveal_child(True)

    def on_btnOpenActionContent_clicked(self,button):
        self.closeActionContentRevealer.set_reveal_child(True)
        self.openActionContentRevealer.set_reveal_child(False)

    def on_mainWindowStatusBar_draw(self, cairo, data):
        mlp_content = self.notebook.get_mlp_content_at_current_page()
        if mlp_content.busy:
            self.status_bar.push(0, "Busy")
            self.status_bar.pop(1)
        else:
            self.status_bar.push(1,"Ready")
            self.status_bar.pop(0)