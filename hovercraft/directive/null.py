# TODO - Remove this file.  It is only here to demonstrate how to implement a
# directive plugin.
from docutils import nodes
from docutils.parsers.rst import Directive, directives


class Null(Directive):
    def run(self):
        para = nodes.paragraph(text='Example null directive')
        return [para]


def register(_):
    directives.register_directive('null', Null)
