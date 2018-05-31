# python_script
**这是一些Python脚本**
* 不生成副本文件的前提下 在文件的指定位置 插入 删除 替换内容
* ansible-Python API
* 链接Redis
* Python格式化文件
* 发送邮件接口等
---
## 不占用大量内存，不生成副本文件的前提下 使用Python 对文件进行 插入 删除 替换
`指定位置插入`

`def add_host(file_name, host, group):
    print file_name, host, group
    res = {
        'status': True,
        'message': ''
    }
    file_name = './deploy/hosts' if not file_name else file_name
    try:
        i = 1
        with open(file_name, 'r') as f:
            with open(file_name, 'r+') as f_w:
                line = f.readline()
                while line:
                    if group in line:
                        f_w.seek(f.tell(), 0)
                        host = host + "\n"
                        f_w.write(host)
                        next_line = f.readline()
                        while next_line:
                            f_w.write(next_line)
                            next_line = f.readline()
                        f_w.truncate()
                        break
                    line = f.readline()
                    i += 1
    except IOError:
        res['status'] = False
        res['message'] = 'file wirte false！'
    return res
`指定位置删除`
def del_host(file_name, host, group):
    res = {
        'status': True,
        'message': ''
    }
    file_name = './deploy/hosts' if not file_name else file_name
    try:
        i = 1
        with open(file_name, 'r') as f:
            line = f.readline()
            # print f.tell()
            while line:
                if group in line:
                    _this = f.tell()
                    break
                line = f.readline()
                i += 1
            else:
                _this = False

        i = i + 1
        with open(file_name, 'r') as f_r:
            lines = f_r.readlines()
            f_r.seek(_this, 0)
            line = f_r.readline()
            while line:
                if "[" in line:
                    _end = f_r.tell()
                    break
                if i == len(lines):
                    print i, lines
                    _end = f_r.tell()
                    print 'last line', _end
                    break
                line = f_r.readline()
                i += 1
            else:
                _end = False
        # print 'start, end', _this, _end
        if _this == False:
            res['status'] = False
            res['message'] = 'start  false！'
        elif _end == False:
            res['status'] = False
            res['message'] = 'end  false！'
        elif _this == _end:
            res['status'] = False
            res['message'] = '_this == _end！'
        else:
            print 'start, end', _this, _end
            try:
                with open(file_name, 'r') as f_r:
                    with open(file_name, 'r+') as f_w:
                        f_r.seek(_this, 0)
                        line = f_r.readline()
                        host_list = []
                        while line and f_r.tell() <= _end:
                            host = "192.168.100.44" if not host else host
                            print(line, f_r.tell())
                            host_list.append(f_r.tell())
                            if line.strip().replace('/n', '') == host:
                                _host = f_r.tell()
                                print f_r.tell()
                                for i in host_list:
                                    if i == _host:
                                        now_location = host_list[host_list.index(i) - 1]
                                print 'now_location', now_location
                                print 'host it..', line, i
                                f_w.seek(now_location, 0)
                                # f_r.readline()
                                print 'i', i, line
                                next_line = f_r.readline()
                                print 'i--', i, next_line
                                # next_line = line
                                while next_line:
                                    # print 'next line', next_line
                                    f_w.write(next_line)
                                    next_line = f_r.readline()
                                # break
                                f_w.truncate()
                            line = f_r.readline()
            except Exception as e:
                res['status'] = False
                res['msg'] = e

    except Exception as e:
        res['status'] = False
        res['msg'] = e
    return res`
---
**格式化文本文件如下**
#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
import sys
print os.getcwd()

# os.environ.update({"DJANGO_SETTINGS_MODULE": "djapi.settings"})
# pro_dir = os.getcwd()  # 如果放在project目录，就不需要在配置绝对路径了
# sys.path.append('/Users/xiaofangl/Downloads/huasheng/hasan/djapi')
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'djapi.settings.settings'  # 项目的settings

import django
django.setup()
print sys.path
sys.path.append(os.path.dirname(__file__))
from app01.models import DnsHost
from app01.models import DnsFiles

# print (DnsFiles.objects.all())


"""
    执行脚本 并携带两个参数，第一个是ip地址，第二个是文件名,脚本跑完 生成的zone文件多一行回车 手动去掉
    将dns zone文件每行格式化
    host + '\t' + ' ' + 'IN' + '\t' + ' ' + type + '\t' + ' ' + value

"""
sou_namelist = {
    '172': ['zoneName', ''],
    '192': ['zoneName', '']
}

dis_namelist = ['172_huashenghaoche.com.zone', '192_huashenghaoche.com.zone', '192_huashenghaoche.net.zone',
             '192_huashenghaoche.work.zone']


