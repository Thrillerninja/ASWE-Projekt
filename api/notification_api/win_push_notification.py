import sys

if sys.platform == "win32":
    from win10toast import ToastNotifier

class PushNotifierAPI:
    def __init__(self):
        if sys.platform == "win32":
            self.toaster = ToastNotifier()
        else:
            self.toaster = None

    def notification_active(self):
        if self.toaster:
            return self.toaster.notification_active()
        else:
            print("Notification not supported on this platform.")
            return False

    def push(self, title: str, message: str, duration: int = 10, icon_path: str = None, threaded: bool = True):
        '''
        Display a notification.
        - threaded: True -> notification runs in its own thread (non-blocking)
        '''
        if self.toaster:
            self.toaster.show_toast(
                title=title,
                msg=message,
                duration=duration,
                icon_path=icon_path,
                threaded=threaded
            )
        else:
            print(f"Notification: {title} - {message} (not supported on this platform)")
