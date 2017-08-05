from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


y = [0, 1, 1, 0]*1000
x = [[0, 0], [0, 1], [1, 0], [1, 1]] * 1000
x_train, x_test, y_train, y_test = train_test_split(x,y, random_state=3)


class XOR:
    activation_functions = ('identity','logistic','tanh','relu')
    solver_functions = ('lbfgs', 'sgd', 'adam')
    learning_rate = ('constant', 'invscaling', 'adaptative')

    def __init__(self):
        self.mlp = MLPClassifier()
        self.train_size = 0.0
        self.test_size = 0.0
        self.random_state = 0
        self.input_set = []
        self.output_set = []
        self.hidden_layers_sizes = None
        self.activation = ""
        self.mlp_random_state = 0
        self.mlp_batch_size = 0
        self.mlp_alpha = 0.0
        self.mlp_max_iter = 0
        self.mlp_tolerance = 0.0
        self.learning_rate_init = 0.001



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
        self.random_state = random_state

