import json


def save_file(filename, obj):
    with open(filename,'w') as fp:
        json.dump(obj, fp)


def read_file(filename):
    pass