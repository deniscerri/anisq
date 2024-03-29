from ast import parse
from posixpath import split
from unittest import result
from bs4 import BeautifulSoup
from lxml import html, etree
import cloudscraper
import os, re, sys, getopt
import json
import difflib
import requests
from time import sleep
import subprocess


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

scraper = cloudscraper.create_scraper(
	browser={
		'browser': 'firefox',
             	'platform': 'windows',
             	'mobile': False
     	}
)


class Config:
	base_url = "https://www.asenshu.com"
	query = ''
	season = 0
	episode = 0
	episodes= None
	media_type = ''
	root_path = os.getcwd()
	output_path = ''
	interactive = True
	automated = False
	watch = False
	title = ''

White='\033[97m'
Red='\033[31m'
Green='\033[32m'
Yellow='\033[33m'
Blue='\033[34m'
LYellow='\033[92m'
LCyan='\033[96m'

def request(URL):
	page = BeautifulSoup(scraper.get(URL).text, "html.parser")
	return page

def post_request(URL):
	return BeautifulSoup(scraper.post(URL).text, "html.parser")


def mp4_upload(URL):
	URL=URL.replace("embed-","").replace(".html","")
	html=requests.get(URL).text
	soup=BeautifulSoup(html,'html.parser')
	
	params=dict()
	inputs=soup.find_all('input')
	for item in inputs:
		params.update({item['name']:item['value']})
	response=requests.post(URL,data=params).text

	soup=BeautifulSoup(response, 'html.parser')
	params=dict()
	inputs=soup.find_all('input')
	for item in inputs:
		params.update({item['name']:item['value']})
	response=requests.post(URL,data=params,verify=False,allow_redirects=False).headers['Location']
	return response

def help_text():
	print("""
Usage:
	anisq [options] [input title or file]
Options:
	-h show this page
	-w watch instead of downloading
	-m search for movies only
	-t search for tv series only
	-a let the script choose the best match from the query
	-s set a particular season to download. By default it downloads all seasons
	-e set a particular episode to download. By default it downloads all episodes
	-o set a custom download path. By default it downloads in your current working directory
	You can Also use .txt files containing lists of titles or url's as input
		""")


def download(referer, video):
	if not video:
		print(f"{Red}Couldn't find a suitable stream! :({White}")
		return 1
	
	if Config.watch:
		mpvTitle = Config.title
		if Config.media_type == "seriale":
			mpvTitle += f" S{Config.season}-E{Config.episode}"
		
		try:
			os.system(f'mpv --referrer="{referer}" "{video}" --force-media-title="{mpvTitle}" --no-terminal')
		except:
			print(f"{Red}Couldn't find a suitable stream! :({White}")
			return 1
		
		streaming(mpvTitle)
		exit()
	
	response = 1
	try:
		if "m3u" in video:
			response = subprocess.run(f'ffmpeg -http_persistent 0 -nostdin -hide_banner -loglevel error -stats -headers "Referer: {referer}" -i "{video}" -c copy "{Config.output_path}"', check = True)
		else:
			response = subprocess.run(f'ffmpeg -nostdin -hide_banner -loglevel error -stats -headers "Referer: {referer}" -i "{video}" -c copy "{Config.output_path}"', check = True)
	except:
		response = 1
	return response


def streaming(mpvTitle):
	os.system('clear') if os.name == 'posix' else os.system('cls')
	print(f"{Blue}Streamed {mpvTitle}. {White}")

	options = ['r', 'q']

	if Config.media_type == "seriale":
		if int(Config.episode) < len(Config.episodes):
			print(f"{Red}[n]{White} Next Episode")
			options.append('n')
		if int(Config.episode) > 1:
			print(f"{Red}[p]{White} Previous Episode")
			options.append('q')
		
		print(f"{Red}[c]{White} Custom Episode number")
		options.append('c')

	
	print(f"{Red}[r]{Green} Replay")
	print(f"{Red}[q]{Green} Quit")

	choice = input(White + f"Write your input: ")

	if choice in options:
		if(choice == "n"):
			Config.episode = int(Config.episode) + 1
			parse_embed(Config.episodes[int(Config.episode)]['url'])
		elif(choice == "p"):
			Config.episode = int(Config.episode) - 1
			parse_embed(Config.episodes[int(Config.episode)-2]['url'])
		elif(choice == "r"):
			parse_embed(Config.episodes[int(Config.episode)-1]['url'])
		elif(choice == "c"):
			choice = input(White + f"Write a number between [{Red}1-{len(Config.episodes)}{White}]: ")
			try:
				choice = int(choice)
			except:
				choice = 0
			while choice == 0 or int(choice) > len(Config.episodes):
				choice = input("Wrong Input. Try Again: ")
				try:
					choice = int(choice)
				except:
					choice = 0
			choice = int(choice)
			Config.episode = choice
			parse_embed(Config.episodes[choice-1]['url'])
	else:
		return
	