# 执行脚本 并携带两个参数，第一个是ip地址，第二个是文件名
class FormatFiles(object):
    def __init__(self):
        # title = 'Reset Password' if not title else title
        self.source_host = sys.argv[1]
        self.source_filename = str(sys.argv[2])
        self.res = {}
        print self.source_filename, self.source_host

    # 将sou_name按格式生成dis_name
    def _gen_filename(self):
        ip = self.source_host.split('.')[0]
        name = self.source_filename
        dis_filename = ip + '_' + name
        return dis_filename

    # 格式化写入，this class not use!
    def _wirte_file(self, file_name, data):
        try:
            with open(file_name, 'w+') as f:
                f.write(data)
        except :
            self.res['status'] = False
            #loger.error('format_file write false!!')

    def _create_files(self, host, name, res, f):
        # f = False
        if f:
            try:
                reco = DnsHost.objects.filter(desc=host[0])
                for i in reco:
                    # print i.host, i.desc
                    f.file_to_host.add(i.id)
            except:
                res['status'] = False
                res['message'] = ' _create_files file failed ..'
        else:
            try:
                files = DnsFiles()
                files.filename = name
                files.save()
                reco = DnsHost.objects.filter(desc=host[0])
                for i in reco:
                    # print i.host, i.desc
                    files.file_to_host.add(i.id)

            except:
                res['status'] = False
                res['message'] = ' _create_files file failed ..'
        return res

    # 同步完文件后 写入数据库
    def _write_db_format_file(self):
        res = {
            'status': True,
            'message': ''
        }
        if '192' in self.source_host:
            host = []
            host.append('lan_dns主机组')
        elif '172' in self.source_host:
            host = []
            host.append('wan_dns主机组')
        f = DnsFiles.objects.filter(filename=self.source_filename)
        if f:
            is_f = DnsFiles.objects.get(filename=self.source_filename)
            res = self._create_files(host, self.source_filename, res, is_f)
        else:
            res = self._create_files(host, self.source_filename, res, f)
        return res

    # 读写文件把源文件格式化后写入新文件
    def _run_format_file(self):
        # 为真时的结果 if 判定条件 else 为假时的结果
        #self.source_filename if self.source_filename else self.source_filename = '172_huashenghaoche.com.zone'
        dis_name = self._gen_filename()
        resu = self._write_db_format_file()
        print '+++++++++++++++++++++++++++++++'
        print '_write_db_format_file', resu
        i = 1
        with open(self.source_filename, 'r') as f:
            with open('../' + dis_name, 'w+') as fw:
                line = f.readline()
                fw.write(line)
                while line:
                    line = f.readline()
                    i += 1
                    if i < 10:
                        fw.write(line)
                    elif i >= 10:
                        # print '------------------------------'
                        one_line = line.strip()
                        # print 'i:', i, one_line.split(' ')
                        one_line2 = one_line.replace('\t', ' ')
                        # print 'i:', i, one_line2.split(' ')
                        one_line3 = '\t '.join(filter(lambda x: x, one_line2.split(' ')))
                        # print 'i:', i, one_line3
                        if len(one_line3) > 0:
                            fw.write(one_line3)
                            fw.write('\n')

        print self.source_filename, '---', dis_name


# format_file = FormatFiles()
# format_file._run_format_file()


# 返回格式化数据，test
def test_file(name, dis_filename):
    print os.getcwd()
    res = {'status': True}
    i = 0
    try:
        with open(name, 'r') as f:
            tmp = []
            with open(dis_filename, 'w') as fw:
                line = f.readline()
                tmp.append(line)
                fw.write(line)
                while line:
                    line = f.readline()
                    i += 1
                    if i < 10:
                        fw.write(line)
                        tmp.append(line)
                    elif i >= 10:
                        #print '------------------------------'
                        one_line = line.strip()
                        #print 'i:', i, one_line.split(' ')
                        one_line2 = one_line.replace('\t', ' ')
                        #print 'i:', i, one_line2.split(' ')
                        one_line3 = '\t '.join(filter(lambda x: x, one_line2.split(' ')))
                        # print 'i:', i, one_line3
                        if len(one_line3) > 0:
                            tmp.append(one_line3)
                            fw.write(one_line3)
                            fw.write('\n')
            print len(tmp)
    except:
        res['status'] = False
        res['message'] = '格式化失败-->>test_file'
    # logging.info(res)
    return res


def write_in_db(host, names):
    res = {
        'status': True,
        'message': ''
    }
    print 'name', host, names, type(host)
    f = DnsFiles.objects.filter(filename=names)

    print 'write_in_db', f
    # res = self._create_files(host, self.source_filename, res, f)
    if f:
        try:
            reco = DnsHost.objects.filter(desc=host)
            for i in reco:
                print i.host, i.desc
                is_f = DnsFiles.objects.get(filename=names)
                is_f.file_to_host.add(i.id)
        except:
            res['status'] = False
            res['message'] = ' _create_files file failed ..'
    else:
        try:
            files = DnsFiles()
            files.filename = names
            files.save()
            reco = DnsHost.objects.filter(desc=host)
            for i in reco:
                print i.host, i.desc
                files.file_to_host.add(i.id)
        except:
            res['status'] = False
            res['message'] = ' _create_files file failed ..'
    return res


if __name__ == "__main__":
    format_file = FormatFiles()
    format_file._run_format_file()
    # test_file('../172_huashenghaoche.com.zone')
    # test = FormatFiles()


