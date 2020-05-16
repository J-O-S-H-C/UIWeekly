import json
from selenium import webdriver

with open('config.json', encoding='utf-8') as file:
    config = json.load(file)

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

if(config["login"]["username"] and config["login"]["password"] != "none"):
    username = config["credentials"]["username"]
    password = config["credentials"]["password"]
else:
    username = input("Username: ")
    password = input("Password: ")

driver = webdriver.Firefox()
driver.get("https://secure.esd.wa.gov/home/")
driver.implicitly_wait(20)

def login(username, password):
    userInput = driver.find_element_by_id("username")
    passInput = driver.find_element_by_id("password")
    userInput.send_keys(username)
    passInput.send_keys(password)
    passInput.submit()

def next():
    try:
        driver.find_element_by_id("j-o1").click()
    except:
        prRed("Could not go to next page.")
        break

def save():
    try:
        driver.find_element_by_id("j-l1").click()
    except:
        prRed("Weekly Claim Failed to save.")
        break

def questionVerify(question):
    for element in driver.find_elements_by_xpath(".//span[@class='CaptionLabel ']"):
        if(element.text.lower() == question.lower()):
            return True
    return False

def getAnswer(question):
    for title in config["quest"]:
        if(question.lower() == config["quest"][title]["question"].lower()):
            return config["quest"][title]["answer"]

def spanText(test, tag=None, type=None):
    if(type != None and tag != None and type.lower() == "class"):
        xpath = ".//span[@class = '" + tag + "']"
    else:
        xpath = ".//span"
    for elem in driver.find_elements_by_xpath(xpath):
        if (elem.text == test):
            elem.click()

#------------------------------------------------------------------------------
login(username, password)
driver.find_element_by_partial_link_text("Apply for unemployment benefits or manage your current and past claims").click()
spanText("No", "ui-button-text")

try:
    pua = driver.find_element_by_partial_link_text("PUA Claim")
    if (pua):
        puaExists = True
        uiExists = False
except:
    pass

try:
    ui = driver.find_element_by_partial_link_text("UI Claim")
    if(ui):
        uiExists = True
        puaExists = False
except:
    pass

driver.find_element_by_partial_link_text("weekly claim to file").click()
driver.find_element_by_css_selector("button.FastEvtLinkClick").click()
next()
spanText("I agree")
next()
for qNum in config["quest"]:

    if any("ALL" in typ for typ in config["quest"][qNum]):
        claimType = "ALL"
    if(puaExists and uiExists == False):
        if any("PUA" in typ for typ in config["quest"][qNum]):
            claimType = "PUA"
    elif(uiExists and puaExists == False):
        if any("UI" in typ for typ in config["quest"][qNum]):
            claimType = "UI"

    if(questionVerify(config["quest"][qNum][claimType]["question"])):
        spanText(getAnswer(config["quest"][qNum][claimType]["question"]))
        print(config["quest"][qNum][claimType]["question"], end=" ") 
        prGreen(getAnswer(config["quest"][qNum][claimType]["question"]))
        if(int(qNum) < 11 or (puaExists and int(qNum) == 11) or int(qNum) == 12):
            next()
            if(puaExists and int(qNum) == 11):
                break
        elif(uiExists and int(qNum) == 11):
            break
    else:
        prRed("Error: Could not verify Question")
        break

if(config["settings"]["save"]):
    save()
    prGreen("Weekly claim has been saved")
    driver.quit()

next()#presents summary if not saving
