# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#!/usr/bin/python3
# Copyright (c) 2023, System Level Solutions (India) Pvt. Ltd.
# 
# Purpose   : Chassis Manager Feature Test without CM serial connection
# Package   : python_scripts
# File name : CMInfoOverIpmi.py
# Author    : Alpesh Dhokia
# Project   : DELL CM
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import time
import textwrap
import re
import subprocess
import paramiko
import socket
import linecache
from datetime import datetime

now = datetime.now()
date0 = now.strftime("%d%m%y")
time0 = now.strftime("%H%M%S")
FILE_NAME = ""


PASS = "PASS"
FAIL = "FAIL"

CM_CONFIG_OL = {
        "CMCfg_LockInternalUseArea": "0x01",
        "CMCfg_FanControlMode": "0x02",
        "CMCfg_FanSpeedSetting": "0x03",
        "CMCfg_FanTypeConfig": "0x04",
        "CMCfg_SledConfig": "0x05",
        "CMCfg_FanZones": "0x06",
        "CMCfg_RequiredPSUsX": "0x07",
        "CMCfg_RedundantPSUsN": "0x08",
        "CMCfg_ReserveByte1": "0x09",
        "CMcfg_ReserveByte2": "0x0a",
        "CMcfg_ReserveByte3": "0x0b",
        "CMcfg_InletTempUpNCthres": "0x0c",
        "CMcfg_InletTempUpCCritThres": "0x0d",
        "CMcfg_MaxSledCount": "0x0e",
        "CMcfg_FanNormalReading": "0x0f",
        "CMcfg_FanUpCritReading": "0x10",
        "CMcfg_FanLowCritReading": "0x11",
        "CMcfg_ReserveWord1": "0x12",
        "CMcfg_ReserveWord2": "0x13",
        "CMcfg_ReserveWord3": "0x14",
        "CMcfg_ReserveWord4": "0x15",
        "CMcfg_ChassisPowerLimit": "0x16",
        "CMcfg_PowerCapActions": "0x17",
        "CMcfg_ChassisPowerCap": "0x18",
        "CMcfg_ChassisServiceTag": "0x19",
        "CMcfg_FTREnable": "0x1a",
        "CMCfg_ReserveByte4": "0x1b",
        "CMcfg_ReserveWord5": "0x1c",
        "CMCfg_ReserveByte5": "0x1d",
        "CMCfg_ReserveByte6": "0x1e"
        }

CM_CONFIG_HOOK = {
        "CMCfg_LockInternalUseArea": "0x01",
        "CMCfg_ReserveByte7": "0x02",
        "CMCfg_ReserveByte8": "0x03",
        "CMCfg_ReserveByte9": "0x04",
        "CMCfg_SledConfig": "0x05",
        "CMcfg_ReserveByte10": "0x06",
        "CMCfg_RequiredPSUsX": "0x07",
        "CMCfg_RedundantPSUsN": "0x08",
        "CMCfg_ReserveByte1": "0x09",
        "CMcfg_ReserveByte2": "0x0a",
        "CMcfg_ReserveByte3": "0x0b",
        "CMcfg_InletTempUpNCthres": "0x0c",
        "CMcfg_InletTempUpCCritThres": "0x0d",
        "CMcfg_MaxSledCount": "0x0e",
        "CMcfg_ReserveByte13": "0x0f",
        "CMcfg_ReserveByte14": "0x10",
        "CMcfg_ReserveByte15": "0x11",
        "CMcfg_ReserveWord1": "0x12",
        "CMcfg_ReserveWord2": "0x13",
        "CMcfg_ReserveWord3": "0x14",
        "CMcfg_ReserveWord4": "0x15",
        "CMcfg_ChassisPowerLimit": "0x16",
        "CMcfg_PowerCapActions": "0x17",
        "CMcfg_ChassisPowerCap": "0x18",
        "CMcfg_ChassisServiceTag": "0x19",
        "CMcfg_FTREnable": "0x1a",
        "CMCfg_ReserveByte4": "0x1b",
        "CMcfg_ReserveWord5": "0x1c",
        "CMCfg_ReserveByte5": "0x1d",
        "CMCfg_ReserveByte6": "0x1e"
        }

CM_CONFIG_AMC = {
        "CMCfg_LockInternalUseArea": "0x01",
        "CMCfg_FanControlMode": "0x02",
        "CMCfg_FanSpeedSetting": "0x03",
        "CMCfg_FanTypeConfig": "0x04",
        "CMCfg_SledConfig": "0x05",
        "CMCfg_FanZones": "0x06",
        "CMCfg_RequiredPSUsX": "0x07",
        "CMCfg_RedundantPSUsN": "0x08",
        "CMCfg_GridChassisICLEnable": "0x09",
        "CMcfg_ReserveByte2": "0x0a",
        "CMcfg_ReserveByte3": "0x0b",
        "CMcfg_InletTempUpNCthres": "0x0c",
        "CMcfg_InletTempUpCCritThres": "0x0d",
        "CMcfg_MaxSledCount": "0x0e",
        "CMcfg_FanNormalReading": "0x0f",
        "CMcfg_FanUpCritReading": "0x10",
        "CMcfg_FanLowCritReading": "0x11",
        "CMcfg_GridICL": "0x12",
        "CMcfg_ChassisICL": "0x13",
        "CMcfg_ReserveWord3": "0x14",
        "CMcfg_ReserveWord4": "0x15",
        "CMcfg_ChassisPowerLimit": "0x16",
        "CMcfg_PowerCapActions": "0x17",
        "CMcfg_ChassisPowerCap": "0x18",
        "CMcfg_ChassisServiceTag": "0x19",
        "CMcfg_FTREnable": "0x1a",
        "CMcfg_BpPresent": "0x1b",
        "CMcfg_BpId": "0x1c",
        "CMcfg_BVMSetting": "0x1d",
        "CMcfg_CableAmpLimit": "0x1e"
        }

CM_CONFIG_STEEDA = {
        "CMCfg_LockInternalUseArea": "0x01",
        "CMCfg_FanControlMode": "0x02",
        "CMCfg_FanSpeedSetting": "0x03",
        "CMCfg_FanTypeConfig": "0x04",
        "CMCfg_SledConfig": "0x05",
        "CMCfg_FanZones": "0x06",
        "CMCfg_RequiredPSUsX": "0x07",
        "CMCfg_RedundantPSUsN": "0x08",
        "CMCfg_ReserveByte1": "0x09",
        "CMcfg_ReserveByte2": "0x0a",
        "CMcfg_ReserveByte3": "0x0b",
        "CMcfg_InletTempUpNCthres": "0x0c",
        "CMcfg_InletTempUpCCritThres": "0x0d",
        "CMcfg_MaxSledCount": "0x0e",
        "CMcfg_FanNormalReading": "0x0f",
        "CMcfg_FanUpCritReading": "0x10",
        "CMcfg_FanLowCritReading": "0x11",
        "CMcfg_ReserveWord1": "0x12",
        "CMcfg_ReserveWord2": "0x13",
        "CMcfg_ReserveWord3": "0x14",
        "CMcfg_ReserveWord4": "0x15",
        "CMcfg_ChassisPowerLimit": "0x16",
        "CMcfg_PowerCapActions": "0x17",
        "CMcfg_ChassisPowerCap": "0x18",
        "CMcfg_ChassisServiceTag": "0x19",
        "CMcfg_FTREnable": "0x1a",
        "CMcfg_BpPresent": "0x1b",
        "CMcfg_BpId": "0x1c",
        "CMcfg_BVMSetting": "0x1d",
        "CMcfg_CableAmpLimit": "0x1e"
        }

FRU2_keys = ["Chassis_Area_Info_Version", "Chassis_Info_Area_Length",
            "Chassis_Type", "Chassis_Part_Number_Type_Length",
            "Chassis_Part_Number", "Chassis_Serial_Number",
            "Chassis_Serial_Number_Type_Length"]

FRU3_keys = ["Board_Area_Format_Version", "Board_Area_Length",
            "Language_Code", "Mfg_Date_Time",
            "Board_Manufacturer_Type_Length", "Board_Manufacturer",
            "Board_Product_Name_Type_Length", "Board_Product_Name",
            "Board_Part_Number_Type_Length",
            "Board_Part_Number_and_revision", 
            "FRU_File_ID_type_length", 
            "Additional_Custom_Mfg_Info_Type1_Length","ePPID",
            "Additional_Custom_Mfg_Info_Type2_Length","First_Power_On"]

FRU4_keys = ["Product_Area_Format_Version", "Product_Area_Length",
            "Language_Code", "Manufacturer_Type_Length", 
            "Board_Manufacturer", "Product_Name_Type_Length",
            "Product_Name", "Product_Part_Model_Type_Length_Description",
            "Product_Version_Type_Length","Product_Version", 
            "Product_Serial_Number_Type_Length",
            "Product_Serial_Number", "Asset_Tag_Type_Length","Asset_Tag"]


def usage():
        usage = textwrap.dedent('''
        ======================================================================
        usage : filename.py <sled_ip> <sled_username> <sled_password>		
        ======================================================================
        ''')
        print(usage)
        
def PrintException():  
    """
    This function is used to print exception due to which script is terminated.
    params:
        output: str
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print("EXCEPTION IN ({}, LINE {} '{}'): {}".format(filename, lineno, line.strip(), exc_obj))  

def log_output(output):
    """
    This function used to write logs in output file.
    params:
        output: bytes or str
    """
    try:
        with open(FILE_NAME, 'a+') as file:
            if type(output) is bytes:
                output = output.decode('cp1252')
            file.write(str(output))
            file.write("\n")
            # file.close()
    except IOError as e:
        print (("==> I/O error({0}): {1}").format(e.errno, e.strerror))
    except ValueError:
        print ("==> Could not convert data to an string.")
    except:
        print ("==> Unexpected error:", sys.exc_info()[0])
        raise RuntimeError('data saving failed')
    
def execute_ipmi_cmd( cmd, ip):
    """
    This function is used to execute ipmi command on command prompt.
    params:
        input: string
        output: bytes or str
    """
    prefix = "ipmitool -I lanplus -H {} -U {} -P {} ".format(ip,USERNAME,PASSWORD)
    ipmi_cmd = prefix + cmd
    # print(ipmi_cmd + "\n")
    MAX_ITERATIONS = 1
    i = 1
    while i <= MAX_ITERATIONS:
        p = subprocess.Popen(ipmi_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout:
            output += line.decode("utf-8")
        i += 1            
    return output

def SSH_connect(sled_ip):
    """
    This function is used to connect sled through SSH protocol.
    params:        
        output: bytes or str
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(sled_ip,
                                username=USERNAME,
                                password=PASSWORD)
    except paramiko.AuthenticationException:
        print("\nSSH Authentication failed: Check user id and password\n")
        sys.exit(1)
    except TimeoutError:
        print("\nSSH Server is not responding!\n"
                "Please check the server address or "
                "turn on the power of the server\n")
        sys.exit(1)
    ssh_shell = ssh_client.invoke_shell()
    ssh_shell.settimeout(10)
    return ssh_shell

def get_ssh_output(connection):
    """
    This function is used to get output through SSH protocol.
    params:   
        input: SSH connection     
        output: str
    """
    output = b""    
    while True:
        connection.settimeout(5)
        try:
            output += connection.recv(1024)
        except socket.timeout:
            break
    output = str(output, 'utf-8')
    return output

def send_ssh_cmd(cmd, connection):
    """
    This function is used to send command through SSH protocol.
    params:   
        input: str         
    """
    cmd = bytes(cmd + "\n", "utf-8")
    connection.sendall(cmd) 

def property_size(id):
    if id in range(18, 23):
        cfgPropSize = 2
    elif id == 25:
        cfgPropSize = 8
    elif id == 28:
        cfgPropSize = 2
    else:
        cfgPropSize = 1
    return cfgPropSize

def reboot_cm(sled_ip):
    cmd = "raw 0x6 0x34 0x45 0x70 0x18 0xC8 0x20 0x0 0x2 0xd8"
    output = execute_ipmi_cmd(cmd,sled_ip)
    print(output)
    if "Unable" in output:
        print("Not successful. ")
        return FAIL
    return output

def ipmitool_sled(sled_ip):
    print(" *Enter IPMI raw bytes only to execute IPMI command")
    print(" *Enter 'exit' for main page")
    while True:
        req_bytes = input()
        if req_bytes.lower() == "exit":
            break   
        cmd = "raw " + req_bytes
        output = execute_ipmi_cmd(cmd,sled_ip)
        print(output)
         
    return output

def rootshell_sled(sled_ip):   
    print(" *Enter iDRAC rootshell Command when promped") 
    print(" *Enter 'exit' for going back to main page")
    sled_ssh = SSH_connect(sled_ip)
    send_ssh_cmd("rootshell",sled_ssh)
    output = get_ssh_output(sled_ssh)
    print(output) 
    while True:
        cmd = input()
        if cmd.lower() == "exit":
            break   
        send_ssh_cmd(cmd,sled_ssh)
        output = get_ssh_output(sled_ssh)
        print(output)                
              
    sled_ssh.close()
    return output

def debuglog_sled(sled_ip):         
    sled_ssh = SSH_connect(sled_ip)
    send_ssh_cmd("rootshell",sled_ssh)
    output = get_ssh_output(sled_ssh)
    print(output) 
    dbg_ctrl = input("Enter debug control: ")
    send_ssh_cmd(dbg_ctrl,sled_ssh)
    output = get_ssh_output(sled_ssh)
    print(output)
    tail_cmd = input("Enter required tail/grep command: ")
    send_ssh_cmd(tail_cmd,sled_ssh)
    while True:
        time.sleep(5)
        output = get_ssh_output(sled_ssh)
        print(output) 
        exit_cmd = input(" *Enter 'exit' for going back to main page: ")  
        if exit_cmd.lower() == "exit":
            break               
    sled_ssh.close()
    return output

def reboot_sled(sled_ip):
    print("racadm racreset from sled :",sled_ip)
    sled_ssh = SSH_connect(sled_ip)
    send_ssh_cmd("racadm racreset",sled_ssh)
    output = get_ssh_output(sled_ssh)
    print(output)    
    if "Unable" in output:
        print("Not successful. ")
        return FAIL
    sled_ssh.close()
    return output

