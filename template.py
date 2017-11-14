from __future__ import with_statement
from mako.template import Template
import os

base_dir = os.path.split(os.path.abspath(__file__))[0]
template_dir = os.path.join(base_dir, 'templates')

class template:

    def __init__(self, path):
        self.path = path

    def __call__(self, func):
        def f(*args,**kwargs):
            result = func(*args,**kwargs)
            if type(result) is not dict:
                raise ValueError('%s does not return type dict' % func)
            tpl_path = os.path.join(template_dir, self.path)
            with open(tpl_path) as tpl:
                return Template(tpl.read()).render(**result)

        f.exposed = True

        return f

