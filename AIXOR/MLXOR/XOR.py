from sklearn.model_selection import train_test_split
from multilayer_perceptron import MLPClassifier
from sklearn import __version__
import threading
import numpy as np

class XOR:
    activation_functions = ('identity','logistic','tanh','relu')
    solver_functions = ("lbfgs", "sgd", "adam")
    learning_rate = ("constant", "invscaling", "adaptative")

    def __init__(self, name=""):
        # self._stop_event = threading.Event()
        # self._sleep_period = 1.0
        # threading.Thread.__init__(self,name=name)

        self._mlp_random_state = 0
        self._mlp_batch_size = 0
        self._mlp_alpha = 0.0001
        self._mlp_max_iter = 0
        self._learning_rate_init = 0.001
        self._random_state = 1
        self._mlp_shuffle = True
        self._mlp_momentum = 0.9
        self._mlp_nesterovs_momentum = True
        self._mlp_early_stopping = False
        self._mlp_validation_fraction = 0.1
        self._mlp_beta_1 = 0.9
        self._mlp_beta_2 = 0.999
        self._mlp_epsilon = 1e-8
        self._mlp_power_t = 0.5
        self._mlp_verbose = True
        self._mlp_warm_start = False

        self._mlp = MLPClassifier()
        self.train_size = 0.0
        self.test_size = 0.0
        self.input_set = []
        self.output_set = []
        self.activation = ""
        self.solver = ""
        self.learning_rate = ""
        self.mlp_tolerance = 0.0
        self.neurons_layer = 0.0
        self.hidden_layers = 0.0

        self.predictions = []
        self.real_output = []
        self.verbose = []
        self.score = 0.0

    @staticmethod
    def get_activation_functions():
        return XOR.activation_functions

    @staticmethod
    def get_solver_functions():
        return XOR.solver_functions

    @staticmethod
    def get_learning_rate():
        return XOR.learning_rate

    def set_input_set(self, input_data):
        self.input_set = input_data

    def set_test_size(self, float_num):
        self.test_size = float_num

    def set_train_size(self, float_num):
        self.train_size = float_num

    def set_random_state(self, random_state):
        self._random_state = random_state

    def run(self):
        x_train, x_test, y_train, y_test = train_test_split(self.input_set,
                                                            self.output_set,
                                                            random_state=self._random_state,
                                                            test_size=self.test_size,
                                                            train_size=self.train_size)

        self._mlp.random_state = self._random_state
        self._mlp.activation = self.activation
        self._mlp.solver = self.solver
        self._mlp.learning_rate = self.learning_rate
        self._mlp.tol = self.mlp_tolerance
        self._mlp.verbose = self._mlp_verbose
        self._mlp.string_verbose = self.verbose
        self._mlp.hidden_layer_sizes = tuple([self.neurons_layer]*self.hidden_layers)

        self._mlp.fit(x_train,y_train)

        self.real_output = y_test
        self.predictions = self._mlp.predict(x_test)
        self.score = self._mlp.score(x_test, y_test)

    def join(self, timeout=None, balancing=True):
        # self._stop_event.set()
        # threading.Thread.join(self, timeout)
        pass
    def is_running(self):
        # return self._stop_event.isSet()
        pass