import os

# This imports all the file names
location = './data/'
filenames = os.listdir(location)

for filename in filenames:
    aux = filename.split('.')
    name = aux[0]
    extension = aux[1]
    new_name = location + name.upper() + '.' + extension
    os.rename(location + filename, new_name)
