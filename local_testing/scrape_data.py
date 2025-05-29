# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
import shutil
import time
import json
import shutil

# get driver object
def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--start-maximized")
    driver_path = shutil.which('chromedriver')
    chrome_service = webdriver.ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    driver.delete_all_cookies()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# function to get job details by scraping foundit.com with job role and required count passed as parameters
def get_jobs(job_role:str, cnt:int):
    lst = job_role.split(' ')
    str_query = "+".join(lst)
    page = f'https://www.foundit.in/srp/results?query="{str_query}"'
    url = page.encode('ascii', 'ignore').decode('unicode_escape')
    driver = get_driver()
    driver.get(url)
    fnl_lst = []
    count = 0
    while count <= cnt:
        driver.refresh()
        if count == cnt:
            break
        x_pth1 = "/html\
                /body\
                /div[@id='srpThemeDefault']\
                /div[@class='srpContainer']\
                /div[@id='srpContent']\
                /div[@class='srpCardContainer']\
                /div[@class='srpResultCard']\
                /div"
        elements = driver.find_elements(By.XPATH,x_pth1)
        for element in elements:
            if count == cnt:
                break
            job_data = {}
            try:
                ele = element.find_element(By.CLASS_NAME,"jobTitle")
                ele.click()
                time.sleep(1)
                x_pth2 = "/html\
                /body\
                /div[@id='srpThemeDefault']\
                /div[@class='srpContainer']\
                /div[@id='srpContent']\
                /div[@class='srpJdContainer']"
                element2 = driver.find_element(By.XPATH,x_pth2)
                job_data['job_title'] = element2.find_element(By.CLASS_NAME,"jdTitle").text
                job_data['company_name'] = element2.find_element(By.CLASS_NAME,"jdCompanyName").text
                highlights = [h for h in element2.find_elements(By.CLASS_NAME,"highlightsRow")]
                job_data['experience'] = highlights[0].find_element(By.XPATH,"./div[1]").text
                try:
                    job_data['salary'] = highlights[0].find_element(By.XPATH,"./div[2]").text
                except:
                    job_data['salary'] = None
                job_data['location'], job_data['industry'] =  highlights[1].text, highlights[2].text
                job_data['job_description'] = element2.find_element(By.CLASS_NAME,"jobDescInfoNew").text
                job_data['skills'] = skills = [s.text for s in element2.find_elements(By.CLASS_NAME,"pillItem")]
                # print(job_data)
                fnl_lst.append(job_data)
                count += 1
            except Exception as e:
                pass
        try:
            element.find_element(By.CLASS_NAME, "mqfisrp-right-arrow").click()
            time.sleep(2)
        except Exception as e:
            pass 
    driver.quit()
    return fnl_lst