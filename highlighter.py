import urllib
import web

import pygments
import pygments.lexers
import pygments.formatters

urls = (
  '/highlight', 'highlight',
  '/css', 'style'
)

class highlight:
  def GET(self):
    src_uri = web.input()['uri']
    src = urllib.urlopen(src_uri).read()
    return self._process(src)

  def POST(self):
    src = web.data()
    return self._process(src)

  def _process(self, src):
    params = web.input(bare='0', wrap='src',lineno='1')
    lang = params['lang']
    wrap = params['wrap']
    bare = int(params['bare'])
    lineno = int(params['lineno'])
    lexer = pygments.lexers.get_lexer_by_name(lang)
    formatter = pygments.formatters.HtmlFormatter(linenos=lineno, cssclass=wrap)
    formatted_code = pygments.highlight(src, lexer, formatter)
    if not bare:
      formatted_code = ''.join([
        '<html><head><link rel="stylesheet" href="/css?wrap=',
        wrap,
        '"/></head><body>',
        formatted_code,
        '</body></html>'
      ])
    return formatted_code

class style:
  def GET(self):
    elem_class = web.input(wrap='source')['wrap']
    web.header('Content-Type', 'text/css')
    return pygments.formatters.HtmlFormatter().get_style_defs('.'+elem_class)

app = web.application(urls, globals())

if __name__ == '__main__':
  app.run()

