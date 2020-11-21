from behave import when, given, then
import os
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

LINKEDIN_URL = "https://linkedin.com"
LINKEDIN_LOGIN = os.getenv("LINKEDIN_LOGIN", "NO LOGIN FOUND")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "NO PASSWORD FOUND")

# MBA Data Science - Turma 202
GOOGLE_DOCS_SPREADSHEET_ID = '1he35eYWRS8JWDf3jugv8XkdgkBBpYCSrXKzZ4RhgpTg'
GOOGLE_DOCS_SPREADSHEET_COLUMN_IDX = 10
SELENIUM_HUB_URL = "http://127.0.0.1:5444/wd/hub"

OPTIONS = webdriver.ChromeOptions()

DRIVER = webdriver.Remote(
    command_executor=SELENIUM_HUB_URL,
    options=OPTIONS,
    #capabilities=DesiredCapabilities.CHROME
)

ALREADY_ADDED_FRIEND_LIST_FILE = "/tmp/already_added_friends.txt"
ALREADY_ADDED_FRIEND_LIST = []
FRIENDS_TO_ADD_LIST = []


@given('I have login screen')
def open_linkedin(context):
    DRIVER.get(LINKEDIN_URL)
    body = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.XPATH, '//body'))
    )
    assert body is not None


@when('login screen is loaded')
def check_login_screen_loaded(context):
    login_field = WebDriverWait(DRIVER, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="session_key"]'))
    )
    if not login_field:
        logged = WebDriverWait(DRIVER, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="presentation"]'))
        )

    assert (login_field is not None) or (logged is not None)


@then('login with user and password')
def do_login(context):
    login_field = WebDriverWait(DRIVER, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="session_key"]'))
    )
    if login_field:
        password_field = DRIVER.find_element_by_xpath('//input[@id="session_password"]')
        submit_button = DRIVER.find_element_by_xpath('//button[@class="sign-in-form__submit-button"]')

        login_field.send_keys(LINKEDIN_LOGIN)
        password_field.send_keys(LINKEDIN_PASSWORD)
        submit_button.click()

    logged = WebDriverWait(DRIVER, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="presentation"]'))
    )

    assert logged is not None


@given('I have a friend list')
def load_friend_list(context):
    FRIENDS_TO_ADD_LIST = list(filter(lambda friend: not is_friend_already_added(friend), FRIENDS_TO_ADD_LIST))


@then('add friends')
def add_friends(context):
    for friend in FRIENDS_TO_ADD_LIST:
        friend_page_loaded = False
        for _ in range(5):
            try:
                visit_friend(friend)
                friend_page_loaded = True
                break
            except:
                continue

        if friend_page_loaded:
            try:
                add_friend(friend)
                add_already_added_friend(friend)
            except:
                pass


def visit_friend(friend):
    if not "http" in friend:
        friend = "https://"+friend
    DRIVER.get(friend)

    WebDriverWait(DRIVER, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="pv-top-card--photo text-align-left"]'))
    )


def add_friend(friend):
    print(f"add friend {friend}")
    btn_connect = WebDriverWait(DRIVER, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Connect"]'))
    )
    btn_connect.click()

    btn_send = WebDriverWait(DRIVER, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Send"]'))
    )
    btn_send.click()


def add_already_added_friend(friend):
    try:
        f = open(ALREADY_ADDED_FRIEND_LIST_FILE, "a")
        f.write(friend + "\n")
        f.close()
        result = True
    except:
        result = False

    assert result


@then('finish the list')
def finish_list(context):
    print("Finish the list")
    assert True is True


def is_friend_already_added(friend):
    return friend in ALREADY_ADDED_FRIEND_LIST


def load_already_added_friends_list():
    try:
        f = open(ALREADY_ADDED_FRIEND_LIST_FILE)
    except:
        return

    for line in f.readlines():
        ALREADY_ADDED_FRIEND_LIST.append(line.replace("\n", ""))
    f.close()



#def download(spreadsheet, gid=0, format="csv"):
    #import urllib2
    #req = urllib2.Request(url_format % (spreadsheet, format, gid), headers=headers)
    #return urllib2.urlopen(req)


def load_friends_to_add():
    print("Loading")
    url_format = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=%s&gid=%i"
    headers = {
        "GData-Version": "3.0"
    }
    r = requests.get(url_format % (GOOGLE_DOCS_SPREADSHEET_ID, "csv", 0), headers=headers)
    for line in str(r.content).split("\\r\\n"):
        fields = line.split(",")
        try:
            linkedin_friend = fields[GOOGLE_DOCS_SPREADSHEET_COLUMN_IDX].lower()
        except IndexError:
            continue

        if "linkedin.com" in linkedin_friend:
            FRIENDS_TO_ADD_LIST.append(linkedin_friend)
            print("Will add friend " + linkedin_friend)


load_already_added_friends_list()
load_friends_to_add()
#import sys
#sys.exit()
