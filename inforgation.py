from modules import hunter
from modules import fofa
from modules import threatbook
from modules import shodan
from modules import _0zero
from modules import output
from modules import zoomeye

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
Powered by Wrong-pixel |___/          version 0.2   
    """)
    # 命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='ip', required=True, help='指定目标 IP')
    parser.add_argument('-o', dest='filename', help='导出报告的名称，默认为<IP+时间>.html，存放路径为output目录')
    args = parser.parse_args()

    if args.ip:
        ip = args.ip
        config_file = 'config.ini'
        cfg.read(config_file, encoding='utf-8')
        if cfg['鹰图/hunter']['username'] == "" or cfg['鹰图/hunter']['apikey'] == "":
            console.print("[red][WRONG] 鹰图配置信息缺失！本次不予查询！")
        else:
            hunter = hunter.hunter(cfg['鹰图/hunter']['username'], cfg['鹰图/hunter']['apikey'])
            # 鹰图查询结果
            hunter_table = hunter.get_result(ip)
            console.print(hunter_table if hunter_table is not None else "")

        if cfg['fofa']['mail'] == "" or cfg['fofa']['apikey'] == "":
            console.print("[red][WRONG] fofa配置信息缺失！本次不予查询！")
        else:
            fofa = fofa.fofa(cfg['fofa']['mail'], cfg['fofa']['apikey'])
            # fofa查询结果
            fofa_table = fofa.get_result(ip)
            console.print(fofa_table if fofa_table is not None else "")

        if cfg['微步/weibu']['apikey'] == "":
            console.print("[red][WRONG] 微步配置信息缺失！本次不予查询！")
        else:
            threatbook = threatbook.threatbook(cfg['微步/weibu']['apikey'])
            # 微步查询结果
            threatbook_table = threatbook.get_result(ip)
            console.print(threatbook_table if threatbook_table is not None else "")

        if cfg['shodan']['apikey'] == "":
            console.print("[red][WRONG] shodan配置信息缺失！本次不予查询！")
        else:
            shodan = shodan.shodan(cfg['shodan']['apikey'])
            # shodan查询结果
            shodan_table = shodan.get_result(ip)
            console.print(shodan_table if shodan_table is not None else "")

        if cfg['0zero']['apikey'] == "":
            console.print("[red][WRONG] 0zero配置信息缺失！本次不予查询！")
        else:
            _0zero = _0zero._0zero(cfg['0zero']['apikey'])
            # 0zero查询结果
            _0zero_table = _0zero.get_result(ip)
            console.print(_0zero_table if _0zero_table is not None else "")

        if cfg['zoomeye']['apikey'] == "":
            console.print("[red][WRONG] zoomeye配置信息缺失！本次不予查询！")
        else:
            zoomeye = zoomeye.zoomeye(cfg['zoomeye']['apikey'])
            # zoomeye查询结果
            zoomeye_table = zoomeye.get_result(ip)
            console.print(zoomeye_table if zoomeye_table is not None else "")

    file_name = args.ip + "-" + time.strftime('%Y-%m-%d-%H:%M:%S')

    if args.filename:
        file_name = args.filename
        table_list = []
    try:
        if threatbook_table is not None:
            table_list.append({"微步": threatbook_table})
    except BaseException:
        pass

    try:
        if hunter_table is not None:
            table_list.append({"鹰图": hunter_table})
    except BaseException:
        pass

    try:
        if fofa_table is not None:
            table_list.append({"FOFA": fofa_table})
    except BaseException:
        pass

    try:
        if shodan_table is not None:
            table_list.append({"shodan": shodan_table})
    except BaseException:
        pass

    try:
        if _0zero_table is not None:
            table_list.append({"0zero": _0zero_table})
    except BaseException:
        pass

    try:
        if zoomeye_table is not None:
            table_list.append({"zoomeye": zoomeye_table})
    except BaseException:
        pass

    output = output.output(args.ip, file_name, table_list)
    output.output_html()
    console.print("[green][INFO] 信息查询完毕，报告保存为%s/output/%s.html" % (sys.path[0], file_name))
