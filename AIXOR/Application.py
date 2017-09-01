import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
import UIXOR.ApplicationWindow
import warnings

warnings.filterwarnings("ignore")
# This would typically be its own file
MENU_XML="AIXOR/ApplicationMenu.ui"


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super(Gtk.Application,self).__init__(*args, application_id="org.example.myapp",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_file(MENU_XML)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = UIXOR.ApplicationWindow(application=self, title="Main Window")

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()
        return 0

    def on_about(self, action, param):
        builder = Gtk.Builder.new_from_file("AIXOR/UIXOR/ApplicationInterface.ui")
        about_dialog = builder.get_object("AboutWindow")
        about_dialog.set_transient_for(self.window)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
