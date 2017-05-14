'''Find all classes of MasterModule and write them to modules.rst for
the autosummary.

'''
# python modules
import glob
import os
import re

# file that will be appended with classes
module_file = 'rst/modules.rst'

# Find classes
classes = glob.glob('../../python/ModuleSetup/MasterModule/*.py')
classes = [os.path.basename(x) for x in classes]

# Sort alphabetically
classes.sort()

# Remove init from the list
classes.remove('__init__.py')

# Read lines of module file
with open(module_file, 'r') as f:
    lines = f.readlines()
    
with open(module_file, 'a') as f:
    for class_ in classes:
        class_ = class_[:-3] # To remove .py ending
        r = re.compile('.*' + class_)
        if not list(filter(r.match, lines)):
           f.write('   ' + str(class_) + '\n')
