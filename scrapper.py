import csv

import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

LINKS_LIST = [
    'https://www.yelp.com/search?cflt=gyms&find_loc=Arlington%2C%20VA',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Seattle%2C%20WA',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Minneapolis%2C%20MN',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=San%20Francisco%2C%20CA',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Madison%2C%20WI',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Washington%2C%20DC',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Saint%20Paul%2C%20MN',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Irvine%2C%20CA',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Denver%2C%20CO',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Portland%2C%20OR',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=Miami%2C%20FL',
    # 'https://www.yelp.com/search?cflt=gyms&find_loc=New%20York%2C%20NY',
]


class Scrapper:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LINKS_CATALOG_FILE = 'links_catalog.csv'

    COMPANY_NAME = 'company_name'
    CATEGORY = 'category'
    WEBSITE = 'website'

    FIELDNAMES = [COMPANY_NAME, CATEGORY, WEBSITE, ]

    def __init__(self):
        self.driver = os.path.join(self.BASE_DIR, 'Yelp_scrapping', 'geckodriver.exe')
        self.options = Options()
        self.options.add_argument('-headless')

        self.browser = webdriver.Firefox(executable_path=self.driver, options=self.options)
        self.browser.implicitly_wait(10)

        self.links_catalog = open(self.LINKS_CATALOG_FILE, 'w')
        self.catalog_writer = csv.writer(self.links_catalog)

        self.file = open('companies.csv', 'w')
        self.writer = \
            csv.DictWriter(self.file, fieldnames=self.FIELDNAMES)

        self.writer.writeheader()

    def __call__(self, *args, **kwargs):
        self.get_info()
        self.scrap_info()

        self.browser.close()
        self.file.close()

    def get_info(self):
        for link in LINKS_LIST:
            self.browser.get(link)

            print('-'*20)
            print('NEW AREA: ')
            print(link)
            print('-'*20)
            while True:
                try:
                    self.get_companies_list_from_page()

                    next_page_link = self.browser.find_element_by_xpath(
                        '/html/body/div[2]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[11]/span'
                    ).find_element_by_tag_name('a').get_property('href')

                    self.browser.get(next_page_link)

                except NoSuchElementException:
                    break
        self.links_catalog.close()

    def get_companies_list_from_page(self):
        page_h4_headers = self.browser.find_elements_by_tag_name('h4')

        for elem in page_h4_headers:
            anchor_elem = elem.find_element_by_tag_name('a')
            link_to_company = anchor_elem.get_property('href')
            print(link_to_company)
            self.catalog_writer.writerow(link_to_company)

    def scrap_info(self):
        with open(self.LINKS_CATALOG_FILE, 'r') as links_catalog:
            for link in links_catalog:
                data = dict.fromkeys(self.FIELDNAMES)

                self.browser.get(link)

                data[self.COMPANY_NAME] = self.browser.find_element_by_tag_name('h1').text

                categories_containers = \
                    self.browser.find_element_by_xpath(
                        '/html/body/div[2]/div[4]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/div/span'
                    ).find_elements_by_tag_name('span')

                try:
                    categories = list()
                    for elem in categories_containers:
                        categories.append(elem.find_element_by_tag_name('a').text)
                    data[self.CATEGORY] = ', '.join(categories)
                except NoSuchElementException:
                    print('EXCEPTION: ', link)
                    pass

                try:
                    data[self.WEBSITE] = \
                        self.browser.find_element_by_xpath(
                            '/html/body/div[2]/div[4]/div/div[4]/div/div/div[2]/div[2]/div/div/section/div/div[1]/div/div[2]/p[2]/a'
                        ).text
                except NoSuchElementException:
                    pass

                print()
                print('OUTPUT: ')
                print(data)

                self.writer.writerow(data)


if __name__ == '__main__':
    Scrapper()()
