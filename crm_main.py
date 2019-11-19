# coding:utf-8
'''
Created on Nov 6, 2019

@author: tianma
'''
import pre_param as p
import commands
import os

class Parameters(object):
    def __init__(self, l_name, path):
        # crm resources parameters
        self.l_name = l_name 
        self.t_iqn = None
        self.lun = None
        self.path = path
        self.g_name = None
        self.p_off_name = None
        self.vip = None
         
    def _get_l_name(self):             
        return self.l_name
    
    def _get_iqn(self):
        crm_conf_iqn = commands.getoutput('crm configure show | grep "params iqn="')
        self.t_iqn = p.get_iqn(crm_conf_iqn)
        return self.t_iqn
     
    def _get_lun_num(self):
        crm_conf_luns = commands.getoutput('crm configure show | grep "lun="')
        if crm_conf_luns == '':
            self.lun = 0
        else:
            l_list = p.get_lun_list(crm_conf_luns) # [0,1]
            self.lun = max(l_list) + 1
        return self.lun
    
    def _get_path(self):
        return self.path
     
    def _get_g_name(self):
        crm_conf_g = commands.getoutput('crm configure show | grep "group"')
        self.g_name = p.get_group_name(crm_conf_g)
        return self.g_name
     
    def _get_p_off_name(self):
        crm_conf_p_off = commands.getoutput('crm configure show | grep "portblock"')
        self.p_off_name = p.get_p_off_name(crm_conf_p_off)
        return self.p_off_name
     
    def _get_vip(self):        
        crm_conf_ip = commands.getoutput('crm configure show | grep "portals="')
        self.vip = p.get_IP(crm_conf_ip)
        return self.vip
    
    def get_param_list(self):
        # Return parameter list [l_name, t_iqn, lun, path, g_name, p_off_name, vip]
        param = []
        param.append(self._get_l_name())
        param.append(self._get_iqn())
        param.append(self._get_lun_num())
        param.append(self._get_path())
        param.append(self._get_g_name())
        param.append(self._get_p_off_name())
        param.append(self._get_vip())
        print param
        return param
        
        
def pre_parameters(name, path):
    # prepare parameters: [l_name, t_iqn, lun, path, g_name, p_off_name, vip]
    par = Parameters(name, path)
    p_list = par.get_param_list() 
    return p_list

def create_iSCSILUN(param):
    # execute iscsi_crm.sh to create iSCSILogicalUnit resource in Pacemaker
    l_name = param[0]
    t_iqn = param[1]
    lun = param[2]
    path = param[3]
    g_name = param[4]
    p_off_name = param[5]
    os.system("/home/klay1/tian/iscsi_crm5.sh %s %s %s %s %s %s" % (l_name, t_iqn, lun, path, g_name, p_off_name))

def check_st(l_name, lun, vip):
    # check whether iSCSI LUN is started or not, then give feedback
    def check_lun(name):
        crm_st = commands.getoutput('crm res show')
        return p.get_iscsi_st(crm_st, name)
        
    if check_lun(l_name) == 'Started':
        print "Createing iSCSI LUN %s (lun=%s) succeeded. Access Portal is %s" % (l_name, lun, vip)
        data_lict = [{"lun name":l_name, "lun ID":lun, "Access IP":vip}]
        print ("return value:", data_lict)
        return data_lict
    else:
        print "Creating iSCSI LUN FAILED..."
        return None

def main(name, path):
    param = pre_parameters(name, path)
    create_iSCSILUN(param)
    return check_st(param[0], param[2], param[6])

if __name__ == '__main__':
    name = "l_test1"
    path = "/dev/drbd1000"
    main(name, path)
    
