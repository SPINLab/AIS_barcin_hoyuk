import glob
import os
import csv
from updater_scripts.config import DATA_DIR, DRIVE_LETTER, ROOT_URL

ROOT_DIR = os.path.join(DRIVE_LETTER, DATA_DIR)
CSV_FILE_LIST_BASE = 'file_list.csv'


def path_to_url(path):
    url = path.replace(DRIVE_LETTER, ROOT_URL)
    return url.replace('\\', '/')


def build_file_list(sub, listfile):
    print('building file list')
    with open(listfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        print(os.path.join(ROOT_DIR, sub, '**/*'))
        for filename in glob.iglob(os.path.join(ROOT_DIR, sub, '**/*'), recursive=True):
            extension = os.path.splitext(filename)[1].lower()
            if extension in ['.tif', '.tiff', '.jpg', '.pdf', '.bmp']:
                basename = os.path.splitext(os.path.basename(filename))[0]
                writer.writerow([basename, path_to_url(filename)])
    print('wrote file_list to: %s' % listfile)


def get_file_list(subdir, list_rebuild=True):
    listfile = '%s_%s' % (subdir, CSV_FILE_LIST_BASE)
    if not os.path.isfile(listfile) or list_rebuild:
        build_file_list(subdir, listfile)
    else:
        print('Found %s, using it' % listfile)
    file_list = {}
    with open(listfile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            file_list[row[0]] = row
    return file_list
