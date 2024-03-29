import sys
import os
import cherrypy
import re
import logging

from cherrypy import expose
from template import template
from sudoku import solve

# add this directory to the path - wsgi environment hack
bd = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(bd)
cfg = os.path.join(bd, 'config.ini')

e = re.compile('^[0-9]{81}$')

class SudokuSolver:

    @template('index.html')
    def index(self):
        return dict(cfg=cfg)

    @expose
    def solve(self, sudoku):
        if e.match(sudoku):
            solution = solve(sudoku)
            if solution.find('0') >= 0:
                return "No solution found"
            else:
                return solution
        else:
            return "Not a valid sudoku"


def error_404(status, message, traceback, version):
    return """<html>
  <head></head>
  <body><h2>Not Found</h2></body>
</html>"""


cherrypy.config.update({'error_page.404': error_404})

logger = logging.Logger('stdout')
cherrypy.log.access_log = logger
cherrypy.log.error_log = logger

if __name__ == '__main__':
    cherrypy.quickstart(SudokuSolver(), config=cfg)
