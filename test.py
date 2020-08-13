from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import time
import channel
import message
import slack_decorators
import signal
import sys

def login_to_slack_general(email, password, driver = None):
    if driver == None:
        raise Exception("Driver is none")
    

    search_form_email = driver.find_element_by_id("email")
    search_form_email.send_keys(email)
    password_form_email = driver.find_element_by_id("password")
    password_form_email.send_keys(password)
    search_form_email.submit()


options = Options()
# options.headless = True
options.headless = False
browser = Firefox(options=options) 
browser.get("SLACK URL")
login_to_slack_general("SLACK EMAIL", "SLACK PASSWD", browser)

delay = 15 # seconds
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'p-channel_sidebar__section_heading_plus')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")


@slack_decorators.register_on_message_func
def on_message_appeared(msg):
    print("A")
    print(msg.text)
    links = msg.find_elements_by_tag_name("a")
    for a_link in links:
        print("-"*15)
        print(a_link.get_attribute("href"))
        print(a_link.text)
        print("-"*15)
    buttons = msg.find_elements_by_tag_name("button")
    for a_btn in buttons:
        print("*"*15)
        print(a_btn.text)
        if "Preview" in a_btn.text:
            print("Clicking the btn")
            a_btn.click()
        print(a_btn)
        print("*"*15)
    print("B")
    print("+"*30)
    id = msg.get_attribute("id")
    message.replyToMessage(id, "message id is {}".format(id), browser)
# channel.search_and_open_channel("test_channel", browser)
# poll_id = '1597220606.001000'
# poll_id = '1597268621.000200'
# element = browser.find_element_by_id(poll_id)
# text_elements = element.find_elements_by_class_name("p-rich_text_section")
# for t in text_elements:
#     print(t.text)

# button_container = element.find_elements_by_class_name("c-message_kit__gutter__right")
# button_container = button_container[0]
# buttons = button_container.find_elements_by_tag_name("button")
# for b in buttons:
#     print(b.text)

# links = element.find_elements_by_tag_name("a")
# for l in links:
#     print(l.text)
# print("-"*50)
# print(element.text)

def signal_handler(sig, frame):
    print("You pressed ctrl + c")
    browser.quit()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)
channel.monitor_channel("test_channel", browser)