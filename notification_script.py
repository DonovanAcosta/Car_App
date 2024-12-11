from plyer import notification
import shelve
from datetime import datetime
import os

def check_and_notify():
    """Check for upcoming notifications and send them."""
    current_time = datetime.now()

    with shelve.open("Notifications") as db:
        keys_to_delete = []
        for notification_id, notification_data in db.items():
            # Check if the date has passed or is today
            notify_date = datetime.strptime(notification_data.date, "%Y-%m-%d")
            if notify_date <= current_time:
                car_name = get_car_name(notification_data.car)
                print(car_name)
                # Send system notification
                notification.notify(
                    title=f"Reminder for {car_name}",
                    message=f"{get_car_name(notification_data.car)} requires maintenance!!",
                    app_name="Car Maintenance App",
                    timeout=10,  # Seconds
                )
                print(f"Notification sent for Car ID {notification_data.car}, Maintenance: {notification_data.maitenance}")
                
                # Mark this notification for deletion
                keys_to_delete.append(notification_id)

        # Remove sent notifications from the database
        for key in keys_to_delete:
            del db[key]
            print(f"Notification ID {key} removed from the database.")


def get_car_name(car_id):
    with shelve.open('car_database') as car_db:
        if car_id in car_db:
            if car_db[car_id].name != '':
                return car_db[car_id].name
            return f'{car_db[car_id].make}: {car_db[car_id].model}'


if __name__ == "__main__":
    check_and_notify()