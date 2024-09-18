import time
import sys
import json
import textwrap
import warnings
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common import exceptions

warnings.filterwarnings("ignore")

with open("./config.json", "r") as fp:
    try:
        CONFIG = json.load(fp)
    except json.JSONDecodeError:
        print("Config is not valid JSON")
        sys.exit(1)
    except Exception as ex:
        print("Exception -", type(ex))
        print(ex.args)
        sys.exit(1)

now = datetime.now()
date0 = now.strftime("%d%m%y")
time0 = now.strftime("%H%M%S")
file_name = "{}_log_{}_{}.log".format(__file__.split("\\")[-1].split(".")[0],date0, time0)
PASS = "PASS"
FAIL = "FAIL"

class iDRAC_GUI_FW_Update_v3:
    def usage(self):
        usage = textwrap.dedent('''
        ======================================================================
        Confirm Sled IP, Update_FW_path and Cycles in config.json file            

        i.e.: iDRAC_GUI_FW_Update.py 
        ======================================================================
        ''')
        print(usage)   

    def PrintException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename        
        logging.exception('EXCEPTION IN ({}, LINE {}): {}'.format(filename, lineno, exc_obj))

    def install_fw_dup(self,driver):        
        fw_update = driver.find_element("xpath","//a[@class='ng-binding']\
            [normalize-space()='System Update']")
        fw_update.click()
        time.sleep(2)
        table_e = fw_update.find_elements("xpath","//form[@name='FWUpdate.Local']\
            //table[@class='table ng-scope']/tbody/tr/td")   
        # browse file to upload
        for i in table_e:            
            if i.get_attribute("ng-switch-when") == "file":
                fw_update_link = i.find_element("xpath","(//input[@id='FWUpdate.Local.fwfile'])[1]")
                fw_update = i.find_element("xpath","//input[@id='FWUpdate.Local.fwfile'] ")                               
                i.find_element("xpath","//input[@id='FWUpdate.Local.fwfile'] ").send_keys(CONFIG["Update_fw_path"])                
                i.find_element("xpath","//button[normalize-space()='Upload']").click()
                logging.info(" File uploading...")

        # select checkbox and click install
        time.sleep(10) 
        # wait until the file is uploaded and after that select checkbox  
        try:    
            WebDriverWait(fw_update, 100).until(EC.element_to_be_clickable((
                "xpath","""//input[@ng-class="{'checked' : row.checked, '' : !row.checked}"]"""))).click()
            # fw_update.find_element("xpath","""//input[@ng-class="{'checked' : row.checked, '' : !row.checked}"]""").click()                    
        except:
            logging.error("- FAIL: Couldn't find the checkbox, File is not uploaded in time.")
        # click install        
        try:
            fw_update.find_element("xpath","//button[normalize-space()='Install']").click()
        except exceptions.NoSuchElementException:
            try:
                fw_update.find_element("xpath","//button[normalize-space()='Install and Reboot']").click()
            except:
                fw_update.find_element("xpath","//button[normalize-space()='Cancel']").click()
                logging.info("Cancel Firmware update as it may not compatible")
                return FAIL


        time.sleep(1)
        logging.info(" File uploaded successfully")
        try:
            fw_update.find_element("xpath","//button[normalize-space()='Job Queue']").click()
        except:
            fw_update.find_element("xpath","//button[normalize-space()='Ok']").click()
            time.sleep(1)
            fw_update.find_element("xpath","//button[normalize-space()='Job Queue']").click()

        time.sleep(5)
        logging.info(" Job ID created")

    def browser_access(self,sled_ip,driver):       
        
        driver.get("https://{}/".format(sled_ip))
        # driver.implicitly_wait(20)
        # #identify for login and password box and enter the value
        driver.find_element("xpath","//input[@name='username']").send_keys("root")
        driver.find_element("xpath","//input[@name='password']").send_keys("calvin")
        driver.find_element("xpath","//button[@type='submit']").send_keys(Keys.ENTER)
        logging.info(" Successfully login to sled ip : {}".format(sled_ip))
        time.sleep(1)
        # navigate to maintenance page -> system update
        maintenance = driver.find_element("xpath","//strong[@id='maintenance']")
        maintenance.click()
        time.sleep(10)
        return maintenance
    
    def init_fw_update(self,sled_ip,cycles,driver):        
        global idrac_reboot 
        idrac_reboot = False
        driver = self.browser_access(sled_ip,driver)        
        for i in range(cycles):
            start_time = datetime.now()
            logging.info(" ***** FW update cycle : {}/{} at {}".format(i+1, cycles, start_time))            
            if self.install_fw_dup(driver) == FAIL:
                return FAIL
            # except Exception as e:
            #     logging.exception(type(e))
            #     return FAIL
            # view job queue (optional)
            # maintenance.find_element("xpath","//li[@id='maintenance.jobqueue']").click()            
            # view LC logs
            lc_log = driver.find_element("xpath","//a[@class='ng-binding'][normalize-space()='Lifecycle Log']").click()
            time.sleep(10)
            stale_element = False
            count = 1
            total_critical_log = []            
            logging.info(" Verifying LC logs")
            last_lclog_time0 = ""
            while True:  
                try: 
                    #last LC log time                                              
                    driver.find_element("xpath","//b[@class='header-links ng-scope']").click() 
                    time.sleep(5)
                    lc_log_time0 =  driver.find_element("xpath","//table[@class='table table-striped ']/tbody/tr[1]/td[3]")
                    last_lclog_time1 = lc_log_time0.text
                
                except exceptions.NoSuchElementException:                    
                    # on iDRAC reboot webpage disconnect and this exception occures
                    # driver.refresh()
                    idrac_reboot = True
                    logging.error("- FAIL: Unable to load LC log page due to iDRAC connection lost\n")
                    return FAIL   
                except exceptions.StaleElementReferenceException as e:
                    # this exception occures when there is not updated webpage for more time                                     
                    if stale_element:
                        logging.error("- FAIL: Unable to load LC log page \n")
                        return FAIL
                    else:
                        logging.error("- ERROR: Stale Element not found\n")
                        pass 
                    stale_element = True    
                logging.info(" ^")   # indicates number of times LC log page refresh                            
                
                # check for new logs entry
                if last_lclog_time1 == last_lclog_time0:
                    logging.info(" Last LC log time: {}".format(last_lclog_time1)) 
                    time.sleep(50)
                    continue                      
                else:
                    pass

                # to identify the table rows                
                r = driver.find_elements("xpath","//table[@class='table table-striped ']/tbody/tr")
                # to identify table columns
                c = driver.find_elements("xpath","//table[@class='table table-striped ']/tbody/tr[1]/td")
                # to get row count with len method
                total_r = len (r)                
                # to get column count with len method
                total_c = len (c)                
                msg_id = []  
                critical_log = []      
                for i in range(5):  
                    # search if any critical log occure in first five logs             
                    x = driver.find_element("xpath","(//span[@ng-class='column.appScope.severityIcon(row.severity)'])[{}]".format(i+1))
                    # print(x.get_attribute("class"))
                    if (x.get_attribute("class")) == "ng-scope ci ci-color-red ci-status-critical-core":                  
                        x = driver.find_element("xpath","//table[@class='table table-striped ']/tbody/tr[{}]".format(i+1))                
                        x = x.text
                        x = x.split(" ")                 
                        critical_log_element = " ".join(x[1:])
                        critical_log.append(critical_log_element) 
                    # get message ID
                    x = driver.find_element("xpath","//table[@class='table table-striped ']/tbody/tr[{}]/td[4]".format(i+1))                    
                    msg_id.append(x.text)  
                
                # time to verify FW update duration
                time_duration = str((datetime.now()-start_time))[0:7]
                

                if "SUP0518" in msg_id:            
                    end_time = datetime.now()
                    logging.info(" FW update successfull at {}".format(end_time))
                    logging.info(" FW update complete in {}".format(end_time-start_time))                    
                    time.sleep(5)
                    if len(critical_log) != 0:
                        logging.warning("- WARNING: Critical log present in LC logs")
                    else:
                        logging.info(" Not any Critical log present in LC logs")                                
                    break
                
                
                if "SUP0520" in msg_id:
                    logging.error("- FAIL: Unable to update FW, script stopped\n")
                    # comment/uncomment below lines as per requirement
                    break                    
                    # return FAIL
                
                if "SUP0516" in msg_id:
                    logging.info(" Installation in Progress (Updating Firmware)")

                if str(time_duration)[0:7] > "0:20:00":
                    logging.error("- FAIL: Timeout of 20 minutes has been hit since start of the update process, script stopped\n")
                    return FAIL
                else:
                    count += 1
                    if critical_log:
                        total_critical_log.append(critical_log)
                        logging.warning("- WARNING: Critical log present in LC logs during FW update")      

                # # check for new logs entry
                # if last_lclog_time1 == last_lclog_time0:
                #     logging.info(" There are not any updated new LC logs, last log time: {}".format(last_lclog_time1)) 
                #     time.sleep(50)
                #     continue                      
                # else:
                #     pass
                # last LC log time
                #lc_log_time0 =  driver.find_element("xpath","//table[@class='table table-striped ']/tbody/tr[1]/td[3]")
                last_lclog_time0 = last_lclog_time1    #lc_log_time0.text
                time.sleep(15)

            if total_critical_log:                
                logging.info(total_critical_log)                
                logging.error("- FAIL: Critical log occure, script stopped\n")                
                # return FAIL            

            # add time delay before starting another cycle of FW update
            time.sleep(80)        

    def main(self):        
        logging.info('---------- Started ----------')
        sled_ip = CONFIG["Sled1_IP"]
        cycles = int(CONFIG["cycles"]) 
        chr_options = Options()
        chr_options.add_argument('--headless')              # added in v4, for not virwing GUI
        chr_options.add_argument('--ignore-ssl-errors=yes')
        chr_options.add_argument('--ignore-certificate-errors')
        chr_options.add_experimental_option("detach", True)
        chr_options.add_argument("--allow-running-insecure-content")
        chr_options.add_argument('--allow-insecure-localhost') # differ on driver version. can ignore. 
        # caps = chr_options.to_capabilities()
        # caps["acceptInsecureCerts"] = True        
        chr_options.add_argument("--disable-proxy-certificate-handler")    
        chr_options.add_argument("--disable-content-security-policy")
        service = Service(executable_path= CONFIG["chromedriver_path"])
        logging.info(" Opening Browser")
        driver = webdriver.Chrome(service=service, options=chr_options)        

        #maximize the window size
        driver.maximize_window()
        #delete the cookies 
        driver.delete_all_cookies()
        #navigate to the url 
        driver.implicitly_wait(20)    
        try:
            if self.init_fw_update(sled_ip,cycles,driver) == FAIL:
                time.sleep(5)  
                if idrac_reboot:
                    logging.info(" Connection lost because of iDRAC is not reachable") 
                else:         
                    logging.error("- ERROR: issue found during FW update, terminate script")
        except Exception as e:
            #logging.exception(type(e))
            self.PrintException()

        time.sleep(5)    
        driver.close()
        logging.info(" Close Browser")
        logging.info('---------- Comleted ---------')

if __name__ == "__main__":
    test = iDRAC_GUI_FW_Update_v3() 
    test.usage()   
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler(file_name),
                                  logging.StreamHandler()])
    test.main()
    
    

    

