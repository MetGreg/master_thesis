'''Find all classes of MasterModule and write them to modules.rst for
the autosummary.

'''
# python modules
import glob
import os
import re

# file that will be appended with scripts
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
    
with open(script_file, 'a') as f:
    for script in scripts:
        script = script[:-3] # To remove .py ending
        r = re.compile('.*' + script)
        if not list(filter(r.match, lines)):
           f.write('   /scripts/' + str(script) + '\n')
