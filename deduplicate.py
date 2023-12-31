"""
This script identifies the deuplicate files from a given directory. 
It recursively traverse the directory to list all the files. For each of the file, it computes the hash and identify the files with duplicate hash.
it returns a pandas dataframe containing hash value and file path of duplicate files
"""

from tqdm import tqdm 
import hashlib 
import pathlib
import pandas as pd
import argparse

block_size = 1024

def hashing (name_of_file):
    h = hashlib.sha1 ()
    with open (name_of_file, 'rb') as file:
        while True:
            block = file.read (block_size)
            if not block:break
            h.update (block)
    return h.hexdigest ()


def get_all_files(path, file_type="*"):    
    glob = pathlib.Path(path)
    return glob.rglob(file_type)

def generate_hash(path):
    hashes = []
    errors=[]
    files = get_all_files(path)
    for file in tqdm(files):
        file = str(file)
        try:
            h = hashing(file) 
            hashes.append((h, file))
        except Exception as ex:
            errors.append(ex)        
    return (hashes, errors)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory',help='directory containing the duplicate files')
    args = parser.parse_args()
    
    hashes, errors = generate_hash(args.directory)
    df = pd.DataFrame(hashes, columns=["hash", "file"])
    duplicated_df = df[df.duplicated(subset='hash', keep='first')]
