import modules
from modules import hunter
from modules import fofa
from modules import threatbook
from modules import shodan
from modules import _0zero
from modules import zoomeye
from modules import domain
from modules import output

from rich.traceback import install
from rich.table import Table
from rich.progress import track, Progress
from configparser import ConfigParser

import argparse
import time
import sys

cfg = ConfigParser()
progress = Progress()
install(show_locals=True)


# 忘了为啥把打印table的过程抽象成方法了。。。但是不影响用就不改了
def print_table(table: Table):
    progress.console.print(table if table is not None else "")


# 为了实现批量查询，需要将查询单个IP的过程抽象为方法，之后只要将需要批量查询的ip转化为列表，对列表中的每个元素调用方法就可以了
def get_single_ip(ip, file_name):
    progress.console.rule("[gray][INFO] 正在查询 %s 的情报" % ip)
    # 预先创建table对象，免得奇奇怪怪的报错
    hunter_table = fofa_table = threatbook_table = shodan_table = _0zero_table = zoomeye_table = None
    config_file = 'config.ini'
    cfg.read(config_file, encoding='utf-8')
    # 鹰图查询结果
    if cfg['鹰图/hunter']['username'] == "" or cfg['鹰图/hunter']['apikey'] == "":
        progress.console.print("[red][WRONG] 鹰图配置信息缺失！本次不予查询！")
    else:
        hunter = modules.hunter.hunter(cfg['鹰图/hunter']['username'], cfg['鹰图/hunter']['apikey'])
        hunter_table = hunter.get_result(ip)
        print_table(hunter_table)

    # fofa查询结果
    if cfg['fofa']['mail'] == "" or cfg['fofa']['apikey'] == "":
        progress.console.print("[red][WRONG] fofa配置信息缺失！本次不予查询！")
    else:
        fofa = modules.fofa.fofa(cfg['fofa']['mail'], cfg['fofa']['apikey'])
        fofa_table = fofa.get_result(ip)
        print_table(fofa_table)

    # 微步查询结果
    if cfg['微步/weibu']['apikey'] == "":
        progress.console.print("[red][WRONG] 微步配置信息缺失！本次不予查询！")
    else:
        threatbook = modules.threatbook.threatbook(cfg['微步/weibu']['apikey'])
        threatbook_table = threatbook.get_result(ip)
        print_table(threatbook_table)

    # shodan查询结果
    if cfg['shodan']['apikey'] == "":
        progress.console.print("[red][WRONG] shodan配置信息缺失！本次不予查询！")
    else:
        shodan = modules.shodan.shodan(cfg['shodan']['apikey'])
        shodan_table = shodan.get_result(ip)
        print_table(shodan_table)

    # 0zero查询结果
    if cfg['0zero']['apikey'] == "":
        progress.console.print("[red][WRONG] 0zero配置信息缺失！本次不予查询！")
    else:
        _0zero = modules._0zero._0zero(cfg['0zero']['apikey'])
        _0zero_table = _0zero.get_result(ip)
        print_table(_0zero_table)

    # zoomeye查询结果
    if cfg['zoomeye']['apikey'] == "":
        progress.console.print("[red][WRONG] zoomeye配置信息缺失！本次不予查询！")
    else:
        zoomeye = modules.zoomeye.zoomeye(cfg['zoomeye']['apikey'])
        zoomeye_table = zoomeye.get_result(ip)
        print_table(zoomeye_table)

    if file_name == "":
        file_name = ip + "-" + time.strftime('%Y-%m-%d-%H:%M:%S')

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
        domain = modules.domain.domain(list(set(domain_list)))
        domain_table = domain.get_result()
        if domain_table is not None:
            progress.console.print(domain_table)
            table_list.append({"域名结果": domain_table})

    output = modules.output.output(ip, file_name, table_list)
    # 调用方法
    output.output_html()
    progress.console.print("[green][INFO] 信息查询完毕，报告保存为%s/output/%s.html" % (sys.path[0], file_name))


# 为了实现批量查询，需要将单个查询的方法进行封装


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    progress.console.print(r"""
 _        __                       _   _             
(_)_ __  / _| ___  _ __ __ _  __ _| |_(_) ___  _ __  
| | '_ \| |_ / _ \| '__/ _` |/ _` | __| |/ _ \| '_ \ 
| | | | |  _| (_) | | | (_| | (_| | |_| | (_) | | | |
|_|_| |_|_|  \___/|_|  \__, |\__,_|\__|_|\___/|_| |_|
Powered by Wrong-pixel |___/          version 1.1   
    """)
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="蓝队信息聚合查询工具")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--ip', dest='ip', help='指定目标 IP')
    group.add_argument('-f', '--file', dest='ip_file', help='批量查询，将IP存放在文件中，一行一个')
    parser.add_argument('-o', '--output', dest='filename', help='导出报告的名称，默认为<IP+时间>.html，存放路径为output目录')
    args = parser.parse_args()
    # 单个IP的检测
    if args.ip:
        # 是否指定文件名
        filename = ""
        if args.filename:
            filename = args.filename
        # 调用方法实现单个IP的查询
        get_single_ip(args.ip, filename)

    # 这个我实在是没想好，是不是要用多线程，输出怎么显示，总之先试着写一写
    if args.ip_file:
        f = open(args.ip_file, 'r')
        # 去重，生成列表
        ip_list = list(set(f.read().split('\n')))
        try:
            # 去除空内容
            ip_list.remove("")
        except ValueError:
            pass
        # 单线程查询，多线程。。后面再做吧
        for ip in track(ip_list, description="正在进行批量查询"):
            get_single_ip(ip, file_name=ip)
