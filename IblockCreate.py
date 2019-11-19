# coding:utf-8
import sys
#import pexpect
#import 
import re
import time
#import cfg
#import configparser as cp
import subprocess
import commands
import pprint
import collections
import os
import crm_main as crm
import GetLinstor as gi

local_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#linstor create or delete resource definition/volume definition and resource
class LinstorCof():
	# ocfg = cp.ConfigParser(allow_novalue=True)
	# ocfg.read('cfg.ini')
	# iblock = ocfg.get('command','iblock_name')
	# size = ocfg.get('command','size')
	def __init__(self,name,size):
		self.iblock = name
		self.size = size
	reSUC = re.compile('SUCCESS')

	def matchS(self,str):
		if self.reSUC.search(str):
			return True
		else:
			if not os.path.exists('failed.log'):
				open('failed.log','w')
			fail_log = open('failed.log','a')
			fail_log.write('---------------' + local_time + '----------------')
			fail_log.write('\n')
			fail_log.write(str)
			fail_log.write('\n')
			fail_log.write('------------------------------')
			fail_log.write('\n')
			fail_log.close()

	#create linstor resource definition
	def linst_rd_c(self):
		output = commands.getoutput('linstor rd c ' + self.iblock)
		return self.matchS(output)

	#create linstor volume definition
	def linst_vd_c(self):
		output = commands.getoutput('linstor vd c ' + self.iblock + ' ' + self.size)
		return self.matchS(output)

	#create linstor resource 
	def linst_r_c(self):
		output = commands.getoutput('linstor r c '+ self.iblock + nodename + '--storage-pool '+ storage_pool)
		return self.matchS(output)

	#auto create linstor resource 
	def linst_r_c_auto(self):
		node_info = commands.getoutput('linstor n l')
		info = gi.GetLinstor(node_info)
		num = info.count_type('Online')
		output = commands.getoutput('linstor r c '+ self.iblock + ' --auto-place ' + str(num))
		return self.matchS(output)

	#delete linstor resource definition
	def linst_rd_d(self):
		output = commands.getoutput('linstor rd d ' + self.iblock)
		return self.matchS(output)

	#delete linstor resource definition
	def linst_vd_d(self):
		output = commands.getoutput('linstor vd d ' + self.iblock + ' 0')
		return self.matchS(output)

			
#create linstor resource and configured by pacemaker
def iblock_create(name,size):
	lst_cof = LinstorCof(name,size)
	resource_name = lst_cof.iblock
	rdc = lst_cof.linst_rd_c()
	if rdc:
		vdc = lst_cof.linst_vd_c()
		print 'rd create'
		if vdc:
			rc = lst_cof.linst_r_c_auto()
			print 'vd create'			
			if rc:
				res_info = commands.getoutput('linstor r lv')
				res_path = gi.GetLinstor(res_info)
				path = res_path.find_device_name(resource_name)
				return crm.main(resource_name, path)
				print 'gooooooooood'
			else:
				lst_cof.linst_vd_d()
				lst_cof.linst_rd_d()
		else:
			lst_cof.linst_rd_d()
			print 'vd not created so rd had deleted'

	else:
		return 





