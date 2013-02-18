import os
import shutil
from lxml import etree, html
from pkg_resources import resource_string

from .parse import rst2xml, SlideMaker
from .position import position_slides
from .template import CSS_RESOURCE
        
class ResourceResolver(etree.Resolver):
    
    def resolve(self, url, pubid, context):
        if url.startswith('resource:'):
            prefix, filename = url.split(':', 1)
            return self.resolve_string(resource_string(__name__, filename), context)
    
    
def rst2html(filepath, template_info, auto_console=False, skip_help=False, skip_notes=False):
    # Read the infile
    with open(filepath, 'rb') as infile:
        rststring = infile.read()
        
    presentation_dir = os.path.split(filepath)[0]
    
    # First convert reST to XML
    xml = rst2xml(rststring)
    tree = etree.fromstring(xml)
    
    # Fix up the resulting XML so it makes sense
    tree = SlideMaker(tree, skip_notes=skip_notes).walk()
    
    # Pick up CSS information from the tree:
    for attrib in tree.attrib:
        if attrib.startswith ('css'):
            if '-' in attrib:
                dummy, media = attrib.split('-', 1)
            else:
                media = 'screen,projection'
            template_info.add_resource(
                os.path.join(presentation_dir, tree.attrib[attrib]),
                CSS_RESOURCE,
                target=tree.attrib[attrib],
                extra_info=media)
    
    # Position all slides
    position_slides(tree)

    # Add the template info to the tree:
    tree.append(template_info.xml_node())
    
    # If the console-should open automatically, set an attribute on the document:
    if auto_console:
        tree.attrib['auto-console'] = 'True'

    # If the console-should open automatically, set an attribute on the document:
    if skip_help:
        tree.attrib['skip-help'] = 'True'
                    
    # We need to set up a resolver for resources, so we can include the
    # reST.xsl file if so desired.
    parser = etree.XMLParser()
    parser.resolvers.add(ResourceResolver())
    
    # Transform the tree to HTML    
    xsl_tree = etree.fromstring(template_info.xsl, parser)
    transformer = etree.XSLT(xsl_tree)
    tree = transformer(tree)
    result = html.tostring(tree)
    
    return template_info.doctype + result
        
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
