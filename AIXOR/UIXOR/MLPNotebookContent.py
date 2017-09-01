from __future__ import print_function

import gi
import os
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Constants import MAIN_CONTENT_FILE
from ..MLXOR.XOR import XOR
from AIXOR.Utils.FileHandler import FileHandler

import matplotlib.cm as cm
from matplotlib.backends.backend_cairo import FigureCanvas

accepted_files = ("*.txt","*.xslx","*.mat")


class MLPNotebookContent:
    __gtype_name__ = "MLPNotebookContent"

    def __init__(self):
        file_path = os.path.dirname(__file__)
        try:
            builder = Gtk.Builder.new_from_file(os.path.join(file_path, MAIN_CONTENT_FILE))
        except Exception as e:
            print(e)
            print("Failed to load XML GUI file " + MAIN_CONTENT_FILE)
            sys.exit(1)

        builder.connect_signals(self)

        self.inputDataSet = []
        self.outputDataSet = []

        self.contents = builder.get_object("MLPNotebookContent")
        self.cbSolverFunction = builder.get_object("cbSolverFunction")
        self.cbActivationFunction = builder.get_object("cbActivationFunction")
        self.cbLearningRate = builder.get_object("cbLearningRate")
        self.spnHiddenLayers = builder.get_object("spnHiddenLayers")
        self.spnNeuronsLayers = builder.get_object("spnNeuronsLayers")
        self.spnMaxTol = builder.get_object("spnMaxTol")
        self.spnTestSize = builder.get_object("spnTestSize")
        self.spnTrainSize = builder.get_object("spnTrainSize")
        self.revealerNoResults = builder.get_object("revealerNoResults")
        self.revealerResults = builder.get_object("revealerResults")
        self.txtViewPredictResults = builder.get_object("txtViewPredictResults")
        self.frameGraphics = builder.get_object("frameGraphics")
        self.frameResults = builder.get_object("frameResults")
        self.lblNoResults = builder.get_object("lblNoResults")

        self.cbInputTrain = builder.get_object("cbInputTrain")
        self.cbOutputTrain = builder.get_object("cbOutputTrain")

        self.modelCbLearningRate = Gtk.ListStore(str)
        self.modelCbActivationFunction = Gtk.ListStore(str)
        self.modelCbSolverFunction = Gtk.ListStore(str)

        self.modelCbFileChooser = Gtk.ListStore(str)

        self.init_cbs_models()

        self.xor = XOR()

        self.busy = False

    def init_cbs_models(self):
        for function in XOR.get_activation_functions():
            self.modelCbActivationFunction.append([function])

        for learning_rate in XOR.get_learning_rate():
            self.modelCbLearningRate.append([learning_rate])

        for solver in XOR.get_solver_functions():
            self.modelCbSolverFunction.append([solver])

        for extension in accepted_files:
            self.modelCbFileChooser.append([extension])

        self.cbLearningRate.set_model(self.modelCbLearningRate)
        self.cbActivationFunction.set_model(self.modelCbActivationFunction)
        self.cbSolverFunction.set_model(self.modelCbSolverFunction)
        self.cbInputTrain.set_model(self.modelCbFileChooser)
        self.cbOutputTrain.set_model(self.modelCbFileChooser)

        self.cbLearningRate.set_active(0)
        self.cbSolverFunction.set_active(0)
        self.cbActivationFunction.set_active(0)
        self.cbInputTrain.set_active(0)
        self.cbOutputTrain.set_active(0)

    def on_btnInputTrain_file_set(self, data):
        if data:
            File = FileHandler(data.get_filename())
            File.read_data()
            self.inputDataSet = File.data
            # print (data.get_filename())

        else:
            print ("No datos")

    def on_btnOutputTrain_file_set(self, data):
        if data:
            File = FileHandler(data.get_filename())
            File.read_data()
            self.outputDataSet = File.data

            # print (data.get_filename())
        else:
            print ("no data")

    def on_cbInputTrain_changed(self, data):
        filefilter = Gtk.FileFilter()
        filefilter.add_pattern(self.cbInputTrain.get_active_text())
        data.set_filter(filefilter)

    def on_cbOutputTrain_changed(self, data):
        filefilter = Gtk.FileFilter()
        filefilter.add_pattern(self.cbInputTrain.get_active_text())
        data.set_filter(filefilter)

    def on_spnTrainSize_value_changed(self, data):
        self.spnTestSize.set_value(1.00 - self.spnTrainSize.get_value())

    def on_spnTestSize_value_changed(self,data):
        self.spnTrainSize.set_value(1.00 - self.spnTestSize.get_value())

    def on_frameResults_draw(self, cr, data):
        if len(self.xor.predictions) > 0:
            buffer = self.txtViewPredictResults.get_buffer()
            iter_ = buffer.get_end_iter()
            buffer.insert(iter_,self.print_results())
            # self.txtViewPredictResults.set_text(str(self.xor.predictions))
            self.revealerNoResults.set_reveal_child(False)
            self.revealerResults.set_reveal_child(True)

    def print_results(self):
        string = '''Accuracy: %s\n''' % (self.xor.score)
        for i, p in enumerate(self.xor.predictions):
            string += "Output: %s Predicted: %s\n" % (self.xor.real_output, self.xor.predictions)
        return string

    def calculate(self):
        if self.inputDataSet == [] and self.outputDataSet == []:
            self.lblNoResults.set_text("Empty DataSets")
            return

        self.xor.activation = self.cbActivationFunction.get_active_text()
        self.xor.learning_rate = self.cbLearningRate.get_active_text()
        self.xor.solver = self.cbSolverFunction.get_active_text()
        self.xor.mlp_tolerance = self.spnMaxTol.get_value()
        self.xor.train_size = float(self.spnTrainSize.get_value())
        self.xor.test_size = float(self.spnTestSize.get_value())

        print (self.xor.train_size)
        print (self.xor.test_size)
        print (self.xor.solver_functions)

        self.xor.neurons_layer = int(self.spnNeuronsLayers.get_value())
        self.xor.hidden_layers = int(self.spnHiddenLayers.get_value())
        self.xor.input_set = self.inputDataSet
        self.xor.output_set = self.outputDataSet

        if not self.xor.isAlive():
            self.xor.start()

        while self.xor.is_running():
            self.busy = True
            # import time
            # time.sleep(1)
        self.frameResults.queue_draw()

    def stop(self):
        self.xor.join()

    def save(self):
        params_map = {}
        params_map['solverFunction'] = self.cbSolverFunction.get_active_text()
        params_map['activationFunction'] = self.cbActivationFunction.get_active_text()
        params_map['learningRate'] = self.cbLearningRate.get_active_text()
        params_map['inputData'] = self.inputDataSet
        params_map['outputData'] = self.outputDataSet
        params_map['hiddenLayers'] = self.spnHiddenLayers.get_value()
        params_map['numNeuronsLayer'] = self.spnNeuronsLayers.get_value()
        params_map['maxTolerance'] = self.spnMaxTol.get_value()
        params_map['testSize'] = self.spnTestSize.get_value()
        params_map['trainSize'] = self.spnTrainSize.get_value()
        params_map['predResults'] = self.txtViewPredictResults.get_text()
        return params_map
