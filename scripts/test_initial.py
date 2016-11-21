import main
import unittest
import hashlib

class MainTest(unittest.TestCase):
    
  def setUp(self):
    self.app = main.app.test_client()

  def test_most_basic_route(self):
    rv = self.app.get('/testing')
    assert b'This is a testing page' in rv.data

  def test_get_firmware_web(self):
    rv = self.app.get('/firmware')
    assert b'Complete below' in rv.data

  # This test checks if the app retuns our new firmware correctly
  # Currently the md5 checksum is not of the file itself but of the complete response
  def test_get_firmware_esp_new(self):
    rv = self.app.get('/firmware',
                       environ_base={'HTTP_USER_AGENT': 'ESP8266-http-Update', 'HTTP_X_ESP8266_STA_MAC': '00:11:22:33:44:55', 'HTTP_X_ESP8266_VERSION': 'different'})
    hs = hashlib.md5()
    hs.update(rv.data)
    self.assertEqual(hs.hexdigest(), '80c9574fc2d169fe9c097239c2ed0b02')

  # This test checks the app when we don't have a new firmware
  def test_get_firmware_esp_current(self):
    rv = self.app.get('/firmware',
                       environ_base={'HTTP_USER_AGENT': 'ESP8266-http-Update', 'HTTP_X_ESP8266_STA_MAC': '00:11:22:33:44:55', 'HTTP_X_ESP8266_VERSION': 'current'})
    self.assertEqual(rv.status_code, 304) 

if __name__ == '__main__':
  unittest.main()
