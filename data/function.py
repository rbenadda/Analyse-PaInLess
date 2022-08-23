from os import listdir
import random

def add_worker(workers):
        workers = workers + 1

def read_directory(path,files):
        dirs = listdir(path)
        
        for file in dirs:
                files.append(file)

def max_value(inputlist):
        return max([sublist[0] for sublist in inputlist])

def random_color():
        hexadecimal = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
        return hexadecimal

def aff_probs(files):
        cpt = 0
        index = "index:"
        for i in files:
                print(index,cpt,i)
                cpt = cpt + 1

def random_color_list(listed):
        color = []
        for i in range(0,listed):
                color.append(random_color())
        return color