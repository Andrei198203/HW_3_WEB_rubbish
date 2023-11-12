from shutil import copyfile
from pathlib import Path
import argparse
from threading import Thread
import logging

"""
python main.py --source -s images
python main.py --output -o dist

"""

parser = argparse.ArgumentParser(description='App for sorting folders')

parser.add_argument('-s', '--source', required=True)      # option that takes a value
parser.add_argument('-o', '--output', default='dist')  # on/off flag

args = vars(parser.parse_args())  # object converted to dict
source = args.get('source')
output = args.get('output')

folders = []

def grabs_folders(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folders(el)

def sorted_file(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as e:
                logging.error(e)


# Виконання основної функції при запуску скрипта
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format= "%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)

    folders.append(base_folder)
    grabs_folders(base_folder)
    print(folders)
    threads = []
    for folder in folders:
        th = Thread(target=sorted_file, args=(folder,))
        th.start()
        threads.append(th)

        [th.join() for th in threads]
        print('The start folder can be deleted')



