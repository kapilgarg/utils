from tqdm import tqdm 
import hashlib 
import pathlib
import pandas as pd

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
  hashes, errors = generate_hash(r"c:\temp")
  df = pd.DataFrame(hashes, columns=["hash", "file"])
  duplicated_df = df[df.duplicated(subset='hash', keep='first')]
