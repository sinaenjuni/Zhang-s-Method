import os
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
    

def check_file_extension(file:str)->bool:
    extensions=['.jpg', '.jpeg', '.png']
    # return any([file_list[0].endswith(extension) for extension in extensions])
    return any(map(file.endswith, extensions)) 

def convert_abs_path(path:str)->str:
    return list(map(os.path.abspath, path))

def find_numbers(s):
    numbers = re.findall(r"\d+", s)
    if numbers:
        return int(numbers[0])
    else:
        return float('inf')

@timing_decorator
def get_img_files(path):
    if os.path.isfile(path):
        assert check_file_extension(path), f"{path} is not image file."
        return os.path.abspath(path)
    else:
        file_list = os.listdir(path)
        file_list = sorted(list(filter(check_file_extension, file_list)), key=find_numbers)
        return convert_abs_path(file_list)
        
if __name__ == "__main__":
    path = "./data/data0/"
    print(get_img_files(path))