import time
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

from remote_testing_updated import remote_test_execution


def expand(expand_link):
    global driver
    # find id for  test suit
    link_id = expand_link.get_attribute("id")
    # print("link id to be expand :",link_id)
    # using link id,find link for dropdown
    link_value = "//a[@id='{}']".format(link_id) +"//span"
    expand_links = expand_link.find_elements("xpath", link_value)
    for link in expand_links:
        # print("attribute id:",link.get_attribute("id"))
        if "expand" in link.get_attribute("id"):
            dropdown_link = driver.find_element("xpath","//span[@id='{}']".format(link.get_attribute("id")))
    return dropdown_link,link_id

def read_excel_file():
    excel_data = pd.read_excel("./DSS_Test_Run_Functional_blank.xlsx",sheet_name="Test Runs_1", engine="openpyxl")
    df_data = pd.DataFrame(excel_data)
    data = df_data[["Run Order","Name","Test Step #","Test Step Actual Result"]]
    data["Run Order"].ffill(inplace=True)
    data["Run Order"] = data['Run Order'].apply(lambda x: int(x))
    return data

chr_options = Options()
chr_options.add_experimental_option("detach", True)
service = Service(executable_path="E:\\NFS_SHARE\\AMC_DSS\\CT_testing_2.20.0.0.0.0\\selenium_test\\chromedriver-win64\\chromedriver.exe")

print("sample test case started")

driver = webdriver.Chrome(service=service, options=chr_options)
#driver=webdriver.firefox()
#driver=webdriver.ie()

#maximize the window size
driver.maximize_window()

#delete the cookies 
driver.delete_all_cookies()

#navigate to the url
driver.get("https://qtest.gtie.dell.com/")

# #identify for login and password box and enter the value
driver.find_element("xpath","//input[@id='userName']").send_keys("alpesh_dhokia99")
driver.find_element("xpath","//input[@id='password']").send_keys("DellDCS@0524")
driver.find_element("xpath","//a[@id='loginButton']").send_keys(Keys.ENTER)

# identify DSS qtest
actions = ActionChains(driver)
driver.find_element("xpath","//div[@id='topLeftTitle']").click() # SLS engg vendor //div[@id='topLeftTitle']
time.sleep(5)
actions.move_to_element(driver.find_element("xpath","//a[normalize-space()='DSS']")).click().perform()
time.sleep(5)

# select test execution tab
driver.find_element("xpath","//span[@id='working-tab_test-execution_label']").click()
time.sleep(5)


# find all links and then search for AMC test suit link
links = driver.find_elements("xpath", "//a")

for link in links:
    if link.text == "AMC" and link.get_attribute("class") == "tree-item removable":
        amc_link = link
amc_dropdown_link, amc_link_id = expand(amc_link)
# Expand AMC test suit
amc_dropdown_link.click()
time.sleep(5)

# find OT phase expand link
links = driver.find_elements("xpath", "//div[@id='{}']//div".format(amc_link_id+"-children"))
for link in links:
    print(link.get_attribute("title"))
    if "OT" in link.get_attribute("title"):
#         print(link.get_attribute("title"))
        amc_ot_phase_link = link.find_element("xpath", "//div[@title='{}']//a".format(link.get_attribute("title")))
#         print(amc_ot_phase_link.get_attribute("id"))
# Expand OT test suit
ot_dropdown_link, _ = expand(amc_ot_phase_link)
try:
    ot_dropdown_link.click()
except:
    # if Ot test suit can't expand than expand AMC test suit first 
    # and again expant OT
    amc_dropdown_link.click()
    time.sleep(5)
    ot_dropdown_link.click()
time.sleep(5)

try:
    driver.find_element("xpath","//span[@class='text'][normalize-space()='AMC FW 2.20.0.0.0.0 - Functional Test']").click()
except:
    # if required test suit can't expand than expand OT test suit first 
    ot_dropdown_link.click()
    time.sleep(5)
    driver.find_element("xpath","//span[@class='text'][normalize-space()='AMC FW 2.20.0.0.0.0 - Functional Test']").click()
time.sleep(5)

try:
    driver.find_element("xpath","//div[@class='items-per-page dropdown']//div[@class='dropdown-toggle']").click()
    driver.find_element("xpath","//div[@class='dropdown-menu show']//a[@class='dropdown-menu-item dropdown-item ng-star-inserted'][normalize-space()='200']").click()
except:
    pass

time.sleep(5)

# to identify the table rows
r = driver.find_elements("xpath","//table[@class= 'grid-table']/tbody/tr")
# to identify table columns
c = driver.find_elements("xpath","//table[@class= 'grid-table']/tbody/tr[3]/td")
# to get row count with len method
rc = len (r)
print(rc)
# to get column count with len method
cc = len (c)
print(cc)
# to traverse through the table rows excluding headers
check_box_id_list = []
test_no_list = []
test_title_list = []
for i in range (1, rc + 1) :
    q = driver.find_element("xpath","//table[@class= 'grid-table']/tbody/tr[{}]".format(i))
#     print(q.get_attribute("data-objid"))
    check_box_id_list.append(q.get_attribute("data-objid"))
    
# to get all the cell data with text method
    test_no_list.append(driver.find_element("xpath", "//table[@class= 'grid-table']/tbody/tr[{}]/td[{}]".format(i,3)).text)
    test_title_list.append(driver.find_element("xpath", "//table[@class= 'grid-table']/tbody/tr[{}]/td[{}]".format(i,5)).text)

test_case_dict = {j:[i, k] for i, j, k in zip(check_box_id_list, test_no_list, test_title_list)}
# print(test_case_dict)

data = read_excel_file()
for test_no in range(168,170,2):            # place range as per the rquired test case entry and also .
    data_1 = data[(data["Run Order"]>=test_no ) & (data["Run Order"]< (test_no+2))]  
    test_case_list = []
    for test_case in range(test_no,data_1["Run Order"].max()+1):
        result_list = data[data["Run Order"]==test_case]["Test Step Actual Result"].tolist()
        if not all(i != i for i in result_list):
            test_case_list.append(test_case)
    print(test_case_list)
    if test_case_list:
        for key in test_case_list:
            try:
                driver.find_element("xpath","//i[@id='testRunGrid_none_{}_selectCheckbox']".format(test_case_dict[str(key)][0])).click()
            except:
                driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
                # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(2)
                driver.find_element("xpath","//i[@id='testRunGrid_none_{}_selectCheckbox']".format(test_case_dict[str(key)][0])).click()
            
            # print(test_case_dict[str(key)][0])
            time.sleep(1)
        driver.find_element("xpath","//button[@id='testRunGrid_btnRun']").click()

        time.sleep(15)
        window_ids = driver.window_handles
        parent_window_id = window_ids[0]
        child_window_id = window_ids[1]
        # print(parent_window_id, child_window_id)
        driver.switch_to.window(child_window_id)
        print(driver.title)
        #maximize the window size
        driver.maximize_window()

        remote_test_execution(driver,data,test_case_list)
        driver.close()
        time.sleep(10)
        driver.switch_to.window(parent_window_id)
        time.sleep(5)
    else:
        print("test results are not found for {} to {}".format(test_no,test_no+9))

actions = ActionChains(driver)
user = driver.find_element("xpath", "//p[@class='username show-user-menu']")
logout = driver.find_element("xpath", "//li[@id='log-out-link']")
actions.move_to_element(user).move_to_element(logout).click().perform()
driver.close()
