To create a new directive create a new directory inside the local_directives directory. In this new directory create __init__.py and use this to define your directive. Any css or js files in your directory will automatically linked to from hovercraft's output html and any xsl file will be automatically imported into your template's xsl file. Any other files (other than __init__.py or README.rst) will be copied into hovercraft's output directory. The content of any child directory within your directory will be ignored, and so can be safely used for your own purposes.

Note that instructions given in your directive's xslt file will overide the instructions given in templates/reST.xsl but will themself be overidden by instructions in your template.xsl file (if you have not specified a template templates/default/template.xsl is used). 

If you have not created a directive before, please see example.__init__.py

If you think your directive might be useful to others, please document it in a file called README.rst and upload it to sandbox/directives. If you think that it is so useful it should be included in the standard install, please not this in your pullrequest.
