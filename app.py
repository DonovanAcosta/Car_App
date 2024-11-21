from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from homepage import Homepage
from carpage import CarPage
#from screenlogpage import LogPage

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.homepage = Homepage(self.screen_manager)
        home_screen = Screen(name='Home')
        home_screen.add_widget(self.homepage)
        self.screen_manager.add_widget(home_screen)
        
        self.carpage = CarPage(name='Car')
        self.screen_manager.add_widget(self.carpage)
        '''
        self.logpage = LogPage()
        screen = Screen(name='log')
        screen.add_widget(self.logpage)
        self.screen_manager.add_widget(screen)
        '''
        return self.screen_manager
    
myapp = MyApp()
myapp.run()