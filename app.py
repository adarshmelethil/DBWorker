import env

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):

	def __init__(self, *args, **kwargs):
		super(LoginScreen, self).__init__(*args, **kwargs)
		self.cols = 2
		self.add_widget(Label(text='User Name'))
		self.username = TextInput(multiline=False)
		self.add_widget(self.username)
		self.add_widget(Label(text='password'))
		self.password = TextInput(password=True, multiline=False)
		self.add_widget(self.password)

class MSAccessApp(App):

	def build(self):
		# self.title = "Microsoft Access Work"
		# return Label(text="Hello world")
		return LoginScreen()


if __name__ == "__main__":
	MSAccessApp().run()
