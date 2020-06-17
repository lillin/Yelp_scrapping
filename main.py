# import csv

import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
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


class Parser:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    COMPANY_NAME = 'company_name'
    CATEGORY = 'category'
    WEBSITE = 'website'

    LINKS_CATALOG = []
    FIELDNAMES = [COMPANY_NAME, CATEGORY, WEBSITE, ]

    def __init__(self):
        self.driver = os.path.join(self.BASE_DIR, 'geckodriver.exe')
        self.options = Options()
        self.options.add_argument('-headless')

        self.browser = webdriver.Firefox(executable_path=self.driver, options=self.options)

        # TODO: uncomment after testing
        # self.file = open('companies.csv', 'w')
        # self.writer = \
        #     csv.DictWriter(self.file, fieldnames=self.FIELDNAMES)
        #
        # self.writer.writeheader()

    def __call__(self, *args, **kwargs):
        self.get_info()
        self.scrap_info()

    def get_info(self):
        for link in LINKS_LIST:
            self.browser.get(link)  # go to page from companies list

            while True:
                try:
                    # find and init button to the next page
                    next_page_button = \
                        self.browser.find_element_by_class_name(
                            'lemon--a__373c0__IEZFH link__373c0__1G70M '
                            'next-link navigation-button__373c0__23BAT '
                            'link-color--inherit__373c0__3dzpk '
                            'link-size--inherit__373c0__1VFlE'
                        )

                    # get links for companies from page with results
                    self.get_companies_list_from_page()

                    next_page_button.click()
                except NoSuchElementException:
                    self.get_companies_list_from_page()
                    break

    def get_companies_list_from_page(self):
        # do we need this?
        ActionChains(self.browser).move_to_element(
            self.browser.find_elements_by_class_name(
                'lemon--div__373c0__1mboc '
                'padding-t1__373c0__2aTOb '
                'padding-b1__373c0__3erWW '
                'border-color--default__373c0__3-ifU'
            )
        ).perform()

        for elem in self.browser.find_elements_by_class_name(
                'lemon--a__373c0__IEZFH '
                'link__373c0__1G70M '
                'link-color--inherit__373c0__3dzpk '
                'link-size--inherit__373c0__1VFlE'
        ):
            link_to_company = elem.get_property('href')
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

# browser.close()
# >>> quit()

# go to link from LINKS
# scroll to:
# div lemon--div__373c0__1mboc padding-t1__373c0__2aTOb padding-b1__373c0__3erWW border-color--default__373c0__3-ifU
# for link h4 on page: scrap_from_page -> write_info
# click on NEXT PAGE button

# methods
# scrap_from_page
# write_info
