import os
import shutil
from lxml import etree, html
from pkg_resources import resource_string

from .parse import rst2xml, SlideMaker
from .position import position_slides
from .template import template_info_node
        
class ResourceResolver(etree.Resolver):
    
    def resolve(self, url, pubid, context):
        if url.startswith('resource:'):
            prefix, filename = url.split(':', 1)
            return self.resolve_string(resource_string(__name__, filename), context)
    
    
def rst2html(rststring, template_info, auto_console=False):
    # First convert reST to XML
    xml = rst2xml(rststring)
    tree = etree.fromstring(xml)
    
    # Fix up the resulting XML so it makes sense
    tree = SlideMaker(tree).walk()
    
    # TODO: Position all slides
    position_slides(tree)

    # Add the template info to the tree:
    tree.append(template_info_node(template_info))
    
    # If the console-should open automatically, set an attribute on the document:
    if auto_console:
        tree.attrib['auto-console'] = 'True'
                    
    # We need to set up a resolver for resources, so we can include the
    # reST.xsl file if so desired.
    parser = etree.XMLParser()
    parser.resolvers.add(ResourceResolver())
    
    # Transform the tree to HTML    
    xsl_tree = etree.fromstring(template_info['xsl'], parser)
    transformer = etree.XSLT(xsl_tree)
    tree = transformer(tree)
    result = html.tostring(tree)
    
    return template_info['doctype'] + result
    
def copy_files(template_info, destination):
    for file in template_info['files']:
        filepath = os.path.join(destination, file)
        directory_name, filename = os.path.split(filepath)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            
        with open(filepath, 'wb') as outfile:
            outfile.write(template_info['files'][file])
    
def copy_resource(filename, sourcedir, targetdir):
    if filename[0] == '/' or ':' in filename:
        # Absolute path or URI: Do nothing
        return
    sourcepath = os.path.join(sourcedir, filename)
    targetpath = os.path.join(targetdir, filename)
    
    if (os.path.exists(targetpath) and 
        os.path.getmtime(sourcepath) <= os.path.getmtime(targetpath)):
        # File has not changed since last copy, so skip.
        return
    targetdir = os.path.split(targetpath)[0]
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    
    shutil.copy2(sourcepath, targetpath)
