import time
import sys
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

warnings.filterwarnings("ignore")
DRIVER_PATH =  "D:\\selenium_tutorial\\chromedriver-win64\\chromedriver.exe"

def init_product_test(driver,args): 
    
    search_product = " ".join(args)  
    driver.get("https://www.amazon.in")        
    driver.find_element(By.XPATH,"//input[@id='twotabsearchtextbox']").send_keys(search_product)    
    driver.find_element(By.XPATH,"//input[@id='nav-search-submit-button']").send_keys(Keys.ENTER)
    print(" Successfully entered {} into search bar".format(search_product))    
    # time.sleep(10)    
    driver.implicitly_wait(20)   
    product_name = []   
    product_price_list = []    
    products = {}    
    items = driver.find_elements(By.XPATH,'//div[contains(@class, "s-result-item s-asin")]')
    for item in items:
        name = item.find_element(By.XPATH,'.//span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)        
        try:
            price = item.find_element(By.XPATH,'.//span[@class="a-price"]//span[@class="a-offscreen"]')
            # print(price.get_attribute("innerHTML"))
            product_price = price.get_attribute("innerHTML")
            product_price = int(product_price.strip('₹').replace(',',''))  
            
        except Exception as e:
            product_price = 0
            
        product_price_list.append(product_price)
        # print(name.text , " : ", product_price)        
        products[name.text] = product_price   
        
    # sorting by this method not working 
    # new_dict = sorted(products.values())
    # for val in new_dict:        
    #     print("{} : {}".format(val,list(products.keys())[list(products.values()).index(val)])) 

    # Method 1:  
    #sort dictionary by value
    sorted_dict = dict(sorted(products.items(), key=lambda item: item[1]))
    print()
    for key in sorted_dict.keys():
        print( " ",sorted_dict[key]," : ",key )

    # Method 2:
    # dict_sort = bubble_sort_dict(products)
    # items = list(products.items())
    # n = len(items) 
    # for i in range(n - 1):
    #     for j in range(0, n - i - 1):
    #         if items[j][1] > items[j + 1][1]:
    #             items[j], items[j + 1] = items[j + 1], items[j]
    # print()
    # y = dict(items)
    # for key in y.keys():
    #     print(" ",y[key]," : ",key)

def bubble_sort_dict(d):
    items = list(d.items())
    n = len(items)
 
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if items[j][1] > items[j + 1][1]:
                items[j], items[j + 1] = items[j + 1], items[j]
 
    return dict(items)

if __name__ == "__main__":      
    search_product = sys.argv[1:]
    if not search_product:
        print("Provide product name to search !")
        sys.exit(1)
    chr_options = Options()
    # chr_options.add_argument('--headless')           
    chr_options.add_experimental_option("detach", True)
    service = Service(executable_path= DRIVER_PATH)    
    driver = webdriver.Chrome(service=service, options=chr_options)     
    # driver.implicitly_wait(20)      
    
    try:
        init_product_test(driver,search_product)         
    except Exception as e:
        print(e) 
    time.sleep(5)    
    driver.close()
    
    
    

    

