import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from selenium.common import exceptions
from .forms import UserForm
import traceback
import threading
import sys
import logging
import time
import os


def index(request):
    global stop
    stop = False
    # submitbutton = request.POST.get("submit")
    # cross = ''
    # reg = ''
    # login = ''
    # pasword = ''
    # all_date = ''
    # data_shedul = ''
    # stop_modul = ''
    # stop_modul_error = ''
    form = UserForm(request.POST or None)
    request.session['test'] = 'value_1'
    request.session['stop'] = 'da'
    test_2_ses = ''
    aaa = ''
    if form.is_valid():
        cross = form.cleaned_data.get("cross")
        reg = form.cleaned_data.get("reg")
        date = form.cleaned_data.get("date").strftime('%Y, %b, %#d')
        date2 = form.cleaned_data.get("date2").strftime('%Y, %b, %#d')
        login = form.cleaned_data.get("login")
        pasword = form.cleaned_data.get("pasword")
        request.session['test_2'] = login
        test_2_ses = request.session.get('test_2')
        all_date = date_change(date, date2)
        timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
        request.session['timestr'] = timestr
        test_3_ses = request.session.get('timestr')
        file_txt = 'logs/Log_' + test_2_ses + '_' + test_3_ses + '_.txt'
        request.session['file_txt'] = file_txt
        threading.Thread(target=modul_test, args=(cross, login, pasword, reg, all_date, file_txt)).start()
        return redirect('UserInfo/log/')
    # if request.POST.get('mybtn'):

    # if request.method == 'POST' and 'mybtn' in request.POST:
    #     print('request.POST==', request.POST.get('mybtn'))
    #     try:
    #         modul_test(cross, login, pasword, all_date)
    #     except Exception:
    #         stop_modul_error = 'с ошибкой'
    #         logging.info(traceback.format_exc())
    #     print("rabota modula zavershena")
    #     stop_modul = 'Модуль по удалению завершил свою работу'
    context = {'form': form, 'aaa': aaa, 'test_2_ses': test_2_ses}
    # context = {'form': form, 'cross': cross,
    #            'reg': reg, 'submitbutton': submitbutton,
    #            'all_date': all_date, 'login': login, 'pasword': pasword, 'data_shedul': data_shedul, 'stop_modul': stop_modul, 'stop_modul_error':
    #                stop_modul_error, 'aaa': aaa, 'test_2_ses': test_2_ses}

    return render(request, 'UserInfo/index.html', context)

def creat_file(request):
    f = open('logs/Log_' + request.session.get('test_2') + '_' + request.session.get('timestr') + '_.txt')
    str1 = f.readlines()
    str2 = []
    for i in reversed(str1):
        str2.append(i)
    str3 = str()
    for k in str2:
        str3 = str3 + k
    return str3

# def creat_file():
#     if login:
#         f = open('logs/Log_' + login + '_' + timestr + '_.log')
#         str1 = f.readlines()
#         str2 = []
#         for i in reversed(str1):
#             str2.append(i)
#         str3 = str()
#         for k in str2:
#             str3 = str3 + k
#         return str3

def creat_file_2(i):
    f = open('logs/'+i)
    str1 = f.readlines()
    str2 = []
    for i in reversed(str1):
        str2.append(i)
    str3 = str()
    for k in str2:
        str3 = str3 + k
    return str3



def log(request):
    global stop
    if request.method == "POST":
        stop = request.session['stop'] = 'net'
    est = 3
    a = 'ЛОГ'
    test_2_ses = request.session.get('test_2')
    vivod_log_test = creat_file(request)

    if 'All tasks have been deleted!' in vivod_log_test:
        est = 999999
    if 'The removal module has been stopped' in vivod_log_test:
        est = 999999
    if 'TimeoutException' in vivod_log_test:
        est = 999999
    return render(request, 'UserInfo/log.html', context={'a': a, 'vivod_log_test': vivod_log_test, 'est': est, 'test_2_ses': test_2_ses})
    # return render(request, 'UserInfo/log.html', context={'a': a, 'est': est, 'test_2_ses': test_2_ses})