def clean_link(link):
	if not link:
		return ''

	link = re.sub('",', '"', link)
	link = re.sub('"', '', link)
	link = re.sub('\'', '', link)
	link = re.sub('\',', '', link)
	link = re.sub('m3u8,', '', link)
	
	return link

def generic_scraper(referer):
	page = str(request(referer))
	mp4 = re.findall(r'https://.*[^"].m3u8', page)

	if not mp4:
		mp4 = ['']
	#	mp4 = re.findall(r'*https://.*([^",]*.mp4.*)', page)

	return clean_link(mp4[0])

def parse_embed(URL):
	soup = request(URL)
	page_str = str(soup)
	page = html.fromstring(page_str).getroottree()
	referers = page.xpath('//*[@id="info"]/div/p[2]/a/@href')
	
	if Config.media_type == "filma":
		embed_title = page.xpath('//*[@id="single"]/div[2]/div[2]/div[2]/h1/text()')[0]
	else:
		embed_title = page.xpath('//*[@id="info"]/h1/text()')[0]
	
	fix_title()

	if not Config.watch:
		if (Config.title == ''):
			Config.title = page.xpath('//*[@id="info"]/h1/text()')[0]
			fix_title()

		if Config.media_type == 'seriale':
			split_title = str(embed_title).split(" ")
			season_nr = split_title[len(split_title)-1].split("x")[0]
			episode_nr = split_title[len(split_title)-1].split("x")[1]
			Config.output_path = f"{Config.root_path}/{Config.title}/{Config.title} - S{season_nr}E{episode_nr}.mkv"
		
			if os.path.exists(str(Config.output_path)):
				if is_file_incomplete():
					print(f"{Green}Episode is Downloaded. {White}")
					return 1

		else:
			Config.output_path = f"{Config.root_path}/{Config.title}.mkv"
			fix_title()

			if os.path.exists(str(Config.output_path)):
				if is_file_incomplete():
					print(f"{Green}Movie is Downloaded. {White}")
					return 1
	
	video = ''
	for referer in referers:
		if 'fembed' in referer or 'suzihaza' in referer or 'femax' in referer:
			print(f"{LYellow}Trying to download from stream: {referer}{White}")
			referer = re.sub("/v/", '/f/', referer)
			videoid = re.sub(".*/f/", '', referer)
			res = str(post_request(f'https://vanfem.com/api/source/{videoid}'))
			res = json.loads(res)

			
			try:
				video = res['data'][len(res['data'])-1]['file']
			except:
				video = ''
			res = download(referer, video)
			if (res == 0):
				break
		
		elif 'mp4upload' in referer:
				print(f"{LYellow}Trying to download from stream: {referer}{White}")
				video = mp4_upload(referer)
				res = download(referer, video)
				if (res == 0):
					break
		else:
			video = generic_scraper(referer)
			
			if not video:
				mp4u_href = re.findall(r'"https://www.mp4upload.*?"', page_str)
				if mp4u_href:
					referer = re.sub("\"", "", mp4u_href[0])
					video = mp4_upload(referer)
			print(f"{LYellow}Trying to download from stream: {referer}{White}")
			res = download(referer, video)
			if (res == 0):
				break

		if os.path.exists(Config.output_path):
			if is_file_incomplete():
				return 1


def is_file_incomplete():
	try:
		dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", str(Config.output_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
		if float(dur.stdout) <= 600:
			os.remove(str(Config.output_path))
			return 0
		else:
			return 1
	except:
		os.remove(str(Config.output_path))
		return 0

def fix_title():
	Config.title = re.sub(':', '', Config.title)

def parse_seasons(URL):
	page = str(request(URL))
	page = html.fromstring(page).getroottree()
	titles = page.xpath('//*[@class="episodios"]//li/div[2]/text()')
	urls = page.xpath('//*[@class="episodios"]//li/div[3]/a/@href')

	episode_list = []
	for i, item in enumerate(titles):
			if '- --' in titles[i] or '- 0' in titles[i]:
					continue
			episode_list.append({'title': titles[i], 'url': urls[i]})

	if not episode_list:
			print(f"{Red}Series not found! :(")



	Config.title = page.xpath('//*[@id="single"]/div[1]/div[1]/div[2]/h1/text()')[0]
	if not Config.watch:
			print("Creating Series Folder")
			fix_title()
			path = os.path.join(Config.root_path, Config.title)
			if not os.path.exists(path):
					os.makedirs(path)

	seasoned_episode_list = []
	chosen_ep = 0
	if int(Config.season) > 0:
			matcher = str(Config.season) + " - "
			for e in episode_list:
					if matcher in e['title']:
							seasoned_episode_list.append(e)
			episode_list = seasoned_episode_list
	else:
		Config.season = 1

	Config.episodes = episode_list

	if int(Config.episode) > 0:
			matcher = "- " + str(Config.episode)
			for e in episode_list:
							if matcher in e['title']:
									chosen_ep = e
									break
			if chosen_ep != 0:
					episode_list = []
					episode_list.append(chosen_ep)			
	else:
		if Config.watch:
				chosen_ep = choose_episode(episode_list)
				episode_list = []
				episode_list.append(chosen_ep)
		else:
			Config.episode = 1

	if Config.watch:
			print(f"Starting stream for {Config.title} [{episode_list[0]['title']}]")
			parse_embed(episode_list[0]['url'])
			exit()

	for e in episode_list:
			print(f"{Blue}Downloading {Config.title} [{e['title']}] {White}")
			parse_embed(e['url'])


