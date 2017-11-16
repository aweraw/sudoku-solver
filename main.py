import sys, os

# add this directory to the path - wsgi environment hack
bd = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(bd)
cfg = os.path.join(bd, 'config.ini')

import cherrypy
import re

from cherrypy import expose
from cherrypy.process.plugins import Daemonizer
from template import template
from sudoku import solve

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

if __name__ == '__main__':
    Daemonizer(cherrypy.engine).subscribe()
    cherrypy.quickstart(SudokuSolver(), config=cfg)
