import os


def get_local_dir_path():
    return os.path.dirname(os.path.realpath(__file__))


def join_to_local_dir(*path):
    return os.path.join(get_local_dir_path(), *path)
