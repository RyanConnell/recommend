#!/usr/bin/env python
#-*- coding: latin-1 -*-

import requests
import urllib
from bs4 import BeautifulSoup
from util import util
from util import file_handler as file
import tvdb_crawler as tvdb

tv_show_layout = "name, image, location, rating, wiki_url, imdb_url, episode_url, genre, image_location, synopsis"
tv_show_schema = "id INTEGER PRIMARY KEY, name VARCHAR(255), image VARCHAR(255), location VARCHAR(255), rating VARCHAR(255), wiki_url VARCHAR(255), imdb_url VARCHAR(255), episode_url VARCHAR(255), genre VARCHAR(255), image_location VARCHAR(255), synopsis VARCHAR(255)"
tv_show_vartype = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
episode_list_layout = "season, episode, title, date"
episode_list_schema = "id INTEGER PRIMARY KEY, season INTEGER, episode INTEGER, title VARCHAR(255), date VARCHAR(255)"
episode_list_vartype = "%d, %d, %s, %s"

# Loads the config file.
config = file.get_config_data("crawler.config")

# Sets up the verbose setting in util file.
util.debug = True
if config['verbose'] is 0:
	util.debug = False

# Chooses which database to use.
# Defaults to sqlite.
from util import sqlite_connector as database
if config['database_type'].lower() == 'mysql':
   from util import mysql_connector as database
db = database.Database()
database.Database.config = config

def scrape_imdb(url):
	data = {}
	data['image'] = ""
	data['rating'] = "Unknown"
	data['genre'] = "Unknown" 
	data['synopsis'] = "Synopsis Unavailable."
	if url == "":
		return data
	html = requests.get(url).text
	bs4 = BeautifulSoup(html)

	# Grabs the image from the left hand side.
	image = bs4.find('td', {'id': 'img_primary'})
	image_url = ""
	if image is not None:
		image = image.find('img')
		if image is not None:
			image_url = image['src']
			name = image_url.split("http://ia.media-imdb.com/images/")[1]
	data['image'] = image_url

	# Grabs Genre
	genre_list = bs4.findAll('span', {'itemprop': 'genre'})
	genre_text = "Unknown"
	if genre_list != None:
		genre_text = ""
		for genre in genre_list:
			if genre_text != "Unknown" and genre_text != "":
				genre_text += "+"
			genre_text += (util.clean_text(genre.text))
	data['genre'] = genre_text

	# Grabs Synopsis
	synopsis = bs4.find('p', {'itemprop': 'description'})
	synopsis_value = "Synopsis Unavailable"
	if synopsis is not None:
		synopsis_value = synopsis.text
	data['synopsis'] = util.clean_text(synopsis_value)

	# Grabs the rating.
	rating = bs4.find('span', {'itemprop': 'ratingValue'})
	rating_value = "Unknown";
	if rating is not None:
		rating_value = rating.text
	data['rating'] = rating_value

	# Grabs the Synopsis.
	# TO BE COMPLETED
	return data

def get_time_config():
	config = {}
	file.open_file('times.config', 'r')
	config = file.read_config()
	date = config['tv'].split("-")
	config['tv'] = util.parse_date(date[0], date[1], date[2])
	file.close_file()
	return config

