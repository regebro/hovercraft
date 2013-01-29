import os
import configparser
from lxml import etree, html
from docutils.core import publish_string
from docutils.writers.docutils_xml import Writer
from pkg_resources import resource_string

def position_slides(tree):
    """Position the slides in the tree"""
    
    # For now, just put them side by side
    for count, step in enumerate(tree.findall('step')):
        step.attrib['data-y'] = str(0)
        step.attrib['data-x'] = str(1600*count)
    return tree
        
        
class ResourceResolver(etree.Resolver):
    
    def resolve(self, url, pubid, context):
        if url.startswith('resource:'):
            prefix, filename = url.split(':', 1)
            return self.resolve_string(resource_string(__name__, filename), context)
    
    
def rest2impress(rststring, template_info):
    # Get template information
    
    # First convert reST to XML
    xml = publish_string(rststring, writer=Writer())
    tree = etree.fromstring(xml)
    
    # Fix up the resulting XML so it makes sense
    tree = SlideMaker(tree).walk()
    
    # TODO: Position all slides
    position_slides(tree)

    # Transform to HTML
    
    # We need to set up a resolver for resources, so we can include the
    # reST.xsl file if so desired.
    parser = etree.XMLParser()
    parser.resolvers.add(ResourceResolver())
    
    xsl_tree = etree.fromstring(template_info['xsl'], parser)
    transformer = etree.XSLT(xsl_tree)
    tree = transformer(tree)
    result = html.tostring(tree)
    
    return result
    
def copy_files(template_info, destination):
    for file in template_info['files']:
        filepath = os.path.join(destination, file)
        directory_name, filename = os.path.split(filepath)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            
        with open(filepath, 'tw', encoding='UTF-8') as outfile:
            outfile.write(template_info['files'][file])
    