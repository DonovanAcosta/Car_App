import shelve
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from classes import Car

class HomePageLayout(FloatLayout):
    def __init__(self):
        super().__init__()

        self.button = Button(text='Add Car', size_hint=(1,0.1), pos_hint={'x':0, 'y':0})
        self.button.bind(on_press=self.show_add_car_popup)
        #self.add_widget(self.button)  

        self.display_saved_cars()

    def show_add_car_popup(self, instance):
        layout = GridLayout(cols=2)

        self.make_input = TextInput(hint_text='Make')
        self.model_input = TextInput(hint_text='Model')
        self.year_input = TextInput(hint_text='Year')
        self.name_input = TextInput(hint_text='Name(Optional)') 

        layout.add_widget(Label(text='Make: '))
        layout.add_widget(self.make_input)       
        layout.add_widget(Label(text='Model: '))
        layout.add_widget(self.model_input)  
        layout.add_widget(Label(text='Year: '))
        layout.add_widget(self.year_input)
        layout.add_widget(Label(text='Name: '))
        layout.add_widget(self.name_input)    

        submit_button =Button(text='Submit')
        submit_button.bind(on_press=self.add_car_to_db)
        layout.add_widget(submit_button)

        self.popup = Popup(title='Add Car', content=layout, size_hint=(0.8,0.8))
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

        # Close the popup
        self.popup.dismiss()
        self.display_saved_cars()

    def display_saved_cars(self):
        self.clear_widgets()
        self.add_widget(self.button)

        with shelve.open('car_database') as db:
            button_count = 0.8
            for car_id in db:
                car = db[car_id]
                if car.name != '':
                    car_button = Button(text=f'{car.name}', size_hint=(1,0.2),  pos_hint={'x':0, 'y':(button_count)})
                else:
                    car_button = Button(text=f'{car.make}: {car.model}', size_hint=(1, 0.2),  pos_hint={'x':0, 'y':(button_count)})
                car_button.bind(on_press=lambda instance, c=car: self.show_car_details(c))
                self.add_widget(car_button)
                button_count -= 0.2

    def show_car_details(self, car):
        # Create a popup or new screen to show car details
        detail_text = f'ID: {car.id}\nMake: {car.make}\nModel: {car.model}\nYear: {car.year}\nName: {car.name}'
        detail_label = Label(text=detail_text, size_hint=(1, 1))

        popup = Popup(title='Car Details', content=detail_label, size_hint=(0.8, 0.8))
        popup.open()