def scrape_wikipedia(url):
	util.debug_print("Grabbing Data from '%s'" % url)
	html = requests.get("http://en.wikipedia.org%s" % url).text
	bs4 = BeautifulSoup(html)
	episode_list_data = []
	
	date = bs4.find('li', {'id': 'footer-info-lastmod'})
	episode_list_data = [{'save': False}]
	if(date != None):
		date = date.text.split("modified on ")[1]
		date = date.split(",")[0]
		date = date.split(" ")
		date1 = util.parse_date(date[0], date[1], date[2])
		date2 = time_config['tv'].split("-")
		date2 = util.parse_date(date2[0], date2[1], date2[2])
		util.debug_print((date1, "  vs  ", date2, " => ", util.compare_dates(date1, date2)))
		
	if(date != None):
		episode_list_data = [{'save': False}]
		if (util.compare_dates(date1, date2)):
			name = bs4.find('h1', {'class': 'firstHeading'})
			if name.i is None:
				name = name.text.split("List of")[1].split("episodes")[0]
				name = util.clean_text(name)
			else:
				name = util.clean_text(name.i.text)

			episode_tables = bs4.find_all('table', {'class': 'wikitable plainrowheaders'})
			season_count = 0
			data = None
			episode_list_data = [{'name': name, 'save': True}]
			for episode_table in episode_tables:
				season_count += 1
				episode_count = 0
				episode_list = episode_table.find_all('tr', {'class': 'vevent'})
				for episode in episode_list:
					if season_count is 2 and data is None:
						season_count = 1;
					episode_count += 1
					title = episode.find('td', {'class', 'summary'}).text
					title = title.replace("\"", "")
					title = util.clean_text(title)

					release_date = episode.find('span', {'class': 'bday dtstart published updated'})
					if release_date is not None:
						banned_dates = {"Unaired"}
						release_date = util.clean_text(release_date.text)
						for date in banned_dates:
							if release_date == date:
								release_date = "-   NA   -"
					else:
						release_date = "-   NA   -"

					if len(episode_list_data) > 2:
						if not util.compare_dates(release_date, episode_list_data[len(episode_list_data)-1]['date']):
							# print("NOT AN EPISODE | %d \t| %d \t| %s \t | %s" % (season_count, episode_count, release_date, title))
							break # Prevents all of the next episodes from being added to database as they are web-series/mini-series and not the actual show.
						else:
							util.debug_print("| %d \t| %d \t| %s \t | %s" % (season_count, episode_count, release_date, title))

					data = {
						'season': season_count,
						'episode': episode_count,
						'title': title,
						'date': release_date
					}
					episode_list_data.append(data)

	return episode_list_data

def save_to_database(data, layout):
	global tv_show_layout
	db.write_to_database(data, layout)
	return True # To verify that there were no errors.

def crawl_wikipedia(base_url, url, link_list):
	skip_first = True
	if url == "":
		skip_first = False
		url = base_url
	html = requests.get(url).text
	bs4 = BeautifulSoup(html)

	section = bs4.find('div', {'id': 'mw-pages'})
	if section is None:
		return link_list
	links = section.find_all('li')
	tick = 0
	for link in links:
		show_name = util.clean_text(link.a.text)
		if (link_list.__contains__(show_name)):
			util.debug_print("Duplicate Found. Removing it. => %s" % util.clean_text(link.a.text))
			links.remove(link)
	if links is None:
		return link_list
	if skip_first and len(links) is not 0:
		links.remove(links[0])
	if len(links) == 0:
		util.debug_print("All Links Saved...")
		return link_list
	for link in links:
		show_name = util.clean_text(link.a.text)
		if (link_list.__contains__(show_name)):
			util.debug_print("Duplicate Found. Removing it. => %s" % util.clean_text(link.a.text))
			links.remove(link)
		else:
			link_list[show_name] = (link.a['href'])
			util.debug_print(util.clean_text(link.a['href']))
	if len(links) == 0:
		util.debug_print("All Links Saved...")
		return link_list

	last_show_name = links[len(list(links))-1].text
	last_show_name = last_show_name.replace(" ", "+")
	next_url = ("%s&pagefrom=%s" % (base_url, last_show_name))
	if next_url == url:
		return link_list
	util.debug_print(util.clean_text(next_url))
	link_list = crawl_wikipedia(base_url, next_url, link_list)

	return link_list

def grab_show_data(url):
	util.debug_print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\turl: \t\t\t %s" % url)
	html = requests.get("http://en.wikipedia.org%s" % url).text
	bs4 = BeautifulSoup(html)

	show_data = {}
	show_data['wiki_url'] = url
	show_data['keep'] = False
	name = bs4.find('h1', {'class': 'firstHeading'}).i
	if name is None:
		return show_data
	show_data['name'] = util.clean_text(name.text)

	infobox = bs4.find('table', {'class': 'infobox vevent'})
	if infobox is None:
		return show_data
	links = infobox.find_all('a')
	episode_link = None
	for link in links:
		if link.text == "List of episodes":
			episode_link = link
			break
	if episode_link is None:
		show_data['episode_url'] = url
	else:
		show_data['episode_url'] = episode_link['href']
		if episode_link['href'].startswith('#'):
			show_data['episode_url'] = url

	ext_links = bs4.find('span', {'id': 'External_links'})
	show_image = ""
	imdb_data = None
	imdb_link = ""
	if ext_links is not None:
		ext_links = ext_links.parent.find_next_sibling('ul')
		if ext_links is not None:
			imdb_link = ext_links.find('a', {'href': '/wiki/Internet_Movie_Database'})
			imdb = ""
			if imdb_link is not None:
				imdb_link = imdb_link.parent.find('a', {'rel': 'nofollow'})
				imdb = imdb_link['href']
			show_data['imdb_url'] = imdb
			imdb_data = scrape_imdb(imdb)

	if imdb_link == "":
		show_data['keep'] = False
		return show_data
	show_data['image'] = ""
	show_data['rating'] = "0.0"
	show_data['genre'] = "Unknown"
	if imdb_data is not None:
		show_data['image'] = imdb_data['image']
		show_data['rating'] = imdb_data['rating']
		show_data['genre'] = imdb_data['genre']
		show_data['synopsis'] = imdb_data['synopsis']
	show_data['keep'] = True
	return show_data

