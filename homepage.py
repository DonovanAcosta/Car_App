import shelve
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from classes import Car

class Homepage(FloatLayout):
    BUTTON_SIZE = (1,0.2)
    BUTTON_Y = 0.8

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.display_home_page()

    def display_home_page(self):
        self.clear_widgets()

        self.add_car_button = Button(text='Add Car', size_hint=(1,0.1), pos_hint={'x':0,'y':0})
        self.add_car_button.bind(on_press=self.show_add_car_popup)
        self.add_widget(self.add_car_button)

        with shelve.open('car_database') as db:
            button_count = self.BUTTON_Y
            for car_id in db:
                car = db[car_id]
                car_button_text = car.name if car.name !='' else f'{car.make}: {car.model}'
                car_button = Button(text=car_button_text, size_hint=self.BUTTON_SIZE, pos_hint={'x':0,'y':button_count})
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
        self.make_input = TextInput(hint_text='Make', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.7})
        self.model_input = TextInput(hint_text='Model', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.55})
        self.year_input = TextInput(hint_text='Year', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.4})
        self.name_input = TextInput(hint_text='Name(Optional)', size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.25})

        submit_button = Button(text='Submit', size_hint = (0.5,0.1), pos_hint={'x':0.25,'y':0.1})
        submit_button.bind(on_press=self.add_car_to_db)

        layout.add_widget(self.make_input)
        layout.add_widget(self.model_input)
        layout.add_widget(self.year_input)
        layout.add_widget(self.name_input)
        layout.add_widget(submit_button)

        self.popup = Popup(title='Add Car', content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def add_car_to_db(self, instance):
        new_make = self.make_input.text
        new_model = self.model_input.text
        new_year = self.year_input.text
        new_name = self.name_input.text

        new_car = Car(Make=new_make, Model=new_model, Year=new_year, Name=new_name)

        with shelve.open('car_database') as db:
            db[new_car.id] = new_car
            print(f'Car {new_car.name} added to the database with ID: {new_car.id}')

        self.popup.dismiss()
        self.display_home_page()