"""
This is an example directive. To use this as a template for your own directive, create a new directory within the local_directives directory. Next move this file into the new directory and reanme it to __init__.py. While this file defines a video directive, it can be used as a skeleton to build any sort of directive you might need.

Directives
===========
Directives are a feature of reStructuredText which allow the basic markup to be extended. There are a number of builtin directives such as the image, code and math directives. The full list of builtin directives can be found at http://docutils.sourceforge.net/docs/ref/rst/directives.html

a directive follows the following pattern

.. DirectiveName:: arguments
        :option: option value

        Content

The only part of this pattern which is mandatory is ".. DirectiveName::". 

The example directive we are going to create is a video directive. It will have the following form:

    .. video:: filename
        :name: name_value
        :autoplay:

        * classname
        * classname2
        * etc...

If we were implementing a real video directive, it would make more sense to use an option to get a list of classes rather than parsing a list in the content section. However, we will parse the content section instead because it gives us a minimal example of parsing a directive's content. More realistic (and hence complicated) examples can be found in the Audio directive in local_directives/media/__init__.py and docutil's builtin list table directive (docutils/parsers/rst/directives/tables.py)

Parsing
========
Directives are included inside your reStructuredText file. Hovercraft passes this document to a programme called docutils to parse. Docutil parses the document into an internal node tree and then uses one of its inbuilt writers to write it out to an output format. Hovercraft request's docutil use its xml writer which creates (unsurprisingly) an xml output document. Hovercraft then uses another programme called lxml to convert that xml document into an html document using the conversion rules specified in the xslt file (template.xsl) stored in the template folder (or provided by the --template argument). Finally this hrml file is read by an internet browser (firefox, chrome, etc.) to actually produce our presentation

Thus the coversion of our directives into the final output we see on the screen is a long an complicated one. Luckily, we don't have to worry about most of these stages. The only stage that is of interest to us here is reST →  node tree. We also have control over two other stages (xml →  html, html →  presentation). These steps are controlled by an xslt file and js/css files respectively. See README.rst for information on these stages. 

This file uses python, a popular programming language, to define the way a directive should be converted into docutil's internal node tree. If you are not familiar with python there are many free resources available such as Alan Downey's fantastic 'Think Python'.
"""

# initial description of your module

# Author: Your name
# Copyright: MIT License

# tell docutils that we are using reStructuredText 
__docformat__ = 'reStructuredText'

# import some useful modules
import sys
import re
import langcodes
from urllib.parse import urlparse
from urllib.request import pathname2url
from docutils import nodes, utils
from docutils.nodes import fully_normalize_name, whitespace_normalize_name
from docutils.parsers.rst import Directive, directives, states
from docutils.parsers.rst.roles import set_classes
from mimetypes import guess_type
from distutils.util import strtobool
from tinycss2 import parse_declaration_list, ast 
from docutils.writers.docutils_xml import XMLTranslator

"""
Create nodes
=============

You do not need to create new nodes classes for all new directives, however, in some cases it will be necessary. Node classes define the sorts of objects that can exist within the node tree that docutils will build. Here we define a video class. When we come to the directive definition below, we will tell docutils to create a new node of class 'video' each time it come across one of our video directives.

There are a large number of builtin node classes. One of these will probably be appropriate for your needs. But if you can't find one that fits, chose the closest one that does and use it as a base class for the node class you are creating. Because videos are treated by html in a simlar way to images, we have used nodes.image as our base class here.

When should I register a new node class?
+++++++++++++++++++++++++++++++++++++++++

That's a great question, but not an easy one to answer definitively. Nodes (with certain exceptions, such as the pending node - see docutils' nodes.py for more) will be converted in a fairly straightforward manner into xml elements. The node name becomes the xml elements's name and the node's attributes become the xml element's attributes. These xml elements are then transformed by an xslt file into html. So the question is can you get the html output you want from the current contigent of xml elements?

For the video directvie we are currently building, we could make an xslt rule that says if there is an xml 'image' element with an attribute of "is_a_video", then produce an html <video> tag, otherwise produce an html <img> tag. This, however, is a bit ugly, and making a video node (and hence a video xml element) is much nicer.

Alternatively, if we were making a directive that takes some text in one language and translates it into an equivalent text in another language, the existing text node (nodes.Text) will do us just fine, and as a bonus we won't have to muck around with adding extra xslt rules either. 

A note on naming node classes
++++++++++++++++++++++++++++++
All the builtin node classes are all lower case (with the sole exception of the 'Text' class). Shortly we will create a 'Video' directive class. Using lower case for nodes and upper for directives makes it easier for others (including future you) to read your code.

"""