def get_show_list(from_database):
	if from_database:
		print("* Retrieving Show list from database.");
		show_list = db.open_database_connection(False, tv_show_layout, config['database_file_name'], "tv_shows", None)
		db.connection.close()
		return show_list
	else:
		wiki_list = {"British_television_programme_debuts", "American_television_series_debuts", "Irish_television_series_debuts"}
		show_list = {} 
		for wiki_link in wiki_list:
			for year in range(config['start_year'], config['end_year']+1):
				print("* Grabbing shows from %s" % year)
				show_list = (crawl_wikipedia("http://en.wikipedia.org/w/index.php?title=Category:%s_%s" % (year, wiki_link), "", show_list))
		return show_list

def update_show_data(show_limit):
	link_list = get_show_list(False)

	db.open_database_connection(True, tv_show_schema, config['database_file_name'], "tv_shows", tv_show_vartype)
	show_link_data = {}
	file.open_file('failures.txt', 'w')
	print("* (%d) shows found." % len(list(link_list)))
	tick = 0
	show_tick = 0
	for link in link_list:
		try:
			show_data = grab_show_data(link_list[link])
			if show_data['keep'] is True:
				show_link_data[show_data['name']] = show_data['episode_url']
				util.debug_print("%d: \t %s \t\t %s" % (tick, show_data['name'], link_list[link]))
				show_data['location'] = util.create_table_name(show_data['name'])
				show_data['image_location'] = show_data['image']
				db.write_to_database(show_data, tv_show_layout)
				tick += 1
				show_tick += 1
				print("%d: %s added to show list." % (show_tick, (show_data['name'])))
				if show_tick >= show_limit and show_limit is not -1:
					break
			else:
				file.output("%s\t| %s" % (link_list[link], link))
				util.debug_print("Invalid Show -> %s" % link)
		except:
			util.debug_print("Exception Caught -> %s" % link)
	db.close_database_connection()
	file.close_file()

def update_show_episodes(index, limit):
	show_link_data = get_show_list(True)
	print ("* Getting Episode Data for all shows..")

	tick = 1
	show_tick = 0
	print("* (%d) shows found in database." % len(list(show_link_data)))
	for show in show_link_data:
		if tick >= index:
			episode_list = scrape_wikipedia(show['episode_url'])
			if (episode_list[0]['save']):
				db.open_database_connection(True, episode_list_schema, config['database_file_name'], util.create_table_name(episode_list[0]['name']), episode_list_vartype)
				episode_list.remove(episode_list[0])
				for episode in episode_list:
					util.debug_print("%d \t | Episode: | %d \t| %d \t| %s \t | %s" % (tick, episode['season'], episode['episode'], episode['date'], episode['title']))
					db.write_to_database(episode, episode_list_layout)
				db.close_database_connection()
				print("%d: [  Episodes Updated  ]: %s." % (show_tick, (show['name'])))
				tick += 1
				if tick >= limit and limit is not -1:
					break
				show_tick += 1
			else:
				tick += 1
				show_tick += 1
				print("%d: [ Had no new Content ]: %s." % (show_tick, (show['name'])))
		else:
			tick += 1
			util.debug_print("Skipping Episode: %d" % tick)

if __name__ == "__main__":
	print("* Starting Crawler...")
	global time_config
	time_config = get_time_config()

	if (config['update_show_indexes'] is 1):
		update_show_data(config['show_limit'])
	if (config['update_show_episodes'] is 1):
		db.create_template_tables(get_show_list(True), episode_list_schema)
		update_show_episodes(config['episode_offset'], config['episode_limit'])
	if (config['use_tvdb'] is 1):
		print("* Scraping/Crawling TVDB")
		tvdb.update_show_data(config['show_limit'])
	if (config['download_images'] is 1):
		print("* Grabbing all Images...")
		image.download_all_images(get_show_list(True), "tv", db)

	print("* Finished...")
	print("* Exiting Crawler...")