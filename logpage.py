import shelve
from datetime import datetime
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen

from classes import Maintenance, Mod

class LogPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.car = None
        
        

    def display_log_page(self, car):
        self.car = car
        self.clear_widgets()

        ###Back Button
        back_button = Button(text='<-', size_hint=(0.33,0.1), pos_hint={'x':0.0,'y':0.0})
        back_button.bind(on_press=self.backward)
        self.add_widget(back_button)

        ####Add Maintenance Button
        add_mait_button = Button(text='Add Maintenance', size_hint=(0.33, 0.1), pos_hint={'x':0.33,'y':0})
        add_mait_button.bind(on_press=self.show_add_mait_popup)
        self.add_widget(add_mait_button)

        ###Add Mod Button
        add_mod_button = Button(text='Add Mod', size_hint=(0.33,0.1), pos_hint={'x':0.66,'y':0.0})
        add_mod_button.bind(on_press=self.show_add_mod_popup)
        self.add_widget(add_mod_button)

    def show_add_mait_popup(self, instance):
        INPUT_SIZE = (0.8,0.1)
        layout = FloatLayout()

        title = Label(text=f'Add new Maintenance for {self.car.name}', size_hint=(1,0.2), pos_hint={'x':0,'y':0.8})
        layout.add_widget(title)

        #############################
        ###Input for maintenance info
        #############################
        self.name_input = TextInput(hint_text='Maintenance Name', size_hint=INPUT_SIZE, pos_hint={'x':0.1, 'y':0.725})
        self.date_input = TextInput(hint_text="Date (YYYY-MM-DD)", size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.575})
        self.freq_input = TextInput(hint_text='Frequency', size_hint=(0.3,0.1), pos_hint={'x':0.1, 'y':0.425})
        
        ###Drop down box
        dropdown = DropDown()
        for unit in ['Days','Months', "Miles"]:
            btn = Button(text=unit, size_hint_y=None, height = 44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)


        self.unit_button = Button(text='Select Unit', size_hint=(0.4,0.1), pos_hint={'x':0.5,'y':0.425})
        self.unit_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x:setattr(self.unit_button, 'text',x))
        layout.add_widget(self.unit_button)


        self.descr_input = TextInput(hint_text='Description', size_hint=(0.8, 0.3), pos_hint={'x':0.1, 'y':0.125})

        ###Submit and Cancel buttons
        submit_button = Button(text='Submit', size_hint=(0.4,0.1), pos_hint={'x':0.1, 'y':0.0})
        submit_button.bind(on_press=self.add_maintenance)
        cancel_button = Button(text='Cancel', size_hint=(0.4,0.1), pos_hint={'x':0.5, 'y':0.0})
        cancel_button.bind(on_press=self.close_popup)

        ###Add widgets
        layout.add_widget(self.name_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.freq_input)
        layout.add_widget(self.descr_input)
        layout.add_widget(submit_button)
        layout.add_widget(cancel_button)

        ###Create Popup
        self.popup = Popup(title='Add Maintenance', content=layout, size_hint=(0.8, 0.8))
        self.popup.open()
    
    def add_maintenance(self, instance):
        name = self.name_input.text
        date = self.date_input.text
        frequency = self.freq_input.text
        unit = self.unit_button.text
        description = self.descr_input.text

        maintenance = Maintenance(name, description, unit, frequency, date)

        self.save_to_database(maintenance)
        self.popup.dismiss()

    def show_add_mod_popup(self, instance):
        INPUT_SIZE = (0.8,0.1)
        layout = FloatLayout()

        title = Label(text=f'Add new Mod for {self.car.name}', size_hint=(1,0.2), pos_hint={'x':0,'y':0.8})
        layout.add_widget(title)

        #############################
        ###Input for maintenance info
        #############################
        self.name_input = TextInput(hint_text='Mod Name', size_hint=INPUT_SIZE, pos_hint={'x':0.1, 'y':0.725})
        self.date_input = TextInput(hint_text="Date (YYYY-MM-DD)", size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.575})
        self.part_input = TextInput(hint_text='Part Name', size_hint=(0.3,0.1), pos_hint={'x':0.1, 'y':0.425})
        self.mech_input = TextInput(hint_text='Mechanic', size_hint=(0.4,0.1), pos_hint={'x':0.5,'y':0.425})
        self.descr_input = TextInput(hint_text='Description', size_hint=(0.8, 0.3), pos_hint={'x':0.1, 'y':0.125})

        ###Submit and Cancel buttons
        submit_button = Button(text='Submit', size_hint=(0.4,0.1), pos_hint={'x':0.1, 'y':0.0})
        submit_button.bind(on_press=self.add_mod)
        cancel_button = Button(text='Cancel', size_hint=(0.4,0.1), pos_hint={'x':0.5, 'y':0.0})
        cancel_button.bind(on_press=self.close_popup)

        ###Add widgets
        layout.add_widget(self.name_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.part_input)
        layout.add_widget(self.mech_input)
        layout.add_widget(self.descr_input)
        layout.add_widget(submit_button)
        layout.add_widget(cancel_button)

        ###Create Popup
        self.popup = Popup(title='Add Mod', content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def add_mod(self, instance):
        name = self.name_input.text
        date = self.date_input.text
        part = self.part_input.text
        mech = self.mech_input.text
        description = self.descr_input.text

        mod = Mod(name, date, mech, part, description)

        self.save_to_database(mod)
        self.popup.dismiss()


    def save_to_database(self, entry):
        # Determine the type of entry
        entry_type = type(entry).__name__.lower()  # e.g., "maintenance" or "mod"
        
        # Create a unique key
        if isinstance(entry, Maintenance):
            key = f"maintenance_{entry.name}_{entry.lastdate}"
        elif isinstance(entry, Mod):
            key = f"mod_{entry.name}_{entry.date}"
        else:
            raise ValueError("Unsupported entry type")

        # Save the object in the database
        with shelve.open(f"cars/{self.car.id}db") as db:
            db[key] = entry
            print(f"Saved {entry_type}: {key}")

   
        
    def close_popup(self, instance):
        self.popup.dismiss()

    def backward(self, instance):
        car_page_screen = self.manager.get_screen('Car')
        car_page_screen.display_car_info(self.car)
        self.manager.transition.direction = 'right'
        self.manager.current = 'Car'