def date_change(date, date2):
    start = datetime.datetime.strptime(date, '%Y, %b, %d')
    end = datetime.datetime.strptime(date2, '%Y, %b, %d')

    date_generated = [start + datetime.timedelta(days=x) for x in range(0, ((end - start).days + 1))]
    print("date_generated=", date_generated)
    spisok_dat = []

    if date_generated:
        for date in date_generated:
            a = date.strftime('%Y, %b, %#d')
            b = a.split(', ')
            spisok_dat.append(b)

    else:
        spisok_dat = date.split(', ')

    print("spisok_dat=", spisok_dat)

    return spisok_dat

def pichu_log(file_log, name_log):
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out),
                        format='[%(asctime)s | %(levelname)s]: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger(name_log)
    return logger



def modul_test(url,log, pas, reg, spisok_dat, file_txt):
    global stop
    print('rq_ses', stop)
    def stop_module():
        global stop
        print('stop_func', stop)
        if stop == 'net':
            my_log(file_txt, ('The removal module has been stopped'))
            driver.close()
            return


    my_file = open(file_txt, 'w')
    text_for_file = 'START'
    my_file.writelines(text_for_file + '\n')
    my_file.close()
    print('stop_func', stop)
    def my_log(file_txt, text):
        my_file = open(file_txt, 'a')
        text_for_file2 = time.strftime('%d.%m.%Y %H:%M:%S') + '-' + text
        my_file.writelines(text_for_file2 + "\n")
        my_file.close()
        my_file = open(file_txt, 'a')
        my_file.writelines('==================================' + "\n")
        my_file.close()
        return


    url_cros1 = "https://*************"  # MOS
    url_cros2 = 'https://*************'  # CHE PRM ORB
    url_cros3 = 'https://*************'  # EKT
    url_cros4 = 'https://*************'  # KEM NSK
    url_cros5 = 'https://*************'
    url_cros6 = 'https://*************'
    url_sonLab = 'https://*************'
    # url_dict = {"Cross#1": url_cros1,'Cross#2': url_cros2,'Cross#3': url_cros3,'Cross#4': url_cros4,'Cross#5': url_cros5,'Cross#6': url_cros6,
    #             'son_Lab': url_sonLab }

    url_str = str(url)

    if url_str == 'Cross#1':
        url = url_cros1
    if url_str == 'Cross#2':
        url = url_cros2
    if url_str == 'Cross#3':
        url = url_cros3
    if url_str == 'Cross#4':
        url = url_cros4
    if url_str == 'Cross#5':
        url = url_cros5
    if url_str == 'Cross#6':
        url = url_cros6
    if url_str == 'son_Lab':
        url = url_sonLab
    print(type(reg))
    print(type(spisok_dat))
    spisok_dat_str = str(spisok_dat)

    def obrabotka_reg(reg):
        a = reg.split(',')
        b = []
        for i in a:
            i = i.lstrip()
            i = i.rstrip()
            b.append(i)
        return b
    name_modules = obrabotka_reg(reg)

    my_log(file_txt, ('Select cross=' + url_str))
    my_log(file_txt, ('Login=' + log))
    my_log(file_txt, ('Select task=' + str(name_modules)))
    my_log(file_txt, ('Select date=' + spisok_dat_str))
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options, executable_path=r'D:\NIkitin_Dima\chromedriver\chromedriver.exe')

    driver.get(url)
    stop_module()

    driver.maximize_window()
    stop_module()
    print('rq_ses2', stop)
    def login_vhod(log, pas):
        login = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Gui-login-userNameTextBox')))
        # ввод логина
        login.send_keys(log)
        stop_module()

        # ввод пароля
        password = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Gui-login-passwordTextBox')))
        password.send_keys(pas)
        time.sleep(1)
        stop_module()

        vhod = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-logInButton')))
        vhod.click()
        # logging.info("Login completed")
        time.sleep(5)
        stop_module()

    def vibor_dati(yaer, month, day):
        # выбор даты
        vibor = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#isc_5M > img')))
        vibor.click()
        time.sleep(2)
        stop_module()
        yaer_selection = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@ class='dateChooserNavButton']/div[contains(text(), '2022')]")))
        yaer_selection.click()
        time.sleep(2)
        stop_module()
        yaer_selection2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@eventpart='showYear' and contains(text(), '" + yaer + "')]")))
        yaer_selection2.click()
        time.sleep(2)
        stop_module()
        month_selection = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@ onfocus='isc.EH.focusInCanvas(isc_Calendar_0_dateChooser_monthChooserButton,true);']")))
        month_selection.click()
        time.sleep(2)
        stop_module()
        print("month=", month)

        month_selection2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@eventpart='showMonth' and contains(text(), '" + month + "')]")))
        month_selection2.click()
        time.sleep(2)
        stop_module()
        day_selection = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            [By.XPATH,
             "//td[@ class='dateChooserWeekday' or @ class='dateChooserWeekend' or @ class='dateChooserWeekdaySelected']/div[contains(text(), '" + day + "')]"]))
        day_selection.click()
        # logging.info("Date selected = {}".format(yaer + '_' + month + '_' + day))
        my_log(file_txt, ('Select date=' + yaer + '_' + month + '_' + day))
        time.sleep(2)
        stop_module()
        date_print = WebDriverWait(driver, 10).until(EC.element_to_be_clickable([By.XPATH, "//*[@id='isc_5K']/table/tbody/tr/td/b"]))
        date_print_text = date_print.text
        print(date_print_text)
        print(date_print_text)
        print(date_print_text)
        stop_module()
    login_vhod(log, pas)
    stop_module()
    # вкладка Calendar
    try:
        Calendar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-GUI-Tab-Calendar')))
        Calendar.click()
        time.sleep(10)
        stop_module()
    except Exception:
        my_log(file_txt, traceback.format_exc())
        my_log(file_txt, "Authorization error check login and password")
        stop_module()
        driver.close()
        return

    # вкладка day
    day = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#isc_42 > table > tbody > tr > td')))
    day.click()
    time.sleep(5)
    stop_module()

    def task_search(name_task):
        time.sleep(5)
        stop_module()
        try:
            task = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                [By.XPATH, "//div[@ eventproxy='isc_Calendar_0_dayView_body']/div[*[text()[contains(., '" + name_task + "')]]]"]))
            ActionChains(driver).move_to_element(task).click(task).perform()
            name2 = task.text
            my_log(file_txt, ('Open task=' + name2))
            time.sleep(5)
            stop_module()
        except exceptions.TimeoutException:
            scroll_end = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@ eventproxy = "isc_Calendar_0_dayView_bodyLayout"]//img[@ class="vScrollEnd"]')))
            stop_module()
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
                stop_module()
                ActionChains(driver).move_to_element(task).click(task).perform()
                stop_module()
                name2 = task.text
                my_log(file_txt, ('Open task=' + name2))
                time.sleep(5)
                stop_module()
            except exceptions.TimeoutException:
                my_log(file_txt, ('There is no car with that name anymore'))
                scroll_start = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@ eventproxy = "isc_Calendar_0_dayView_bodyLayout"]//img[@ class="vScrollStart"]')))
                stop_module()
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
                stop_module()
                return 'exit'

        try:
            task2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                [By.XPATH, "//div[@ class='calendarEvent_list_container']/select/option [text()[contains(., '" + name_task + "')]]"]))
            stop_module()
            task2.click()
            stop_module()
            name = task2.text
            my_log(file_txt, ('Open task=' + name))
            time.sleep(5)
            stop_module()
            delete = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Calendar-editEventDialogBox-deleteButton')))
            delete.click()
            time.sleep(5)
            stop_module()
            Delete_This_Event_Only = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "// button[ @ type = 'button' and contains(text(), 'Delete This Event Only')]")))
            Delete_This_Event_Only.click()
            my_log(file_txt, ('Delete task=' + name))
            # logging.info('task delete = {}'.format(name))
            time.sleep(5)
            stop_module()

        except exceptions.TimeoutException:
            # logging.info('exept')
            delete = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#gwt-debug-Calendar-editEventDialogBox-deleteButton')))
            stop_module()
            delete.click()
            stop_module()
            time.sleep(5)
            Delete_This_Event_Only = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "// button[ @ type = 'button' and contains(text(), 'Delete This Event Only')]")))
            Delete_This_Event_Only.click()
            # logging.info("Task delete = {}".format(name2))
            my_log(file_txt, ('Delete task=' + name2))
            stop_module()
            time.sleep(5)
            # print(name2, 'delete')

        return 'norm_exit'

    for data in spisok_dat:
        vibor_dati(data[0], data[1], data[2])
        stop_module()
        for a in name_modules:
            my_log(file_txt, ('Starting to work out the tasks ' + a))
            stop_module()
            while task_search(a) == 'norm_exit':
                print("kuku")

    driver.close()

    my_log(file_txt, ('All tasks have been deleted!'))
    return

