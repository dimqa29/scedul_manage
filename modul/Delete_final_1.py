import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  # Модуль для двойного нажатия клавиш
from selenium.webdriver.common.keys import Keys  # Модуль для имитации работы клавиатуры
from selenium.common import exceptions
import logging

# logger
file_log = logging.FileHandler('loggers/Log_Cross#1.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                            format='[%(asctime)s | %(levelname)s]: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.INFO)

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

url_cros1 = "https://*************"  # MOS
url_cros2 = 'https://*************'  # CHE PRM ORB
url_cros3 = 'https://*************'  # EKT
url_cros4 = 'https://*************'  # KEM NSK
url_cros5 = 'https://*************'
url_cros6 = 'https://*************'
url_sonLab = 'https://*************'
url = url_cros1


logging.info("Selected Cross# = {}".format(url))

s = Service(r'G:\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get(url)
login_sonlab = 'testerTele2'
pass_sonlab = 'Tester2!'
login_dnikit = 'dnikitin'
pass_dnikit = 'Siski123!'

driver.maximize_window()

log = login_dnikit
pas = pass_dnikit
yaer = '2022'
# month = 'Apr'
month = 'May'
day = '7'
day2 = '8'
day3 = '9'
day4 = '10'
# day5 = '4'

spisok_dat = [[yaer,month,day], [yaer,month,day2], [yaer,month,day3], [yaer,month,day4]]
name_modules = ['PCE', 'PCI', 'SCReuse', 'PRACH', 'CA_IFLB']
# name_modules = ['PRACH']

logging.info("Selected module name = {}".format(name_modules))
logging.info("Selected date = {}".format(spisok_dat))


def login_vhod (log, pas):

    login = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Gui-login-userNameTextBox')))
    # ввод логина
    login.send_keys(log)

    # ввод пароля
    password = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Gui-login-passwordTextBox')))
    password.send_keys(pas)
    time.sleep(1)

    # вход
    vhod = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-logInButton')))
    vhod.click()
    logging.info("Login completed")
    time.sleep(5)


def vibor_dati(yaer, month, day):
    # выбор даты
    vibor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#isc_5M > img')))
    vibor.click()
    time.sleep(2)

    yaer_selection = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//td[@ class='dateChooserNavButton']/div[contains(text(), '2022')]")))
    yaer_selection.click()
    time.sleep(2)

    yaer_selection2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//td[@eventpart='showYear' and contains(text(), '"+yaer+"')]")))
    yaer_selection2.click()
    time.sleep(2)

    month_selection = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@ onfocus='isc.EH.focusInCanvas(isc_Calendar_0_dateChooser_monthChooserButton,true);']")))
    month_selection.click()
    time.sleep(2)

    month_selection2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//td[@eventpart='showMonth' and contains(text(), '"+month+"')]")))
    month_selection2.click()
    time.sleep(2)


    day_selection = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        [By.XPATH, "//td[@ class='dateChooserWeekday' or @ class='dateChooserWeekend' or @ class='dateChooserWeekdaySelected']/div[contains(text(), '" + day + "')]"]))
    day_selection.click()
    logging.info("Date selected = {}".format(yaer + '_' + month + '_' + day))
    time.sleep(2)


login_vhod(log, pas)

# вкладка Calendar
Calendar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-GUI-Tab-Calendar')))
Calendar.click()
time.sleep(10)

# вкладка day
day = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '#isc_42 > table > tbody > tr > td')))
day.click()
time.sleep(5)




# выбор таска
def task_search(name_task):
    time.sleep(5)
    try:
        task = WebDriverWait(driver, 10).until(EC.element_to_be_clickable([By.XPATH, "//div[@ eventproxy='isc_Calendar_0_dayView_body']/div[*[text()[contains(., '"+name_task+"')]]]"]))
        ActionChains(driver).move_to_element(task).click(task).perform()
        name2 = task.text
        time.sleep(5)
    except exceptions.TimeoutException:
        scroll_end = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@ eventproxy = "isc_Calendar_0_dayView_bodyLayout"]//img[@ class="vScrollEnd"]')))
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        scroll_end.click()
        try:
            task = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                [By.XPATH, "//div[@ eventproxy='isc_Calendar_0_dayView_body']/div[*[text()[contains(., '" + name_task + "')]]]"]))
            ActionChains(driver).move_to_element(task).click(task).perform()
            name2 = task.text
            logging.info("The task is open = {}".format(name2))
            time.sleep(5)
        except exceptions.TimeoutException:
            logging.info("There is no task with that name")
            scroll_start = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@ eventproxy = "isc_Calendar_0_dayView_bodyLayout"]//img[@ class="vScrollStart"]')))
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            scroll_start.click()
            return 'exit'

    try:
        task2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable([By.XPATH, "//div[@ class='calendarEvent_list_container']/select/option [text()[contains(., '"+name_task+"')]]"]))
        task2.click()
        name = task2.text
        logging.info('task selected = {}'.format(name))
        time.sleep(5)
        delete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Calendar-editEventDialogBox-deleteButton')))
        delete.click()
        time.sleep(5)
        Delete_This_Event_Only = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "// button[ @ type = 'button' and contains(text(), 'Delete This Event Only')]")))
        Delete_This_Event_Only.click()
        logging.info('task delete = {}'.format(name))
        time.sleep(5)

    except exceptions.TimeoutException:
        logging.info('exept')
        delete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Calendar-editEventDialogBox-deleteButton')))
        delete.click()
        time.sleep(5)
        Delete_This_Event_Only = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "// button[ @ type = 'button' and contains(text(), 'Delete This Event Only')]")))
        Delete_This_Event_Only.click()
        logging.info("Task delete = {}".format(name2))
        time.sleep(5)


    return 'norm_exit'

# 'body > div:nth-child(22) > div > table > tbody > tr.dialogMiddle > td.dialogMiddleCenter > div > div > button:nth-child(3)'


if __name__ == "__main__":
    for data in spisok_dat:
        vibor_dati(data[0], data[1], data[2])
        for a in name_modules:
            logging.info("Task delete = {}".format(a))
            while task_search(a) == 'norm_exit':
                logging.info("=========================")

    logging.info("Task all delete = {}".format(url))
