# imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# get driver object
def get_driver():
    # return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')  
options.add_argument('--disable-dev-shm-usage')

# function to get all the states in India by scraping knowindia.india.gov.in site
def get_states_indian():
    states = []
    page = 'https://knowindia.india.gov.in/states-uts/'
    url = page.encode('ascii', 'ignore').decode('unicode_escape')
    driver = get_driver()
    driver.get(url)
    elements = driver.find_elements(By.XPATH,"/html/body/div[1]/div[2]/section[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[@class='page-menu']")
    for e in elements:
        for i in e.find_elements(By.TAG_NAME, 'a'):
            state = i.text.split('\n')[0]
            states.append(state.strip().lower())
    driver.quit()
    return states

# function to get all the countries by scraping the country.io site
def get_countries():
    countries = []
    page = 'http://country.io/countries/'
    url = page.encode('ascii', 'ignore').decode('unicode_escape')
    driver = get_driver()
    driver.get(url)
    elmement = driver.find_element(By.XPATH, "/html/body/section[1]/div[1]/div[1]")
    lst = elmement.find_elements(By.TAG_NAME, 'a')
    for i in lst:
        countries.append(i.text.strip().lower())
    driver.quit()
    return countries

# try except block to handle failures if happened while scraping states and countries 
try:
    states    = get_states_indian()
    countries = get_countries()
except:
    states    = ['andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chhattisgarh', 'goa', 'gujarat', 'haryana', 'himachal pradesh', 'jharkhand', 'karnataka', 'kerala', 'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura', 'uttarakhand', 'uttar pradesh', 'west bengal']
    countries = ['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire, saint eustat...', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean ...', 'british virgin islands', 'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos islands', 'colombia', 'comoros', 'cook islands', 'costa rica', 'croatia', 'cuba', 'curacao', 'cyprus', 'czech republic', 'democratic republic o...', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'east timor', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern terri...', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdo...', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'ivory coast', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'north korea', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territory', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'republic of the congo', 'reunion', 'romania', 'russia', 'rwanda', 'saint barthelemy', 'saint helena', 'saint kitts and nevis', 'saint lucia', 'saint martin', 'saint pierre and miqu...', 'saint vincent and the...', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the...', 'south korea', 'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor o...', 'uruguay', 'u.s. virgin islands', 'uzbekistan', 'vanuatu', 'vatican', 'venezuela', 'vietnam', 'wallis and futuna', 'western sahara', 'yemen', 'zambia', 'zimbabwe']

# function to process skill list passed and in turn returns a list of expected values
def process_skills(skills_lst):
    skills = [i.text.lower() for i in skills_lst if 'project' not in i.text.lower() and 'internship' not in i.text.lower() and 'bca' not in i.text.lower() and 'b-tech' not in i.text.lower() and 'mca' not in i.text.lower() and 'be' not in i.text.lower() and 'computer science' not in i.text.lower() and 'b - tech' not in i.text.lower()]
    while("" in skills):
        skills.remove("")
    while("data engineer" in skills): 
        skills.remove("data engineer")
    while("data engineering" in skills):
        skills.remove("data engineering")
    while("data scientist" in skills):
        skills.remove("data scientist")
    while("data analyst" in skills):
        skills.remove("data analyst")
    while("data architect" in skills):
        skills.remove("data architect")
    while("machine learning engineer" in skills):
        skills.remove("machine learning engineer")
    return skills

# function to extract cities from location string passed as parameter
def parse_location(location_str : str):
    location = [i.strip() for i in location_str.replace('/', ',').split(",")]
    loc_lst = []
    for loc in location:
        if loc not in states and loc not in countries:
            if loc == 'bangalore':
                loc = 'bengaluru'
            elif loc == 'gurgaon':
                loc = 'gurugram'
            elif 'mumbai' in loc:
                loc = 'mumbai'
            elif 'noida' in loc:
                loc = 'noida'
            loc_lst.append(loc)
    return list(set(loc_lst)) # remove duplicates

# function to parse job type string passed and in turn returns a list of expected values
def parse_job_type(job_type_str):
    type_lst = []
    if 'full' in job_type_str:
        type_lst.append('full time')
    if 'home' in job_type_str:
        type_lst.append('work from home')
    if 'contract' in job_type_str:
        type_lst.append('contract job')
    if 'remote' in job_type_str:
        type_lst.append('remote job')
    if 'part' in job_type_str:
        type_lst.append('part time')
    return type_lst

# function to parse experience string passed and returns required experience integer value
def parse_experience(experience_str):
    if '-' in experience_str:
        lst = [int(i) for i in experience_str.split(' ')[0].split('-')]
        res = sum(lst) // len(lst)
    else:
        if experience_str == 'fresher':
            res = 0
        else:
            res = int(experience_str.split(' ')[0])
    return res

# function to get a list of job details by scraping foundit.com with job role passed as parameter
def get_job_details(job_role : str):
    fnl_lst = []
    lst = job_role.split(' ')
    str_query = "+".join(lst)
    page = f'https://www.foundit.in/srp/results?query="{str_query}"'
    url = page.encode('ascii', 'ignore').decode('unicode_escape')
    driver = get_driver()
    driver.get(url)
    count = 0
    while count <= 100:
        elements = driver.find_elements(By.XPATH, "/html/body/div[@id='srpThemeDefault']/div[@class='srpContainer']/div[@id='srpContent']/div[@class='srpCardContainer']/div[@class='srpResultCard']/div")
        for element in elements:
            try:
                job_dict = {}
                job_title                = element.find_element(By.CLASS_NAME, "jobTitle").text
                company_name             = element.find_element(By.CLASS_NAME, "companyName").text
                skills_lst               = element.find_elements(By.CLASS_NAME, "skillTitle")
                skills                   = process_skills(skills_lst)
                sub_element              = element.find_element(By.CLASS_NAME, "cardBody")
                job_type_str             = sub_element.find_element(By.XPATH, "div[1]/div[@class='details']").text.lower()
                job_types                = parse_job_type(job_type_str)
                locations_str            = sub_element.find_element(By.XPATH, "div[2]/div[@class='details']").text.lower()
                locations                = parse_location(locations_str)
                experience_str           = sub_element.find_element(By.XPATH, "div[3]/div[@class='details']").text.lower()
                experience               = parse_experience(experience_str)
                job_dict['job_title']    = job_title
                job_dict['company_name'] = company_name
                job_dict['skills']       = skills
                job_dict['job_types']    = job_types
                job_dict['locations']    = locations
                job_dict['experience']   = experience
                fnl_lst.append(job_dict)
                count += 1
                if count == 100:
                    break
            except:
                pass
        try:
            element.find_element(By.CLASS_NAME, "mqfisrp-right-arrow").click()
        except :
            break
    driver.quit()
    return fnl_lst
