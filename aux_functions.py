import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

sys.tracebacklimit = 0


class AuxFunc:

    def __init__(self, driver):
        self.driver = driver

    def wait_element_load(self, xpath, timeout=10):
        """задержка для того чтобы загрузились скрипты, ajax и прочее гавно"""
        try:
            WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located((By.XPATH, xpath)))
            return 1
        except TimeoutException:
            return 0

    def wait_window_load_and_switch(self, window_number, timeout=5):
        """функция ожидания загрузки окон и переключения на целевое окно (1й аргумент функции)"""
        try:
            self.driver.implicitly_wait(timeout)
            WebDriverWait(self.driver, timeout).until(ec.number_of_windows_to_be(window_number + 1))
            self.driver.switch_to.window(self.driver.window_handles[window_number])
            self.driver.implicitly_wait(timeout)
            return 1
        except TimeoutException:
            return 0

    def try_click(self, xpath, element=0, window_numb=None, try_numb=10):
        """функция для попыток клика по элементу"""
        for i in range(try_numb):
            try:
                if window_numb is not None:
                    self.driver.switch_to.window(self.driver.window_handles[window_numb])
                if element:
                    self.driver.find_elements(By.XPATH, xpath)[element].click()
                else:
                    self.driver.find_element(By.XPATH, xpath).click()
                return 1
            except Exception as ex:
                if i >= try_numb - 1:
                    break
                time.sleep(1)
                continue
        return 0

    def try_get_text(self, xpath, amount=0, try_numb=10):
        """пытаемся извлечь текст из элемента"""
        for i in range(try_numb):
            if not amount:  # если нужно искать несколько элементов
                try:
                    element = self.driver.find_elements(By.XPATH, xpath)
                except Exception as ex:
                    time.sleep(1)
                    continue
                text_list = []
                if element:  # если element НЕ пуст. Иногда не успевает считаться зн-ие, поэтому иначе будем ждать
                    for each in element:
                        try:
                            if each.get_attribute('innerText'):
                                text_list.append(each.get_attribute('innerText'))
                                if len(text_list) >= len(element):
                                    return text_list
                                continue
                            else:  # если хоть одно значение не содержит текст то сбрасываем счетчик найденных зн-ий
                                time.sleep(1)
                                break
                        except Exception as ex:
                            time.sleep(1)
                            break
                else:  # если element пуст тогда ждем
                    time.sleep(1)
                    continue
            else:  # если нужно искать один элемент
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                except Exception as ex:
                    time.sleep(1)
                    continue
                if element:  # если element НЕ пуст. Иногда не успевает считаться значение, поэтому иначе будем ждать
                    try:
                        if element.get_attribute('innerText'):
                            return element.get_attribute('innerText')
                    except Exception as ex:
                        time.sleep(1)
                        continue
                else:  # если element пуст тогда ждем
                    time.sleep(1)
                    continue

    def try_get_elements(self, xpath, try_numb=10, amount=0):
        for i in range(try_numb):
            try:
                if not amount:
                    element = self.driver.find_elements(By.XPATH, xpath)
                else:
                    element = self.driver.find_element(By.XPATH, xpath)
                return element
            except Exception as ex:
                if i >= try_numb - 1:
                    break
                time.sleep(1)
                continue

    def try_get_link(self, question_id, try_numb=10):
        answer_link_mask = "//*[@data-quiz-uid='" + question_id + "']//div//table//tbody//tr//td//div//span"
        for i in range(try_numb):
            try:
                question_id = self.driver.find_elements(By.XPATH, answer_link_mask)
                return question_id
            except Exception as ex:
                if i >= try_numb - 1:
                    break
                time.sleep(1)
                continue

    def switch_to_frame(self, xpath=None, try_numb=10):
        """функция для переключения на фрейм"""
        for i in range(try_numb):  # пробуем переключиться на тест
            try:
                self.driver.implicitly_wait(1)
                WebDriverWait(self.driver, 1).until(ec.number_of_windows_to_be(2))
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.implicitly_wait(1)
                if xpath:
                    self.driver.switch_to.frame(self.driver.find_element(By.XPATH, xpath))
                else:  # если не передан путь до фрейма то берем дефолтный
                    xpath = '//*[@id="Content"]'
                    self.driver.switch_to.frame(self.driver.find_element(By.XPATH, xpath))
                break
            except Exception as ex:
                time.sleep(1)
                continue


class Dictionary:
    """Объект для работы со словарями"""
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def add_value(self, key, value):
        """Метод для добавления нескольких значений по ключу"""
        if key not in self.dictionary:
            self.dictionary[key] = []
        if not isinstance(self.dictionary[key], list):
            self.dictionary[key] = [self.dictionary[key]]
        self.dictionary[key].append(value)
        return self.dictionary


class DataDict(Dictionary):
    """Объект для формирования структуры словаря с категориями"""
    def __init__(self, main_dict=None):
        self.sub_dict = {}
        super(DataDict, self).__init__(self.sub_dict)
        if main_dict:
            self.main_dict = main_dict
        self.main_dict = {}

    def add_element(self, key, sub_key, sub_value):
        """Добавляем элементы и подэлементы в словарь"""
        if key in self.main_dict:
            for value in self.main_dict[key]:
                self.dictionary[value] = self.main_dict[key][value]
        self.add_value(sub_key, sub_value)
        self.main_dict[key] = self.dictionary.copy()
        self.dictionary.clear()

    def get_dict(self):
        return self.main_dict
