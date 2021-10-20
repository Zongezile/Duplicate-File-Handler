import os
import sys
from collections import defaultdict
import hashlib

args = sys.argv


def scan_dir():
    if len(args) != 2:
        print("Directory is not specified")

    elif os.path.isdir(str(args[1])):
        f_format = input('Enter file format:\n')
        print('''Size sorting options:
        1. Descending
        2. Ascending''')
        while True:
            sorting = input('Enter a sorting option: \n')
            if sorting == '1' or sorting == '2':
                break
            print('\nWrong option\n')

        sorted_paths = defaultdict(list)
        for root, dirs, files in os.walk(args[1]):
            for filename in files:
                if f_format == '':
                    sorted_paths[os.path.getsize(os.path.join(root, filename))].append(os.path.join(root, filename))
                elif f_format in filename:
                    sorted_paths[os.path.getsize(os.path.join(root, filename))].append(os.path.join(root, filename))
        if sorting == '1':
            sorted_paths = sorted(sorted_paths.items(), reverse=True)
        else:
            sorted_paths = sorted(sorted_paths.items())

        possibly_copy = {}
        for size, paths in sorted_paths:
            the_same = 0
            print(size, 'bytes')
            for path in paths:
                print(path)
                the_same += 1
                if the_same >= 2:
                    possibly_copy[size] = paths
            print('')

        while True:
            checking = input('Check for duplicates? \n')
            if checking == 'yes' or checking == 'no':
                break
            print('\nWrong option\n')

        i = 0
        paths_to_remove = {}
        if checking == 'yes':
            for size, paths in possibly_copy.items():
                print(size, 'bytes')
                check_copy = defaultdict(list)
                for path in paths:
                    with open(path, 'rb') as file:
                        check_copy[hashlib.md5(file.read()).hexdigest()].append(path)
                for f_hash, n_paths in check_copy.items():
                    if len(n_paths) > 1:
                        print('Hash:', f_hash)
                        for path in n_paths:
                            i += 1
                            print(f'{i}. ' + path)
                            paths_to_remove[i] = path

                print('')
        else:
            pass

        while True:
            delete = input('Delete files? \n')
            if delete == 'yes' or delete == 'no':
                break
            print('\nWrong option\n')

        if delete == 'yes':
            while True:
                which = input('Enter file numbers to delete: \n').split()
                wrong = 0
                try:
                    for x in which:
                        if 0 >= int(x) or int(x) > i:
                            wrong = 1
                except ValueError:
                    wrong = 1
                if wrong == 1 or len(which) == 0:
                    print('\nWrong option\n')
                else:
                    break

            freed_up_space = 0
            for number in paths_to_remove.keys():
                for x in which:
                    if int(x) == number:
                        freed_up_space += os.path.getsize(paths_to_remove[number])
                        os.remove(paths_to_remove[number])
            print(f'Total freed up space: {freed_up_space} bytes')
        else:
            sys.exit()

    else:
        print("Directory is not specified")


scan_dir()
