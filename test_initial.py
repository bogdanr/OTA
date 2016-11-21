import main
import unittest
import hashlib

class MainTest(unittest.TestCase):
    
  def setUp(self):
    self.app = main.app.test_client()

  def test_most_basic_route(self):
    rv = self.app.get('/testing')
    assert 'This is a testing page' in rv.data

  def test_get_firmware_web(self):
    rv = self.app.get('/firmware')
    assert 'Complete below' in rv.data

  # This test checks if the app retuns our new firmware correctly
  # Currently the md5 checksum is not of the file itself but of the complete response
  def test_get_firmware_esp_new(self):
    rv = self.app.get('/firmware',
                       environ_base={'HTTP_USER_AGENT': 'ESP8266-http-Update', 'HTTP_X_ESP8266_STA_MAC': '00:11:22:33:44:55', 'HTTP_X_ESP8266_VERSION': 'different'})
#   print rv.response.__dict__
    hs = hashlib.md5()
    for i in rv.response:
      hs.update(i)
    self.assertEqual(hs.hexdigest(), 'd41d8cd98f00b204e9800998ecf8427e')

  # This test checks the app when we don't have a new firmware
  def test_get_firmware_esp_current(self):
    rv = self.app.get('/firmware',
                       environ_base={'HTTP_USER_AGENT': 'ESP8266-http-Update', 'HTTP_X_ESP8266_STA_MAC': '00:11:22:33:44:55', 'HTTP_X_ESP8266_VERSION': 'current'})
    self.assertEqual(rv.status_code, 304) 

if __name__ == '__main__':
  unittest.main()
