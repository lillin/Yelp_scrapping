# import csv

import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

LINKS_LIST = [
    'https://www.yelp.com/search?cflt=gyms&find_loc=Arlington%2C%20VA',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Seattle%2C%20WA',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Minneapolis%2C%20MN',
    'https://www.yelp.com/search?cflt=gyms&find_loc=San%20Francisco%2C%20CA',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Madison%2C%20WI',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Washington%2C%20DC',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Saint%20Paul%2C%20MN',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Irvine%2C%20CA',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Denver%2C%20CO',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Portland%2C%20OR',
    'https://www.yelp.com/search?cflt=gyms&find_loc=Miami%2C%20FL',
    'https://www.yelp.com/search?cflt=gyms&find_loc=New%20York%2C%20NY',
]


class Scrapper:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    COMPANY_NAME = 'company_name'
    CATEGORY = 'category'
    WEBSITE = 'website'

    LINKS_CATALOG = []
    FIELDNAMES = [COMPANY_NAME, CATEGORY, WEBSITE, ]

    def __init__(self):
        self.driver = os.path.join(self.BASE_DIR, 'Yelp_scrapping', 'geckodriver.exe')
        self.options = Options()
        self.options.add_argument('-headless')

        self.browser = webdriver.Firefox(executable_path=self.driver, options=self.options)
        self.browser.implicitly_wait(10)

        # TODO: uncomment after testing
        # self.file = open('companies.csv', 'w')
        # self.writer = \
        #     csv.DictWriter(self.file, fieldnames=self.FIELDNAMES)
        #
        # self.writer.writeheader()

    def __call__(self, *args, **kwargs):
        self.get_info()
        # self.scrap_info()

        self.browser.close()

    def get_info(self):
        for link in LINKS_LIST:
            self.browser.get(link)  # go to page from companies list

            while True:
                try:
                    self.get_companies_list_from_page()

                    next_page_link = self.browser.find_element_by_xpath(
                        '/html/body/div[2]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[11]/span'
                    ).find_element_by_tag_name('a').get_property('href')

                    self.browser.get(next_page_link)

                except NoSuchElementException:
                    break

    def get_companies_list_from_page(self):
        page_h4_headers = self.browser.find_elements_by_tag_name('h4')

        for elem in page_h4_headers:
            anchor_elem = elem.find_element_by_tag_name('a')
            link_to_company = anchor_elem.get_property('href')
            self.LINKS_CATALOG.append(link_to_company)

    def scrap_info(self):
        for link in self.LINKS_CATALOG:
            data = dict.fromkeys(self.FIELDNAMES)

            self.browser.get(link)

            # TODO: implement find_elem
            data[self.COMPANY_NAME] = None
            data[self.CATEGORY] = None
            data[self.WEBSITE] = None

            # self.writer.writerow(data)


if __name__ == '__main__':
    Scrapper()()
