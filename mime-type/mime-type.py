import sys
import math

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.
ext_dict = {}

for i in range(n):
    ext, mime_type = input().split()
    ext_dict[ext.lower()] = mime_type

for i in range(q):
    file_name = input()
    split_file_name = file_name.split('.')
    if len(split_file_name) > 1:
        print(ext_dict.get(split_file_name[-1].lower(),"UNKNOWN"))
    else:
        print("UNKNOWN")