class video (nodes.image):
    pass

# Now that we have made a node class, we need to register the new class with docutils. _add_node_class_names() takes a single argument, a tuple with one or more strings representing class names.

nodes._add_node_class_names(('video'))

"""
Create Video directive class
=============================

This is the where the interesting stuff happens!

All directive classes should inheret from the 'Directive' class. This may be a direct inheretence (such as here) or via another directive class (eg. we could have used "class Video(Image)" instead. This inheretence allows us to define a couple of class attributes and then let docutils do the magic of transforming these attributes in pre-defined ways.

"""

class Media(Directive): 
    # First define a bunch of useful attributes. See docutils/parsers/rst/__init__.py for more info
    messages = [] # this will hold any errors we raise.
    required_arguments = 1 
    optional_arguments = 0 # if you want an unlimited number of arguments use sys.maxsize
    final_argument_whitespace = True

    """
    option_spec
    ============

    option_spec defines a directive's allowable options. It is made up of two parts, a 
    string representing the key. This is followed by the name of a funciton which will 
    be used to check the supplied value is appropriate. The key must not contain spaces.
    A list of useful functions can be found in docutils/parsers/rst/directives/__init__.py
    (from which the function directives.flag, used below, comes) 

    You can also make your own functions, in which case, because you aren't actually
    calling the function, but rather passing the functions name to docutils for it to
    call, you need to define the function above where you define option_spec (like we
    have done for unchanged(), below).

    To inheret the option_spec from a different directive class use 
    "option_spec = Media.option_spec.copy()". You can then add (or delete) from this
    inhereted option_spec using normal dictionary operations (eg.
    "option_spec['key'] = checking_function" or "del option_spec['key'].
    """

    def unchanged(arg):
        return arg
    option_spec = { 
        # the 'name' value is used by docutils to allow internal hyperlinks form elsewhere
        # in your reST document. Putting 'name' in option_spec isn't mandatory, but it can
        # be useful if it would make sense for users to be able to link to the output of
        # your directive from elsewhere in the document.
        'name': unchanged, 
        # note: because we are not calling this in an instance of the Media class, but rather
        # giving it to docutils to call, we reference the functions as "unchanged" rather 
        # than "self.unchanged()"
        'autoplay': directives.flag # raises error if any value is provided to 'autoplay'
    }

