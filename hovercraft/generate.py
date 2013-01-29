import os
import configparser
from lxml import etree, html
from docutils.core import publish_string
from docutils.writers.docutils_xml import Writer
from pkg_resources import resource_string

from .parse import SlideMaker
from .position import position_slides
from .template import get_template_info, template_info_node
        
class ResourceResolver(etree.Resolver):
    
    def resolve(self, url, pubid, context):
        if url.startswith('resource:'):
            prefix, filename = url.split(':', 1)
            return self.resolve_string(resource_string(__name__, filename), context)
    
    
def rst2html(rststring, template_info):
    # First convert reST to XML
    xml = publish_string(rststring, writer=Writer())
    tree = etree.fromstring(xml)
    
    # Fix up the resulting XML so it makes sense
    tree = SlideMaker(tree).walk()
    
    # TODO: Position all slides
    position_slides(tree)

    # Add the template info to the tree:
    tree.append(template_info_node(template_info))
                    
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
            
        with open(filepath, 'bw') as outfile:
            outfile.write(template_info['files'][file])
    
    
def main(infile, outdir, template=None, extra_css=None, console=False):
    # Parse the template info
    template_info = get_template_info(template)

    # Read the infile
    with open(infile, 'rb') as infile:
        rst = infile.read()

    # Make the resulting HTML
    html = rst2html(rst, template_info)
    
    # Write the HTML out
    with open(os.path.join(outdir, 'index.html'), 'wb') as outfile:
        outfile.write(html)
        
    # Copy supporting files
    copy_files(template_info, outdir)
    