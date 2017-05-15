'''Find all classes of MasterModule and write them to modules.rst for
the autosummary.

'''
# Python modules
import glob
import os
import re

# File that will be appended with scripts
script_file = 'rst/scripts.rst'

# Find scripts
scripts = glob.glob('../../python/scripts/*.py')
scripts = [os.path.basename(x) for x in scripts]

# Remove functions and parameters
scripts.remove('functions.py')
scripts.remove('parameters.py')

# Sort alphabetically
scripts.sort()

# Read lines of module file
with open(script_file, 'r') as f:
    lines = f.readlines()

# Define list for new file
new_file = []

# Go through all lines until toctree starts and write them to list
for line in lines:
    if line != '.. toctree::' + '\n':
        new_file.append(line)
    else:
        break

# Write toctree and maxdepth to list of new file
new_file.append('.. toctree::' + '\n')
new_file.append('   :maxdepth: 1' + '\n')
new_file.append('\n')

# Go through all scripts and write them to list
for script in scripts:
    script = script[:-3] # To remove .py ending
    r = re.compile('.*' + script)
    new_file.append('   scripts/' + str(script) + '\n')

# Write list to file
with open(script_file, 'w') as f:
    for line in new_file:
        f.write(line)
        