def choose_episode(ep_list):
	choice = input(White + f"Write episode number between [{Green}1-{len(ep_list)}{White}]: ")
	try:
		choice = int(choice)
	except:
		choice = 0
	while choice == 0 or int(choice) > len(ep_list):
		choice = input("Wrong Input. Try Again: ")
		try:
			choice = int(choice)
		except:
			choice = 0
	choice = int(choice)
	Config.episode = choice
	return ep_list[choice - 1]

def search():
	query = re.sub(" ", "+", Config.query)
	page = str(request(f"{Config.base_url}/?s={query}"))
	page = html.fromstring(page).getroottree()
	result = page.xpath('//*[@id="contenedor"]/div[3]/div[1]/div/*[@class="result-item"]/article/div[2]/div[1]/a')
	if not result:
		print(f"{Red}No results found with this query :/{White}")
		sys.exit()
	
	result_list = []

	for r in result:
		url = r.attrib['href']
		media_type = 'filma' if '/filma/' in url else 'seriale'
		if Config.media_type in url:
			obj = {'title':r.text_content(), 'url':url, 'type': media_type}
			result_list.append(obj)

	if Config.interactive:
		if len(result_list) == 1:
			print(f"Only one result found. [{result_list[0]['title']}]\nContinuing")
		else:
			for index, r in enumerate(result_list):
				i = index + 1
				if r['type'] == 'filma':
					print(f"{LCyan}{i}. [{r['type']}]  {r['title']}")
				else:
					print(f"{LYellow}{i}. [{r['type']}]  {r['title']}")


			choice = input(White + f"Write a number between [{Red}1-{len(result_list)}{White}]: ")
			
			try:
				choice = int(choice)
			except:
				choice = 0
			while choice == 0 or int(choice) > len(result_list):
				choice = input("Wrong Input. Try Again: ")
				try:
					choice = int(choice)
				except:
					choice = 0
			choice = int(choice)
			Config.media_type = result_list[choice-1]['type']
			Config.title = result_list[choice-1]['title']
			parse_title(result_list[choice-1]['url'])


	elif len(result_list) == 1:
		Config.media_type = result_list[0]['type']
		Config.title = result_list[0]['title']
		parse_title(result_list[0]['url'])
	else:
		match = find_match(result_list)
		if match:
			Config.media_type = match['type']
			Config.title = match['title']
			parse_title(match['url'])


def find_match(list):
	elements = []
	for i, e in enumerate(list):
		elements.append(e['title'])

	res = difflib.get_close_matches(str(Config.query), elements, 3, 0.7)[0]

	for i, e in enumerate(list):
		if res == e['title']:
			return e
	
	return None


def parse_title(result_url):
	if Config.media_type == "filma":
		return parse_embed(result_url)
	else:
		return parse_seasons(result_url)



def init_start():
	if "http" in Config.query:
		if "/filma/" in Config.query or "/episode/" in Config.query:
			parse_embed(Config.query)
		else:
			parse_seasons(Config.query)
	else:
		search()


def parse_args(argv):
	opts, args = getopt.getopt(argv, "m:t:hwas:e:o:")
	for opt, arg in opts:
		opt = opt[1:]
		if opt == "h":
			help_text()
			sys.exit()
		elif opt == "m":
			Config.media_type = 'filma'
			Config.query = arg
		elif opt == "t":
			Config.media_type = 'seriale'
			Config.query = arg
		elif opt == "w":
			Config.watch = True
		elif opt == "a":
			Config.interactive = False
		elif opt == "s":
			Config.media_type = 'seriale'
			Config.season = arg
		elif opt == "e":
			Config.media_type = 'seriale'
			Config.episode = arg
		elif opt == "o":
			if not os.path.exists(arg):
				print(f"{Red}This path doesn't exist")
				sys.exit()
			Config.root_path = arg
		else:
			help_text()
			sys.exit()

	if args:
		Config.query = args[0]
		return

	if not opts:
		help_text()
		sys.exit()
	

def main():
	parse_args(sys.argv[1:])
	if not Config.query:
		print(f"{Red}You need to provide a query!")
		sys.exit()

	if ".txt" in Config.query:
		if not os.path.exists(Config.query):
			print(f"{Red}Txt file could not be found!")
			sys.exit()

		
		txtfile = open(Config.query, 'r')
		lines = txtfile.readlines()

		for line in lines:
			Config.query = line
			print(f"Searching for {Config.query}")
			init_start()
	else:
		init_start()
main()
