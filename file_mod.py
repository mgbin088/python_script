#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu


import re
import sys
import shlex
import time
import datetime
import subprocess


def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
        封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
        参数:
      cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
      timeout: 超时时间，秒，支持小数，精度0.1秒
      shell: 是否通过shell运行
    Returns: return_code
    Raises: Exception: 执行超时
    """
    res = {}
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    sub = subprocess.Popen(cmdstring_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while sub.poll() is None:
        line = sub.stdout.read()
        line = line.strip()
        tmp = line.split("\n")
        time.sleep(0.1)
        # print 'line', line
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)
    res['status'] = str(sub.returncode)
    res['data'] = tmp
    return res


def find_file(find_path):
    res = execute_command('ls -l %s' % find_path)
    res_test = ['1525322118686_082521', '1525322118687_082825', '1525336170089_082906', '1525343215147_073302', '1525343215150_082207', '1525411322548_070801', '1525411322548_073212', '1525411322549_072723', '1525411322549_074115', '1525411322549_074343', '1525411322549_075055', '1525411322549_075243', '1525411322549_080431', '1525411322549_080651', '1525411322549_080802', '1525411322550_074831', '1525411322550_204831', 'test.py']

    print '++++', res


def run_sort(find_path, data):
    res = []
    for i in data:
        same = []
        for c in data:
            if i.split("_")[0] == c.split("_")[0]:
                _i = i.split("_")[1]
                i_str = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", str(_i))
                same.append(int(i_str))
        same = set(same)
        biggest = sorted(same)[-1]
        _one = find_path + '/' + biggest
        res.append(_one)
    return res


# 存在问题，dest_path 目标目录要自动生成 不能写死 ！！！需求有异 要改
def move_mp4(src_path, dest_path):
    res = []
    for i in src_path:
        file_path = execute_command('find %s  -name "*.mp4"' % i)
        tmp = execute_command('mv %s %s' % file_path, dest_path)
        res.append(tmp)
    return res


def run_script():
    find_path = sys.argv[1]
    next_path_prefix = sys.argv[2]
    dest_path = sys.argv[3]
    file_list = find_file(find_path)
    if file_list:
        tmp = run_sort(find_path, file_list)
        if tmp:
            res = move_mp4(tmp, dest_path)
    return res


if __name__ == '__main__':
    run_script()
