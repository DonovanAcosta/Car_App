import shelve
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from classes import Car
from logspage import LogsPage

class CarPopUp(FloatLayout):
    def __init__(self, car, homepage):
        super().__init__()
        self.homepage = homepage
        self.display_car_popup(car)

    def display_car_popup(self, car):
        layout = FloatLayout()

        ###Details of car label
        detail_label = Label(
            text=f"ID:{car.id}\nMake: {car.make}\nModel: {car.model}\nYear: {car.year}\nName: {car.name}", size_hint=(0.8, 0.4), pos_hint={'x':0.1, 'y':0.5}
        )
        layout.add_widget(detail_label)


        ###Delete Button
        delete_button = Button(text="Delete Car", size_hint=(0.33, 0.1), pos_hint={'x':0.0, 'y':0.0})
        delete_button.bind(on_press=lambda instance:self.show_delete_confirmation(car))
        layout.add_widget(delete_button)


        ###Edit Button
        edit_button = Button(text="Edit Details", size_hint=(0.33, 0.1), pos_hint={'x':0.33, 'y':0.0})
        edit_button.bind(on_press=lambda instance:self.show_edit_car_popup(car))
        layout.add_widget(edit_button)


        ###View Logs Button
        view_logs_button = Button(text="View Logs", size_hint=(0.33, 0.1), pos_hint={'x':0.66, 'y':0.0})
        view_logs_button.bind(on_press=lambda instance, c=car: LogsPage(car=c, carpopup=self))
        layout.add_widget(view_logs_button)


        ###Naming the pop up
        if car.name == '':
            popupname = f'{car.make}: {car.model}'
        else:
            popupname = car.name

        ###Creating pop up
        self.popup = Popup(title=f"{popupname}", content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def show_delete_confirmation(self, car):
        layout = FloatLayout()

        ###Confirmation Message
        label = Label(text='Are you sure you want to delete this car?', size_hint=(0.8, 0.3), pos_hint={'x':0.1, 'y':0.5})
        layout.add_widget(label)

        confirmation_popup = Popup(title="Confirm Deletion", content=layout, size_hint=(0.6, 0.4))

        ###Yes an No buttons
        yes_button = Button(text='Yes', size_hint=(0.4, 0.2), pos_hint={'x': 0.05, 'y':0.2})
        yes_button.bind(on_press=lambda instance: self.delete_car(car, confirmation_popup))
        layout.add_widget(yes_button)

        no_button = Button(text='No', size_hint=(0.4, 0.2), pos_hint={'x':0.55, 'y':0.2})
        no_button.bind(on_press=confirmation_popup.dismiss)
        layout.add_widget(no_button)

        confirmation_popup.open() 

    def delete_car(self, car, confirmation_popup):
        ###Delete Car
        with shelve.open('car_database') as db:
            del db[car.id]
            print(f'Car {car.name} with ID {car.id} deleted.')

        ##close confirmation
        confirmation_popup.dismiss()
        ##close car popup
        self.popup.dismiss()
        ###Refresh homepage with changes
        self.homepage.display_home_page()


    def show_edit_car_popup(self, car):
        layout = FloatLayout()

        self.make_input = TextInput(text=car.make, size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.7})
        self.model_input = TextInput(text=car.model, size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.55})
        self.year_input = TextInput(text=car.year, size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.4})
        self.name_input = TextInput(text=car.name, size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.25})

        submit_button = Button(text='Save Changes', size_hint=(0.5, 0.1), pos_hint={'x': 0.25, 'y': 0.1})
        submit_button.bind(on_press=lambda instance: self.update_car_in_db(car))

        layout.add_widget(self.make_input)
        layout.add_widget(self.model_input)
        layout.add_widget(self.year_input)
        layout.add_widget(self.name_input)
        layout.add_widget(submit_button)

        self.edit_popup = Popup(title='Edit Car', content=layout, size_hint=(0.8, 0.8))
        self.edit_popup.open()

    def update_car_in_db(self, car):
        car.make = self.make_input.text
        car.model = self.model_input.text
        car.year = self.year_input.text
        car.name = self.name_input.text

        with shelve.open('car_database') as db:
            db[car.id] = car
            print(f'Car {car.name} with ID {car.id} updated.')

        self.edit_popup.dismiss()
        self.popup.dismiss()
        self.homepage.display_home_page()
        


         
        
