from docutils import nodes
from docutils.core import publish_string
from docutils.readers.standalone import Reader
from docutils.transforms.misc import Transitions
from docutils.writers.docutils_xml import Writer
from lxml import etree


class HovercraftTransitions(Transitions):

    @property
    def _doc_transitions(self):
        if not hasattr(self.document, '_transitions'):
            self.document._transitions = []
        return self.document._transitions

    def visit_transition(self, node):
        # First add the level of the transition as a class
        char = node.rawsource[0]
        if char not in self._doc_transitions:
            self._doc_transitions.append(char)
        level = self._doc_transitions.index(char) + 1
        node.attributes['level'] = str(level)

        index = node.parent.index(node)
        error = None
        # Here the default transformer complained if you had a transition as
        # the first thing in a section. I don't see why.
        if isinstance(node.parent[index - 1], nodes.transition):
            error = self.document.reporter.error(
                'At least one body element must separate transitions; '
                'adjacent transitions are not allowed.',
                source=node.source, line=node.line)
        if error:
            # Insert before node and update index.
            node.parent.insert(index, error)
            index += 1
        assert index < len(node.parent)
        if index != len(node.parent) - 1:
            # No need to move the node.
            return
        # Node behind which the transition is to be moved.
        sibling = node
        # While sibling is the last node of its parent.
        while index == len(sibling.parent) - 1:
            sibling = sibling.parent
            # If sibling is the whole document (i.e. it has no parent).
            if sibling.parent is None:
                # Transition at the end of document.  Do not move the
                # transition up, and place an error behind.
                error = self.document.reporter.error(
                    'Document may not end with a transition.',
                    line=node.line)
                node.parent.insert(node.parent.index(node) + 1, error)
                return
            index = sibling.parent.index(sibling)
        # Remove the original transition node.
        node.parent.remove(node)
        # Insert the transition after the sibling.
        sibling.parent.insert(index + 1, node)


class HovercraftReader(Reader):

    def get_transforms(self):
        transforms = Reader().get_transforms()
        transforms.remove(Transitions)
        transforms.append(HovercraftTransitions)
        return transforms


def rst2xml(rststring, source_path=None):
    reader = HovercraftReader()
    writer = Writer()
    result =  publish_string(rststring,
                          source_path=source_path,
                          reader=reader,
                          writer=writer,
                          settings_overrides={'syntax_highlight': 'short'})
    dependencies = reader.settings.record_dependencies.list
    return result, dependencies


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

    def __init__(self, intree, skip_notes=False):
        self.intree = intree
        self.result = None
        self.curnode = None
        self.steps = 0
        self.skip_notes = skip_notes
        self.skip_nodes = ('docinfo', 'field_list', 'field', 'field_body',)

    def _newstep(self, level):
        step = etree.Element('step', attrib={
            'step': str(self.steps),
            'class': 'step step-level-%s' % level,
        })
        self.steps += 1
        return step

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
            step = self._newstep(1)
            self.result.append(step)
            self.curnode = step

        # Then carry on as normal
        self.default_start(node)

    def start_transition(self, node):
        level = int(node.attrib['level'])
        step = self._newstep(level)
        # Walk back up to a transition of the same level
        curnode = self.curnode
        def get_level(clss):
            for cls in clss.split():
                # Skip unrelated classes, such as those added by the user.
                if cls.startswith('step-level-'):
                    return int(cls.split('-')[-1])
        while (curnode.tag != 'step' or
               get_level(curnode.attrib['class']) >= level):
            parent = curnode.getparent()
            if parent is None:
                # Top of tree
                break
            curnode = parent

        # This is the transition above the new transition.
        # Add the new transition to the end.
        curnode.append(step)
        self.curnode = step

    def end_transition(self, node):
        self.default_end(node)

    def start_field_name(self, node):
        # Fields are made into attribute, nothing to do here:.
        pass

    def end_field_name(self, node):
        # Fields are made into attributes
        pass

    def start_paragraph(self, node):
        # Fields are made into attributes.
        parent = node.getparent()
        if parent.tag == 'field_body':
            fieldname = parent.getprevious().text
            current = self.curnode.get(fieldname)
            if current:
                value = current + ' ' + node.text
            else:
                value = node.text
            self.curnode.set(fieldname, value)
        else:
            self.default_start(node)

    def end_paragraph(self, node):
        parent = node.getparent()
        if parent.tag != 'field_body':
            self.default_end(node)

    def start_note(self, node):
        if not self.skip_notes:
            return self.default_start(node)
        # Skip this node completely, including children:
        while len(node) > 0:
            del node[0]
