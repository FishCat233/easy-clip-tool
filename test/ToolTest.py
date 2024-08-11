import unittest
from EasyClipToolMainFrame import ConfigTool


class MyTestCase(unittest.TestCase):
    def test_timeStrIsValid(self):
        self.assertTrue(ConfigTool.timeStrIsValid("00 00"))
        self.assertTrue(ConfigTool.timeStrIsValid("00:00"))
        self.assertTrue(ConfigTool.timeStrIsValid("00：00"))
        self.assertTrue(ConfigTool.timeStrIsValid("23 59"))
        self.assertTrue(ConfigTool.timeStrIsValid("11:11:23"))
        self.assertTrue(ConfigTool.timeStrIsValid("11：11 23"))
        self.assertFalse(ConfigTool.timeStrIsValid("错误的"))
        self.assertFalse(ConfigTool.timeStrIsValid("daigoaf"))

    def test_compareTimeStr(self):
        pass


if __name__ == '__main__':
    unittest.main()
