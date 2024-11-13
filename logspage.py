import shelve
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from classes import Maintenance, Mod

class LogsPage(FloatLayout):
    def __init__(self, car, carpopup):
        super().__init__()
        self.car = car
        self.carpopup = carpopup
        self.display_log_page()

    def display_log_page(self): 
        self.carpopup.popup.dismiss()
        self.carpopup.homepage.clear_widgets()
        
        # Display existing logs
        with shelve.open(f'cars/{self.car.id}') as db:
            for key in db:
                entry = db[key]
                entry_type = 'Maintenance' if isinstance(entry, Maintenance) else 'Mod'
                label = Label(text=f"{entry_type}: {entry.name}", size_hint=(1, 0.1))
                self.add_widget(label)

        # Button to add maintenance
        add_maintenance_button = Button(text="Add Maintenance", size_hint=(0.5, 0.1), pos_hint={'x': 0.0, 'y': 0.0})
        add_maintenance_button.bind(on_press=self.show_add_maintenance_popup)
        self.add_widget(add_maintenance_button)

        # Button to add mod
        add_mod_button = Button(text="Add Mod", size_hint=(0.5, 0.1), pos_hint={'x': 0.5, 'y': 0.0})
        add_mod_button.bind(on_press=self.show_add_mod_popup)
        self.add_widget(add_mod_button)

    def show_add_maintenance_popup(self, instance):
        # Popup for adding a maintenance log
        layout = FloatLayout()
        name_input = TextInput(hint_text='Maintenance Name', size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.7})
        date_input = TextInput(hint_text='Date', size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'y': 0.5})
        submit_button = Button(text='Submit', size_hint=(0.5, 0.1), pos_hint={'x': 0.25, 'y': 0.1})
        submit_button.bind(on_press=lambda x: self.add_maintenance(name_input.text, date_input.text))
        
        layout.add_widget(name_input)
        layout.add_widget(date_input)
        layout.add_widget(submit_button)

        self.popup = Popup(title='Add Maintenance', content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def add_maintenance(self, name, date):
        maintenance = Maintenance(Name=name, Description="Routine Maintenance", Unit="miles", Freq="6 months", LastDate=date)
        with shelve.open(f'{self.car.id}') as db:
            db[f"maintenance_{len(db)+1}"] = maintenance
        self.popup.dismiss()
        self.display_log_page()
    
    # Similarly, implement `show_add_mod_popup` and `add_mod` for modifications

    def show_add_mod_popup(self, instance):
        return
    
        
