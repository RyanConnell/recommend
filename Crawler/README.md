# Crawler #

### Installing Dependancies

* In order to have `pip`, Pythons Package Manager:<br />
   _- If using Python 3 make sure your version is 3.4 or greater._ <br />
   _- If using Python 2 make sure your version is 2.7.9 or greater._ <br />

* Install Beautiful Soup 4:<br />
   _- By typing: `pip install beautifulsoup4`_

### Launching Crawlers:

* Run `film_crawler.py` to start the film crawler.<br />
    _- Change the `start_year` and `end_year` variables in the `Config/Crawler.config` file to specify the range._
    
* Run `tv_crawler.py` to start the tv crawler.<br />
    _- When running the crawler for the first time set `update_show_indexes` to `1`_

### Database Changing:

* Set the `database_type` in the `Config/Crawler.config` file to either `mysql` or `sqlite` depending on which you would prefer to use.

### Testing:

* Test Film Crawler with: `test_film_crawler.py` or `test_film_crawler.py -v` for more descriptive tests.

* Test Util with: `test_util.py` or `test_util.py -v` for more descriptive tests.

* Test TV Crawler with: `test_tv_crawler.py` or `test_tv_crawler.py -v` for more descriptive tests.

