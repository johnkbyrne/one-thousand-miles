from jinja2 import Environment, FileSystemLoader
from bokeh.resources import CDN
from bokeh.layouts import column
from bokeh.embed import file_html, server_session
from bokeh.server.server import Server
from bokeh.models import CheckboxGroup
from tornado.web import RequestHandler, StaticFileHandler
import pandas as pd
import os
import json
import pygsheets
import tornado
import plots
import authn
from extract import ExtractFromSheets
from functools import partial

# Load all the templates from the 'templates' directory
env = Environment(loader=FileSystemLoader('templates'))
PORT = int(os.environ.get('PORT', '5006'))
setting_string = os.environ.get('VCAP_APPLICATION')

def get_base_url():
     if setting_string is not None:
         setting = json.loads(setting_string)
         # uris = setting.get('application_uris')
         urls = None

         if uris is not None:
             uri = uris[0]
             return uri
         else:
             return 'localhost:{}'.format(PORT)

def get_protocol():
    if setting_string is not None:
        return 'https://'
    else:
        return 'http://'

class IndexHandler(RequestHandler):
  def get(self):
    user = self.get_secure_cookie("user")
    sid = self.get_secure_cookie("bkapp_sid")

    if (user is not None) and (sid is not None):
        username = tornado.escape.json_decode(user)
        if authn.isAuthenticated(username):
            self.redirect("/parking-permits")
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Incorrect credential")
            self.redirect("/login" + error_msg)
    else:
      error_msg = "?error=" + tornado.escape.url_escape("Please log in")
      self.redirect("/login" + error_msg)

class PlotsHandler(RequestHandler):
    def initialize(self, council_name, service, path, charts, all_pages, key):
      self.council_name = council_name
      self.service_name = service
      self.path = path
      self.charts = charts
      self.all_pages = all_pages

    def get(self):
        user = self.get_secure_cookie("user")
        sid = self.get_secure_cookie("bkapp_sid")

        if (user is not None) and (sid is not None):
            username = tornado.escape.json_decode(user)
            if authn.isAuthenticated(username):
                template = env.get_template('embed.html')
                links = []
                for path, config in self.all_pages.items():
                    if config['service'] != self.service_name:
                        links.append({"href": path, "caption": config['service']})



                sid = tornado.escape.json_decode(sid)
                script = server_session(None, sid, '{}{}{}'.format(get_protocol(), get_base_url(), self.path))

                self.write(template.render(
                  script=script,
                  asset_path='/assets/',
                  links=links,
                  council_name=self.council_name,
                  service_name=self.service_name
                ))
            else:
                error_msg = "?error=" + tornado.escape.url_escape("Incorrect credential")
                self.redirect("/login" + error_msg)
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Please log in")
            self.redirect("/login" + error_msg)

def create_plots(key, charts, doc):
    print(doc)
    with open('config/table_config.json') as tblcfg:
      ls_table = json.load(tblcfg)

    data_notts = ExtractFromSheets().get_data_from_sheets(key)
    data_notts_table = ExtractFromSheets().get_data_from_sheets(key)
    data_notts['Week commencing'] = pd.to_datetime(data_notts['Week commencing'])

    all_plots = []
    for chart, columns in charts.items():

        all_plots.append(plots.CouncilLineChart(data_notts, columns, chart))

        all_plots.insert(0, plots.CouncilDataTable(data_notts_table))

        elements = [*[plot.plot() for plot in all_plots]]
        doc.add_root(column(*elements))

if __name__ == '__main__':
    with open('verifylocal_modules.json') as lacfg:
        ls_metrics = json.load(lacfg)
    pages = []
    apps = {}

    for page, config in ls_metrics.items():
      apps['/{}-data'.format(page)]=partial(create_plots, config['key'], config['charts'])
      pages.append(('/{}'.format(page), PlotsHandler, {'path': '/{}-data'.format(page),'all_pages':ls_metrics, **config}))

    server = Server(apps,
    port=PORT,
    allow_websocket_origin=["{}".format(get_base_url())],
    extra_patterns = [
      ('/', IndexHandler),
      ('/login', authn.AuthLoginHandler),
      ('/logout', authn.AuthLogoutHandler),
      (r'/assets/(.*)', StaticFileHandler, {'path': './assets'}),
      *pages
    ],
    generate_session_ids = False,
    sign_sessions = True,
    secret_key = '7vchp9EInHrD11xgrdXT02gASwvoIQBIfoEUxVMaRRYx'
    )

    server._tornado.settings.update({'cookie_secret': "some super secret cookie and cake stuff"})
    server.start()
    print('Tornado created with embedded Bokeh server on {}{}/'.format(get_protocol(), get_base_url()))
    server.io_loop.start()
