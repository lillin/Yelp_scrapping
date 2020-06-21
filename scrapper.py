import csv
import logging
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


logging.basicConfig(level=logging.INFO)

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
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Yelp_scrapping')
    LINKS_CATALOG_FILE = os.path.join(BASE_DIR, 'resulting_files', 'links_catalog.csv')
    COMPANIES_FILE = os.path.join(BASE_DIR, 'resulting_files', 'companies.csv')

    COMPANY_NAME = 'company_name'
    CATEGORY = 'category'
    WEBSITE = 'website'

    FIELDNAMES = [COMPANY_NAME, CATEGORY, WEBSITE, ]

    RESULTS_TEMPLATE = dict.fromkeys(FIELDNAMES)

    def __init__(self):
        self.driver = os.path.join(self.BASE_DIR, 'geckodriver', 'geckodriver.exe')
        self.options = Options()
        self.options.add_argument('-headless')

        self.browser = webdriver.Firefox(executable_path=self.driver, options=self.options)
        self.browser.implicitly_wait(10)

        self.file = open(self.COMPANIES_FILE, 'w')
        self.writer = \
            csv.DictWriter(self.file, fieldnames=self.FIELDNAMES)

        self.writer.writeheader()

    def __call__(self, *args, **kwargs):
        self.scrap_info()

        self.browser.close()
        self.file.close()

    def init_writers(self):
        links_catalog = open(self.LINKS_CATALOG_FILE, 'w')
        catalog_writer = csv.writer(links_catalog)

        setattr(self, 'links_catalog', links_catalog)
        setattr(self, 'catalog_writer', catalog_writer)

    def get_info(self):
        self.init_writers()

        for link in LINKS_LIST:
            logging.info(f'Process link from set {link}')
            self.browser.get(link)

            while True:
                try:
                    self._get_companies_list_from_page()

                    next_page_link = self.browser.find_element_by_xpath(
                        '/html/body/div[2]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[11]/span'
                    ).find_element_by_tag_name('a').get_property('href')
                    self.browser.get(next_page_link)
                except NoSuchElementException:
                    break

        getattr(self, 'links_catalog').close()

    def scrap_info(self):
        if os.path.getsize(self.LINKS_CATALOG_FILE) > 0:
            with open(self.LINKS_CATALOG_FILE, 'r') as links_catalog:
                for link in links_catalog:

                    self.browser.get(link)
                    logging.info(f'Getting info from {link}')
                    results = self._compose_resulting_info()

                    logging.info(f'Writing output {results}')

                    self.writer.writerow(results)
        else:
            self.get_info()
            self.scrap_info()

    def _get_companies_list_from_page(self):
        page_h4_headers = self.browser.find_elements_by_tag_name('h4')

        for elem in page_h4_headers:
            anchor_elem = elem.find_element_by_tag_name('a')
            link_to_company = anchor_elem.get_property('href')

            logging.info(f'Get link {link_to_company}')
            getattr(self, 'catalog_writer').writerow([link_to_company])

    def _compose_resulting_info(self):
        data = self.RESULTS_TEMPLATE.copy()

        data[self.COMPANY_NAME] = self._get_company_name()
        data[self.CATEGORY] = self._get_categories()
        data[self.WEBSITE] = self._get_website()

        return data

    def _get_company_name(self):
        try:
            return self.browser.find_element_by_tag_name('h1').text
        except NoSuchElementException:
            pass

    def _get_categories(self):
        pattern_1 = \
            '/html/body/div[2]/div[4]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/div/span'

        pattern_2 = \
            '/html/body/div[2]/div[4]/div/div[4]/div/div/div[2]/div[1]/div[1]/div/div/span[2]'

        pattern_3 = \
            '/html/body/div[2]/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/span'

        categories = list()
        categories_containers = None

        try:
            categories_containers = \
                self.browser.find_element_by_xpath(
                    pattern_1
                ).find_elements_by_tag_name('span')
        except NoSuchElementException:
            try:
                categories_containers = self.browser.find_element_by_xpath(
                        pattern_2
                    ).find_elements_by_tag_name('span')
            except NoSuchElementException:
                try:
                    categories_containers = self.browser.find_element_by_xpath(
                        pattern_3
                    ).find_elements_by_tag_name('span')
                except NoSuchElementException:
                    pass

        if categories_containers:
            try:
                for elem in categories_containers:
                    categories.append(elem.find_element_by_tag_name('a').text)
            except NoSuchElementException:
                pass

        return ', '.join(categories)

    def _get_website(self):
        pattern = \
            '/html/body/div[2]/div[4]/div/div[4]/div/div/div[2]/div[2]/div/div/section/div/div[1]/div/div[2]/p[2]/a'

        try:
            return \
                self.browser.find_element_by_xpath(
                    pattern
                ).text
        except NoSuchElementException:
            pass


if __name__ == '__main__':
    scrapper = Scrapper()

    try:
        scrapper()
    except Exception as e:
        logging.exception(f'Unexpected exception {e}')
        scrapper.browser.close()
        scrapper.file.close()
