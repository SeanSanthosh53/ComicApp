from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.core.window import Window
from multiprocessing import Process
from modules.swiper import MDSwiper, MDSwiperItem
from modules.external import page
from modules.change_page import change_page
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.screenmanager import Screen

from webbrowser import open as webopen
from bs4 import BeautifulSoup as bs
from requests import get
from os import system
from time import sleep
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast


class MainScreen(Screen):
	pass

class DownloadScreen(Screen):
	pass


__version__ = '1.0.0'
class MainCard(MDCard):
	img_src = StringProperty()
	title = StringProperty()
	sypnosis = StringProperty()
	source = StringProperty()
	



class ComicApp(MDApp):
	dialog = None
	progress = f"[{'•' * 50}]"
	page = page
	active_comic_link = None
	active_comic = 'Unknown'
	page_no = 1
	
	def build(self):
		self.root = Builder.load_file('design.kv')
		print(self.root.ids.main.ids)
		return self.root
	
	def search(self, from_query=True):
		self.root.ids.main.ids.MainCardContainer.clear_widgets()
		
		if from_query:
			self.query = self.root.ids.main.ids.query.text
			self.link = f"https://getcomics.info/?s={self.query.replace(' ', '+').lower()}"
		else:
			self.link = self.link
		
		
		try:
			net = True
			self.page = get(self.link).content
		except Exception as e:
			print(e)
			self.page = self.page
			net = False
		
		if self.query == '':
			print('wrote')
			with open('./modules/external.py', 'w') as f:
				f.write(f'page = {self.page}')
		
		soup = bs(self.page, 'html.parser')
		try:
			results = list(soup.find('div', class_='post-list-posts').children)
		except:
			results = None
		
		if results:	
			for comic in results:
				if net:
					img = comic.find('img')['src']
				else:
					img = "assets/Spider-Man.jpg"
				title = list(comic.find('h1', class_='post-title').children)[0].text
				link = 1
				year = 1
				size = 1
				source = list(comic.find('h1', class_='post-title').children)[0]['href']
				sypnosis = comic.find('p', class_='post-excerpt').text[comic.find('p', class_='post-excerpt').text.index('B')+1:]
				upload_age = 1
				
				self.root.ids.main.ids.MainCardContainer.add_widget(MainCard(img_src=img, title=title, sypnosis=sypnosis, source=source))
			if net:
				return True
		else:
			return False		
	
	
	def on_start(self):
		Process(target=self.search()).start
		
	
	def confirm_download(self):
		def dismiss():
			self.dialog.dismiss()
			self.dialog = None
		if not self.dialog:
			self.dialog = MDDialog(
				text=f"Download Comic: {self.active_comic} ?",
				buttons=[
					MDFlatButton(
						text="CANCEL", text_color=self.theme_cls.primary_color
					),
					MDRaisedButton(
						text="DOWNLOAD", text_color=self.theme_cls.primary_color
					),
				],
			)
		self.dialog.buttons[0].on_press = dismiss
		self.dialog.buttons[1].on_press = self.find_comic
		self.dialog.size_hint = (None, 1)
		self.dialog.width = 1000
		self.dialog.open()
	
	def find_comic(self):
		self.dialog.dismiss()
		try:
			self.root.current = 'download_screen'
			page = get(self.active_comic_link).content
			soup = bs(page, 'html.parser')
			self.active_link = soup.find('a', class_='aio-red')['href']
		except:
			pass
	
	def copy_link(self):
		Clipboard.copy(self.active_link)
		toast('Link Copied to Clipboard')
	
	def open_link(self, link):
		webopen(link)
		
	
	def download_link(self):
		command = f"python /storage/emulated/0/test.py {self.active_link} pj"
		toast(command)
		system(command)
	
	def add_page(self):
		page_no, self.link = change_page(self.link, 'add')
		if self.search(False):
			self.page_no = page_no
			self.root.ids.main.ids.page_no_label.text = str(self.page_no)
	
	def prev_page(self):
		page_no, link = change_page(self.link, 'subtract')
		if link != None:
			self.link = link
			if self.search(False):
				self.page_no = page_no
				self.root.ids.main.ids.page_no_label.text = str(self.page_no)
		
		

ComicApp().run()
