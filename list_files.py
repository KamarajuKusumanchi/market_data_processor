#! /usr/bin/env python3


import os


def list_files_by_extension(path, extension):
    # sample usage:
    # list_files_by_extension('.', '.py')
    # list_files_by_extension('.', ('.py'))
    # list_files_by_extension('.', ('.html', '.htm'))
    file_list = [os.path.join(root, file)
                 for root, dirs, files in os.walk(path)
                 for file in files
                 if file.endswith(extension)]
    return file_list


def list_python_files(path):
    return list_files_by_extension(path, '.py')


def list_csv_files(path):
    return list_files_by_extension(path, '.csv')


if __name__ == "__main__":
    # files = list_files_by_extension('.', '.py')
    # files = list_files_by_extension('.', ('.py'))
    # files = list_files_by_extension('.', ('.py', '.txt'))
    files = list_python_files('.')
    print(*files, sep='\n')
