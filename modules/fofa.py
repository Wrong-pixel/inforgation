import requests
from base64 import b64encode
from rich.table import Table
from rich.console import Console

console = Console()


class fofa:

    def __init__(self, mail, apikey):
        self.mail = mail
        self.apikey = apikey

    def get_result(self, ip, timeout=5):
        self.table = Table()
        console.rule('[green][INFO] 正在FOFA上查询 %s 的信息...' % ip)
        # base64编码查询语句
        words = b64encode(bytes(str(ip).encode())).decode()
        # 拼接url
        self.url = 'https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&fields=host,title,country_name,' \
                   'province,city,server,protocol,banner,isp'.format(
            self.mail, self.apikey, words)
        try:
            self.data = requests.get(self.url, timeout=timeout).json()
        except requests.ReadTimeout:
            console.print("[red][WRONG] 查询FOFA信息超时!")
            return None
        # api请求错误
        if self.data['error']:
            console.print("[red][WRONG] FOFA查询 %s 失败！" % ip)
            return None
        if self.data['size'] == 0:
            console.print("[yellow][WARNING] 没有在FOFA上查询到 %s 的相关信息！" % ip)
            return None
        self.table.add_column('host', justify="left")
        self.table.add_column('标题', justify="left")
        self.table.add_column('地理位置', justify="left")
        self.table.add_column('服务名', justify="left")
        self.table.add_column('协议', justify="left")
        for item in self.data['results']:
            self.table.add_row(item[0], item[1], item[2] + " " + item[3] + " " + item[4], item[5], item[6])
        return self.table
