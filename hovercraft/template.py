import os
import configparser
from lxml import etree
from pkg_resources import resource_string    
    
def get_template_info(template=None, extra_css=None):
    result = {'css': [], 
              'js-header':[], 
              'js-body': [], 
              'files': {}, 
              'resources': [],
              'doctype': b'<!DOCTYPE html>' }

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
        result['xsl'] = resource_string(__name__, template + template_file)
    else:
        with open(os.path.join(template_root, template_file), 'rb') as xslfile:
            result['xsl'] = xslfile.read()
    
    for key in hovercraft:
        # CSS files:
        if key.startswith('css'):
            # This is a css_file. The media can be specified, and defaults to 'all':
            if '-' in key:
                css, media = key.split('-')
            else:
                media = 'all'
            for file in hovercraft[key].split():
                result['css'].append((file, media))
                result['files'][file] = '' # Add the file to the file list. We'll read it later.

        # JS files:
        elif key in ('js-header', 'js-body'):
            for file in hovercraft[key].split():
                result[key].append(file)
                result['files'][file] = '' # Add the file to the file list. We'll read it later.

        # Other files:
        elif key == 'resources':
            for file in hovercraft[key].split():
                result['resources'].append(file) # Resorces can't be inlined.

        # And finally the optional doctype:
        elif key == 'doctype':
            result['doctype'] = hovercraft['doctype'].encode()
        
    # Load the file contents. We do this because this enables the template to
    # inline css and javascript.
    for file in result['files']:
        if builtin_template:
            data = resource_string(__name__, template + file)
        else:
            with open(os.path.join(template_root, file), 'br') as infile:
                data = infile.read()
        result['files'][file] = data

    if extra_css:
        filename = os.path.split(extra_css)[-1]
        target = 'css/' + filename
        result['css'].append((target, 'all'))
        with open(os.path.join(extra_css), 'br') as infile:
            result['files'][target] = infile.read()
        
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
        header.append(etree.Element('css', attrib={'href': css[0], 'media': css[1]}))
    for js in template_info['js-header']:
        header.append(etree.Element('js', attrib={'src': js}))

    body = etree.Element('body')
    node.append(body)
    for js in template_info['js-body']:
        body.append(etree.Element('js', attrib={'src': js}))
    
    return node
                      
        
    
    