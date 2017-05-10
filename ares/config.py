import os.path

from yaml import load

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = load(open(path + '/dev.yaml'))

if os.path.isfile(path + '/local.yaml'):
    data_local = load(open(path + '/local.yaml'))
    data.update(data_local)


def get_config(key):
    return data.get(key)
