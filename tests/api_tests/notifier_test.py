import sys
import unittest
from unittest.mock import patch
from api.notification_api import PushNotifierAPI

# Mocking the ToastNotifier class
class MockToastNotifier:
    def notification_active(self):
        return True

    def show_toast(self, title, msg, duration, icon_path=None, threaded=True):
        pass  # No implementation needed for the test

class TestPushNotifierAPI(unittest.TestCase):

    @patch('win10toast.ToastNotifier', new=MockToastNotifier)  # Patch the actual import
    @unittest.skipUnless(sys.platform == 'win32', "Skipping Windows-specific tests on non-Windows platforms.")
    def test_init_windows(self):
        api = PushNotifierAPI()
        self.assertIsNotNone(api.toaster)

    @patch.object(sys, 'platform', 'linux')
    def test_init_non_windows(self):
        api = PushNotifierAPI()
        self.assertIsNone(api.toaster)
        
    @patch.object(sys, 'platform', 'linux')
    def test_notification_active_non_windows(self):
        api = PushNotifierAPI()
        with patch('builtins.print') as mocked_print:
            self.assertFalse(api.notification_active())
            mocked_print.assert_called_once_with("Notification not supported on this platform.")

    @patch('win10toast.ToastNotifier', new=MockToastNotifier)  # Patch the actual import
    @unittest.skipUnless(sys.platform == 'win32', "Skipping Windows-specific tests on non-Windows platforms.")
    def test_push_windows(self):
        api = PushNotifierAPI()
        api.push("Test Title", "Test Message", duration=5, icon_path="icon.ico", threaded=False)
        # Here you can verify behavior if needed

    @patch.object(sys, 'platform', 'linux')
    def test_push_non_windows(self):
        api = PushNotifierAPI()
        with patch('builtins.print') as mocked_print:
            api.push("Test Title", "Test Message")
            mocked_print.assert_called_once_with("Notification: Test Title - Test Message (not supported on this platform)")


if __name__ == '__main__':
    unittest.main()
