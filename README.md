## About The Project
This project is python script to Pagekite Tunnel (HTTP, SSH over HTTP) with flask server. It adjust for run on notebook tool (e.g. colab).

### Installation
1. Install required packages.
`$ pip install certifi==2021.10.8 chardet==4.0.0 idna==2.10 requests==2.27.1 urllib3==1.26.9 argparse==1.2.1 flask`

2. Run tunnel with flask API on www.demo.wot.mecacloud.top
`$ python main.py -subdomain <sub-domain> -token <token> `
`$ python main.py -subdomain demo -token xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx    # example command` 
```
Velidate Domain: demo.wot.mecacloud.top
Validate Configuration: OK
Tunnel: www is overwritten by --local-server with default port: 8000
Initial TUNNEL for [www]: OK
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.30.193.129:8000
Press CTRL+C to quit
 * Restarting with stat
>>> Hello! This is pagekite.py v1.5.2.201011.                   [CTRL+C = Stop]
Velidate Domain: demo.wot.mecacloud.top..                                      
Validate Configuration: OK
Tunnel: www is overwritten by --local-server with default port: 8000
Initial TUNNEL for [www]: OK
 * Debugger is active!
 * Debugger PIN: 113-408-177
>>> Hello! This is pagekite.py v1.5.2.201011.                   [CTRL+C = Stop]
    Connecting to front-end relay 203.185.97.17:80 ...                         
     - Relay supports 3 protocols on 2 public ports.                           
     - Raw TCP/IP (HTTP proxied) kites are available.                          
     - To enable more logging, add option: --logfile=/path/to/logfile          
    Quota: You have plenty of time and bandwidth left.                         
~<> Flying localhost:8000 as http://www.demo.wot.mecacloud.top/                
    Connecting to front-end relay 203.185.97.17:80 ...                         
     - Relay supports 3 protocols on 2 public ports.                           
     - Raw TCP/IP (HTTP proxied) kites are available.                          
     - To enable more logging, add option: --logfile=/path/to/logfile                    
 << pagekite.py [flying]   Kites are flying and all is well.
```

### Testing
You can access webpage on http://www.demo.wot.mecacloud.top/hello
```
Hello, World!
```