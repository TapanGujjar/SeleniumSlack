import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import timeinterval
import pickledb
from slack_decorators import start_registered_function_call


def openChannelSearch(driver):
    if driver == None:
        raise Exception("Driver is None")
    
    time.sleep(1)
    element = driver.find_elements_by_class_name("p-channel_sidebar__section_heading_plus")
    # if element == None:
    #     raise Exception("No element found with id p-channel_sidebar__section_heading_plus")
    # if isinstance(element, list):
    element = element[0]
    element.location_once_scrolled_into_view
    # action = ActionChains(driver)
    # action.move_to_element(element).click()
    element.click()
    print(element)
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'c-menu_item__label')))
    element = driver.find_elements_by_class_name("c-menu_item__label")
    element = element[0]
    print(element)

    element.click()

def search_and_open_channel(channel_name, driver):
    openChannelSearch(driver)
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'c-filter_input__input')))
    search_box = driver.find_element_by_class_name("c-filter_input__input")
    search_box.click()
    search_box.clear()
    search_box.send_keys(channel_name[0] + channel_name)
    search_box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME,"c-truncate")))
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"c-truncate")))
    check_no_results = driver.find_elements_by_xpath("//*[contains(text(), 'No results')]")
    
    if isinstance(check_no_results, list) and len(check_no_results) > 0:
        raise Exception("No channel found with name "+channel_name)
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"p-bp__list")))

    search_result_container = driver.find_elements_by_class_name("p-bp__list")
    search_result_container = search_result_container[0]
    search_result_possible_div = search_result_container.find_elements_by_tag_name("div")
    print(search_result_possible_div)
    for search_elem in search_result_possible_div:
        possible_id = search_elem.get_attribute("id")
        print(possible_id)
        if possible_id is None or len(possible_id) == 0:
            continue
        search_elem.click()
        break


def check_for_new_msg(msg_container, driver, db):
    message_elements = msg_container.find_elements_by_class_name("c-virtual_list__item")
    id_name = None
    message_item = []
    index = 0
    last_id = db.get("last_id")
    index = len(message_elements)
    was_last_id_set = False
    last_id_to_set = None
    while index >=0:

        try:
            id_name = message_elements[index].get_attribute("id")
            if id_name == "" or id_name == None or "div" in id_name or "C" in id_name or "x" in id_name or "Div" in id_name:
                continue
            if id_name == last_id:
                break

            if was_last_id_set == False and id_name is not None:
                was_last_id_set = True
                last_id_to_set = id_name

            message_item.append(id_name)
            
        except Exception:
            pass
        index -= 1
    if last_id_to_set is not None:
        db.set("last_id", last_id_to_set)
    
    for id in reversed(message_item):
        print("new msg", id)
        try:
            msg_id_element = driver.find_element_by_id(id)
            start_registered_function_call(msg_id_element)
            # text_element = id_element.find_elements_by_class_name("p-rich_text_section")
            # print(text_element)
            # if len(text_element) == 0:
            #     print("text element is none")
            #     print(id_element)
            #     print(id_element.get_attribute("id"))
            #     preview_element = id_element.find_elements_by_xpath('//button[contains(text(), "Show Preview Anyway")]')
            #     print("element is ", preview_element)
            #     if len(preview_element) == 0:
            #         preview_element.location_once_scrolled_into_view
            #         preview_element.click()
            # if isinstance(text_element, list):
            #     text_element = text_element[0]
            # print(text_element.text)
            # link_element = text_element.find_elements_by_tag_name("a")
            # for link in link_element:
            #     print(link.get_attribute("href"))
            
        except Exception:
            pass
        # start_registered_function_call(id_element)
    
def monitor_channel(channel_name, driver):
    search_and_open_channel(channel_name, driver)
    workspace_primary_element = driver.find_elements_by_class_name("p-workspace__primary_view")
    if workspace_primary_element == None:
        raise Exception("Unable to find primary view")
    if isinstance(workspace_primary_element, list):
        workspace_primary_element = workspace_primary_element[0]

    msg_container = workspace_primary_element.find_elements_by_class_name("c-virtual_list__scroll_container")
    if msg_container == None:
        raise Exception("Unable to find slack msg container")
    if isinstance(msg_container, list):
        msg_container = msg_container[0]

    message_elements = msg_container.find_elements_by_class_name("c-virtual_list__item")
    index = len(message_elements) - 1
    id_name = None
    while index >=0:
        try:
            id_name = message_elements[index].get_attribute("id")
            if id_name == "" or id_name == None or "div" in id_name or "C" in id_name:
                continue
            break
        except Exception:
            pass
        index -= 1
    
    db = pickledb.load('example.db', False)
    db.set("last_id", id_name)
    print("Started monitoring channel")
    # return timeinterval.start(1, check_for_new_msg, msg_container, driver, db)
    while True:
        # time.sleep(1)
        check_for_new_msg(msg_container, driver, db)
    