from plyer import notification

def notification_set(log, car):
    notification.notify(
                    title=f"New Reminder",
                    message=f"Reminder for {log.name} has been set for {log.calcNextDate(car)}",
                    app_name="Car Maintenance App",
                    timeout=10,  # Seconds
                )