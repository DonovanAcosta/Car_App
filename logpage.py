import shelve
from datetime import datetime
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

from classes import Maintenance, Mod

class LogPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.car = None
        self.bind(size=self.update_background, pos=self.update_background)
        with self.canvas.before:
            self.bg_color = Color(0.05, 0.1, 0.2, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
    
    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        
        

    def display_log_page(self, car):
        self.car = car
        self.clear_widgets()

        ###Back Button
        back_button = Button(text='<-', size_hint=(0.33,0.1), pos_hint={'x':0.0,'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))

        back_button.bind(on_press=self.backward)
        self.add_widget(back_button)

        ####Add Maintenance Button
        add_mait_button = Button(text='Add Maintenance', size_hint=(0.33, 0.1), pos_hint={'x':0.33,'y':0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        add_mait_button.bind(on_press=self.show_add_mait_popup)
        self.add_widget(add_mait_button)

        ###Add Mod Button
        add_mod_button = Button(text='Add Mod', size_hint=(0.34,0.1), pos_hint={'x':0.66,'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        add_mod_button.bind(on_press=self.show_add_mod_popup)
        self.add_widget(add_mod_button)


        ###Load logs onto Screen
        logs = self.load_logs()

        log_y = 0.9
        for log in logs:
            log_label = Button(text=self.format_log_entry(log), size_hint=(1,0.1),pos_hint={'x':0.0,'y':log_y},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
            log_label.bind(on_press=lambda instance, log=log: self.show_log_popup(instance, log))
            self.add_widget(log_label)
            log_y-=0.1

    def show_add_mait_popup(self, instance):
        INPUT_SIZE = (0.8,0.1)
        layout = FloatLayout()

        title = Label(text=f'Add new Maintenance for {self.car.name}', size_hint=(1,0.2), pos_hint={'x':0,'y':0.8})
        layout.add_widget(title)

        #############################
        ###Input for maintenance info
        #############################
        self.name_input = TextInput(hint_text='Maintenance Name', size_hint=INPUT_SIZE, pos_hint={'x':0.1, 'y':0.725}, background_color = (1,1,1, 0.7))
        self.date_input = TextInput(hint_text="Date (YYYY-MM-DD)", size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.575}, background_color = (1,1,1, 0.7))
        self.freq_input = TextInput(hint_text='Frequency', size_hint=(0.3,0.1), pos_hint={'x':0.1, 'y':0.425}, background_color = (1,1,1, 0.7))
        
        ###Drop down box
        dropdown = DropDown()
        for unit in ['Days','Months', "Miles"]:
            btn = Button(text=unit, size_hint_y=None, height = 44,background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)



        self.unit_button = Button(text='Select Unit', size_hint=(0.4,0.1), pos_hint={'x':0.5,'y':0.425},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        self.unit_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x:setattr(self.unit_button, 'text',x))
        layout.add_widget(self.unit_button)

        self.descr_input = TextInput(hint_text='Description', size_hint=(0.8, 0.3), pos_hint={'x':0.1, 'y':0.125}, background_color = (1,1,1, 0.7))

        ###Submit and Cancel buttons
        submit_button = Button(text='Submit', size_hint=(0.4,0.1), pos_hint={'x':0.1, 'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        submit_button.bind(on_press=self.add_maintenance)
        cancel_button = Button(text='Cancel', size_hint=(0.4,0.1), pos_hint={'x':0.5, 'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))

        cancel_button.bind(on_press=self.close_popup)

        ###Add widgets
        layout.add_widget(self.name_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.freq_input)
        layout.add_widget(self.descr_input)
        layout.add_widget(submit_button)
        layout.add_widget(cancel_button)

        ###Create Popup
        self.popup = Popup(title='Add Maintenance', content=layout, size_hint=(0.8, 0.8), background='')
        self.popup.background_color = (0.05, 0.1, 0.2, 1)
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
        self.display_log_page(self.car)

    def show_add_mod_popup(self, instance):
        INPUT_SIZE = (0.8,0.1)
        layout = FloatLayout()

        title = Label(text=f'Add new Mod for {self.car.name}', size_hint=(1,0.2), pos_hint={'x':0,'y':0.8})
        layout.add_widget(title)

        #############################
        ###Input for maintenance info
        #############################

        self.name_input = TextInput(hint_text='Mod Name', size_hint=INPUT_SIZE, pos_hint={'x':0.1, 'y':0.725}, background_color = (1,1,1, 0.7))
        self.date_input = TextInput(hint_text="Date (YYYY-MM-DD)", size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.575}, background_color = (1,1,1, 0.7))
        self.part_input = TextInput(hint_text='Part Name', size_hint=(0.3,0.1), pos_hint={'x':0.1, 'y':0.425}, background_color = (1,1,1, 0.7))
        self.mech_input = TextInput(hint_text='Mechanic', size_hint=(0.4,0.1), pos_hint={'x':0.5,'y':0.425}, background_color = (1,1,1, 0.7))
        self.descr_input = TextInput(hint_text='Description', size_hint=(0.8, 0.3), pos_hint={'x':0.1, 'y':0.125}, background_color = (1,1,1, 0.7))

        ###Submit and Cancel buttons
        submit_button = Button(text='Submit', size_hint=(0.4,0.1), pos_hint={'x':0.1, 'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        submit_button.bind(on_press=self.add_mod)
        cancel_button = Button(text='Cancel', size_hint=(0.4,0.1), pos_hint={'x':0.5, 'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))

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
        self.popup = Popup(title='Add Mod', content=layout, size_hint=(0.8, 0.8), background='')
        self.popup.background_color = (0.05, 0.1, 0.2, 1)
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
        self.display_log_page(self.car)


    def save_to_database(self, entry):
        # Determine the type of entry
        entry_type = type(entry).__name__.lower()  # e.g., "maintenance" or "mod"
        
        # Create a unique key
        if isinstance(entry, Maintenance):
            key = f"maintenance_{entry.name}_{entry.date}"
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

    def load_logs(self):
        """
        Load and return a list of logs (maintenance and mods) sorted by date.
        """
        logs = []
        with shelve.open(f"cars/{self.car.id}db") as db:
            for key in db:
                logs.append(db[key])
        # Sort logs by date in descending order
        logs.sort(key=lambda entry: datetime.strptime(entry.date if isinstance(entry, Mod) else entry.date, "%Y-%m-%d"), reverse=True)
        return logs

    def format_log_entry(self, log):
        """
        Format a log entry for display.
        """
        if isinstance(log, Maintenance):
            return f"{log.name} (Maintenance)"
        elif isinstance(log, Mod):
            return f"{log.name} (Mod)"
        return "Unknown Log Entry"
    
    def show_log_popup(self, instance, log):
        layout=FloatLayout()
        label = Label(text=f'Date:{log.date}\n')
        layout.add_widget(label)

        self.popup = Popup(title=f'{log.name}', content=layout, size_hint=(0.8, 0.8), background='')
        self.popup.background_color = (0.05, 0.1, 0.2, 1)
        self.popup.open()

        return



