# coding:utf-8
import re
import collections
import commands
import pprint

class GetLinstor():
    def __init__(self,info):
        self.info = info
        self.reColor = re.compile('(\\x1b.*m(.*)\\x1b.*m)')
        self.reSpace = re.compile('( .*? \|)?')
        self.all_result = self.get_result()

    def get_result(self):
        lstN = []
        info_line = self.info.split('\n')
        for i in range(len(info_line)):
            if info_line[i].startswith('|') and '=' not in info_line[i]:
                result_line = self.reSpace.findall(info_line[i])
                self.clear_color(result_line)
                lstN.append(result_line)

        self.clear_info(lstN)
        return self.turn_dict(lstN)

    def clear_color(self,info_line):
        for idx in range(len(info_line)):
            ColorOrNot = self.reColor.findall(info_line[idx])
            if ColorOrNot:
                info_line[idx] = ColorOrNot[0][1]
            else:
                pass

    def clear_info(self,info_lst):
        for line in info_lst:
            for i in range(len(line)):
                if ' ' in line[i]:
                    line[i] = line[i].replace(' ', '')
                    line[i] = line[i].replace('|', '')
                else:
                    pass

        for line in info_lst:
            if line[0] == '':
                line.remove('')
            if line[-1] == '':
                del line[-1]
            if line[-1] == '':
                del line[-1]
            if line[-1] == '':
                del line[-1]

    def turn_dict(self,lst):
        list_all=[]
        list_key = lst[0]
        for n in range(len(lst)):
            if n > 0:
                list_value = lst[n]
                dic = collections.OrderedDict()
                for i in range(len(list_key)):
                    dic[list_key[i]] = list_value[i]
                list_all.append(dic)
        return list_all

    #Find 'Devicename' according to a Resourcename
    def Find_device_name(self,resourcename):
        for i in self.all_result:
            if resourcename in i.values():
                if i.get('DeviceName') != 'None':
                    device_name = i.get('DeviceName')
        return device_name

    #Count a certain type of quantity
    def count_type(self,info_type):
        n = 0
        for i in self.all_result:
            if info_type in i.values():
                n+=1
        return n