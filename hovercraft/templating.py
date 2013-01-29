import os
import configparser
from lxml import etree, html
from docutils.core import publish_string
from docutils.writers.docutils_xml import Writer
from pkg_resources import resource_string    
    
def get_template_info(template=None):
    result = {'css': [], 'js-header':[], 'js-body': [], 'files': {} }

    # It it is a builtin template we use pkg_resources to find them.
    if template is None or template in ('default',):
        builtin_template = True
        if template is None:
            template = 'default'
        template = '/templates/%s/' % template
    else:
        builtin_template = False
        
        
    config = configparser.ConfigParser()
    if builtin_template:
        cfg_string = resource_string(__name__, template + 'template.cfg').decode('UTF-8')
        config.read_string(cfg_string)
    else:
        if os.path.isdir(template):
            template_root = template
            config_file = os.path.join(template, 'template.cfg')
        else:
            template_root = os.path.split(template)[0]
            config_file = template
        config.read(config_file)
    
    hovercraft = config['hovercraft']
    template_file = hovercraft['template']        

    # The template
    if builtin_template:
        xsl = resource_string(__name__, template + template_file)
    else:
        with open(os.path.join(template_root, template_file), 'rb') as xslfile:
            result['xsl'] = xslfile.read()
        
    # Screen CSS files:
    for key in hovercraft:
        if key.startswith('css'):
            # This is a css_file. The media can be specified, and defaults to 'screen,print,projection':
            if '-' in key:
                css, media = key.split('-')
            else:
                media = 'screen,print,projection'
            for file in hovercraft[key].split():
                result['css'].append((file, media))
                result['files'][file] = '' # Add the file to the file list. We'll read it later.
        if key in ('js-header', 'js-body'):
            for file in hovercraft[key].split():
                result[key].append(file)
                result['files'][file] = '' # Add the file to the file list. We'll read it later.
        if key == 'resources':
            for file in hovercraft[key].split():
                result['files'][file] = '' # Add the file to the file list. We'll read it later.
        
    for file in result['files']:
        if builtin_template:
            data = resource_string(__name__, template + file)
        else:
            with open(os.path.join(template_root, file), 'br') as infile:
                data = infile.read()
        result['files'][file] = data
        
    return result


def template_info_node(template_info):
    """Makes a template info node"""
    
    # The file data is ignored by template_info_node(). It would only be
    # meningful to include the actual file data if we want to embed the
    # css/js, but we don't, so we won't.
    
    node = etree.Element('templateinfo')
    header = etree.Element('header')
    node.append(header)
    for css in template_info['css']:
        header.append(etree.Element('css', attrib={'link': css[0], 'media': css[1]}))
    for js in template_info['js-header']:
        header.append(etree.Element('js', attrib={'link': js}))

    body = etree.Element('body')
    node.append(body)
    for js in template_info['js-body']:
        body.append(etree.Element('js', attrib={'link': js}))
    
    return node
                      
        
    
    