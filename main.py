from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.toast import toast

KV = '''

#: import ScrollEffect kivy.effects.scroll.ScrollEffect
#: import Window kivy.core.window.Window

<MainCard>:
	orientation: "vertical"
	spacing: 5
	padding: 0
	size_hint: None, None
	size: Window.size[0]/2 - 30, Window.size[1]/3 - 20
	pos_hint: {"center_x": .5, "center_y": .5}
	
	FitImage:
		source: "Image.jpg"
	
	MDBoxLayout:
		orientation: "vertical"
		padding: 8
		spacing: 5
		size_hint_y: None
		size: 50, 60

		MDLabel:
			text: "Card Title"
			#theme_text_color: "Secondary"
			size_hint_y: None
			font_style: 'H6'
			height: self.texture_size[1]

		MDLabel:
			text: "Secondary Text"
			theme_text_color: "Secondary"
			size_hint_y: None
			height: self.texture_size[1]


Screen:
	
	ScrollView:
		effect_cls: ScrollEffect
		StackLayout:
			#StackLayout Properties
			orientation: "lr-tb"
			id: MainCardContainer
			spacing: 15
			padding: 20
			# Properties needed for ScrollView
			size_hint_y: None
			height: self.minimum_height	
		


'''


class MainCard(MDCard):
	def __init__(self, **kwargs):
		super(MainCard, self).__init__(**kwargs)
		self.bind(size=self.update)
	
	def update(self, *args):
		print(1)




class TestCard(MDApp):
	def build(self):
		self.root = Builder.load_string(KV)
		
		return self.root
	
	def on_start(self):
		for i in range(100): 
			self.root.ids.MainCardContainer.add_widget(MainCard())
		#toast(str(Window.orientation))


TestCard().run()