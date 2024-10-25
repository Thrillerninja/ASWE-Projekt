from win10toast import ToastNotifier


class PushNotiffierAPI:

    def __init__(self) -> None:
        self.toaster = ToastNotifier()
    
    def notification_active(self):
        self.toaster.notification_active()

    def push(self, title:str, message:str, duration:int=10, icon_path:str=None, threaded:bool=True):
        '''
        Zeige eine Benachrichtigung an
        - threaded: True -> notification gets its own thread (non blocking)
        '''
        self.toaster.show_toast(title=title, 
                        msg=message, 
                        duration=duration,  # Dauer der Benachrichtigung in Sekunden
                        icon_path=icon_path,  # Pfad zu einem Icon (Optional)
                        threaded=threaded)  # Benachrichtigung in eigenem Thread

