import sys
import os
import json
import requests
import shlex, subprocess
# import SocketServer
# import BaseHTTPServer, SimpleHTTPServer
import ssl
import argparse
from datetime import datetime
if sys.version_info[0] == 2:
  import BaseHTTPServer
  import SimpleHTTPServer
  import SocketServer
elif sys.version_info[0] == 3:
  import http.server as SimpleHTTPServer
  import http.server as BaseHTTPServer
  import socketserver as SocketServer
else:
  raise Exception("Unknow Python")

from flask import Flask, request, send_file, abort

PYTHON_DEFAULT = 'python'+str(sys.version_info[0])
SETTING_METHOD = ""
SETTING = {}
#USERNAME = os.getlogin()                     ### WSL2 & systemd cannot call os.getlogin()
USERNAME = os.popen('whoami').read().strip()

DOWNLOAD_PATH = "/home/napat/flask-kidbright/static"
SUFFIX_DOMAIN = "wot.mecacloud.top"
API_URL = "https://api-wot.mes.meca.in.th"

def main():
  baseConfig = {}
  baseConfig['CONFIGS'] = {}
  script_dir = os.path.abspath( os.path.dirname( __file__ ) )
  # configFileName = script_dir + '/config.json'
  # baseConfig = readConfiguration(configFileName)

  baseConfig['CONFIGS']['API_TOKEN'] = SETTING['token']
  baseConfig['CONFIGS']['DOMAIN'] = SETTING['subdomain'] + '.' + SUFFIX_DOMAIN

  baseConfig['CONFIGS']['SCRIPT_DIR'] = script_dir
  baseConfig['CONFIGS']['API_URL'] = API_URL
  baseConfig['CONFIGS']['API_RECLAIM_TOKEN'] = ""
  baseConfig['CONFIGS']['EMAIL'] = ""

  validateConfig(baseConfig)
  initTunnels(baseConfig)

def runFlaskHTTPServer(port):
  app = Flask(__name__)

  @app.route('/hello')
  def hello():
    return 'Hello, World!'

  @app.route("/download", methods=["GET"])
  def handle_download():
    print("download model file")
    file = request.args.get("file")
    file_path = os.path.join(DOWNLOAD_PATH, file)
    print("Path: "+file_path)
    if not os.path.exists(file_path):
      abort(404)
    return send_file(file_path, as_attachment=True)

  app.run(host='0.0.0.0', port=port, debug=True)

def initTunnels(baseConfig):
  config = baseConfig['CONFIGS']
  port = '8000'
  
  print("Tunnel: www is overwritten by --local-server with default port: "+port)
  initTunnel(config, 'www', 'http', port)
  runFlaskHTTPServer(port)

def initTunnel(config, subdomain, protocol, port):
  frontend = " --frontend="+config['DOMAIN']+":80"
  service_on = " --service_on="+protocol+":"+subdomain+"."+config['DOMAIN']+":localhost:"+port+":"+config['API_TOKEN']
  command = PYTHON_DEFAULT+" "+config['SCRIPT_DIR']+"/pagekite.py --clean"+frontend+service_on
  args = shlex.split(command)
  p = subprocess.Popen(args)
  print('Initial TUNNEL for ['+subdomain+']: OK')


def validateConfig(baseConfig):
  config = baseConfig['CONFIGS']

  print('Velidate Domain: '+config['DOMAIN'])
  info = requests.get(config['API_URL']+'/info?token='+config['API_TOKEN'])
  # print(info.status_code)
  if info.status_code != 200:
    print('Validate Configuration: !!! Failed !!!')
  else:
    print('Validate Configuration: OK')

def setupArgument():
  global SETTING
  global SETTING_METHOD
  # parser = argparse.ArgumentParser(description="Just an example",
  #                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  # parser.add_argument("-init", action="store_true", help="Config the base configuration")
  # parser.add_argument("-run", action="store_true", help="Establish the tunnel connection")
  # parser.add_argument("--local-server", choices=['http', 'https'], help="Optional: Run local web server")
  # parser.add_argument("-sign-certificate", action="store_true", help="Sign wildcard certificate with let's encrypt")
  # parser.add_argument("-systemd", action="store_true", help="Generate systemd file. This Flag require --service-tunnel & --service-certificate")
  # parser.add_argument("--service-tunnel", metavar="TUNNEL_NAME", help="Generate service file for specific tunnel")
  # parser.add_argument("--service-certificate", action="store_true", help="Generate timer & service file to sign certificate")
  # parser.add_argument("-tunnel-list", action="store_true", help="List all tunnels")
  # parser.add_argument("-tunnel-add", metavar="TUNNEL_NAME", help="Add new tunnel. This Flag require --protocol & --port")
  # parser.add_argument("--protocol", choices=['raw', 'http', 'https'], help="Specify protocol of backend service")
  # parser.add_argument("--port", type=int, help="Specify port of backend service")
  # parser.add_argument("-tunnel-del", metavar="TUNNEL_NAME", help="Delete the specify tunnel")

  ### argument for kidbright
  parser = argparse.ArgumentParser(description="Just an example",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-token", metavar="token", help="Specify API_TOKEN", required=True)
  parser.add_argument("-subdomain", metavar="subdomain", help="Specify SUBDOMAIN", required=True)

  args = parser.parse_args()
  SETTING = vars(args)

setupArgument()
main()