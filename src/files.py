import os
from glob import glob
import time
import re

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"!!!! {func.__name__} function took {start_time - end_time} second")
        return result
    return wrapper
    

def check_extensions(path:str)->bool:
    extensions=['.jpg', '.jpeg', '.png']
    return any(map(path.endswith, extensions))

def check_paths_extensions(paths:str)->bool:
    return list(filter(check_extensions, paths))

def convert_abs_path(path:str)->str:
    return list(map(os.path.abspath, path))

def find_numbers(s):
    numbers = re.findall(r"\d+", s)
    if numbers:
        return int(numbers[0])
    else:
        return float('inf')

# @timing_decorator
def get_img_paths(dir):
    paths = glob(dir+"*")
    assert not os.path.isfile(dir) or len(paths) < 3, "At least require more than 3 images, you must input a directory path"

    paths = check_paths_extensions(paths)
    paths = sorted(paths, key=find_numbers)
    return convert_abs_path(paths)
        
if __name__ == "__main__":
    dir = "./data/data0/"
    paths= get_img_paths(dir)
    print(paths)