from util import sqlite_connector as database
from util import util
from util import file_handler as file
import film_crawler
import unittest

# Unit Testing for the Film Crawler.
class TestCrawler(unittest.TestCase):

    db = database.Database()
    
    def test_wikipedia_crawl(self):
        '''Should return the correct link for the movies wikipedia page'''
        film_list = film_crawler.crawl_wikipedia(2014, 2014)
        for film in film_list:
            self.assertTrue(film.startswith("/wiki/"))

    def test_imdb_scrape(self):
        '''Each section of IMDB data should be correct'''
        data = film_crawler.scrape_imdb("http://www.imdb.com/title/tt0926084/");
        self.assertEqual(data['synopsis'], util.clean_text(data['synopsis']))
        self.assertEqual(data['rating'], float(data['rating']))
        self.assertEqual(data['runtime'], util.clean_int(data['runtime']))
        self.assertEqual(data['age_rating'], util.clean_text(data['age_rating']))

    def test_wikipedia_scrape(self):
        '''Should return the correct data from the wikipedia page'''
        data = film_crawler.scrape_wikipedia("http://en.wikipedia.org/wiki/Divergent_(film)");
        self.assertEqual(data['name'], util.clean_text(data['name']))
        self.assertEqual(data['director'], util.clean_text(data['director']))
        self.assertEqual(data['runtime'], util.clean_int(data['runtime']))
        self.assertEqual(data['starring'], util.clean_text(data['starring']))
        self.assertTrue(data['wiki_url'].startswith("http://en.wikipedia.org/wiki/"))

if __name__ == "__main__":
    unittest.main()