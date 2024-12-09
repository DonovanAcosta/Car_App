import shelve
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

from classes import Car

class Homepage(FloatLayout):
    BUTTON_SIZE = (1,0.2)
    BUTTON_Y = 0.8

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.display_home_page()
        self.bind(size=self.update_background, pos=self.update_background)
        with self.canvas.before:
            self.bg_color = Color(0.05, 0.1, 0.2, 1)  # RGBA
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
    
    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def display_home_page(self):
        self.clear_widgets()

        self.add_car_button = Button(
            text='Add Car', 
            size_hint=(1,0.1), 
            pos_hint={'x':0,'y':0},
            background_color=(0, 0.6, 0.8, 1),    #Button Color
            color=(1, 1, 1, 1),)    #Text Color
        self.add_car_button.bind(on_press=self.show_add_car_popup)
        self.add_widget(self.add_car_button)

        with shelve.open('car_database') as db:
            button_count = self.BUTTON_Y
            for car_id in db:
                car = db[car_id]
                car_button_text = car.name if car.name !='' else f'{car.make}: {car.model}'
                car_button = Button(
                    text=car_button_text, 
                    size_hint=self.BUTTON_SIZE, 
                    pos_hint={'x':0,'y':button_count},
                    background_color=(0, 0.6, 0.8, 1),
                    color=(1, 1, 1, 1),)
                car_button.bind(on_press=lambda _, car=car: self.show_car_page(car))
                self.add_widget(car_button)
                button_count -= 0.2

    def show_car_page(self, car):
        carpage = self.screen_manager.get_screen('Car')
        carpage.display_car_info(car)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'Car'

    def show_add_car_popup(self, instance):
        layout = FloatLayout()

        INPUT_SIZE = (0.8,0.1)
        self.make_input = TextInput(hint_text='Make', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.7}, background_color = (1,1,1, 0.7))
        self.model_input = TextInput(hint_text='Model', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.55}, background_color = (1,1,1, 0.7))
        self.year_input = TextInput(hint_text='Year', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.4}, background_color = (1,1,1, 0.7))
        self.name_input = TextInput(hint_text='Name(Optional)', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.25}, background_color = (1,1,1, 0.7))

        submit_button = Button(
            text='Submit',
            size_hint = (0.4,0.1),
            pos_hint={'x':0.1,'y':0.1},
            background_color=(0, 0.6, 0.8, 1),
            color=(1, 1, 1, 1))
        submit_button.bind(on_press=self.add_car_to_db)
        cancel_button = Button(
            text='Cancel',
            size_hint = (0.4,0.1),
            pos_hint={'x':0.5,'y':0.1},
            background_color=(0, 0.6, 0.8, 1),
            color=(1, 1, 1, 1))
        cancel_button.bind(on_press=self.close_popup)

        layout.add_widget(self.make_input)
        layout.add_widget(self.model_input)
        layout.add_widget(self.year_input)
        layout.add_widget(self.name_input)
        layout.add_widget(submit_button)
        layout.add_widget(cancel_button)

        self.popup = Popup(title='Add Car', content=layout, size_hint=(0.8, 0.8),background='')

        self.popup.title_color = [1, 1, 1, 1]
        self.popup.background_color = (0.05, 0.1, 0.2, 1)
        self.popup.open()

    def add_car_to_db(self, instance):
        new_make = self.make_input.text
        new_model = self.model_input.text
        new_year = self.year_input.text
        new_name = self.name_input.text

        new_car = Car(Make=new_make, Model=new_model, Year=new_year, Name=new_name)

        validation_check = new_car.check()
        if validation_check:
            error_popup = Popup(
                title = "Error",
                content = Label(
                    text = validation_check,
                    color = (1,0,0,1),
                    halign = "center",
                    valign = "middle",
                ),
                size_hint = (0.6,0.4),
                background = '',
            )
            error_popup.background_color = (0.05, 0.1, 0.2, 1)
            error_popup.open()
            return

        with shelve.open('car_database') as db:
            db[new_car.id] = new_car
            print(f'Car {new_car.name} added to the database with ID: {new_car.id}')

        self.popup.dismiss()
        self.display_home_page()

    def close_popup(self, instance):
        self.popup.dismiss()