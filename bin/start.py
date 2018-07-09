import os
import sys
import logging

bin_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.split(bin_path)[0]

src_path = os.path.join(root_path,'src')
config_path = os.path.join(root_path,'config')
static_path = os.path.join(root_path,'static')
templates_path = os.path.join(root_path,'templates')
log_path = os.path.join(root_path,'log')
append_path =(root_path,src_path,bin_path, config_path,static_path,templates_path,log_path)
sys.path.extend(append_path)

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='%s/MaterialWeb.log'%log_path,
        filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

import service as MaterialWeb

config = {}
config['static'] = static_path 
config['templates'] = templates_path
exec(open(os.path.join(config_path,'MaterialWeb.conf')).read(),config)

def start_server():
    print("start material web")
    MaterialWeb.start_http(config)

if __name__ == '__main__':
    start_server()

