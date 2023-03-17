from time import sleep
from argparse import ArgumentParser
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def searchTerminalUrl(broswer:Chrome):
    for linktag in broswer.find_elements(By.TAG_NAME,"a"):
        linkhref = linktag.get_attribute("href")
        if linkhref != None:
            if "/terminal" in linkhref:
                return linkhref
    return 1

def keepAlive(broswer: Chrome, user, passwd, terminalUrl = ""):
    print("Loading Login Page...", end='', flush=True)
    login_url = "https://accounts.goorm.io/login?return_url=aHR0cHM6Ly9pZGUuZ29vcm0uaW8vbXkvZGFzaGJvYXJk&keep_login=true"
    broswer.get(login_url)
    WebDriverWait(broswer,30).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="app"]/section/div[4]/button')
            )
    )
    print(f"\rNow Login With {user}/{passwd}", end='', flush=True)
    inputEmail = broswer.find_element(By.NAME, "email")
    inputPasswd = broswer.find_element(By.NAME, "password")
    inputEmail.clear()
    inputEmail.click()
    inputEmail.send_keys(user)
    inputPasswd.clear()
    inputPasswd.click()
    inputPasswd.send_keys(passwd)
    broswer.find_element(By.XPATH, '//*[@id="app"]/section/div[4]/button').click()
    try:
        WebDriverWait(broswer,30).until(
            EC.url_matches("https://ide.goorm.io/my/dashboard")
        )
    except TimeoutException:
        if broswer.find_element(By.CLASS_NAME, "invalid-feedback").is_displayed():
            print("\rLogin Failed!Please Check Your Email And Password!", flush=True)
            broswer.quit()
            return 1
    broswer.implicitly_wait(30)
    print("\rLogin Successed!", end='', flush=True)
    if terminalUrl == "":
        sleep(5)
        while 1:
            terminalUrl = searchTerminalUrl(broswer)
            if terminalUrl == 1:
                sleep(5)
            else:
                print(f"\rTerminal Url Found: {terminalUrl}", end='', flush=True)
                break
    print("\rStart KeepAlive Workflow!Enjot it!", end='', flush=True)
    while 1:
        broswer.get(terminalUrl)
        broswer.implicitly_wait(30)
        sleep(7200)
    return 0

def main():
    terminalUrl = ""
    chromeOptions = Options()
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--single-process")
    chromeOptions.add_argument("--disabled-gpu")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("blink-settings=imagesEnabled=false")
    parser = ArgumentParser()
    parser.add_argument("-U","--user",help="Your Goorm Account Email",required=True,type=str)
    parser.add_argument("-P","--passwd",help="Your Goorm Account Password",required=True,type=str)
    parser.add_argument("-DRV","--driver",help="chromedriver Path(Default in $PATH)",required=False,type=str)
    parser.add_argument("-C","--console",help="Console Url",required=False,type=str)
    parser.add_argument("--noheadless",help="Run Chrome Without Headless Mode",required=False,action="store_true")
    args = parser.parse_args()
    if args.console:
        terminalUrl = args.console
    if not args.noheadless:
        chromeOptions.add_argument('--headless')
    if args.driver:
        broswer = Chrome(executable_path=args.driver,options=chromeOptions)
    else:
        broswer = Chrome(options=chromeOptions)
    keepAlive(broswer, args.user, args.passwd, terminalUrl)

if __name__ == "__main__":
    main()