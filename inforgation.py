from modules import hunter
from modules import fofa
from modules import threatbook
from modules import shodan
from modules import _0zero
from modules import zoomeye
from modules import domain
from modules import output

from rich.traceback import install
from rich.console import Console
from configparser import ConfigParser

import argparse
import time
import sys

cfg = ConfigParser()
console = Console()
install(show_locals=True)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    console.print(r"""
 _        __                       _   _             
(_)_ __  / _| ___  _ __ __ _  __ _| |_(_) ___  _ __  
| | '_ \| |_ / _ \| '__/ _` |/ _` | __| |/ _ \| '_ \ 
| | | | |  _| (_) | | | (_| | (_| | |_| | (_) | | | |
|_|_| |_|_|  \___/|_|  \__, |\__,_|\__|_|\___/|_| |_|
Powered by Wrong-pixel |___/          version 0.3   
    """)
    # 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='ip', required=True, help='指定目标 IP')
    parser.add_argument('-o', dest='filename', help='导出报告的名称，默认为<IP+时间>.html，存放路径为output目录')
    args = parser.parse_args()

    # 预创建table，免得后面output报错
    hunter_table = fofa_table = threatbook_table = shodan_table = _0zero_table = zoomeye_table = None
    if args.ip:
        ip = args.ip
        config_file = 'config.ini'
        cfg.read(config_file, encoding='utf-8')
        # 鹰图查询结果
        if cfg['鹰图/hunter']['username'] == "" or cfg['鹰图/hunter']['apikey'] == "":
            console.print("[red][WRONG] 鹰图配置信息缺失！本次不予查询！")
        else:
            hunter = hunter.hunter(cfg['鹰图/hunter']['username'], cfg['鹰图/hunter']['apikey'])
            hunter_table = hunter.get_result(ip)
            console.print(hunter_table if hunter_table is not None else "")

        # fofa查询结果
        if cfg['fofa']['mail'] == "" or cfg['fofa']['apikey'] == "":
            console.print("[red][WRONG] fofa配置信息缺失！本次不予查询！")
        else:
            fofa = fofa.fofa(cfg['fofa']['mail'], cfg['fofa']['apikey'])
            fofa_table = fofa.get_result(ip)
            console.print(fofa_table if fofa_table is not None else "")

        # 微步查询结果
        if cfg['微步/weibu']['apikey'] == "":
            console.print("[red][WRONG] 微步配置信息缺失！本次不予查询！")
        else:
            threatbook = threatbook.threatbook(cfg['微步/weibu']['apikey'])
            threatbook_table = threatbook.get_result(ip)
            console.print(threatbook_table if threatbook_table is not None else "")

        # shodan查询结果
        if cfg['shodan']['apikey'] == "":
            console.print("[red][WRONG] shodan配置信息缺失！本次不予查询！")
        else:
            shodan = shodan.shodan(cfg['shodan']['apikey'])
            shodan_table = shodan.get_result(ip)
            console.print(shodan_table if shodan_table is not None else "")

        # 0zero查询结果
        if cfg['0zero']['apikey'] == "":
            console.print("[red][WRONG] 0zero配置信息缺失！本次不予查询！")
        else:
            _0zero = _0zero._0zero(cfg['0zero']['apikey'])
            _0zero_table = _0zero.get_result(ip)
            console.print(_0zero_table if _0zero_table is not None else "")

        # zoomeye查询结果
        if cfg['zoomeye']['apikey'] == "":
            console.print("[red][WRONG] zoomeye配置信息缺失！本次不予查询！")
        else:
            zoomeye = zoomeye.zoomeye(cfg['zoomeye']['apikey'])
            zoomeye_table = zoomeye.get_result(ip)
            console.print(zoomeye_table if zoomeye_table is not None else "")

    file_name = args.ip + "-" + time.strftime('%Y-%m-%d-%H:%M:%S')

    if args.filename:
        file_name = args.filename
    table_list = []
    domain_list = []
    if threatbook_table is not None:
        table_list.append({"微步": threatbook_table})

    if hunter_table is not None:
        table_list.append({"鹰图": hunter_table})
        domain_list += hunter.get_domain()

    if fofa_table is not None:
        table_list.append({"FOFA": fofa_table})
        domain_list += fofa.get_domain()

    if shodan_table is not None:
        table_list.append({"shodan": shodan_table})
        domain_list += shodan.get_domain()

    if _0zero_table is not None:
        table_list.append({"0zero": _0zero_table})

    if zoomeye_table is not None:
        table_list.append({"zoomeye": zoomeye_table})

    # 处理域名结果，暂时不准备封装成类了，因为get_domain方法是在每个模块类中定义的，如果需要抽象成类的话需要传入类对象
    # 不封白不封，传列表
    if domain_list:
        domain = domain.domain(list(set(domain_list)))
        domain_table = domain.get_result()
        if domain_table is not None:
            console.print(domain_table)
            table_list.append({"域名结果": domain_table})

    # 实例化
    output = output.output(args.ip, file_name, table_list)
    # 调用方法
    output.output_html()
    console.print("[green][INFO] 信息查询完毕，报告保存为%s/output/%s.html" % (sys.path[0], file_name))