"""
run(self)
==========

This is the actual meat of the directive. This method is called to create each new instance of our Directive class. There are three things to do here. Play with your input, raise useful errors and finally create a node instance and pass your attributes to the node instance. 

Some potentially useful attributes that are created for you (thanks directive class!):
self.options: contains the values entered by the user after having been run through the functions defined in option_spec
self.content: a list made up of each line of content provided by the user (useful for debugging)
self.block_text: a copy of the whole directive the user entered (used in error messages)
"""
    def run(self): 
        # Play with our input
        if 'name' in self.options:
            if self.options['name'] in ('name', 'boringName', 'iCantThinkOfAName'):
                # This is great method available to any children of the Directive class.
                # it raises an error, but is not fatal (ie. it allows parsing to continue).
                self.state_machine.reporter.error(
                    '\nError parsing the "%s" directive: \n'
                    'The name you chose ("%s") is too boring. \n'
                    'Using "AwesomeName!!!" instead. \n'
                    % (self.name, self.options['name']),
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                self.options['name'] = 'AwesomeName!!!'
        
        # Parse content. See definition below.
        parse_content(self)

        # create media node and return system messages
        set_classes(self.options)
        # create an instance of the video node class called "video_node". This takes 
        # everything is self.options and turns them into attributes of video_node. 
        # Note: If you are using an inbuilt node class you will have to call it a 
        # nodes.class_name. 
        # Note: at present video_node is an orphan node, that is, it is not part of 
        # docutil's node tree.
        video_node = video(self.block_text, **self.options)
        # registers self.name which is the value of self.options['name'] if it has one,
        # or alternatively one automatically generated by docutils. This name allows
        # linking between various docutils nodes.
        self.add_name(video_node)
        """
        Returning our nodes
        ====================

        Video.run() was called by docutils/parsers/rst/states.py which is expecting a
        list. The list can contain lists of messages (self.messages) or nodes. Every 
        node is a potential node tree, so we can return more than just a single node
        if we like. For example, thed video directive implemented in local_directives/media
        returns a node tree that looks like this [video [[source, source, ...][track,
        track, ...]]]
        This ends up as html that looks like <video> <source \> <source \> <track />
        <track /> </video>. Thus, lists within lists represent parent-child node 
        relationships, whereas list items within a list represent sibling node
        relationships.
        Returning video_node connects our little orphan node branch onto the correct
        location within the node tree.
        """
        return self.messages + [video_node]

    def parse_content(self):
        # The key:value pairs in the dictionary self.options are converted by
        # docutils into node (and thence xml) attributes. So, we create a 'class'
        # key to hold our class values.
        self.options['class'] = []
        # create orphan container node for parsing
        node = nodes.Element() # Element is the most basic of all the node classes        
        # take content (defined as all text until a non-indented line is reached), 
        # parse it and then put the output into node
        self.state.nested_parse(self.content, self.content_offset, node)
        # If appropriate input has been given node should now be a list-like 
        # object of the following form:
        # [Element[bullet_list[list_item[paragraph[Text]]]]]
        # The text in each list item will be contained with the the leaf Text nodes.
        # However, goodness only know what users might do, so it is necessary to 
        # check that the sort of input you were expecting is the input you got.
        if self.check_for_list(node):
            for list_item in node[0]: # node[0] == bullet_list
                self.options['class'].append(list_item[0][0]) # list_item[0][0] == Text

    def check_for_list(self, node):
        if len(node) is 0: # user didn't input any content 
            return False
        elif len(node) > 1 or not isinstance(node[0], nodes.bullet_list):
            self.state_machine.reporter.error(
                'Error parsing content block for the "%s" directive: \n'
                'The only content allowed in %s directive is a single \n'
                'bullet list representing class names. '
                % (self.name, self.name),
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
        # So we are sure we have a bullet list, and nothing else,
        # but bullet lists can contain nested lists. We only want a 
        # flat list.
        for i in range(len(node[0])):
            list_item = node[0][i]
            if len(list_item) is not 1 or not isinstance(list_item[0], nodes.paragraph):
                self.state_machine.reporter.error(
                    'Error parsing content block for the "%s" directive: \n'
                    'single-level bullet list of %s tracks expected.'
                    % (self.name, self.name), nodes.literal_block(
                    self.block_text, self.block_text), line=self.lineno)
        return True # single level bullet list found

"""
Register directives
====================

Almost done! All that is left to do is register our new directive with docutils. This takes two arguments. The first is the sort of node the directive will return and the second is the name of the class that we have just defined. Note that when we defined our node class we called "nodes._add_node_class_names(('video'))". This added our node class to a list of possible node classes. The first argument of register_directive is used to look up this list.
"""

directives.register_directive('video', Video)

"""
All done! Congratulations! If you think your directive may be useful to other people, either directly or as an inspiration for similar directives, please upload it to the sandbox directory
"""
