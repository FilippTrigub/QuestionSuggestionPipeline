import os


def clean_directory(directory):
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))
    if os.listdir(directory):
        raise OSError('Failed to clean data directory.')
    if directory not in os.listdir():
        os.mkdir(directory)
