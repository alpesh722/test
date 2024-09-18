import time

import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains




def find_text_box(driver):
    try:
        driver.find_element("xpath","//div[@class='items-per-page dropdown']//div[@class='dropdown-toggle']").click()
        driver.find_element("xpath","//div[@class='dropdown-menu show']//a[@class='dropdown-menu-item dropdown-item ng-star-inserted'][normalize-space()='200']").click()
    except:
        pass
    # to identify the table rows
    r = driver.find_elements("xpath","//table[@class= 'grid-table']/tbody/tr")
    # to identify table columns
    c = driver.find_elements("xpath","//table[@class= 'grid-table']/tbody/tr[1]/td")
    # to get row count with len method
    rc = len (r)
    print(rc)
    # to get column count with len method
    cc = len (c)
    print(cc)

    check_box_id_list =[]
    for i in range (1, rc + 1) :
        q = driver.find_element("xpath","//table[@class= 'grid-table']/tbody/tr[{}]".format(i))
        # print(q.get_attribute("data-objid"))
        check_box_id_list.append(q.get_attribute("data-objid"))
    return check_box_id_list

def write_text_box(driver,check_box_id,text_value):
    try:
        text_box = driver.find_element("xpath","//td[@id='testStepsGrid_none_{}_actualResult']//div[@class='richtext-editor ng-star-inserted']".format(check_box_id))
        text_box.click()
    except:
        driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
        time.sleep(2)
        text_box = driver.find_element("xpath","//td[@id='testStepsGrid_none_{}_actualResult']//div[@class='richtext-editor ng-star-inserted']".format(check_box_id))
        text_box.click()

    text_box.find_element("xpath","//div[@class='note-editor note-frame card']//div[@class='note-editing-area']//div[@role='textbox']//p").send_keys(text_value)

def save_run_window(check_box_id_list,driver):
    # print(check_box_id_list)
    # update_test_notes(driver)
    # update_Test_Run_details(driver)
    time.sleep(5)
    driver.find_element("xpath", "//panel[@class='test-log-detail panel-wrapper block']//div[@class='panel-body']").click()
    time.sleep(5)
    for check_box_id in check_box_id_list:
        # print(check_box_id)
        driver.find_element("xpath", "//i[@id='testStepsGrid_none_{}_selectCheckbox']".format(check_box_id)).click()
        time.sleep(2)

    driver.find_element("xpath", "//span[@type='button']").click()
    driver.find_element("xpath", "//div[@class='dropdown-menu show']//a[@class='dropdown-item ng-star-inserted'][normalize-space()='Passed']").click()
    driver.find_element("xpath", "//button[@id='testpad_markStatus_btn']").click()
    
    driver.find_element("xpath","//span[normalize-space()='Execute Steps']").click()
    driver.find_element("xpath", "//button[@id='testpad_save']").click()

def update_Test_Run_details(driver):
    driver.find_element("xpath", "//span[normalize-space()='Test Run']").click()
    time.sleep(5)
    execution_type = driver.find_element("xpath","//property[@id='testrun_properties_DefaultField_ExecutionType(qMetry)']//span[@role='presentation']")
    driver.execute_script("arguments[0].scrollIntoView();",execution_type)    
    execution_type.click()
    selected_type = driver.find_element("xpath","//input[@role='searchbox']")
    selected_type.send_keys("Manual")
    selected_type.send_keys(Keys.ENTER)
    time.sleep(1)
        
    systems_development_engg = driver.find_element("xpath","//property[@id='testrun_properties_InheritedField_SystemsDevelopmentEngineer']//multiselect[@class='property-value multi-select']")
    driver.execute_script("arguments[0].scrollIntoView();",systems_development_engg)
    systems_development_engg.click()
    selected_type = driver.find_element("xpath","//input[@role='searchbox']")
    selected_type.send_keys("Etta Chieng")
    time.sleep(2)
    selected_type.send_keys(Keys.ENTER)
            
    driver.find_element("xpath", "//span[normalize-space()='Execute Steps']").click()
    time.sleep(5)

def update_test_notes(driver):
    time.sleep(1)
    driver.find_element("xpath", "//span[normalize-space()='Notes']").click()
    time.sleep(2)
    # driver.find_element("xpath", "//i[@class='note-icon-bold']").click()   
    
    text_notes = "AMC iDRAC 7.10.70.00 x16 , CPLD 1.2.0 , BIOS 2.2.0, CM 2.20.0.0.0.0 "
    text_notes_bc = "\nBC iDRAC 7.10.70.00 x16 , CPLD 1.4.0 , BIOS 1.2.3, CM 2.20.0.0.0.0"
    try:
        notes = driver.find_element("xpath","//div[@role='textbox']//p")
        time.sleep(2)
        notes.send_keys(text_notes_bc)
        time.sleep(2)
    except:
        pass

    finally:
        driver.find_element("xpath", "//span[normalize-space()='Execute Steps']").click()
        time.sleep(2)    
    
def read_excel_file():
    excel_data = pd.read_excel("./DSS_Test_Run_Functional_blank.xlsx",sheet_name="Test Runs_1", engine="openpyxl")
    df_data = pd.DataFrame(excel_data)
    data = df_data[["Run Order","Name","Test Step #","Test Step Actual Result"]]
    data["Run Order"].ffill(inplace=True)
    data["Run Order"] = data['Run Order'].apply(lambda x: int(x))
    return data

def remote_test_execution(driver,data,test_case_list):
    # data = read_excel_file()    
    for test_case_no in test_case_list:
        output_list = data[data["Run Order"] == test_case_no]["Test Step Actual Result"].tolist()
        print("*"*100)
        print("{} : {}".format(test_case_no,data[data["Run Order"]==test_case_no]["Name"].tolist()[0]))
        print("*"*100)
        # update_Test_Run_details(driver)
        update_test_notes(driver)
        # time.sleep(5)
        check_box_id_list = find_text_box(driver)
        print("Total number of steps in a test case :",len(check_box_id_list))
        for check_box_id,output in zip(check_box_id_list,output_list):
            # if output is blank in xlsx sheet than it shows nan which in float type
            # nan replace by ""
            try:
                output = output.replace("\n",(Keys.SHIFT+Keys.ENTER+Keys.SHIFT))
                output = output.replace("\t","    ")
            except:
                output = ""
            print(output)
            # print(check_box_id)
            time.sleep(2)
            write_text_box(driver,check_box_id,output)
        save_run_window(check_box_id_list,driver)
        time.sleep(10)




