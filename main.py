from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.toast import toast
from modules.swiper import MDSwiper, MDSwiperItem
from modules.external import page
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.uix.screenmanager import Screen

from webbrowser import open
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



class MainCard(MDCard):
	img_src = StringProperty()
	title = StringProperty()
	sypnosis = StringProperty()
	source = StringProperty()
	



class ComicApp(MDApp):
	dialog = None
	progress = f"[{'•' * 50}]"
	page = page
	active_comic = None
	
	def build(self):
		self.root = Builder.load_file('design.kv')
		print(self.root.ids.main.ids)
		return self.root
	
	def search(self):
		self.root.ids.main.ids.MainCardContainer.clear_widgets()
		
		self.query = self.root.ids.main.ids.query.text
		self.link = f"https://getcomics.info/?s={self.query.replace(' ', '+').lower()}"
		print(self.link)
		
		
		try:
			net = True
			self.page = get(self.link).text
		except:
			self.page = self.page
			net = False
		
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
	
	
	def on_start(self):
		self.search()
		
	
	def confirm_download(self):
		if not self.dialog:
			self.dialog = MDDialog(
				text="Download Comic?",
				buttons=[
					MDFlatButton(
						text="CANCEL", text_color=self.theme_cls.primary_color
					),
					MDRaisedButton(
						text="DOWNLOAD", text_color=self.theme_cls.primary_color
					),
				],
			)
		self.dialog.buttons[0].on_press = self.dialog.dismiss
		self.dialog.buttons[1].on_press = self.find_comic
		self.dialog.size_hint = (None, 1)
		self.dialog.width = 1000
		self.dialog.open()
	
	def find_comic(self):
		self.dialog.dismiss()
		try:
			self.root.current = 'download_screen'
			page = get(self.active_comic).content
			soup = bs(page, 'html.parser')
			self.active_link = soup.find('a', class_='aio-red')['href']
		except:
			pass
	
	def copy_link(self):
		Clipboard.copy(self.active_link)
		toast('Link Copied to Clipboard')
	
	def open_link(self):
		open(self.active_link)
		

ComicApp().run()