def powertest_sled(sled_ip):
    # print("racadm racreset from sled :",sled_ip)
    sled_ssh = SSH_connect(sled_ip)
    send_ssh_cmd("rootshell",sled_ssh)
    output = get_ssh_output(sled_ssh)
    send_ssh_cmd("scbmctest -s",sled_ssh)
    output = get_ssh_output(sled_ssh)
    print(output)    
    if "Unable" in output:
        print("Not successful. ")
        return FAIL
    send_ssh_cmd("powertest -p",sled_ssh)
    output = get_ssh_output(sled_ssh)
    print(output)    
    if "Unable" in output:
        print("Not successful. ")
        return FAIL
    sled_ssh.close()
    return output

def default_cm_config(sled_ip):
    cmd = "raw 0x6 0x34 0x45 0x70 0xC0 0xc8 0x20 0x0 0xC8 0x0 0x15 0x0 0x0 0x0 0x0 0xd8"
    output = execute_ipmi_cmd(cmd,sled_ip)
    print(output)
    if "Unable" in output:
        print("Not successful. ")
        return FAIL    
    return output

def set_chassisId(sled_ip):
    id = input("Enter 'CMCfg_ChassisID' value: ")
    output = set_hidden_config(sled_ip, "0x01", id)
    print(output)
    output_list = output.split()
    output_list = [output_list.remove(i) for i in output_list if i == ""]
    print(output_list)
    if "Unable" in output:
        print("\nUnable to execute set hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        return FAIL
    
def set_allow_fw_downgrade(sled_ip):
    value = input("Enter 'CMCfg_AllowFWDowngrade' value :")
    output = set_hidden_config(sled_ip, "0x02", value)
    print(output)
    output_list = output.split()
    output_list = [output_list.remove(i) for i in output_list if i == ""]
    print(output_list)
    if "Unable" in output:
        print("\nUnable to execute set hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        return FAIL

def set_connector_max_threshold(sled_ip):
    usage = """LSB MSB 
               0x10 0x04   (1040)
               0x64 0x00   (100)"""
    print(usage)
    value = input("Enter 'CMcfg_Connector_Max_Threshold' value: ")
    output = set_hidden_config(sled_ip, "0x03", value)
    print(output)
    output_list = output.split()
    output_list = [output_list.remove(i) for i in output_list if i == ""]
    if "Unable" in output:
        print("\nUnable to execute set hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        return FAIL

def set_golden_chassis(sled_ip):
    value = input("Enter 'CMcfg_GoldenChassis' value: ")
    output = set_hidden_config(sled_ip, "0x04", value)
    print(output)
    output_list = output.split()
    output_list = [output_list.remove(i) for i in output_list if i == ""]
    if "Unable" in output:
        print("\nUnable to execute set hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        return FAIL
    
def set_fixed_ftb(sled_ip):
    value = input("Enter 'CMcfg_Fixed_FTB' value: ")
    output = set_hidden_config(sled_ip, "0x05", value)
    print(output)
    output_list = output.split()
    output_list = [output_list.remove(i) for i in output_list if i == ""]
    if "Unable" in output:
        print("\nUnable to execute set hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        return FAIL

def set_manifest(sled_ip):
    value = input("Enter 'CMcfg_Manifest_Index_Number' value: ")
    output = set_hidden_config(sled_ip, "0x06", value)
    print(output)
    output_list = output.split()
    output_list = [output_list.remove(i) for i in output_list if i == ""]
    if "Unable" in output:
        print("\nUnable to execute set hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        return FAIL
    
def get_hidden_cfg(sled_ip):
    
    # Get the passcode:
    passcode = get_passcode(sled_ip)
    if passcode == "":
        print("\nFailed to get a passcode\n")
        sys.exit(0)
    print("\n Get_CM_hidden_property :\n")
    # Verify using get hidden config command:
    get_hidden_config_cmd = "raw 0x6 0x34 0x45 0x70 0xc8 0xc8 0x20 0x0 "\
                            "0x02 0x0 0x64 0x65 0x6c 0x6c 0x63 0x6d "\
                            "0x31 0x34 " + passcode + "0xFF 0xd8"
    output = execute_ipmi_cmd(get_hidden_config_cmd, sled_ip)
    print(output)
    if "Unable" in output:
        print("\nUnable to execute get hidden config IPMI cmd "
                "from sled: {}\n".format(sled_ip))
        sys.exit(0)

    data = []
    for line in output.splitlines():
        data += line.strip("\r\n").strip().split(" ")
    line7 = ""
    line8 = ""
    if PLATFORM == "Outlander":
        end_index = 26
        pwr_btn = data[9:end_index][14]
        wn_hb = data[9:end_index][16]
        line1 = "CMCfg_ChassisID               : 0x{}".format(data[9:end_index][1])
        line7 = "CMcfg_existing_PWRBTN_Status  : 0x{}".format(pwr_btn)
        line8 = "CMcfg_existing_Heartbeat_Status: 0x{}".format(wn_hb)
    elif PLATFORM == "AMC":
        end_index = 22
        line1 = "CMCfg_ChassisID               : 0x{} (Factory Mode Disable)".format(data[9:end_index][1])    
    else:
        end_index = 22
        line1 = "CMCfg_ChassisID               : 0x{}".format(data[9:end_index][1])
    
    hidden_config = data[9:end_index]     
    line2 = "CMCfg_AllowFWDowngrade        : 0x{} (Allowed)".format(hidden_config[3])
    line3 = "CMcfg_Connector_Max_Threshold : 0x{}".format(hidden_config[6] + hidden_config[5])
    line4 = "CMcfg_GoldenChassis           : 0x{}".format(hidden_config[8])
    line5 = "CMcfg_Fixed_FTB               : 0x{}".format(hidden_config[10])
    line6 = "CMcfg_Manifest_Index_Number   : 0x{}".format(hidden_config[12])
    
    txt1 = "\n".join(
                    [line1, line2, line3, line4, line5,line6,line7,line8]
                )
    
    data_str = """
Element Length = 0x30
Element Revision = 0x01
************************************

Hidden properties INFO::

"""
    data_str += txt1

    return data_str

def get_passcode(sled_ip):
    # Get the passcode:
    get_pass_cmd = "raw 0x6 0x34 0x45 0x70 0xc8 0xc8 0x20 0x0 0x01 "\
                    "0x64 0x65 0x6c 0x6c 0x63 0x6d 0x31 0x34 0xd8"

    output = execute_ipmi_cmd(get_pass_cmd, sled_ip)      
    if "Unable" in output:
        print("\nUnable to execute get passcode IPMI cmd "
                "on sled: {}\n".format(sled_ip))
        # sys.exit()
        return FAIL

    # 20 cc 14 70 00 01 00 38 46 a8 94 0f cf 6d 40 4a // passcode
    output = output.strip("\r\n").split(" ")
    passcode = ""
    for index in range(8, 16):
        passcode += "0x" + output[index] + " "
    # print("\nPASSCODE: {}\n".format(passcode))
    return passcode

def set_hidden_config(sled_ip, cfg_ID, cfg_val):
    # Get the passcode:
    passcode = get_passcode(sled_ip)
    if passcode == "":
        print("\nFailed to get a passcode\n")
        return FAIL
    # Set hidden config property:
    set_hidden_config_cmd = "raw 0x6 0x34 0x45 0x70 0xc8 0xc8 0x20 0x0 "\
                            "0x03 0x01 0x64 0x65 0x6c 0x6c 0x63 0x6d "\
                            "0x31 0x34 " + passcode + "0x01 " + cfg_ID +\
                            " " + cfg_val + " 0xd8"

    output = execute_ipmi_cmd(set_hidden_config_cmd, sled_ip)
    return output

def get_chas_power(sled_ip):
    print('\n Get Chassis Power Reading Command :\n')
    cmd = "raw 0x30 0x2E"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    # Act_GCPR_Data = {}
    GCPR_data = output.strip("\r\n").split(" ")
    GCPR_data = list(filter(None, GCPR_data))
    print(output)
    try:        
        support_bitmask = GCPR_data[4]  # Get the value of support bitmask byte        
        CTPC = int(GCPR_data[6] + GCPR_data[5], 16) # Get the value of CTPC byte        
        CIPC = int(GCPR_data[8] + GCPR_data[7], 16) # Get the value of CIPC byte        
        total_sleds = (GCPR_data[9])    # present numberof sleds
    except IndexError:
        print("\nUnable to fetch the result of " "GetChassisPowerReadings cmd!\n")
        return FAIL
    
    print(f"""                                             
        {'suppoerted bitmask ' :<40} : {support_bitmask:<5}    
        {'Chassis Total Power (dumpPSU Pout) ' :<40} : {CTPC:<5}  
        {'Chassis Infrastructure Power (HDD+Fan)' :<40} : {CIPC:<5} 
        {'Total Present Sleds ' :<40} : {total_sleds :<5}   
        """)
    return output

def set_chassis_servicetag(sled_ip):
    randomTag = input("ENTER SERVICE TAG TO SET:")
    servicetag = [hex(ord(char)) for char in randomTag]
    servicetag_len = hex(len(servicetag))
    servicetag = " ".join(servicetag)

    cmd = "raw 0x30 0x20 0x11 {} {}".format(servicetag_len, servicetag)
    # cmd = ("raw 0x6 0x34 0x45 0x70 0xc0 0xc8 0x20 0x0 0xa1 0x1 0x1 0x19 {} 0xd8".format(servicetag))
    output_set = execute_ipmi_cmd(cmd, sled_ip)
    print(output_set)
    if "Unable" in output_set:
        print("Command not successful. ",output_set)
        print("\nFailed to set servicetag using cmConfigSet command!\n")
        return FAIL
    return output_set

def get_device_id(sled_ip):
    print("\n GetDevice ID :\n")
    IPMI_cmd = "raw 0x6 0x34 0x45 0x70 0x18 0xC8 0x20 0x0 0x1 0xd8"
    output = execute_ipmi_cmd(IPMI_cmd, sled_ip)
    print(output)

    if "Unable" in output:        
        print("\nUnable to execute IPMI command on sled !\n")
        return FAIL

    getDevId_data = output.strip("\r\n").split(" ")
    getDevId_data = list(filter(None, getDevId_data))
    MAJOR_VER = int(getDevId_data[9], 16)
    MINOR_VER = int(getDevId_data[10], 16)
    CM_FW_VER = str(MAJOR_VER) + "." + str(MINOR_VER)
    print("\nCM FW version from getDevId cmd: {}\n".format(CM_FW_VER))
    return output

def get_chassis_servicetag(sled_ip):
    print("\n Get Chassis Serice Tag IPMI:\n")

    cmd = "raw 0x6 0x34 0x45 0x70 0xc0 0xc8 0x20 0x0 0xa0 0x0 0x1 0x19 0xd8"
    output_get = execute_ipmi_cmd(cmd,sled_ip)
    print(output_get)
    if "Unable" in output_get:
        print("Command not successful. ",output_get)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        return FAIL
    match = re.search("a0 00 01 01 ", output_get)
    if match:
        res = output_get[match.end():]
    res_list = res.split(" ")
    service_tag_len = res_list[0]
    print("Length of service tag: {}".format(service_tag_len))
    res_st = res_list[1:-1]
    service_tag = "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in res_st])
    print("Chassis Service Tag: ",service_tag)
    configData = output_get.split()
    configData = " ".join(configData)    

    return output_get

def fw_update_status_ipmi(sled_ip):
    print("\n Firmware Update Status IPMI:\n")
    cmd = "raw 0x6 0x34 0x45 0x70 0xc0 0xc8 0x20 0x00 0xa5 0x30 0x00 0xce 0xd8"
    output = execute_ipmi_cmd(cmd,sled_ip)
    print(output)
    data = {"00":"Transmitting Image",
            "01":"Validating Image",
            "02":"Programming/Updating in progress",
            "80":"General Error",
            "81":"Cannot establish connection",
            "82":"Path not found",
            "83":"Transmission Abort",
            "84":"Checksum Error",
            "85":"Incorrect Platform",
            "86":"Allocate memory failed",
            "FF":"Complete"
            }
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    match = re.search(" a5 ", output)
    if match:
        res = output[match.end():]
    res_list = res.split(" ")
    for key in data.keys():
        if key == res_list[0]:
            print("     FW update status: {}  {}".format(res_list[0],data[key])) 
    if res_list[0] not in data.keys():
        print("     Undefined Status Found: ",res_list[0])       
    return output

def get_chassis_config(sled_ip):
    print("\n Get Chassi Config: \n")
    GCC_cmd = "raw 0x30 0x12" 
    Exp_ChassisCfg_Data = {
        "Request_Length_Byte": "21",
        "MC_FW_Major_Rev": "",
        "MC_FW_Minor_Rev": "",
        "Temp_Lookup_Table Major_Ver": "01",
        "Temp_Lookup_Table Minor_Ver": "00",
        "Rack_Id": "00",
        "Chassis_ID": "00",
        "Sled_ID": "",
        "SledConfig": "02",
        "LED_Support_Chassis": "00",
        "Temp_Sensors_Support": "01",
        "Inlet_Temp_Upper_NC_Threshold": "",
        "Inlet_Temp_Upper_C_Threshold": "",
        "Exhaust_Temp_Upper_NC_Threshold": "ff",
        "Exhaust_Temp_Upper_C_Threshold": "ff",
        "Power_Monitoring_Sensors_Support": "08",
        "PSU_Info": "c2",
        "HDD_Status_Support": "00",
        "Number_HDDs_Supported": "00",
        "Fan_Control_Support": "00",
        "Chassis_ID_Thermal_Throttling_Support": "08",
        "Fan_Types_Number": "01",
        "Type_1_Fans_Number": "08",
        "Type_1_Fans_Nominal_Reading": "",
        "Type_1_Fans_Normal_Max_Reading": "64",
        "Type_1_Fans_Normal_Min_Reading": "23",
        "Type_1_Fans_UC_Threshold": "",
        "Type_1_Fans_LC_Threshold": "",
        "Type_2_Fans_Number": "02",
        "Type_2_Fans_Nominal_Reading": "",
        "Type_2_Fans_Normal_Max_Reading": "64",
        "Type_2_Fans_Normal_Min_Reading": "23",
        "Type_2_Fans_UC_Threshold": "",
        "Type_2_Fans_LC_Threshold": "",
    }
    
    Act_ChassisCfg_Data = {}    
    # Execute Get Chassis Config command
    output = execute_ipmi_cmd(GCC_cmd, sled_ip)
    print(output)
    if "Unable" in output:
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        return FAIL       

    GCC_data = output.split()
    GCC_data = list(filter(None, GCC_data))
    # index = 2
    id = 0
    # Get the actual data returned by the BMC 
    prop = list(Exp_ChassisCfg_Data.keys())    
    for index in range(2,len(GCC_data)):
        Act_ChassisCfg_Data[prop[id]] = GCC_data[index]
        id = id + 1
    
    print(f"|{'Property':<40}|{'Value(Default)':^15}|{'Value(Hex)':^15}|{'Value(Dec)':^15}|")
    print(f"{'-'*90}")
    for key in Act_ChassisCfg_Data.keys(): 
        try:       
            print(f"|{key:<40}|{Exp_ChassisCfg_Data[key]:^15}|{Act_ChassisCfg_Data[key]:^15}|{int(Act_ChassisCfg_Data[key],16):^15}|") 
        except:
            print(f"|{key:<40}|{Exp_ChassisCfg_Data[key]:^15}|{Act_ChassisCfg_Data[key]:^15}|{'-':^15}|")

    return output

def chassis_power_cycle(sled_ip):
    print("Chassis Power Cycle IPMI:\n")
    # Execute chassis power cycle IPMI command
    cmd = "raw 0x6 0x34 0x45 0x70 0x00 0xc8 0x20 0x0 0x2 0x02 0xd8"
    output = execute_ipmi_cmd(cmd, sled_ip)
    if "Unable" in output:
        print("Failed to execute CPC IPMI command!")
        return FAIL
    print(output)
    return output

def get_sensor_info(sled_ip):
    print("\n Get Sensor Info: \n")
    cmd = "raw 0x30 0x16"
    output = execute_ipmi_cmd(cmd, sled_ip)
    if "Unable" in output:
        print("Failed to execute IPMI command!")
        return FAIL
    print(output)
    GSI_data = output.split()
    GSI_data = list(filter(None, GSI_data))
    act_sensor_info = {}
    sensor_info = {"SC-BMC protocol version":"01",
                "Checksum byte":"15",
                "Request data length":"2a/21",
                "FW update status":"ff",
                "Chassis Inlet Temp":"",
                "Chassis Exhaust Temp":"00",
                "Sled Power Reading LSB":"00",
                "Sled Power Reading MSB":"00",
                "Sled Iin Current Reading":"00",
                "Sled 12v Vin Reading":"00",
                "PSU Presence Byte":"03",
                "PSU Fault Byte":"00",
                "PSU 1 Pout LSB":"00",
                "PSU 1 Pout MSB":"00",
                "PSU 2 Pout LSB":"00",
                "PSU 2 Pout MSB":"00",
                "PSU 3 Pout LSB":"00",
                "PSU 3 Pout MSB":"00",
                "PSU 4 Pout LSB":"00",
                "PSU 4 Pout MSB":"00",
                "PSU 5 Pout LSB":"00",
                "PSU 5 Pout MSB":"00",
                "PSU 6 Pout LSB":"00",
                "PSU 6 Pout MSB":"00",
                "PSU 7 Pout LSB":"00",
                "PSU 7 Pout MSB":"00",
                "PSU 8 Pout LSB":"00",
                "PSU 8 Pout MSB":"00",
                "Chassis identification LED status":"",
                "Chassis Fault LED status":"",
                "PSU AC loss byte":"",
                "Reserved":"00",
                "Fan Control Scheme":"",
                }
    prop = list(sensor_info.keys())
    id = 0
    for key in sensor_info.keys():
        try:
            act_sensor_info[key] = GSI_data[id]
        except:
            pass
        id = id + 1
     
    if act_sensor_info["Fan Control Scheme"] != "00": 
        total_fans = 8
        if act_sensor_info["Request data length"] != "2a" and len(GSI_data) > 45:
            total_fans = 10
        for i in range(0,total_fans):
            sensor_info[f"Fan {i} Reading"] = "00"
            act_sensor_info[f"Fan {i} Reading"] = GSI_data[id]
            id = id + 1
            if (PLATFORM == "Outlander") and (i == 1):
                break
    for i in range(0,4):
        sensor_info[f"Time Stamp {i}"] = "00"
        act_sensor_info[f"Time Stamp {i}"] = GSI_data[id]
        id = id + 1
    print(f"|{'Property':<35} | {'Value(Default)':^15}|{'Value(Hex)':^15}|{'Value(Dec)':^15}|")
    print(f"{'-'*90}")
    for key in act_sensor_info.keys(): 
        try:       
            print(f"|{key:<35} | {sensor_info[key]:^15}|{act_sensor_info[key]:^15}|{int(act_sensor_info[key],16):^15}|") 
        except:
            pass
    return output

def get_power_reading(sled_ip):
    print("\n Get Power Reading (Sled): \n")
    cmd = "raw 0x2c 0x02 0xdc 0x01 0x00 0x00"
    output = execute_ipmi_cmd(cmd, sled_ip)
    if "Unable" in output:
        print("Failed to execute CPC IPMI command!")
        return FAIL
    print(output)
    GPR_data = output.split()
    GPR_data = list(filter(None, GPR_data))
    sled_power = GPR_data[8]+GPR_data[7]
    print(f"""
    {'Sled Power(Hex)'} = {sled_power}h
    {'Sled Power(Dec)'} = {int(sled_power,16)}
    """)
    return output

def psu_extended_info(sled_ip,flag):
    # print("\n Get PSU Extended Info: \n")
    cmd = "raw 0x6 0x34 0x45 0x70 0xc0 0xc8 0x20 0x00 0xa3 0x30 0x0 0xd0 0xd8"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    # print(output)   
    fix_bytes = "20 c4 1c 70 00 a3 "
    match = re.search(fix_bytes, output)
    res = output[match.end():]
    res_list = res.split(" ")  
    for i in range(len(res_list)):
        res_list[i] = res_list[i].strip().strip("\r\n")    
    # print(res_list)
    act_extended_info = {}
    extended_info = {"Completion code":"00",
                    "SC-BMC protocol version":"30",
                    "Checksum byte":"20",
                    "Request data length":"3a",
                    "Payload Type":"02",
                    "Number of PSUs":"02",
                    "PSU-0 Index-":"00",
                    "PSU Input Current I- In":"0000",
                    "PSU Input Voltage V-In":"0000",
                    "PSU Input Rate Wattage":"0000",
                    "PSU Output Rate Wattage":"0000",
                    "PSU Actual Input Wattage":"0000",
                    "PSU Actual Output Wattage":"0000",
                    "PSU line Status":"02",
                    "PSU FW Version":"000000",
                    "PSU Input Type(AC/DC)":"02",
                    "PSU Length Byte":"09",
                    "PSU Part No. + HW rev":"xxx"
                }
    info_update = {"PSU-1 Index-":"01",
                    "PSU1 Input Current I- In":"0000",
                    "PSU1 Input Voltage V-In":"0000",
                    "PSU1 Input Rate Wattage":"0000",
                    "PSU1 Output Rate Wattage":"0000",
                    "PSU1 Actual Input Wattage":"0000",
                    "PSU1 Actual Output Wattage":"0000",
                    "PSU1 line Status":"02",
                    "PSU1 FW Version":"000000",
                    "PSU1 Input Type(AC/DC)":"02",
                    "PSU1 Length Byte":"09",
                    "PSU1 Part No. + HW rev":"xxx"
                }
    prop = list(extended_info.keys())
    id = 0
    for key in extended_info.keys():  
        if extended_info[key] == "xxx":
            value = ""            
            for _ in range(0,9):
                value = value + res_list[id]
                id = id + 1
            act_extended_info[key] = value      
        elif len(extended_info[key])/2 == 2:
            value = res_list[id+1] + res_list[id]
            act_extended_info[key] = value
            id = id + 2
        elif len(extended_info[key])/2 == 3:
            value = res_list[id]+res_list[id+1]+res_list[id+2] 
            act_extended_info[key] = value
            id = id + 3        
        else:           
            act_extended_info[key] = res_list[id]            
            id = id + 1                
    
    if res_list[id] == "01":        
        extended_info.update(info_update)
        for key in info_update.keys():
            if extended_info[key] == "xxx":
                value = ""                
                for _ in range(0,9):
                    value = value + res_list[id]
                    id = id + 1
                act_extended_info[key] = value
            elif len(extended_info[key])/2 == 2:
                value = res_list[id+1] + res_list[id]
                act_extended_info[key] = value
                id = id + 2
            elif len(extended_info[key])/2 == 3:
                value = res_list[id]+res_list[id+1]+res_list[id+2] 
                act_extended_info[key] = value
                id = id + 3            
            else:
                act_extended_info[key] = res_list[id]
                id = id + 1            
    
    if flag == False:
        return act_extended_info  
    else: 
        print("\n Get PSU Extended Info: \n")
        print(output)                   
        print(f"|{'Property':<30}|{'Value Info':^15}|{'Value(Hex)':^20}|{'Value(Dec)':^20}|")    
        print(f"{'-'*90}")
        for key in act_extended_info.keys():   
            try:     
                print(f"|{key:<30}|{extended_info[key]:^15}|{act_extended_info[key]:^20}|{int(act_extended_info[key],16):^20}|")            
            except:
                print(f"|{key:<30}|{extended_info[key]:^15}|{act_extended_info[key]:^20}|{'No decimal value':^20}|")            

        return act_extended_info

def sled_power_cycle(sled_ip):
    sled_id = input("Enter which sled to reseat(1/2/3/4) :")
    cmd = "raw 0x6 0x34 0x45 0x70 0x00 0xc8 0x20 0x0 0x2 0x{}2 0xd8".format(sled_id)
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    return output

def bmc_hard_reset(sled_ip):
    sled_id = input("Enter which sled to hard reset(1/2/3/4) :")
    cmd = "raw 0x6 0x34 0x45 0x70 0x00 0xc8 0x20 0x0 0x2 0x{}6 0xd8".format(sled_id)
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    return output

def sled_info(sled_ip):
    print("\n Get Sled/BMC Info: \n")
    cmd = "mc info"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    return output

def sel_logs_idrac(sled_ip):
    print(f"\n Get SEL logs from {sled_ip} : \n")
    cmd = "sel list"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    return output

def sensor_data_idrac(sled_ip):
    print(f"\n Get sensor data from {sled_ip} : \n")
    cmd = "sensor"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    return output

def data_repository_idrac(sled_ip):
    print(f"\n Get data repository from {sled_ip} : \n")
    cmd = "sdr"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    return output

def get_psu_info(sled_ip):
    print("\n Get PSU Info: \n")
    cmd = "raw 0x30 0x1F"
    output = execute_ipmi_cmd(cmd,sled_ip)
    if "Unable" in output:
        print("Command not successful. ",output)
        print("\nFailed to execute the cmd on sled: {}\n".format(sled_ip))
        # sys.exit(1)
        return FAIL
    print(output)
    GPI_data = output.split()
    GPI_data = list(filter(None, GPI_data))
    act_psu_info = {}
    psu_info = {"SC-BMC protocol version":"01",
                "Checksum byte":"d8",
                "Request data length":"08",
                "PSU mismatch sensor reading":"00",
                "PSU redundancy sensor reading":"00",
                "PSU configuration -X":"2",
                "PSU configuration -N":"0",
                "PSU 1 Max Pout value(9-10)":"",
                "PSU 2 Max Pout value(11-12)":""
                }
    prop = list(psu_info.keys())
    id = 0
    for index in range(0,len(GPI_data)-3):
        act_psu_info[prop[id]] = GPI_data[index]
        id = id + 1
    act_psu_info["PSU 1 Max Pout value(9-10)"] = GPI_data[8]+GPI_data[7]
    act_psu_info["PSU 2 Max Pout value(11-12)"] = GPI_data[10]+GPI_data[9]
    print(f"|{'Property':<30} | {'Value(Default)':^15}|{'Value(Hex)':^15}|{'Value(Dec)':^15}|")
    print(f"{'-'*80}")
    for key in act_psu_info.keys():        
        print(f"|{key:<30} | {psu_info[key]:^15}|{act_psu_info[key]:^15}|{int(act_psu_info[key],16):^15}|")  

    return output

def write_fru_data(sled_ip):
    Exp_FRU_Data = {
        "dumpFRU1" : ["0x23 0x00", "0x24 0x00", "0x25 0x00", "0x26 0x00",
                    "0x27 0x00", "0x28 0x00", "0x29 0x00", "0x2A 0x00",
                    "0x2B 0x00", "0x2C 0x00", "0x2D 0x00", "0x2E 0x00",
                    "0x2F 0x00", "0x30 0x00", "0x31 0x00", "0x32 0x00",
                    "0x33 0x00", "0x34 0x00", "0x35 0x00", "0x36 0x00",
                    "0x37 0x00", "0x38 0x00", "0x39 0x00", "0x3A 0x00",
                    "0x3B 0x00", "0x3C 0x00", "0x3D 0x00", "0x3E 0x00",
                    "0x3F 0x00", "0x40 0x00", "0x48 0x00", "0x49 0x00",
                    "0x4A 0x00", "0x4B 0x00", "0x4C 0x00", "0x4D 0x00"],

        "dumpFRU2" : ["0x50 0x00", "0x51 0x00", "0x52 0x00", "0x53 0x00",
                     "0x54 0x00", "0x5D 0x00", "0x5E 0x00"],
            
        "dumpFRU3" : ["0x70 0x00", "0x71 0x00", "0x72 0x00", "0x73 0x00",
                     "0x76 0x00", "0x77 0x00", "0x97 0x00", "0x98 0x00",
                     "0xA8 0x00", "0xAA 0x00", "0xB3 0x00", "0xB4 0x00", 
                     "0xB5 0x00",  "0xCC 0x00", "0xCD 0x00"],

        "dumpFRU4" : ["0xD8 0x00", "0xD9 0x00", "0xDA 0x00", "0xDB 0x00",
                     "0xDC 0x00", "0xFC 0x00", "0xFD 0x00", "0x16 0x01",
                     "0x34 0x00", "0x35 0x01", "0x38 0x01", "0x39 0x01", 
                     "0x42 0x01", "0x43 0x01"],
        }
    while True:
        address = input("Enter FRU property address (Two bytes LSB first):")
        try:
            address_list =list(filter(None, address.lower().split()))       
            address_list_len = len(address_list)
        except:
            print("Provide address in hex : E.g, 0x11 0xA0")
        if address_list_len == 2:
            break
        else:
            print("Provide required number of address bytes.")
           
    if address == "0x40 0x00":
        data_size = "0x08"
    elif address in ["0x73 0x00","0x35 0x01","0x97 0x00"]:
        data_size = "0x03"
    elif address in ["0x54 0x00","0x5E 0x00","0x77 0x00","0xAA 0x00","0xDC 0x00","0x39 0x01"]:
        data_size = "0x09"
    elif address == "0x98 0x00":
        data_size = "0x0E"
    elif address in ["0x98 0x00","0xFD 0x00","0x16 0x01","0x43 0x01", "0xB5 0x00"]:
        data_size = "0x0F"           
    else:
        data_size = "0x01"    
    
    while True:
        write_data = input("Enter {} bytes to write:".format(int(data_size,16))) 
        try:
            write_data_list =list(filter(None, write_data.lower().split()))       
            write_data_len = len(write_data_list)
        except:
            print("Provide data in hex : E.g, 0x11 0xA0")
        if write_data_len == int(data_size,16):
            break
        else:
            print("Provide required number of data bytes {}".format(int(data_size,16)))
    
    if PLATFORM == "Outlander":
        writeByte = "0x00"
    else:
        writeByte = "0x01"
    Write_FRU_Cmd = (
            "raw 0x6 0x34 0x45 0x70 0x28 0xc8 0x20 0x0 0x12 "
            "{} {} {} 0xff".format(writeByte, address, write_data)
        )
    output = execute_ipmi_cmd(Write_FRU_Cmd, sled_ip)
    # print(output + "\n")
    if "Unable" in output:
        print("\nFailed to execute Read FRU cmd!!\n")
        return FAIL
    print(output)
    FRU_write_Data = output.split()
    completion_code = FRU_write_Data[6]
    data_len_returned = int(FRU_write_Data[7], 16)
    data_returned = FRU_write_Data[8: -1]
    # data_returned = ["0x" + data for data in data_returned]
    # data_returned = " ".join(data_returned)
    
    if completion_code != "00":
        print("Failure completion code returned !")
        # return FAIL
    return output

def view_fru_ipmi(sled_ip):
    Act_FRU_data = {}
    Exp_FRU_Data = {
        "dumpFRU1" : ["0x23 0x00", "0x24 0x00", "0x25 0x00", "0x26 0x00",
                    "0x27 0x00", "0x28 0x00", "0x29 0x00", "0x2A 0x00",
                    "0x2B 0x00", "0x2C 0x00", "0x2D 0x00", "0x2E 0x00",
                    "0x2F 0x00", "0x30 0x00", "0x31 0x00", "0x32 0x00",
                    "0x33 0x00", "0x34 0x00", "0x35 0x00", "0x36 0x00",
                    "0x37 0x00", "0x38 0x00", "0x39 0x00", "0x3A 0x00",
                    "0x3B 0x00", "0x3C 0x00", "0x3D 0x00", "0x3E 0x00",
                    "0x3F 0x00", "0x40 0x00", "0x48 0x00", "0x49 0x00",
                    "0x4A 0x00", "0x4B 0x00", "0x4C 0x00", "0x4D 0x00"],

        "dumpFRU2" : ["0x50 0x00", "0x51 0x00", "0x52 0x00", "0x53 0x00",
                     "0x54 0x00", "0x5D 0x00", "0x5E 0x00"],
            
        "dumpFRU3" : ["0x70 0x00", "0x71 0x00", "0x72 0x00", "0x73 0x00",
                     "0x76 0x00", "0x77 0x00", "0x97 0x00", "0x98 0x00",
                     "0xA8 0x00", "0xAA 0x00", "0xB3 0x00", "0xB4 0x00", 
                     "0xB5 0x00",  "0xCC 0x00", "0xCD 0x00"],

        "dumpFRU4" : ["0xD8 0x00", "0xD9 0x00", "0xDA 0x00", "0xDB 0x00",
                     "0xDC 0x00", "0xFC 0x00", "0xFD 0x00", "0x16 0x01",
                     "0x34 0x00", "0x35 0x01", "0x38 0x01", "0x39 0x01", 
                     "0x42 0x01", "0x43 0x01"],
        }
    # Read and verify FRU data:
    for FRU in Exp_FRU_Data:
        dumpFRU = []
        for address in Exp_FRU_Data[FRU]: #Exp_FRU_Data["dumpFRU1"]:          
            if address == "0x40 0x00":
                data_size = "0x08"
            elif address in ["0x73 0x00","0x35 0x01"]:
                data_size = "0x03"
            elif address in ["0x54 0x00","0x5E 0x00","0x77 0x00","0xAA 0x00","0xDC 0x00","0x39 0x01"]:
                data_size = "0x09"
            elif address == "0x98 0x00":
                data_size = "0x0E"
            elif address in ["0x98 0x00","0xFD 0x00","0x16 0x01","0x43 0x01", "0xB5 0x00"]:
                data_size = "0x0F"           
            else:
                data_size = "0x01"    
            
            Read_FRU_Cmd = "raw 0x6 0x34 0x45 0x70 0x28 0xc8 0x20 0x0 0x11 "\
                            "0x0 {} {} 0xff".format(address, data_size)
            output = execute_ipmi_cmd(Read_FRU_Cmd, sled_ip)
            # print(output + "\n")
            if "Unable" in output:
                print("\nFailed to execute Read FRU cmd!!\n")
                return FAIL

            FRU_Read_Data = output.split()
            completion_code = FRU_Read_Data[6]
            data_len_returned = int(FRU_Read_Data[7], 16)
            data_returned = FRU_Read_Data[8: -1]
            # data_returned = ["0x" + data for data in data_returned]
            # data_returned = " ".join(data_returned)
            
            if completion_code != "00":
                print("Failure completion code returned !")
                return FAIL
            if data_len_returned != int(data_size, 16):
                print("\nInvalid data length returned!\n")
                return FAIL
            dumpFRU.append(data_returned)        
        if FRU == "dumpFRU1":
            dumpFRU[17]= dumpFRU[18]+dumpFRU[17]            
            dumpFRU[18]= dumpFRU[20]+dumpFRU[19]
            dumpFRU[19]= dumpFRU[22]+dumpFRU[21]
            dumpFRU[20]= dumpFRU[24]+dumpFRU[23]
            dumpFRU[21]= dumpFRU[26]+dumpFRU[25]            
            dumpFRU[32]= dumpFRU[33]+dumpFRU[32]  
            del dumpFRU[22:27]  
            del dumpFRU[28]        

        Act_FRU_data.update({FRU:dumpFRU})
    # print(Act_FRU_data)
    for FRU in Act_FRU_data: 
        data = []            
        print("\n\n $ {} \n".format(FRU))
        if FRU == "dumpFRU2":
            data = FRU2_keys
        elif FRU == "dumpFRU3":
            data = FRU3_keys
        elif FRU == "dumpFRU4":
            data = FRU4_keys
        else:
            if PLATFORM == "AMC":
                data = list(CM_CONFIG_AMC.keys())
            elif PLATFORM == "Outlander":
                data = list(CM_CONFIG_OL.keys())
            elif PLATFORM == "Hook":
                data = list(CM_CONFIG_HOOK.keys())
            else:
                data = list(CM_CONFIG_STEEDA.keys())

        for index in range(0,len(data)):
            if (len(Act_FRU_data[FRU][index]) > 2) and (data[index] != "Mfg_Date_Time"):                 
                final_value_bytes = " ".join([value for value in (Act_FRU_data[FRU][index])])
                final_value = "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in (Act_FRU_data[FRU][index])])   
                print(f" {data[index]:<35} : {final_value:<20} : [{final_value_bytes:<10}]")                                           
            else:
                final_value = " ".join([value for value in (Act_FRU_data[FRU][index])])     #Act_FRU_data[FRU][index][0]            
                print(f" {data[index]:<35} : {final_value:<10}")

    return Act_FRU_data

def getCMConfig(sled_ip):    
    # get chassis id hidden config property:
    getCMConfig_cmd = "raw 0x6 0x34 0x45 0x70 0xc0 0xc8 0x20 0x0 0xa0 0x0 0xff 0xd8"
    output = execute_ipmi_cmd(getCMConfig_cmd, sled_ip)
    
    spl_word = '20 c4 1c 70 00 a0 00 01 '  

    # Get String after first occurrence of substring
    match = re.search(spl_word, output)
    if match:
        res = output[match.end():]
    else:
        res = ''
    # print("String after the first occurrence of substring:", res)
    res_list = res.split(" ")
    # print(res_list)
    no_of_properties = int(res_list[0],16)
    print("Total Properties: {}".format(no_of_properties))
    bit_no = 1
    cmconfig_list = []
    while True:
        id = int(res_list[bit_no],16)
        property_data_size = property_size(id)
        cmconfig_list.append(res_list[bit_no+1 : bit_no+1+property_data_size])
        bit_no += property_data_size+1
        if bit_no > 75:
            break

    # print(cmconfig_list)

    cmconfig_dict = {
        "LockInternalUseArea" : {
            0 : "unlocked",
            1 : "locked"
        },
        "FanControlMode" : {
            0 : "Manual",
            1 : "OpenLoop",
            2 : "ClosedLoop",
            3 : "Liquid Immersion Cooling"
        },
        "FanTypeConfig" : {
            13 : "4fan,8tach,dual-rotor",
            18 : "1fan,2tach,dual-rotor",
            14 : "5fan,10tach,dual-rotor",
            15 : "4fan,8tach,dual-rotor"
        },
        "SledConfig" : {
            2 : "half-width",
            4 : "Double-high half-width"
        },
        "RedundantPSUsN" : {
            0 : "no redundancy",
            1 : "1+1 redundant config"
        },
        "PowerCapActions" : {
            1 : "log event in sled SEL",
            0 : "Nothing"
        },
        "FTREnable" : {
            1 : "Enable",
            0 : "Disable"
        },
        "BpPresent" : {
            1 : "Present",
            0 : "Absent"
        }

    }
    if PLATFORM == "Outlander":
        getCMConfig_OL = """
        $ getCMConfig

        INTERNAL USE AREA INFO::
        CMCfg_LockInternalUseArea     : {} : {}
        CMCfg_FanControlMode          : {} : {}
        CMCfg_FanSpeedSetting         : {}
        CMCfg_FanTypeConfig           : 0x{} : {}
        CMCfg_SledConfig              : {} : {}
        CMCfg_FanZones                : {}
        CMCfg_RequiredPSUsX           : {}
        CMCfg_RedundantPSUsN          : {} : {}
        CMCfg_ReserveByte1            : {} W
        CMcfg_ReserveByte2            : {} W
        CMcfg_ReserveByte3            : {} W
        CMcfg_InletTempUpNCthres      : {} Degree Celsius
        CMcfg_InletTempUpCCritThres   : {} Degree Celsius
        CMcfg_MaxSledCount            : {}
        CMcfg_FanNormalReading        : {} ({} * {} = {} RPM)
        CMcfg_FanUpCritReading        : {} ({} * {} = {} RPM)
        CMcfg_FanLowCritReading       : {} ({} * {} = {} RPM)
        CMcfg_ReserveWord1            : {} W
        CMcfg_ReserveWord2            : {} W
        CMcfg_ReserveWord3            : {} W
        CMcfg_ReserveWord4            : {} W
        CMcfg_ChassisPowerLimit       : {} W
        CMcfg_PowerCapActions         : {} : {}
        CMcfg_ChassisPowerCap         : {}
        CMcfg_ChassisServiceTag       : {}
        CMcfg_FTREnable               : {} : {}
        CMCfg_ReserveByte4            : {}
        CMcfg_ReserveWord5            : {}
        CMCfg_ReserveByte5            : {}
        CMCfg_ReserveByte6            : {}
        """.format(int(cmconfig_list[0][0],16),cmconfig_dict["LockInternalUseArea"][int(cmconfig_list[0][0],16)],
                int(cmconfig_list[1][0],16),cmconfig_dict["FanControlMode"][int(cmconfig_list[1][0],16)],
                int(cmconfig_list[2][0],16),
                int(cmconfig_list[3][0]),cmconfig_dict["FanTypeConfig"][int(cmconfig_list[3][0])],
                int(cmconfig_list[4][0],16),cmconfig_dict["SledConfig"][int(cmconfig_list[4][0],16)],
                int(cmconfig_list[5][0],16),int(cmconfig_list[6][0],16),
                int(cmconfig_list[7][0],16),cmconfig_dict["RedundantPSUsN"][int(cmconfig_list[7][0],16)],
                int(cmconfig_list[8][0],16),int(cmconfig_list[9][0],16),int(cmconfig_list[10][0],16),
                int(cmconfig_list[11][0],16),int(cmconfig_list[12][0],16),int(cmconfig_list[13][0],16),
                int(cmconfig_list[14][0],16),int(cmconfig_list[14][0],16),136,int(cmconfig_list[14][0],16)*136,
                int(cmconfig_list[15][0],16),int(cmconfig_list[15][0],16),136,int(cmconfig_list[15][0],16)*136,
                int(cmconfig_list[16][0],16),int(cmconfig_list[16][0],16),136,int(cmconfig_list[16][0],16)*136,
                int(cmconfig_list[17][1]+cmconfig_list[17][0],16),int(cmconfig_list[18][1]+cmconfig_list[18][0],16),
                int(cmconfig_list[19][1]+cmconfig_list[19][0],16),int(cmconfig_list[20][1]+cmconfig_list[20][0],16),
                int(cmconfig_list[21][1] + cmconfig_list[21][0],16),
                int(cmconfig_list[22][0],16),cmconfig_dict["PowerCapActions"][int(cmconfig_list[22][0],16)],
                int(cmconfig_list[23][0],16), "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in cmconfig_list[24]]) ,
                int(cmconfig_list[25][0],16),cmconfig_dict["FTREnable"][int(cmconfig_list[25][0],16)],
                int(cmconfig_list[26][0],16),int(cmconfig_list[27][1] + cmconfig_list[27][0],16),
                int(cmconfig_list[28][0],16), int(cmconfig_list[29][0],16)
                )

        # print(getCMConfig_OL)
        return getCMConfig_OL


    elif PLATFORM == "AMC":
        getCMConfig_AMC = """
        $ getCMConfig

        INTERNAL USE AREA INFO::
        CMCfg_LockInternalUseArea     : {} : {}
        CMCfg_FanControlMode          : {} : {}
        CMCfg_FanSpeedSetting         : {}
        CMCfg_FanTypeConfig           : 0x{} : {}
        CMCfg_SledConfig              : {} : {}
        CMCfg_FanZones                : {}
        CMCfg_RequiredPSUsX           : {}
        CMCfg_RedundantPSUsN          : {} : {}
        CMCfg_GridChassisICLEnable    : 0x{}
        CMcfg_ReserveByte2            : {} W
        CMcfg_ReserveByte3            : {} W
        CMcfg_InletTempUpNCthres      : {} Degree Celsius
        CMcfg_InletTempUpCCritThres   : {} Degree Celsius
        CMcfg_MaxSledCount            : {}
        CMcfg_FanNormalReading        : {} ({} * {} = {} RPM)
        CMcfg_FanUpCritReading        : {} ({} * {} = {} RPM)
        CMcfg_FanLowCritReading       : {} ({} * {} = {} RPM)
        CMcfg_GridICL                 : {} mA
        CMcfg_ChassisICL              : {} mA
        CMcfg_ReserveWord3            : {} W
        CMcfg_ReserveWord4            : {} W
        CMcfg_ChassisPowerLimit       : {} W
        CMcfg_PowerCapActions         : {} : {}
        CMcfg_ChassisPowerCap         : {}
        CMcfg_ChassisServiceTag       : {}
        CMcfg_FTREnable               : {} : {}
        CMcfg_BpPresent               : {} : {}
        CMcfg_BpId                    : 0x{}
        CMcfg_BVMSetting              : {}
        CMcfg_CableAmpLimit           : {} A
        """.format(int(cmconfig_list[0][0],16),cmconfig_dict["LockInternalUseArea"][int(cmconfig_list[0][0],16)],
                int(cmconfig_list[1][0],16),cmconfig_dict["FanControlMode"][int(cmconfig_list[1][0],16)],
                int(cmconfig_list[2][0],16),
                int(cmconfig_list[3][0]),cmconfig_dict["FanTypeConfig"][int(cmconfig_list[3][0])],
                int(cmconfig_list[4][0],16),cmconfig_dict["SledConfig"][int(cmconfig_list[4][0],16)],
                int(cmconfig_list[5][0],16),int(cmconfig_list[6][0],16),
                int(cmconfig_list[7][0],16),cmconfig_dict["RedundantPSUsN"][int(cmconfig_list[7][0],16)],
                cmconfig_list[8][0],int(cmconfig_list[9][0],16),int(cmconfig_list[10][0],16),
                int(cmconfig_list[11][0],16),int(cmconfig_list[12][0],16),int(cmconfig_list[13][0],16),
                int(cmconfig_list[14][0],16),int(cmconfig_list[14][0],16),120,int(cmconfig_list[14][0],16)*120,
                int(cmconfig_list[15][0],16),int(cmconfig_list[15][0],16),120,int(cmconfig_list[15][0],16)*120,
                int(cmconfig_list[16][0],16),int(cmconfig_list[16][0],16),120,int(cmconfig_list[16][0],16)*120,
                int(cmconfig_list[17][1]+cmconfig_list[17][0],16),int(cmconfig_list[18][1]+cmconfig_list[18][0],16),
                int(cmconfig_list[19][1]+cmconfig_list[19][0],16),int(cmconfig_list[20][1]+cmconfig_list[20][0],16),
                int(cmconfig_list[21][1] + cmconfig_list[21][0],16),
                int(cmconfig_list[22][0],16),cmconfig_dict["PowerCapActions"][int(cmconfig_list[22][0],16)],
                int(cmconfig_list[23][0],16), "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in cmconfig_list[24]]) ,
                int(cmconfig_list[25][0],16),cmconfig_dict["FTREnable"][int(cmconfig_list[25][0],16)],
                int(cmconfig_list[26][0],16),cmconfig_dict["BpPresent"][int(cmconfig_list[26][0],16)],
                "".join([cmconfig_list[27][1],cmconfig_list[27][0]]),
                int(cmconfig_list[28][0],16), int(cmconfig_list[29][0],16)
                )
        
        # print(getCMConfig_AMC)
        return getCMConfig_AMC

    elif PLATFORM == "Hook":        
        getCMConfig_Hook = """
        $ getCMConfig
        
        INTERNAL USE AREA INFO::
        CMCfg_LockInternalUseArea     : {} : {}
        CMCfg_ReserveByte7            : {}
        CMCfg_ReserveByte8            : {}
        CMCfg_ReserveByte9            : {}
        CMCfg_SledConfig              : {} : {}
        CMcfg_ReserveByte10           : {}
        CMCfg_RequiredPSUsX           : {}
        CMCfg_RedundantPSUsN          : {} : {}
        CMCfg_ReserveByte1            : {} 
        CMcfg_ReserveByte2            : {} 
        CMcfg_ReserveByte3            : {} 
        CMcfg_InletTempUpNCthres      : {} Degree Celsius
        CMcfg_InletTempUpCCritThres   : {} Degree Celsius
        CMcfg_MaxSledCount            : {}
        CMcfg_ReserveByte13           : {} 
        CMcfg_ReserveByte14           : {} 
        CMcfg_ReserveByte15           : {} 
        CMcfg_ReserveWord1            : {} 
        CMcfg_ReserveWord2            : {} 
        CMcfg_ReserveWord3            : {} 
        CMcfg_ReserveWord4            : {} 
        CMcfg_ChassisPowerLimit       : {} W
        CMcfg_PowerCapActions         : {} : {}
        CMcfg_ChassisPowerCap         : {} 
        CMcfg_ChassisServiceTag       : {}   
        CMcfg_FTREnable               : {} : {}
        CMCfg_ReserveByte4            : {} 
        CMcfg_ReserveWord5            : {} 
        CMCfg_ReserveByte5            : {} 
        CMCfg_ReserveByte6            : {} 
        """.format(int(cmconfig_list[0][0],16),cmconfig_dict["LockInternalUseArea"][int(cmconfig_list[0][0],16)],
                int(cmconfig_list[1][0],16),
                int(cmconfig_list[2][0],16),
                int(cmconfig_list[3][0],16),
                int(cmconfig_list[4][0],16),cmconfig_dict["SledConfig"][int(cmconfig_list[4][0],16)],
                int(cmconfig_list[5][0],16),int(cmconfig_list[6][0],16),
                int(cmconfig_list[7][0],16),cmconfig_dict["RedundantPSUsN"][int(cmconfig_list[7][0],16)],
                int(cmconfig_list[8][0],16),int(cmconfig_list[9][0],16),int(cmconfig_list[10][0],16),
                int(cmconfig_list[11][0],16),int(cmconfig_list[12][0],16),int(cmconfig_list[13][0],16),
                int(cmconfig_list[14][0],16),
                int(cmconfig_list[15][0],16),
                int(cmconfig_list[16][0],16),
                int(cmconfig_list[17][1]+cmconfig_list[17][0],16),int(cmconfig_list[18][1]+cmconfig_list[18][0],16),
                int(cmconfig_list[19][1]+cmconfig_list[19][0],16),int(cmconfig_list[20][1]+cmconfig_list[20][0],16),
                int(cmconfig_list[21][1] + cmconfig_list[21][0],16),
                int(cmconfig_list[22][0],16),cmconfig_dict["PowerCapActions"][int(cmconfig_list[22][0],16)],
                int(cmconfig_list[23][0],16), "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in cmconfig_list[24]]) ,
                int(cmconfig_list[25][0],16),cmconfig_dict["FTREnable"][int(cmconfig_list[25][0],16)],
                int(cmconfig_list[26][0],16),int(cmconfig_list[27][1] + cmconfig_list[27][0],16),
                int(cmconfig_list[28][0],16), int(cmconfig_list[29][0],16)
                )

        # print(getCMConfig_Hook)
        return getCMConfig_Hook

    elif PLATFORM == "Steeda":
        getCMConfig_Steeda = """
        $ getCMConfig

        INTERNAL USE AREA INFO::
        CMCfg_LockInternalUseArea     : {} : {}
        CMCfg_FanControlMode          : {} : {}
        CMCfg_FanSpeedSetting         : {}
        CMCfg_FanTypeConfig           : 0x{} : {}
        CMCfg_SledConfig              : {} : {}
        CMCfg_FanZones                : {}
        CMCfg_RequiredPSUsX           : {}
        CMCfg_RedundantPSUsN          : {} : {}
        CMCfg_MaxFanPwr               : {} W
        CMcfg_MaxHddChasPwr           : {} W
        CMcfg_MaxCmChasPower          : {} W
        CMcfg_InletTempUpNCthres      : {} Degree Celsius
        CMcfg_InletTempUpCCritThres   : {} Degree Celsius
        CMcfg_MaxSledCount            : {}
        CMcfg_FanNormalReading        : {} ({} * {} = {} RPM)
        CMcfg_FanUpCritReading        : {} ({} * {} = {} RPM)
        CMcfg_FanLowCritReading       : {} ({} * {} = {} RPM)
        CMcfg_SledPowerLimit1         : {} W
        CMcfg_SledPowerLimit2         : {} W
        CMcfg_SledPowerLimit3         : {} W
        CMcfg_SledPowerLimit4         : {} W
        CMcfg_ChassisPowerLimit       : {} W
        CMcfg_PowerCapActions         : {} : {}
        CMcfg_ChassisPowerCap         : {}
        CMcfg_ChassisServiceTag       : {}
        CMcfg_FTREnable               : {} : {}
        CMcfg_BpPresent               : {} : {}
        CMcfg_BpId                    : 0x{}
        CMcfg_BVMSetting              : {}
        CMcfg_CableAmpLimit           : {} A

        """.format(int(cmconfig_list[0][0],16),cmconfig_dict["LockInternalUseArea"][int(cmconfig_list[0][0],16)],
                int(cmconfig_list[1][0],16),cmconfig_dict["FanControlMode"][int(cmconfig_list[1][0],16)],
                int(cmconfig_list[2][0],16),
                int(cmconfig_list[3][0]),cmconfig_dict["FanTypeConfig"][int(cmconfig_list[3][0])],
                int(cmconfig_list[4][0],16),cmconfig_dict["SledConfig"][int(cmconfig_list[4][0],16)],
                int(cmconfig_list[5][0],16),int(cmconfig_list[6][0],16),
                int(cmconfig_list[7][0],16),cmconfig_dict["RedundantPSUsN"][int(cmconfig_list[7][0],16)],
                int(cmconfig_list[8][0]),int(cmconfig_list[9][0],16),int(cmconfig_list[10][0],16),
                int(cmconfig_list[11][0],16),int(cmconfig_list[12][0],16),int(cmconfig_list[13][0],16),
                int(cmconfig_list[14][0],16),int(cmconfig_list[14][0],16),86,int(cmconfig_list[14][0],16)*86,
                int(cmconfig_list[15][0],16),int(cmconfig_list[15][0],16),86,int(cmconfig_list[15][0],16)*86,
                int(cmconfig_list[16][0],16),int(cmconfig_list[16][0],16),86,int(cmconfig_list[16][0],16)*86,
                int(cmconfig_list[17][1]+cmconfig_list[17][0],16),int(cmconfig_list[18][1]+cmconfig_list[18][0],16),
                int(cmconfig_list[19][1]+cmconfig_list[19][0],16),int(cmconfig_list[20][1]+cmconfig_list[20][0],16),
                int(cmconfig_list[21][1] + cmconfig_list[21][0],16),
                int(cmconfig_list[22][0],16),cmconfig_dict["PowerCapActions"][int(cmconfig_list[22][0],16)],
                int(cmconfig_list[23][0],16), "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in cmconfig_list[24]]) ,
                int(cmconfig_list[25][0],16),cmconfig_dict["FTREnable"][int(cmconfig_list[25][0],16)],
                int(cmconfig_list[26][0],16),cmconfig_dict["BpPresent"][int(cmconfig_list[26][0],16)],
                "".join([cmconfig_list[27][1],cmconfig_list[27][0]]),
                int(cmconfig_list[28][0],16), int(cmconfig_list[29][0],16)
                )
        
        # print(getCMConfig_Steeda) 
        return getCMConfig_Steeda   

def set_hidden_config(sled_ip, cfg_ID, cfg_val):
    # Get the passcode:
    passcode = get_passcode(sled_ip)
    if passcode == "":
        print("\nFailed to get a passcode\n")
        sys.exit()
    # Set hidden config property:
    set_hidden_config_cmd = "raw 0x6 0x34 0x45 0x70 0xc8 0xc8 0x20 0x0 "\
                            "0x03 0x01 0x64 0x65 0x6c 0x6c 0x63 0x6d "\
                            "0x31 0x34 " + passcode + "0x01 " + cfg_ID +\
                            " " + cfg_val + " 0xd8"

    output = execute_ipmi_cmd(set_hidden_config_cmd, sled_ip)
    print("Response: ",output)
    output = output.strip("\r\n").split(" ")
    if output[-2] == "81":
        print("  Error")
    elif output[-2] != "00":
        print("Unble to write property")
    return output

def set_cm_config(sled_ip):    
    print("Property ID range is 0x01 to 0x1E, view 'getCMConfig' for all property list.")
    property_id = input("Insert Property ID [Hex]: ")
    property_value = input("Insert Property Value [Hex]: ")
    cmd = "raw 0x6 0x34 0x45 0x70 0xc0 0xc8 0x20 0x0 0xa1 0x1 0x1 {} {} 0xd8".format(property_id,property_value)
    output = execute_ipmi_cmd(cmd,sled_ip)
    print(output)    
    output_list=[]
    try:
        # output_list = [output_list.remove(i) for i in output_list if i == ""]
        output_list = output.strip("\r\n").split(" ")
        for item in output_list:
            if item == "":
                output_list.remove(item)        
    except:
        pass
    if "Unable" in output or output_list[6] != "00":
        print("Can't set config property ",output_list)        

    return output

def set_cmd_debug_info(sled_ip,flag):
    sled_ssh = SSH_connect(sled_ip)
    send_ssh_cmd("rootshell",sled_ssh)
    output = get_ssh_output(sled_ssh)
    # print(output)   
    send_ssh_cmd("debugcontrol -s IPMI_DCS -l 10 -o RAM -r 10240",sled_ssh)
    output = get_ssh_output(sled_ssh)
    # print(output) 
    send_ssh_cmd("tail -f /var/log/idraclogs",sled_ssh)
    time.sleep(30)
    send_ssh_cmd("\x03", sled_ssh)
    output = get_ssh_output(sled_ssh)
    # print(output)  
    output = output.splitlines()
    output = list(filter(None, output))
    debug_log = {"Set_PSU_info":"","Set_Chas_Pwr_Reading":"","Set_PSU_thermal":"",
                 "set_additional_psu_info":"","set_sensor_info":"",
                 "setPsuExtended_partial":"","other_logs":""}
    
    for line in output:        
        if "DellDCSSetPSUInfo" in line:            
            if debug_log["Set_PSU_info"].count("Cmd 0x1E>>") > 1:
                pass
            else:
                debug_log["Set_PSU_info"] += line + "\n"                

        if "DellDCSSetChassPwrReadings" in line:                      
            if debug_log["Set_Chas_Pwr_Reading"].count("Cmd 0x2F>>") > 1:
                pass
            else:
                debug_log["Set_Chas_Pwr_Reading"] += line + "\n"                  

        if "DellDCSSetPSUThermal" in line:                      
            if debug_log["Set_PSU_thermal"].count("DellDCSSetPSUThermal: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                debug_log["Set_PSU_thermal"] += line + "\n"                  

        if "DellDCSSetAdditinalPSUInfo" in line:                       
            if debug_log["set_additional_psu_info"].count("DellDCSSetAdditinalPSUInfo: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                debug_log["set_additional_psu_info"] += line + "\n"                

        if "DellDCSSetSensorInfo" in line:                      
            if debug_log["set_sensor_info"].count("DellDCSSetSensorInfo: NetFn 0x30, Cmd 0x15>>") > 1:
                pass
            else:
                debug_log["set_sensor_info"] += line + "\n" 
        if "DellDCSSetExtendedPSUInfo" in line:                      
            if debug_log["setPsuExtended_partial"].count("DellDCSSetExtendedPSUInfo: NetFn 0x30, Cmd 0xD7>>") > 1:
                pass
            else:
                debug_log["setPsuExtended_partial"] += line + "\n"                 
    
    sled_ssh.close()
    if flag == False:
        return debug_log
    else:
        sep = "="*70      
        print(sep,"\n [1] 'SetPSUInfo' Command Output : \n\n",debug_log["Set_PSU_info"])  
        print(sep,"\n [2] 'SetChassPwrReadings' Command Output : \n\n",debug_log["Set_Chas_Pwr_Reading"])
        print(sep,"\n [3] 'SetPSUThermal' Command Output : \n\n",debug_log["Set_PSU_thermal"])
        print(sep,"\n [4] 'SetAdditinalPSUInfo' Command Output : \n\n",debug_log["set_additional_psu_info"])
        print(sep,"\n [5] 'SetSensorInfo' Command Output : \n\n",debug_log["set_sensor_info"])
        print(sep,"\n [6] 'SetPSUExtendedInfo' Partial data : \n\n",debug_log["setPsuExtended_partial"])
        print(sep)
        
        return debug_log

def set_cmd_debug_log_w_reboot(sled_ip):
    sled_ssh1 = SSH_connect(sled_ip)
    send_ssh_cmd("rootshell",sled_ssh1)
    output = get_ssh_output(sled_ssh1)    
    # print(output)   
    send_ssh_cmd("debugcontrol -s IPMI_DCS_START -l 10 -o RAM -r 10240",sled_ssh1)
    output = get_ssh_output(sled_ssh1)      
    send_ssh_cmd("racadm cmreset",sled_ssh1) 
    time.sleep(1)   
    send_ssh_cmd("tail -f /var/log/idraclogs",sled_ssh1)    
    time.sleep(80)
    send_ssh_cmd("\x03", sled_ssh1)    
    output1 = get_ssh_output(sled_ssh1)     
    output1 = output1.splitlines()    
    output1_list = list(filter(None, output1))    
    SyncChasEncPwr = ""
    SetFanFailure = ""
    SetCmCfgEvent = ""
    SyncChasServiceTag = ""
    getBMCprotocol = ""
    setChassisCfg = ""
    setCMsupport = ""
    setPowerAlloc = ""
    sledPowerBudget = ""
    setSledICL = ""
    getHDDCount = ""
    SubCmdThermalPro = ""
    setPsuExtended_full = ""
    other_logs = ""
    for line in output1_list:        
        if "DellDCSSyncChassisEncPwr" in line:            
            if SyncChasEncPwr.count("DellDCSSyncChassisEncPwr: NetFn 0x30, Cmd 0x29>>") > 1:
                pass
            else:
                SyncChasEncPwr += line + "\n" 
        if "DellDCSSetFanFailure" in line:                      
            if SetFanFailure.count("IPMI_DCS_START: DellDCSSetFanFailure: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                SetFanFailure += line + "\n"   
        if "DellDCSSetCmCfgEvent" in line:                      
            if SetCmCfgEvent.count("IPMI_DCS_START: DellDCSSetCmCfgEvent: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                SetCmCfgEvent += line + "\n"
        if "DellDCSSyncChassisServiceTag" in line:                       
            if SyncChasServiceTag.count("DellDCSSyncChassisServiceTag: NetFn 0x30, Cmd 0x26>>") > 1:
                pass
            else:
                SyncChasServiceTag += line + "\n"  
        if "DellDCSGetBMCProtocolVer" in line:                      
            if getBMCprotocol.count("DellDCSGetBMCs_SC_BMC_ProtocolVer: NetFn 0x30, Cmd 0x2C>>") > 1:
                pass
            else:
                getBMCprotocol += line + "\n"          
        if "DellDCSSetChassisConfig" in line:                      
            if setChassisCfg.count("DellDCSSetChassisConfig: NetFn 0x30, Cmd 0x11>>") > 1:
                pass
            else:
                setChassisCfg += line + "\n"  
        if "DellDCSSetCMSupport" in line:                      
            if setCMsupport.count("DellDCSSetCMSupport: NetFn 0x30, Cmd 0xD8>>") > 1:
                pass
            else:
                setCMsupport += line + "\n" 
        if "DellDCSSetSledPowerAlloc" in line:                      
            if setPowerAlloc.count("DellDCSSetSledPowerAlloc: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                setPowerAlloc += line + "\n"   
        if "DellDCSSetSledPowerBudget" in line:                      
            if sledPowerBudget.count("DellDCSSetSledPowerBudget: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                sledPowerBudget += line + "\n" 
        if "DellDCSSetSledICL" in line:                      
            if setSledICL.count("DellDCSSetSledICL: NetFn 0x30, Cmd 0xDF>>") > 1:
                pass
            else:
                setSledICL += line + "\n"   
        if "DellDCSGetHDDCount" in line:                      
            if getHDDCount.count("DellDCSGetHDDCount: NetFn 0x30, Cmd 0xC8>>") > 1:
                pass
            else:
                getHDDCount += line + "\n" 
        if "DellDCSSubCmdThermalProperties" in line:                      
            if SubCmdThermalPro.count("DellDCSSubCmdThermalProperties: NetFn 0x30, Cmd 0xC8, Get/Set 0x00, SubCmd 0x01>>") > 1:
                pass
            else:
                SubCmdThermalPro += line + "\n"   
    
    sep = "="*70      
    print(sep,"\n [1] 'DellDCSSyncChassisEncPwr' Command Output : \n\n",SyncChasEncPwr)  
    print(sep,"\n [2] 'DellDCSSetFanFailure' Command Output : \n\n",SetFanFailure)
    print(sep,"\n [3] 'DellDCSSyncChassisServiceTag' Command Output : \n\n",SyncChasServiceTag)
    print(sep,"\n [4] 'DellDCSGetBMCProtocolVer' Command Output : \n\n",getBMCprotocol)
    print(sep,"\n [5] 'DellDCSSetChassisConfig' Command Output : \n\n",setChassisCfg)
    print(sep,"\n [6] 'DellDCSSetCMSupport' Command Output : \n\n",setCMsupport)
    print(sep,"\n [7] 'DellDCSSetSledPowerAlloc' Command Output : \n\n",setPowerAlloc)
    print(sep,"\n [8] 'DellDCSSetSledPowerBudget' Command Output : \n\n",sledPowerBudget)
    print(sep,"\n [9] 'DellDCSSetSledICL' Command Output : \n\n",setSledICL)
    print(sep,"\n [10]'DellDCSGetHDDCount' Command Output : \n\n",getHDDCount)
    print(sep,"\n [11]'DellDCSSubCmdThermalProperties' Command Output : \n\n",SubCmdThermalPro)
    print(sep,"\n [12]'DellDCSSetCmCfgEvent' Command Output : \n\n",SetCmCfgEvent)
    # print(sep,"\n [13]'DellDCSSetExtendedPSUInfo' Full Data : \n\n",setPsuExtended_full)
    print(sep)

    sled_ssh1.close()
    return output1

def debug_log_extendedPsuInfo(sled_ip):
    sled_ssh1 = SSH_connect(sled_ip)
    send_ssh_cmd("rootshell",sled_ssh1)
    output = get_ssh_output(sled_ssh1)    
    # print(output)   
    send_ssh_cmd("debugcontrol -s IPMI_DCS -l 10 -o RAM -r 10240",sled_ssh1)
    output = get_ssh_output(sled_ssh1)      
    send_ssh_cmd("racadm cmreset",sled_ssh1) 
    output = get_ssh_output(sled_ssh1)    
    send_ssh_cmd('tail -f /var/log/idraclogs | grep -i "DellDCSSetExtendedPSUInfo"',sled_ssh1)    
    time.sleep(80)
    send_ssh_cmd("\x03", sled_ssh1)    
    output1 = get_ssh_output(sled_ssh1)     
    output1 = output1.splitlines()    
    output1_list = list(filter(None, output1))    
    extendedPsu_full = ""
    for line in output1_list:
        if extendedPsu_full.count("DellDCSSetExtendedPSUInfo: NetFn 0x30, Cmd 0xD7>>") > 3:
            break
        else:
            extendedPsu_full += line + "\n"  
    print("\n 'DellDCSSetExtendedPSUInfo' Full Data : \n\n",extendedPsu_full)
    
    sled_ssh1.close()
    return output1

def dumpPSU(sled_ip):    
        
    psu_data = {"psu1":{},
                "psu2":{}}    
    debug_log = set_cmd_debug_info(sled_ip,flag=False)
    PsuAdditionalInfo = debug_log["set_additional_psu_info"]
    psuThermal_list = debug_log["Set_PSU_thermal"].splitlines()
    psuInfo_list = debug_log["Set_PSU_info"].splitlines()
    PsuAdditionalInfo_list = PsuAdditionalInfo.splitlines()    
    for line in range(0,len(PsuAdditionalInfo_list)):
        PsuAdditionalInfo_list[line] = PsuAdditionalInfo_list[line].split()
    for line in range(0,len(PsuAdditionalInfo_list)):
        if "u8nPSUs" in PsuAdditionalInfo_list[line] :
            total_psu = PsuAdditionalInfo_list[line][7].strip()
        if "u8PsuIndex" in PsuAdditionalInfo_list[line]:
            if PsuAdditionalInfo_list[line][7].strip() == "0":
                psu1_id = line
            else:
                psu2_id = line
    psu1_status_reg = "0x" + PsuAdditionalInfo_list[psu1_id+2][7] + PsuAdditionalInfo_list[psu1_id+1][7] 
    psu2_status_reg = "0x" + PsuAdditionalInfo_list[psu2_id+2][7] + PsuAdditionalInfo_list[psu2_id+1][7] 
    psu2_line = 0   
    for line in range(0,len(psuThermal_list)):
        psuThermal_list[line] = psuThermal_list[line].split()
    # if ("u8PSUIndex :1" in psuThermal_list) and ("u8PSUIndex :0" in psuThermal_list):    
    Act_extended_info = psu_extended_info(sled_ip,flag=False) 

    if "PSU-0 Index-" not in Act_extended_info.keys():
        for line in range(0,len(psuThermal_list)):                  
            if "u8PSUFan1Speed" in psuThermal_list[line]:
                    psu2_fan_speed = psuThermal_list[line][8].strip(":")                    
                    break         
        psu1_fan_speed = "0"
    
    elif "PSU-1 Index-" not in Act_extended_info.keys():
        for line in range(0,len(psuThermal_list)):                  
            if "u8PSUFan1Speed" in psuThermal_list[line]:
                psu1_fan_speed = psuThermal_list[line][8].strip(":")                    
                break         
        psu2_fan_speed = "0"

    else:           # "PSU-0 Index-" in Act_extended_info.keys() and "PSU-1 Index-" in Act_extended_info.keys():
        for line in range(0,len(psuThermal_list)):                  
            if "u8PSUFan1Speed" in psuThermal_list[line]:
                psu1_fan_speed = psuThermal_list[line][8].strip(":")
                psu2_line = line
                break          
        psu2_fan_speed = psuThermal_list[psu2_line+7][8].strip(":")

    
    for line in range(0,len(psuInfo_list)):
        psuInfo_list[line] = psuInfo_list[line].split()
    for line in range(0,len(psuInfo_list)):
        if "gDCSPSUInfo.u8PSUMismatch" in psuInfo_list[line][6]:
            psu_mismatch = psuInfo_list[line][8]      
    time.sleep(1)  
    # based on input type, dumpPSU line status message   
    line_status = {"00":", Low Line AC, 50Hz","01":", No input for wide range AC",
                   "02":", High Line AC, 50Hz" ,"03":", No input for telecom DC",
                   "04":", Low Line AC, 60Hz","05":", No input for extended AC",
                   "06":", High Line AC, 60Hz","07":", Telecom DC",
                   "08":", wide-range AC/low-line DC mixed-mode Unplugged",
                   "09":", No input for High Line AC","0a":"High Line DC",
                   "0b":", No input for extended AC/ wide range DC",
                   "0c":", Low Line DC","0d":", Extended AC, 50Hz",
                   "0e":", Extended AC, 60Hz","ff":", Unknown"}
    # if GSI_data[10] == "03" or GSI_data[10] == "01":
    if "PSU-0 Index-" in Act_extended_info.keys():
        if int(Act_extended_info["PSU Actual Output Wattage"],16) != 0:        
            psu_data["psu1"]["PGOOD"] = "1 : YES"
        elif int(psu1_fan_speed,16) != 0:
            psu_data["psu1"]["PGOOD"] = "1 : YES"
        else:
            psu_data["psu1"]["PGOOD"] = "0 : NO"
        psu_data["psu1"]["PRESENT_N"] = "0 : PRESENT"
        psu_data["psu1"]["ALERT_N"] = "-----"
        psu_data["psu1"]["VIN_GOOD"] = "-----"
        psu_data["psu1"]["FW Ver."] = Act_extended_info["PSU FW Version"].upper()
        psu_data["psu1"]["Pout"] = str(int(Act_extended_info["PSU Actual Output Wattage"],16))+" W"
        psu_data["psu1"]["Vout"] = "-----"
        psu_data["psu1"]["Iout"] = "-----"
        psu_data["psu1"]["Pin"] = str(int(Act_extended_info["PSU Actual Input Wattage"],16))+" W"
        psu_data["psu1"]["Vin"] = str(int(Act_extended_info["PSU Input Voltage V-In"],16))+" V"            
        psu_data["psu1"]["Iin"] = str(int(Act_extended_info["PSU Input Current I- In"],16))+" mA"
        if PLATFORM == "AMC":
            psu_data["psu1"]["IinMax"] = "-----"
        psu_data["psu1"]["Pout(Max)"] = str(int(Act_extended_info["PSU Output Rate Wattage"],16))+" W"
        psu_data["psu1"]["Pout(Max) "] = str(int(Act_extended_info["PSU Output Rate Wattage"],16))+ " W (True)"           
        psu_data["psu1"]["Pin(Max)"] = str(int(Act_extended_info["PSU Input Rate Wattage"],16))+" W"  
        # if Act_extended_info["PSU line Status"] in line_status:

        if Act_extended_info["PSU Input Type(AC/DC)"] in line_status.keys(): 
            status = line_status[Act_extended_info["PSU Input Type(AC/DC)"]]        
        else:
            status = ""  
        psu_data["psu1"]["LineSatatus"] = Act_extended_info["PSU line Status"]+status
        
        if int(Act_extended_info["PSU Input Voltage V-In"],16) == 0:
            psu_data["psu1"]["AC Loss"] = "1, YES"
        else:
            psu_data["psu1"]["AC Loss"] = "0, NO"
            psu_data["psu1"]["VIN_GOOD"] = "1 : GOOD"
        if PsuAdditionalInfo_list[psu1_id+3][7] == "0" and PsuAdditionalInfo_list[psu1_id+4][7] == "0" \
            and PsuAdditionalInfo_list[psu1_id+5][7] == "0":
            psu_data["psu1"]["Fault"] = "0, NO"
        elif PsuAdditionalInfo_list[psu1_id+10][7] != "0":
            psu_data["psu1"]["Fault"] = "1, YES (FAN)"
        else: 
            psu_data["psu1"]["Fault"] = "1, YES"
        psu_data["psu1"]["stat_reg**"] = psu1_status_reg
        psu_data["psu1"]["InputType"]= Act_extended_info["PSU Input Type(AC/DC)"]
        part_n = Act_extended_info["PSU Part No. + HW rev"]
        partNum_list = [part_n[i:i+2] for i in range(0,len(part_n),2)]
        psu1_part_num = "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in partNum_list])
        psu_data["psu1"]["PartNum"] = psu1_part_num
        psu_data["psu1"]["SerialNum"]= "-----"
        psu_data["psu1"]["vendor"] = "-----"
        psu_data["psu1"]["Allow list"] = "-----"
        psu_data["psu1"]["POWER STAT"] = "-----"
        if psu_mismatch != "0x00" and \
            int(Act_extended_info["PSU Output Rate Wattage"],16) < \
                int(Act_extended_info["PSU1 Output Rate Wattage"],16):
            
            psu_data["psu1"]["Mismatch"]="YES  [Rated Power]"
            psu_data["psu1"]["PGOOD"] = "0 : NO"
        else:
            psu_data["psu1"]["Mismatch"]="NO"
        psu_data["psu1"]["Hot_spot_Temp"] = str(int(PsuAdditionalInfo_list[psu1_id+12][7],16))+" Degree Celsius"
        psu_data["psu1"]["Inlet_Temp"] = str(int(PsuAdditionalInfo_list[psu1_id+13][7],16))+" Degree Celsius"
        psu_data["psu1"]["Exhaust_Temp"] = str(int(PsuAdditionalInfo_list[psu1_id+14][7],16))+" Degree Celsius"
        psu_data["psu1"]["Device_ID"] = "-----"
        psu_data["psu1"]["Airflow_Status"] = "-----"
        psu_data["psu1"]["Fan1_Speed"] = str(int(psu1_fan_speed,16)) + " RPM"

    # if GSI_data[10] == "03" or GSI_data[10] == "02":
    if "PSU-1 Index-" in Act_extended_info.keys():
        if int(Act_extended_info["PSU1 Actual Output Wattage"],16) != 0:        
            psu_data["psu2"]["PGOOD"] = "1 : YES"
        elif int(psu2_fan_speed,16) != 0:
            psu_data["psu2"]["PGOOD"] = "1 : YES"
        else:
            psu_data["psu2"]["PGOOD"] = "0 : NO"
        psu_data["psu2"]["PRESENT_N"] = "0 : PRESENT"
        psu_data["psu2"]["ALERT_N"] = "-----"
        psu_data["psu2"]["VIN_GOOD"] = "-----"
        psu_data["psu2"]["FW Ver."] = Act_extended_info["PSU1 FW Version"].upper()
        psu_data["psu2"]["Pout"] = str(int(Act_extended_info["PSU1 Actual Output Wattage"],16))+" W"
        psu_data["psu2"]["Vout"] = "-----"
        psu_data["psu2"]["Iout"] = "-----"
        psu_data["psu2"]["Pin"] = str(int(Act_extended_info["PSU1 Actual Input Wattage"],16))+" W"
        psu_data["psu2"]["Vin"] = str(int(Act_extended_info["PSU1 Input Voltage V-In"],16) )+" V"           
        psu_data["psu2"]["Iin"] = str(int(Act_extended_info["PSU1 Input Current I- In"],16))+" mA"
        if PLATFORM == "AMC":
            psu_data["psu2"]["IinMax"] = "-----"
        psu_data["psu2"]["Pout(Max)"] = str(int(Act_extended_info["PSU1 Output Rate Wattage"],16))+" W"
        psu_data["psu2"]["Pout(Max) "] = str(int(Act_extended_info["PSU1 Output Rate Wattage"],16))+" W (True)"            
        psu_data["psu2"]["Pin(Max)"] = str(int(Act_extended_info["PSU1 Input Rate Wattage"],16) )+" W"  
        if Act_extended_info["PSU1 Input Type(AC/DC)"] in line_status.keys(): 
            status = line_status[Act_extended_info["PSU1 Input Type(AC/DC)"]]         
        else:
            status = ""       
        psu_data["psu2"]["LineSatatus"] = Act_extended_info["PSU1 line Status"]+status
        if int(Act_extended_info["PSU1 Input Voltage V-In"],16) == 0:
            psu_data["psu2"]["AC Loss"] = "1, YES"
        else:
            psu_data["psu2"]["AC Loss"] = "0, NO"
            psu_data["psu2"]["VIN_GOOD"] = "1 : GOOD"
        if PsuAdditionalInfo_list[psu2_id+3][7] == "0" and PsuAdditionalInfo_list[psu2_id+4][7] == "0" \
            and PsuAdditionalInfo_list[psu2_id+5][7] == "0":
            psu_data["psu2"]["Fault"] = "0, NO"
        elif PsuAdditionalInfo_list[psu2_id+10][7] != "0":
            psu_data["psu2"]["Fault"] = "1, YES (FAN)"
        else:
            psu_data["psu2"]["Fault"] = "1, YES"
        psu_data["psu2"]["stat_reg**"] = psu2_status_reg
        psu_data["psu2"]["InputType"]= Act_extended_info["PSU1 Input Type(AC/DC)"]
        part_n = Act_extended_info["PSU1 Part No. + HW rev"]
        partNum_list = [part_n[i:i+2] for i in range(0,len(part_n),2)]
        psu2_part_num = "".join([bytes.fromhex(value.strip()).decode("ASCII") for value in partNum_list])
        psu_data["psu2"]["PartNum"] = psu2_part_num
        psu_data["psu2"]["SerialNum"]= "-----"
        psu_data["psu2"]["vendor"] = "-----"
        psu_data["psu2"]["Allow list"] = "-----"
        psu_data["psu2"]["POWER STAT"] = "-----"
        if psu_mismatch != "0x00" and \
            int(Act_extended_info["PSU1 Output Rate Wattage"],16) < \
                int(Act_extended_info["PSU Output Rate Wattage"],16):
            psu_data["psu2"]["Mismatch"]="YES  [Rated Power]"
            psu_data["psu2"]["PGOOD"] = "NO"
        else:
            psu_data["psu2"]["Mismatch"]="NO"
        psu_data["psu2"]["Hot_spot_Temp"] = str(int(PsuAdditionalInfo_list[psu2_id+12][7],16)) +" Degree Celsius"
        psu_data["psu2"]["Inlet_Temp"] = str(int(PsuAdditionalInfo_list[psu2_id+13][7],16))+" Degree Celsius"
        psu_data["psu2"]["Exhaust_Temp"] = str(int(PsuAdditionalInfo_list[psu2_id+14][7],16))+" Degree Celsius"
        psu_data["psu2"]["Device_ID"] = "-----"
        psu_data["psu2"]["Airflow_Status"] = "-----"
        psu_data["psu2"]["Fan1_Speed"] = str(int(psu2_fan_speed,16)) + " RPM"    
    # print(psu_data)
    print("\n $ dumpPSU ALL\n\n")    
    for psu in psu_data:
        num = 1 if psu == "psu1" else 2 
        # if psu == "psu1":
        #     num = "1"
        # else:
        #     num = "2"       
        for key in psu_data[psu]:
            print(" PSU[{}] {:<15} = {:<10}".format(num,key,psu_data[psu][key]))
        print("\n\n")

    return psu_data

def main(args):
    global FILE_NAME
    global PLATFORM
    global CM_CONFIG
    if len(args) == 3:        
        chas_name_cmd = "raw 0x30 0x14"   
        try:       
            chassis_name_asci = execute_ipmi_cmd(chas_name_cmd,args[0])            
        except:
            PrintException()
        chassis_name_list = chassis_name_asci.split(" ")        
        chassis_name_chr = ""
        [chassis_name_list.remove(i) for i in chassis_name_list if i == ""]        
        for word in chassis_name_list[1:]:
            word = chr(int(word,16))
            chassis_name_chr += str(word)
        # print(chassis_name_chr)
        if chassis_name_chr[:3] == "XR4":
            PLATFORM = "Outlander"
            CM_CONFIG = CM_CONFIG_OL
        elif chassis_name_chr[:3] == "XR8":
            PLATFORM = "Hook"
            CM_CONFIG = CM_CONFIG_HOOK
        elif chassis_name_chr[:3] == "C66":
            PLATFORM = "AMC"
            CM_CONFIG = CM_CONFIG_AMC
        elif chassis_name_chr[:3] == "C64":
            PLATFORM = "Steeda"
            CM_CONFIG = CM_CONFIG_STEEDA
        else:
            print("Alert : Unidentified Chassis")
            PLATFORM = "Steeda"
            CM_CONFIG = {}
            return FAIL         
               
        help = f"""
                {'|Command Description' :<35}|{'Command Name':^20} |{'Command Code |' :>15} 
                {'-'*73} 
                {'|display CM cfg properties' :<35}|{'getCMConfig':>20} |{'-gcmc  |' :>15}
                {'|display FRU properties' :<35}|{'dumpFRU':>20} |{'-fru  |' :>15}
                {'|display hidden CMConfig properties' :<35}|{'get_hidden_cfg':>20} |{'-ghc  |' :>15}   
                {'|display PSU Info' :<35}|{'dumpPSU_ALL':>20} |{'-dpsu  |' :>15}               
                {'|get device ID' :<35}|{'deviceid':>20} |{'-gdi  |' :>15}   
                {'|get sled fw info' :<35}|{'mcinfo':>20} |{'-gsf  |' :>15}   
                {'|get chassis name' :<35}|{'chasname':>20} |{'-gcn  |' :>15}                   
                {'|get power reading' :<35}|{'powerreading':>20} |{'-gpr  |' :>15} 
                {'|power-budget sled' :<35}|{'powertest':>20} |{'-pwr  |' :>15}   
                {'|get chassis power (0x30 0x2E)' :<35}|{'chaspower':>20} |{'-gcp  |' :>15}   
                {'|get chassis config (0x30 0x12)' :<35}|{'chasconfig':>20} |{'-gcc  |' :>15}   
                {'|get chassis service tag (0xA0)' :<35}|{'getchasservicetag':>20} |{'-gcs  |' :>15}  
                {'|set chassis service tag (0xA1)' :<35}|{'setchasservicetag':>20} |{'-scs  |' :>15}  
                {'|get sensor info (0x30 0x1F)' :<35}|{'get_sensor_info':>20} |{'-gsi  |' :>15}   
                {'|get PSU info (0x30 0x1F)' :<35}|{'psu_info':>20} |{'-gpi  |' :>15}   
                {'|get PSU extended info (0xA3)' :<35}|{'psu_extended_get':>20} |{'-pei  |' :>15}   
                {'|get fw update status ipmi(0xA5)' :<35}|{'updatestatus':>20} |{'-fus  |' :>15} 
                {'|Debug Log Commands Set' :<35}|{'IPMI_DCS':>20} |{'-dlc  |' :>15} 
                {'|Debug Log SC to BMC on CM reboot ' :<35}|{'IPMI_DCS_START':>20} |{'-dlcr  |' :>15}
                {'|Debuglog ExtndedPSUInfo Full data ' :<35}|{'psu_extended_set':>20} |{'-dlep  |' :>15}
                {'|read SEL logs from idrac' :<35}|{'sel_logs':>20} |{'-rsl  |' :>15}  
                {'|read sensor data from idrac' :<35}|{'sensor_data':>20} |{'-rsd  |' :>15}
                {'|read data repository idrac' :<35}|{'data_repository':>20} |{'-sdr  |' :>15}                    
                {'|chassis power cycle ipmi' :<35}|{'powercycle':>20} |{'-cpc  |' :>15}   
                {'|sled power cycle ipmi' :<35}|{'sledpowercycle':>20} |{'-spc  |' :>15}   
                {'|bmc hard reseat ipmi' :<35}|{'hardreset':>20} |{'-bhr  |' :>15}                 
                {'|reboot CM' :<35}|{'reboot':>20} |{'-rcm  |' :>15}   
                {'|reboot sled' :<35}|{'racreset':>20} |{'-rsl  |' :>15}   
                {'|config set to default' :<35}|{'config_to_default':>20} |{'-ctd  |' :>15}
                {'|set CM config property' :<35}|{'setCMConfig':>20} |{'-set_cfg  |' :>15} 
                {'|set CM hidden cfg property' :<35}|{'set_hidden_cfg':>20} |{'-set_hidden  |' :>15}   
                {'|write FRU property ipmi' :<35}|{'writeFRU':>20} |{'-fru_write  |' :>15} 
                {'|iDRAC SSH connection' :<35}|{'rootshell':>20} |{'-rootshell  |' :>15} 
                {'|iDRAC IPMI command' :<35}|{'ipmitool':>20} |{'-ipmitool  |' :>15}
                {'|iDRAC debugControl log view' :<35}|{'debuglog':>20} |{'-debuglog  |' :>15}                                                                
                """

        code_list = ["deviceid","mcinfo","chasname","powerreading","chaspower",
                     "chasconfig","psu_info","psu_extended_info","get_hidden_cfg",
                     "get_sensor_info","getchasservicetag"]    
        FILE_NAME = "{}_{}_log_{}_{}.log".format(PLATFORM,
                                        __file__.split("\\")[-1].split(".")[0],
                                        date0, time0)
        print("\nEnter -h/help/? for list of commands: ")
        print("\n Platform: {}\n".format(PLATFORM)) 
        log_output("Platform: ")
        log_output(PLATFORM)
        while True: 
            view = input("\n ")            
            if view.lower() in ("-h","h","help","?"):
                print(help)
                log_output(help)

            # factory reset 
            elif view.lower() in ("-ctd","factoryreset","config_to_default"):
                response = default_cm_config(args[0])
                log_output("Factory reset CM config: \n{}".format(response))
                # break

            # set CM Hidden Cfg            
            elif view.lower() in ("set_hidden_cfg","set hidden config","-set_hidden"): 
                print(f"""
                {'Hidden Cfg Property' :<35}   {'Prop ID':>15}
                {'-------------------------------------------------------':<50}
                {'<Chassis ID hidden config>' :<35}   {'0x01':>15} 
                {'<Allow FW downgrade hidden config>' :<35}   {'0x02':>15}
                {'<Connector Max hidden config>' :<35}   {'0x03':>15}   
                {'<GoldenChassis hidden config>' :<35}   {'0x04':>15}
                {'<Fixed FTB hidden config>' :<35}   {'0x05':>15}
                {'<Manifest index hidden config>' :<35}   {'0x06':>15}
                    """) 
                      
                property_id = input("Insert Property ID [in Hex]: ")
                if property_id == "0x03":
                    property_value_lsb = input("Insert Connector Max Value LSB [in Hex]: ")
                    property_value_msb = input("Insert Connector Max Value MSB [in Hex]: ")
                    property_value = property_value_lsb + " " + property_value_msb
                else:
                    property_value = input("Insert Property Value [in Hex]: ")                 
                response = set_hidden_config(args[0],property_id,property_value)
                log_output("set hidden config: \n{}".format(response))
                # break

            # set cm config
            elif view in ("set_cm_config", "setCMConfig", "-set_cfg"):
                response = set_cm_config(args[0])
                log_output("Set CM config property:\n{}".format(response))
                #break

            # get CM config data
            elif view in ("-gcmc", "getCMConfig"):                
                config_data = getCMConfig(args[0])
                print(config_data) 
                log_output("get CM config: \n{}".format(config_data))

            # get CM hidden config data
            elif view.lower() in ("-ghc", "get_hidden_cfg"):                
                config_data = get_hidden_cfg(args[0])
                print(config_data) 
                log_output("Get Hidden Config Serial:\n{}".format(config_data))               
                # break

            # view FRU ipmi
            elif view in ("-fru","dumpFRU"):
                response = view_fru_ipmi(args[0])
                log_output("dumpFRU CM serial command: \n{}".format(response))
                # break
            
            # write FRU ipmi
            elif view in ("-fru_write","writeFRU"):
                response = write_fru_data(args[0])
                log_output("Write CM FRU response: \n{}".format(response))
                # break

            # set Manifest Index
            elif view.lower() in ("0x06","manifest_index"):
                response = set_manifest(args[0])
                log_output("set manifest index hidden config: \n{}".format(response))
                # break
            # set Fixed_FTB
            elif view.lower() in ("0x05","fixed_ftb"):
                response = set_fixed_ftb(args[0])
                log_output("set fixed ftb hidden config: \n{}".format(response))
                # break
            # set GoldenChassi
            elif view.lower() in ("0x04","golden_chassis"):
                response = set_golden_chassis(args[0])
                log_output("set golden chassis hidden config: \n{}".format(response))
                # break
            # set Connector_Max
            elif view.lower() in ("0x03","connector_max"):
                response = set_connector_max_threshold(args[0])
                log_output("set connector max hidden config: \n{}".format(response))
                # break
            # set AllowFWDowngrade
            elif view.lower() in ("0x02","allow_fw_downgrade"):
                response = set_allow_fw_downgrade(args[0])
                log_output("set allow fw downgrade hidden config: \n{}".format(response))
                # break
            # set ChassisID
            elif view.lower() in ("0x01","chassis_id"):
                response = set_chassisId(args[0])
                log_output("set chassis id hidden config: \n{}".format(response))
                # break
            # reboot CM
            elif view.lower() in ("-rcm","cmreset","reboot"):
                response = reboot_cm(args[0])
                log_output("CM reboot : \n{}".format(response))
                # break
            # reboot sled
            elif view.lower() in ("-rsl","racreset","rebootsled"):
                response = reboot_sled(args[0])
                log_output("racreset : \n{}".format(response))
                # break
            # get_chassis_power (dumpPSU Pout , Infrastructure power, No. of sleds)
            elif view.lower() in ("-gcp","chaspower","get_chassis_power"):                
                response = get_chas_power(args[0])
                log_output("get chassis power:\n{}".format(response))
                # break
            # get_chassis_config (0x30 0x12)
            elif view.lower() in ("-gcc","chasconfig","get_chassis_config"):                
                response = get_chassis_config(args[0])
                log_output("get chassis config: \n{}".format(response))
                # break

            # get_chassis_service_tag (0x30 0xC8 0xA0)
            elif view.lower() in ("-gcs","getchasservicetag","get_chassis_servicetag"):                
                response = get_chassis_servicetag(args[0])
                log_output("get chassis service tag: \n{}".format(response))
                # break

            # set_chassis_service_tag (0x30 0xC8 0xA1)
            elif view.lower() in ("-scs","setchasservicetag","set_chassis_servicetag"):
                response = set_chassis_servicetag(args[0])
                log_output("set chassis service tag:\n{}".format(response))
                # break

            # get_psu_etended_info (0xA3)
            elif view.lower() in ("-pei","psu_extended_get","0xa3"):                
                response = psu_extended_info(args[0],flag=True)
                log_output("get psu extended info:\n{}".format(response))
                # break

            # get_psu_info (0x30 0x1F)
            elif view.lower() in ("-gpi","psu_info","0x30 0x1F"):                
                response = get_psu_info(args[0])
                log_output("get psu info:\n{}".format(response))
                # break

            # get_fw_update_status (0xA5)
            elif view.lower() in ("-fus","updatestatus","0xa5"):                
                response = fw_update_status_ipmi(args[0])
                log_output("fw update status:\n{}".format(response))
                # break

            # get_device_ID (0xA5)
            elif view.lower() in ("-gdi","deviceid","get_device_id"):                
                response = get_device_id(args[0])
                log_output("get device id:\n{}".format(response))
                # break

            # chassis_power_cycle
            elif view.lower() in ("-cpc","powercycle","chassis_power_cycle"):
                response = chassis_power_cycle(args[0])
                log_output("chassis power cycle : \n{}".format(response))
                # break

            # chassis_name
            elif view.lower() in ("-gcn","chasname","get_chassis_name"):
                print(" Platform: {}".format(PLATFORM))
                print(chassis_name_chr)
                log_output("get chassis name: \n{}".format(chassis_name_chr))                
                # break

            # get_sensor_info
            elif view.lower() in ("-gsi","sensoronfo","get_sensor_info"):                               
                response = get_sensor_info(args[0])
                log_output("get sensor info:\n{}".format(response))
                # break

            # get_power_reading
            elif view.lower() in ("-gpr","powerreading","get_sled_power"):                                
                response = get_power_reading(args[0])
                log_output("get power reading :\n{}".format(response))
                # break

            # sled_power_cycle
            elif view.lower() in ("-spc","sledpowercycle","sledreseat"):                
                response = sled_power_cycle(args[0])
                log_output("sled power cycle: \n{}".format(response))
                # break

            # sled_hard_reset
            elif view.lower() in ("-bhr","hardreset","bmcreset"):                
                response = bmc_hard_reset(args[0])
                log_output("bmc hard reset:\n{}".format(response))
                # break

            # sled_info
            elif view.lower() in ("-gsf","mcinfo","bmcinfo"):                              
                response = sled_info(args[0])
                log_output("bmcinfo: \n{}".format(response))
                # break

            # SEL logs
            elif view.lower() in ("-rsl","sel_logs","sel_logs_idrac"):                               
                response = sel_logs_idrac(args[0])
                log_output("sel_logs_idrac: \n{}".format(response))
                # break

            # sensor data idrac
            elif view.lower() in ("-rsd","sensor_data","sensor_data_idrac"):                                
                response = sensor_data_idrac(args[0])
                log_output("sensor_data_idrac: \n{}".format(response))
                # break

            # data repository idrac
            elif view.lower() in ("-sdr","data_repository","data_repository_idrac"):                              
                response = data_repository_idrac(args[0])
                log_output("data_repository_idrac: \n{}".format(response))
                # break

            # power budget idrac
            elif view.lower() in ("-pwr","power_budget","powertest_idrac"):                              
                response = powertest_sled(args[0])
                log_output("powertest_idrac: \n{}".format(response))
                # break

            # debug log command
            elif view in ("-dlc","IPMI_DCS","debug_log_commands"):                              
                response = set_cmd_debug_info(args[0],flag=True)                
                log_output("debug_log_commands: \n{}".format(response))
                # break

            # debug log command with reboot
            elif view in ("-dlcr","IPMI_DCS_START","debug_log_commands_reboot"):                              
                response = set_cmd_debug_log_w_reboot(args[0])
                log_output("debug_log_commands_reboot: \n{}".format(response))
                # break

            # debug log extended PSU Full adat with reboot
            elif view.lower() in ("-dlep","psu_extended_set","debug_log_extended_psu"):                              
                response = debug_log_extendedPsuInfo(args[0])
                log_output("debug_log_extendedPSU full data: \n{}".format(response))
                # break

            # dumpPSU ALL
            elif view in ("-dpsu","dumpPSU","dumpPSU ALL"):                              
                response = dumpPSU(args[0])
                log_output("dumpPSU serial command output: \n{}".format(response))
                # break   

            # Any other rootshell command
            elif view.lower() in ("-rootshell","rootshell"):                              
                response = rootshell_sled(args[0])
                log_output("rootshell command output: \n{}".format(response))
                # break       

            # Any other ipmi command
            elif view.lower() in ("-ipmitool","ipmitool"):                              
                response = ipmitool_sled(args[0])
                log_output("IPMItool command output: \n{}".format(response))
                # break

            # Any debug log command
            elif view.lower() in ("-debuglog", "debuglog"):                              
                response = debuglog_sled(args[0])
                log_output("debug log command output: \n{}".format(response))
                # break
                   
            else:
                print("Invalid Option...")
                log_output("Invalid Option...")
    else:
        usage()        

if __name__ == "__main__":   
    try: 
        USERNAME = sys.argv[2]
        PASSWORD = sys.argv[3]
    except:
        usage()
        sys.exit()
    try:
        main(sys.argv[1:])
    except:        
        PrintException()
        


