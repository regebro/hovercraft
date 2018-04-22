import os
import tempfile
from collections import defaultdict

# import all directives defined in local_directives directory
d = os.path.dirname(os.path.realpath(__file__)) # local_directives directory
__all__ = [] # list of local directive modules
for item in os.listdir(d):
    if os.path.isdir(os.path.join(d, item)) and item != 'sandbox':
        __all__.append(item)
from . import *

# create dict with all supporting files for generate.py to import
sources = defaultdict(list)
for module in __all__:
    path = os.path.join(d, module)
    files = os.listdir(path)
    for f in files:
        if f.endswith('.css'):
            sources['css'].append(os.path.join(path, f))
        elif f.endswith('.js'):
            sources['js'].append(os.path.join(path, f))
        elif f.endswith('.xsl'):
            sources['xsl'].append([module.encode('utf-8'), f.encode('utf-8')])
        elif f.startswith('__') or f == 'README.rst' or os.path.isdir(f):
            pass
        else:
            sources['content'].append(os.path.join(path, f))

# Generate new xsl file which imports all directive xsl files.
# This is imported by template.xsl as directives.xsl
def generate_xsl():
    output = b''
    with open(d + '/start.xsl', 'rb') as f:
        output += f.read()
    for l in sources['xsl']:
        output = output + b'<xsl:import href="resource:local_directives/' + l[0] + b'/' + l[1] + b'" /> \n'
    with open(d + '/end.xsl', 'rb') as f:
        output += f.read()
    return output
