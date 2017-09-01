import os,json


class FileHandler:
    def __init__(self, filename):
        self.original_filename = filename
        name, extension = os.path.splitext(filename)
        self.name = name
        self.extension = extension
        self.data = []

    def read_data(self):
        if self.extension in ".csv":
            self.__csv_handle__()
        elif self.extension in ".txt":
            self.__txt_handle__()
        elif self.extension in ".xlsx":
            self.__excel_handle__()

    def __csv_handle__(self):
        pass

    def __txt_handle__(self):
        with open(self.original_filename,'r') as f:
            for line in f.readlines():
                try:
                    self.data = eval(line)
                except Exception as e:
                    print (e.message)

    def __excel_handle__(self):
        pass

    def __own_format__(self):
        pass

    def save_object_in_file(self, obj):
        with open(self.original_filename, 'w') as fp:
            json.dump(obj, fp)

    def read_object_from_file(self,obj):
        pass