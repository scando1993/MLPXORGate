import gi,sys,os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from Constants import MAIN_CONTENT
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
            builder = Gtk.Builder.new_from_file(os.path.join(file_path, MAIN_CONTENT))
        except Exception as e:
            print e
            print "Failed to load XML GUI file " + MAIN_CONTENT
            sys.exit(1)

        builder.connect_signals(self)

        self.inputDataSet = []
        self.outputDataSet = []

        self.content = builder.get_object("notebookContent")
        self.cbSolverFunction = builder.get_object("cbSolverFunction")
        self.cbActivationFunction = builder.get_object("cbActivationFunction")
        self.cbLearningRate = builder.get_object("cbLearningRate")
        # self.modelCbLearningRate = builder.get_object("datModelCbLearningRate")
        # self.modelCbActivationFunction = builder.get_object("dataModCbActFunctions")
        # self.modelCbSolverFunction = builder.get_object("datModCbSolverFunction")
        self.spnHiddenLayers = builder.get_object("spnHiddenLayers")
        self.spnNeuronsLayers = builder.get_object("spnNeuronsLayers")
        self.spnMaxTol = builder.get_object("spnMaxTol")
        self.spnTestSize = builder.get_object("spnTestSize")
        self.spnTrainSize = builder.get_object("spnTrainSize")
        self.revealerNoResults = builder.get_object("revealerNoResults")
        self.revealerResults = builder.get_object("revealerResults")
        self.txtViewPredictResults = builder.get_object("txtViewPredictResults")
        self.frameGraphics = builder.get_object("frameGraphics")
        self.lblNoResults = builder.get_object("lblNoResults")

        self.modelCbLearningRate = Gtk.ListStore(str)
        self.modelCbActivationFunction = Gtk.ListStore(str)
        self.modelCbSolverFunction = Gtk.ListStore(str)

        self.init_cbs_models()

    def init_cbs_models(self):
        #
        # renderer_text = Gtk.CellRendererText()
        # self.cbSolverFunction.pack_start(renderer_text,True)
        # self.cbSolverFunction.add_attribute(renderer_text,"Text",0)
        # # self.cbSolverFunction.set_size_request(200,255)
        #
        # self.cbActivationFunction.pack_start(renderer_text,True)
        # self.cbActivationFunction.add_attribute(renderer_text,"Text",0)
        #
        # self.cbLearningRate.pack_start(renderer_text, True)
        # self.cbLearningRate.add_attribute(renderer_text,"Text",0)
        #
        for function in XOR.get_activation_functions():
            self.modelCbActivationFunction.append([function])

        for learning_rate in XOR.get_learning_rate():
            self.modelCbLearningRate.append([learning_rate])

        for solver in XOR.get_solver_functions():
            self.modelCbSolverFunction.append([solver])

        self.cbLearningRate.set_model(self.modelCbLearningRate)
        self.cbActivationFunction.set_model(self.modelCbActivationFunction)
        self.cbSolverFunction.set_model(self.modelCbSolverFunction)

        self.cbLearningRate.set_active(0)
        self.cbSolverFunction.set_active(0)
        self.cbActivationFunction.set_active(0)

    def on_btnInputTrain_file_set(self, data):
        if data:
            print data.get_filename()
        else:
            print "No datos"

    def on_btnOutputTrain_file_set(self, data):
        if data:
            print data.get_filename()
        else:
            print "no data"

    def calculate(self):
        if self.inputDataSet == [] and self.outputDataSet == []:
            self.lblNoResults.set_text("Empty DataSets")

    def stop(self):
        pass
