import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



class Car:
    def __init__(self, Make='none', Model='none', Year='none', Name='none', Mileage= None):
        self.make = Make
        self.model = Model
        self.year = Year
        self.name = Name
        self.mileage = Mileage

        self.id = f'{random.randint(0, 9999999):07}'
        self.check()

    def check(self):
        if not self.model or not self.make or not self.year:
            return "Make, Model, Year and Mileage are required fields"
        elif self.mileage is not None and not str(self.mileage).isdigit():
            return "Mileage must contain only numerical values in string format"
        self.mileage = int(self.mileage)
        return None

    def getLog(self):
        return

    def addMaintenance(self, name, date, unit, freq):
        return

    def addMod(self, date, mech, part, track):
        return

    

class Maintenance:
    def __init__(self, Name, Description, Unit, Freq, LastDate):
        self.name = Name
        self.description = Description
        self.unit = Unit
        self.freq = Freq
        self.date = LastDate

    def calcNextDate(self, car = None):
        if self.unit == "Months":
            next_date = self.date + relativedelta(months=self.freq)
            return next_date.strftime("%Y-%m-%d")
        elif self.unit == "Days":
            next_date = self.date + relativedelta(days =self.freq)
            return next_date.strftime("%Y-%m-%d")
        elif self.unit == "Miles":
            next_mileage = car.mileage + self.freq
            return next_mileage
          
class Mod:
    def __init__(self, Name, Date, Mechanic, PartName, Description):
        self.name = Name
        self.date = Date
        self.mechanic = Mechanic
        self.partname = PartName
        self.description = Description

class Notification:
    def __init__(self, car_id, maint_name, next_date):
        self.car = car_id
        self.maitenance = maint_name
        self.date = next_date
        self.notificationId =  f'{random.randint(0, 9999999):07}'  