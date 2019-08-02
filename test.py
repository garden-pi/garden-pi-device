import os
from datetime import datetime
current_dir = os.getcwd()

myFile = open(current_dir + '/append_to_me.txt', 'w+') 
myFile.write('\nAccessed on ' + str(datetime.now()))