import requests
import json
from src.plugins import PluginManager
from lib.conf.config import settings
from concurrent.futures import ThreadPoolExecutor
from lib.utils import encrypt,auth   #auth =API验证 encrypt=数据加密

class Base(object):
    def post_asset(self,server_info):
        data = encrypt(json.dumps(server_info))
        requests.post(
            url=settings.API,
            data=data,
            headers={'OpenKey': auth(), 'Content-Type': 'application/json'}
        )

class Agent(Base):

    def execute(self):
        server_info = PluginManager().exec_plugin()
        hostname = server_info['basic']['data']['hostname']
        certname = open(settings.CERT_PATH,'r',encoding='utf-8').read().strip()
        if not certname:
            with open(settings.CERT_PATH,'w',encoding='utf-8') as f:
                f.write(hostname)
        else:
            server_info['basic']['data']['hostname'] = certname

        self.post_asset(server_info)

class SSHSALT(Base):
    def get_host(self):
        # 获取未采集的主机列表：
        response = requests.get(settings.API)
        result = json.loads(response.text) # "{status:'True',data: ['c1.com','c2.com']}"
        if not result['status']:
            return
        return result['data']

    def run(self,host):
        server_info = PluginManager(host).exec_plugin()
        self.post_asset(server_info)

    def execute(self):

        host_list = self.get_host()
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(self.run,host)
