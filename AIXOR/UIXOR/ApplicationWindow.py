import gi, sys, os
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
from MLPNotebook import MLPNotebook
from MLPNotebookContent import MLPNotebookContent
from Constants import UI_FILE


class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "ApplicationWindow"

    # def __new__(cls, *args, **kwargs):
    #     file_path = os.path.dirname(__file__)
    #     try:
    #         builder = Gtk.Builder.new_from_file(os.path.join(file_path, UI_FILE))
    #     except:
    #         print "Failed to load XML GUI file" + UI_FILE
    #         sys.exit(1)
    #
    #     window = builder.get_object("MainApplicationWindow")
    #     # builder.connect_signals(self)
    #     # window.finish_init(builder)
    #     return window
    #
    # def finish_init(self, builder):
    #     builder.connect_signals(self)

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

        self.main_window_content = builder.get_object("MainWindowContent")

        self.swMainAnalysis = builder.get_object("swMainAnalysis")

        self.openActionContentRevealer = builder.get_object("OpenActionContentRevealer")

        self.closeActionContentRevealer = builder.get_object("CloseActionContentRevealer")

        self.moreThanOnePage = False

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                           GLib.Variant.new_boolean(False))

        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                            lambda obj, pspec: max_action.set_state(
                                               GLib.Variant.new_boolean(obj.props.is_maximized)))

        self.notebookContent = MLPNotebookContent()
        self.swMainAnalysis.add_with_viewport(self.notebookContent.content)
        # lbl_variant = GLib.Variant.new_string("String 1")
        # lbl_action = Gio.SimpleAction.new_stateful("change_label", lbl_variant.get_type(),
        #                                        lbl_variant)
        #
        # lbl_action.connect("change-state", self.on_change_label_state)
        # self.add_action(lbl_action)
        #
        # self.main_window_content.pack_start(MLPNotebookTab().notebook,True,True,0)
        self.add(self.main_window_content)
        self.main_window_content.show_all()

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
        self.moreThanOnePage = True


    def on_btnToolOpen_clicked(self, button):
        pass

    def on_btnToolStatistics_clicked(self, button):
        pass

    def on_btnToolCalculate_clicked(self, button):
        pass

    def on_btnToolCancel_clicked(self, button):
        pass

    def on_btnToolCancel_clicked(self, button):
        pass

    def on_btnToolHelp_clicked(self, button):
        pass

    def on_btnCalculate_clicked(self, button):
        pass

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