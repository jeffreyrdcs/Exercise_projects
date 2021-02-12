#
#  This is the version I submitted to the github ticket (12/02/2021)
#

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.metrics import dp, sp
from kivy.core.window import Window

wininit = (450,650)
Window.size = wininit

class LoginScreen(BoxLayout):

	test_font_size = NumericProperty(40)
	base_font_size = NumericProperty(40)

	def __init__(self, *args):
		super(LoginScreen, self).__init__()
		self.window_size_safe = [0, 0]
		self.window_pixel_dim_safe = [0, 0]
		self.display_num = 0
		self.window_width_min = wininit[0]
		self.window_height_min = wininit[1]
		Window.bind(on_resize = self.resolution_check_update)

	def resolution_check_update(self, instance, x, y):
		#Properties that I found:
		#0. I notice that in retina display the actual height and width in pixel is actually a multiple of the window.size (?)
		#1. Moving the window to an external display doesn't change get_system_size().
		#2. Rescaling the window changes system.size instantly.
		#3. on_resize gets triggered on both resizing the screen and switching displays.
		#4. During initization, self.height and self.width gives 1600, 1200, but x, y give correct sizes (Don't understand why).
		#5. The self.height and self.width values lag. It only gets set AFTER we finish resizing the window and confirm the size.
		#6. Looking through the code I discovered that there is this x,y that return from on_resize, which seems to be the instanteous size that get updated faster than height,width
		# get_system_size = Window._get_system_size()
		# selfheightwidth = [int(self.width), int(self.height)]
		# print(f'Get_System_size: {get_system_size},  SelfHW: {selfheightwidth},  System_size: {Window.system_size}, X:{x}, Y:{y}')

		# Initialize the values when it first launches
		if self.window_size_safe == [0, 0]:
			self.window_size_safe = Window._get_system_size()
			self.window_pixel_dim_safe = [x, y]
			print(f'Saved the initiated size_safe: {self.window_size_safe}')
			return 

		# Check whether the resize is caused by switching monitors or resizing
		if Window._get_system_size() == self.window_size_safe:
			print(f'Window moved to another display: {Window.size}')
			window_current_pixel_dim = [x, y]

			# Check if the window pixel dimensions suddenly changes (in my retina display it is 2x less when move to external) 
			if self.window_pixel_dim_safe == multiply_list(window_current_pixel_dim, 2):
				print('Resizing font for External Display')
				self.display_num = 1

			# Check if the window pixel dimensions suddenly changes (in my retina display it is 2x more when move to retina) 				
			elif self.window_pixel_dim_safe == multiply_list(window_current_pixel_dim, 0.5):
				print('Resizing font for Retina Display')
				self.display_num = 0

			# Update the font_size, x,y change should be identical
			scale_fac = window_current_pixel_dim[0]/self.window_pixel_dim_safe[0]
			self.test_font_size = self.test_font_size * scale_fac

			# Save it to base_font for font resizing when window size changes
			self.base_font_size = self.test_font_size

			# Saved the current window pixel dimensions
			self.window_pixel_dim_safe = window_current_pixel_dim

		else:
			window_current_pixel_dim = [x, y]			
			print(f'Window being resized: {Window.size}')
			# Update the font size (Enlarge font size after window resize)
			# Idea from here: https://www.reddit.com/r/kivy/comments/86okok/update_font_sizes_in_a_layoutwidget_after_window/
			if self.display_num == 0:
				scale_fac_display = 2
			elif self.display_num == 1:
				scale_fac_display = 1
			scale_fac = min(window_current_pixel_dim[0]/(scale_fac_display * self.window_width_min), window_current_pixel_dim[1]/(scale_fac_display * self.window_height_min))
			self.test_font_size = self.base_font_size * scale_fac
			print(f'Scale fac {scale_fac}')
			self.window_pixel_dim_safe = window_current_pixel_dim
			self.window_size_safe = Window._get_system_size()
			

def multiply_list(in_list, value):
	return [element * value for element in in_list]


class DisplayTextTestApp(App):
	Window.minimum_width = wininit[0]
	Window.minimum_height = wininit[1]
	def build(self):
		return LoginScreen()	


if __name__ == "__main__":
	DisplayTextTestApp().run()


