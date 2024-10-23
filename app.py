from kivy.app import App
from homepage import HomePageLayout

class MyApp(App):
    def build(self):
        return HomePageLayout()
    
if __name__ == '__main__':
    Car_App = MyApp()
    Car_App.run()
