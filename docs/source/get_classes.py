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

# Define list for new file
new_file = []

# Go through all lines until toctree starts and write them to list
for line in lines:
    if line != '.. autosummary::' + '\n':
        new_file.append(line)
    else:
        break

# Write toctree and maxdepth to list of new file
new_file.append('.. autosummary::' + '\n')
new_file.append('   :toctree: stubs' + '\n')
new_file.append('\n')

# Go through all classes and write them to list
for class_ in classes:
    class_ = class_[:-3] # To remove .py ending
    r = re.compile('.*' + class_)
    new_file.append('   ' + str(class_) + '\n')

# Write list to file
with open(module_file, 'w') as f:
    for line in new_file:
        f.write(line)
