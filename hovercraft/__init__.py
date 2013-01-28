from lxml import etree, html
from docutils.core import publish_string
from docutils.writers.docutils_xml import Writer
from pkg_resources import resource_string

def copy_node(node):
    """Makes a copy of a node with the same attributes and text, but no children."""
    element = node.makeelement(node.tag)
    element.text = node.text
    element.tail = node.tail
    for key, value in node.items():
        element.set(key, value)
        
    return element

class SlideMaker(object):
    """A docutils XML walker that will organize the XML into slides"""
    
    def __init__(self, intree):
        self.intree = intree
        self.result = None
        self.curnode = None
        self.steps = 0
        self.skip_nodes = ('docinfo', 'field_list', 'field', 'field_body',)

    def _newstep(self):
        step = etree.Element('step', attrib={'step': str(self.steps)})
        self.steps += 1
        self.result.append(step)
        self.curnode = step
        
    def walk(self):
        walken = etree.iterwalk(self.intree, events=('start', 'end'))
        for event, node in walken:
            if node.tag in self.skip_nodes:
                continue
            method = getattr(self, '%s_%s' % (event, node.tag), None)
            if method is None:
                if event == 'start':
                    self.default_start(node)
                else:
                    if event == 'end':
                        self.default_end(node)
            else:
                method(node)
                
        return self.result
                
    def default_start(self, node):
        new = copy_node(node)
        self.curnode.append(new)
        self.curnode = new
        
    def default_end(self, node):
        if self.curnode.tag != 'step':
            self.curnode = self.curnode.getparent()
                
    def start_document(self, node):
        self.curnode = self.result = copy_node(node)
        
    def start_section(self, node):
        # If there has been no transition by now, start a new step:
        if self.steps == 0:
            self._newstep()
        # Then carry on as normal
        self.default_start(node)

    def start_transition(self, node):
        self._newstep()
        
    def start_field_name(self, node):
        # Fields are made into attributes.
        self.curnode.set(node.text, '')

    def end_field_name(self, node):
        # Fields are made into attributes, nothing to do here:
        pass
    
    def start_paragraph(self, node):
        # Fields are made into attributes.
        parent = node.getparent()
        if parent.tag == 'field_body':
            fieldname = parent.getprevious().text
            self.curnode.set(fieldname, node.text)
        else:
            self.default_start(node)
            
    def end_paragraph(self, node):
        parent = node.getparent()
        if parent.tag != 'field_body':
            self.default_end(node)


def position_slides(tree):
    """Position the slides in the tree"""
    
    # For now, just put them side by side
    import pdb;pdb.set_trace()
    for count, step in enumerate(tree.findall('step')):
        step.attrib['data-y'] = str(0)
        step.attrib['data-x'] = str(1600*count)
    return tree
        
        
class ResourceResolver(etree.Resolver):
    
    def resolve(self, url, pubid, context):
        if url.startswith('resource:'):
            prefix, filename = url.split(':', 1)
            return self.resolve_string(resource_string(__name__, filename), context)
        
def rest2impress(rststring, template=None):
    # First convert reST to XML
    xml = publish_string(rststring, writer=Writer())
    tree = etree.fromstring(xml)
    
    # Fix up the resulting XML so it makes sense
    tree = SlideMaker(tree).walk()
    print(etree.tostring(tree))
    
    # TODO: Position all slides
    position_slides(tree)

    # Transform to HTML
    
    # We need to set up a resolver for resources, so we can include the
    # reST.xsl file if so desired.
    parser = etree.XMLParser()
    parser.resolvers.add(ResourceResolver())
    
    if template is None:
        xslt = resource_string(__name__, 'templates/default/template.xslt')
    else:
        xslt = open(template, 'rb').read()
        
    xsl_tree = etree.fromstring(xslt, parser)
    transformer = etree.XSLT(xsl_tree)
    tree = transformer(tree)
    return html.tostring(tree)
