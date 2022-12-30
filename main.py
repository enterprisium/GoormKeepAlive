from time import sleep
from argparse import ArgumentParser
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

# 遍历GoormIDE - Dashboard页面所有<a>标签
def searchTerminalUrl(broswer: Chrome):
    for linktag in broswer.find_elements(By.TAG_NAME,"a"):
        linkhref = linktag.get_attribute("href")
        if (linkhref):
            if "ide-run.goorm.io/terminal" in linkhref:
                return linkhref
    return 0

def keepAlive(broswer: Chrome, user: str, passwd: str):
    login_url = "https://accounts.goorm.io/login?return_url=aHR0cHM6Ly9pZGUuZ29vcm0uaW8vbXkvZGFzaGJvYXJk&keep_login=true"
    broswer.get(login_url)
    WebDriverWait(broswer,30).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app"]/section/div[4]/button')
            )
        )
    inputEmail = broswer.find_element(By.NAME, "email")
    inputPasswd = broswer.find_element(By.NAME, "password")
    inputEmail.clear()
    inputEmail.click()
    inputEmail.send_keys(user)
    inputPasswd.clear()
    inputPasswd.click()
    inputPasswd.send_keys(passwd)
    broswer.find_element(By.XPATH, '//*[@id="app"]/section/div[4]/button').click()
    WebDriverWait(broswer,30).until(
    EC.url_matches("https://ide.goorm.io/my/dashboard")
    )
    broswer.implicitly_wait(30)
    terminalUrl = searchTerminalUrl(broswer)
    print("Start KeepAlive Workflow!Enjot it!")
    while 1:
        broswer.get(terminalUrl)
        broswer.implicitly_wait(30)
        sleep(7200)
    return 0

def main():
    chromeOptions = Options()   
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--no-sandbox')
    parser = ArgumentParser(
        description="Less is More."
    )
    parser.add_argument("-U","--user",help="Your Goorm Account Email",required=True,type=str)
    parser.add_argument("-P","--passwd",help="Your Goorm Account Password",required=True,type=str)
    parser.add_argument("--noheadless",help="Run Chronium in Normal Mode",required=False,action="store_true")
    parser.add_argument("-DRV","--chromedriver",help="Chromedriver Path(Default in $PATH)",required=False,type=str)
    args = parser.parse_args()
    if args.chromedriver:
        broswer = Chrome(executable_path=args.chromedriver,options=chromeOptions)
    else:
        broswer = Chrome(options=chromeOptions)
    if not args.noheadless:
        chromeOptions.add_argument('--headless')
    keepAlive(broswer, args.user, args.passwd)

if __name__ == "__main__":
    main()