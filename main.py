from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from multiprocessing import Process
from modules.external import page
from modules.change_page import change_page
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
import json

from webbrowser import open as webopen
from urllib.parse import unquote
from bs4 import BeautifulSoup as bs
from requests import get
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivy.network.urlrequest import UrlRequest



class SearchScreen(Screen):
	pass

class DownloadScreen(Screen):
	pass

class NoResults(MDBoxLayout):
	pass


__version__ = '0.1.0'
class MainCard(MDCard):
	img_src = StringProperty()
	title = StringProperty()
	sypnosis = StringProperty()
	source = StringProperty()
	



class ComicApp(MDApp):
	progress = f"[{'•' * 50}]"
	page = page
	active_comic_link = None
	active_comic = 'Unknown'
	page_no = 1
	comic_name = "Empty?"
	acive_comic_details = "None"
	
	def build(self):
		self.root = Builder.load_file('design.kv')
		
		try:
			with open("data/AppData.json", "r") as file:
				self.history = json.load(file)['History']
				print(self.history)
		except FileNotFoundError:
			with open("data/AppData.json", "x") as file:
				self.history = []
				json.dump({"History":self.history}, file, indent = 4)
		
		
		return self.root
	
	
	def on_stop(self):
		with open("data/AppData.json", "w") as file:
			json.dump({"History":self.history}, file, indent = 4)
	
	
	def search(self, from_query=True):
		self.root.ids.search.ids.MainCardContainer.clear_widgets()
		
		if from_query:
			self.query = self.root.ids.search.ids.query.text
			self.link = f"https://getcomics.info/?s={self.query.replace(' ', '+').replace(':', '%3A').lower()}"
			toast(self.link)
		else:
			self.link = self.link
		
		
		try:
			net = True
			self.page = get(self.link).content
		except Exception as e:
			print(e)
			self.page = self.page
			net = False
		
		#Save Offline
		if self.query == '':
			with open('./modules/external.py', 'w') as f:
				f.write(f'page = {self.page}')
		else:
			self.history.append(self.query)
		
		soup = bs(self.page, 'html.parser')
		page_text = soup.find('nav', class_="pagination pagination-ajax")
		if page_text:
			self.page_text = page_text.text[9:]
			self.root.ids.search.ids.page_no_label.text = self.page_text	
		try:
			results = list(soup.find('div', class_='post-list-posts').children)
		except:
			results = None
		
		if results:	
			for comic in results:
				if net:
					try:
						img = comic.find('img')['src']
					except:
						img = "assets/Avengers.jpg"
							
				else:
					img = "assets/Spider-Man.jpg"
				title = list(comic.find('h1', class_='post-title').children)[0].text
				link = 1
				year = 1
				size = 1
				source = list(comic.find('h1', class_='post-title').children)[0]['href']
				sypnosis = comic.find('p', class_='post-excerpt').text[comic.find('p', class_='post-excerpt').text.index('B')+1:]
				upload_age = 1
				
				self.root.ids.search.ids.MainCardContainer.add_widget(MainCard(img_src=img, title=title, sypnosis=sypnosis, source=source))
			if net:
				return True
		else:
			toast('No Results!')
			self.root.ids.search.ids.MainCardContainer.add_widget(NoResults())
			return False		
	
	
	def on_start(self):
		Process(target=self.search()).start
		
	
	def find_comic(self):
		print("[APP][LOG] Finding Comic!")
		try:
			page = get(self.active_comic_link).content
			soup = bs(page, 'html.parser')
			
			# Comic Details
			info = soup.find_all('p', class_="")
			details = [i for i in info if "Language" in i.text][0]
			
			info = [i.text for i in info]
			rel_info = info[0:info.index(details.text) + 1]
			rel_info = "\n".join(rel_info)
			print(rel_info)
			rel_index = rel_info.index('Language :')
			rel_info = rel_info[:rel_index] + '\n\n' + rel_info[rel_index:]
#			details = details[:relevant_index] + '\n' + details[relevant_index:]
			self.acive_comic_details = rel_info
			self.root.ids.download_screen.ids.active_comic_details.text = rel_info
			
			
			# Find Comic Name
			self.active_link = soup.find('a', class_='aio-red')['href']
			self.active_link = get(self.active_link, stream=True).url
			
			self.comic_name = unquote(self.active_link.split('/')[-1])
			self.root.ids.download_screen.ids.filename.text = "/storage/emulated/0/#Comics/" + self.comic_name
			
			self.root.current = 'download_screen'
		except Exception as e:
			print(e)
			#print(f"[APP][ERROR] Couldn't Find Comic! ({self.active_comic_link})")
	
	def copy_link(self):
		Clipboard.copy(self.active_link)
		toast('Link Copied to Clipboard')
	
	def open_link(self, link):
		webopen(link)
	
	
	def download_comic(self):
		filename = self.root.ids.download_screen.ids.filename.text
		req = UrlRequest(self.active_link, on_progress=self.update_download_progress,
						chunk_size=1024,
						file_path=filename, on_success=self.download_success)
		toast('Download Started!')
	
	def update_download_progress(self, request, current_size, total_size):
		print(current_size)
		toast(str(current_size))
		self.root.ids.download_screen.ids['download_progress_bar'].value = current_size / total_size
	
	def download_success(self):
		toast('Download Completed!')
		
	
	def add_page(self):
		page_no, self.link = change_page(self.link, 'add')
		if self.search(False):
			self.page_no = page_no
			self.root.ids.search.ids.page_no_label.text = self.page_text
	
	def prev_page(self):
		page_no, link = change_page(self.link, 'subtract')
		if link != None:
			self.link = link
			if self.search(False):
				self.page_no = page_no
				self.root.ids.search.ids.page_no_label.text = self.page_text
	
		
		

ComicApp().run()
