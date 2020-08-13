from channel import search_and_open_channel
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import clipboard

def postMessageToChannel(channel_name, message, driver):
    if driver == None:
        raise Exception("Driver is None")

    search_and_open_channel(channel_name, driver)
    main_element = driver.find_element_by_class_name("p-workspace__input")
    if main_element == None:
        raise Exception("Unable to find element by class name")
    if isinstance(main_element, list) == True:
        main_element = main_element[0]
        
    item = main_element.find_elements_by_class_name("ql-editor")
    item[0].click()
    item[0].send_keys(message)
    submit_btn = main_element.find_element_by_class_name("c-texty_input__button--send")
    submit_btn.click()

def postMessage(message, driver):
    if driver == None:
        raise Exception("Driver is None")

    # search_and_open_channel(channel_name, driver)
    main_element = driver.find_element_by_class_name("p-workspace__input")
    if main_element == None:
        raise Exception("Unable to find element by class name")
    if isinstance(main_element, list) == True:
        main_element = main_element[0]
        
    item = main_element.find_elements_by_class_name("ql-editor")
    item[0].click()
    item[0].send_keys(message)
    submit_btn = main_element.find_element_by_class_name("c-texty_input__button--send")
    submit_btn.click()
    


def replyToMessage(message_id, message, driver):
    open_message_reply_section(message_id, driver)
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'p-threads_footer__input')))
    main_element = driver.find_element_by_class_name("p-threads_footer__input")
    if main_element == None:
        raise Exception("Unable to find element by class name")
    if isinstance(main_element, list) == True:
        main_element = main_element[0]
        
    item = main_element.find_elements_by_class_name("ql-editor")
    item[0].location_once_scrolled_into_view
    item[0].click()
    item[0].send_keys(message)
    submit_btn = main_element.find_element_by_class_name("c-texty_input__button--send")
    submit_btn.click()

def open_message_reply_section(message_id, driver):
    if driver == None:
        raise Exception("No driver found")

    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.ID, message_id)))
    msg_element = driver.find_element_by_id(message_id)
    if msg_element == None:
        raise Exception("No message found with id {}".format(message_id))

    msg_element.location_once_scrolled_into_view
    # msg_element.send_keys(Keys.ENTER)
    # time.sleep(5)
    # time.sleep(10)
    ActionChains(driver).move_to_element(msg_element).click_and_hold(msg_element).perform()
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'c-icon--comment-alt')))
    # time.sleep(1)

    more_action_panel = driver.find_elements_by_class_name("c-icon--comment-alt")
    more_action_panel = more_action_panel[0]
    more_action_panel.location_once_scrolled_into_view
    more_action_panel.click()

def postMessageAsFile(file_name, file_content, driver):
    if driver is None:
        raise Exception("Unable to find driver")
    
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'p-workspace__input')))
    element = driver.find_elements_by_class_name("p-workspace__input")
    element = element[0]
    open_input_shortcut_menu(element, "code or text", driver)
    post_message_as_file_modal("asdsadsad",'apple\norange\npineapple\ngrapges', 'asdjsaodiasd isajd ijsaidjasidj ijsidjisajdisj ', driver)

def reply_to_message_with_file(message_id, file_name, file_content, driver):
    if driver is None:
        raise Exception("Unable to find driver")
    open_message_reply_section(message_id, driver)
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'p-threads_footer__input')))
    main_element = driver.find_element_by_class_name("p-threads_footer__input")
    open_input_shortcut_menu(main_element, "code or text", driver)
    post_message_as_file_modal(file_name, file_content, None, driver)
    close_reply_section(driver)
   

def close_reply_section(driver):
    close_btn = driver.find_elements_by_class_name("p-flexpane_header__control")
    close_btn = close_btn[0]
    close_btn.click()

def open_input_shortcut_menu(main_item, menu_item, driver):
    if driver is None:
        raise Exception("Unable to find driver")

    shortcut_trigger = main_item.find_elements_by_class_name("p-shortcuts_menu_trigger_button")
    shortcut_trigger = shortcut_trigger[0]
    shortcut_trigger.click()
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.ID, 'shortcuts_menu_select')))
    # shortcut_menu_filter = driver.find_element_by_id("shortcuts_menu_select")
    # shortcut_menu_filter.clear()
    # time.sleep(1)
    # shortcut_menu_filter.send_keys(menu_item)
    # print(shortcut_menu_filter.text)
    # print(shortcut_menu_filter)
    # shortcut_menu_filter.submit()
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'ReactVirtualized__Grid__innerScrollContainer')))
    filter_container = driver.find_elements_by_class_name("ReactVirtualized__Grid__innerScrollContainer")
    filter_container = filter_container[0] 
    # time.sleep(2)
    # try:
    option_to_select = filter_container.find_element_by_id("shortcuts_menu_select_option_3")
    option_to_select.click()


def post_message_as_file_modal(file_name, file_content, extra_message, driver):
    # WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'ReactModal__Content')))
    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'c-input_character_count')))
    time.sleep(1)

    clipboard.copy(file_content)
    content_container = driver.find_elements_by_class_name("CodeMirror-scroll") #CodeMirror-scroll  CodeMirror-line  CodeMirror-code 
    content_container = content_container[0]
    actions = ActionChains(driver)
    actions.move_to_element(content_container)
    actions.click_and_hold(content_container)
    actions.key_down(Keys.CONTROL).send_keys("v").perform()


    close_btn = driver.find_elements_by_class_name("c-dialog__close")
    close_btn = close_btn[0]
    title_container = driver.find_elements_by_class_name("c-input_character_count")
    title_container = title_container[0]
    title_input = title_container.find_elements_by_tag_name("input")
    title_input = title_input[0]
    title_input.send_keys(file_name)


    # content_container = driver.find_elements_by_class_name("CodeMirror-scroll") #CodeMirror-scroll  CodeMirror-line  CodeMirror-code 
    # content_container = content_container[0]
    # actions = ActionChains(driver)
    # actions.move_to_element(content_container)
    # actions.click_and_hold(content_container)
    # actions.key_down(Keys.CONTROL).send_keys("v").perform()

    if extra_message is not None:
        message_container = driver.find_element_by_id("share-dialog-message-input")
        message_container.click()
        message_container.clear()
        message_container.send_keys(extra_message)
    # actions = ActionChains(driver)
    # actions.move_to_element(message_container)
    # actions.click_and_hold(message_container)
    # actions.key_down(Keys.CONTROL).send_keys("v").perform()

    # modal_footer = driver.find_elements_by_class_name("c-dialog__footer_buttons")
    # modal_footer = modal_footer[0]
    modal_submit_btn = driver.find_elements_by_class_name("c-button")
    modal_submit_btn = modal_submit_btn[0]
    modal_submit_btn.location_once_scrolled_into_view
    modal_submit_btn.click()


    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'ReactModal__Content')))

    WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'p-file_upload_banner__text_name')))
    print("file uploader appeared")
    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME,'p-file_upload_banner__text_name')))
    print("file banner disappeared")

# def postMessageAsFileHelper(main_element, file_name, file_content, driver):
#     WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, main_element)))
    
