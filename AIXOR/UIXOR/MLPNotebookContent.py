import gi,sys,os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Constants import UI_FILE
from ..MLXOR.XOR import XOR


class MLPNotebookContent():
    __gtype_name__ = "MLPNotebookContent"

    # def __new__(cls, *args, **kwargs):
    #     file_path = os.path.dirname(__file__)
    #     try:
    #         builder = Gtk.Builder()
    #         builder.add_from_file(os.path.join(file_path, UI_FILE))
    #     except:
    #         print "Failed to load XML GUI file" + UI_FILE
    #         sys.exit(1)
    #
    #     new_object = builder.get_object("notebookContent")
    #     # new_object.finish_init(builder)
    #     return new_object

    # def finish_init(self, builder):
        # builder.connect_signals(self)

    def __init__(self):
        file_path = os.path.dirname(__file__)
        try:
            builder = Gtk.Builder()
            builder.add_from_file(os.path.join(file_path, UI_FILE))
        except:
            print "Failed to load XML GUI file" + UI_FILE
            sys.exit(1)

        builder.connect_signals(self)

        self.inputDataSet = []
        self.outputDataSet = []

        self.content = builder.get_object("notebookContent")
        self.cbSolverFunction = builder.get_object("cbSolverFunction")
        self.spnHiddenLayers = builder.get_object("spnHiddenLayers")
        self.spnNeuronsLayers = builder.get_object("spnNeuronsLayers")
        self.cbActivationFunction = builder.get_object("cbActivationFunction")
        self.cbLearningRate = builder.get_object("cbLearningRate")
        self.spnMaxTol = builder.get_object("spnMaxTol")
        self.spnTestSize = builder.get_object("spnTestSize")
        self.spnTrainSize = builder.get_object("spnTrainSize")
        self.revealerNoResults = builder.get_object("revealerNoResults")
        self.revealerResults = builder.get_object("revealerResults")
        self.txtViewPredictResults = builder.get_object("txtViewPredictResults")
        self.frameGraphics = builder.get_object("frameGraphics")
        self.lblNoResults = builder.get_object("lblNoResults")

    def on_btnInputTrain_file_set(self, data):
        pass

    def on_btnOutputTrain_file_set(self, data):
        pass

    def calculate(self):
        if self.inputDataSet == [] and self.outputDataSet == []:
            self.lblNoResults.set_text("Empty DataSets")

    def stop(self):
        pass
