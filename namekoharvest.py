# coding=utf-8
# Copyright 2011, Android Test and Evaluation Club
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    Nameko auto harvest script.
"""
__author__ = "Koji Hasegawa"
__copyright__ = "Copyright 2012, Android Test and Evaluation Club."
__credits__ = ["Koji Hasegawa"]
__license__ = "Apache License Version 2.0"
__version__ = "1.0"

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import unittest
import sys
import os
sys.path.append(os.path.dirname(__file__))
import monkeyutils


def nameko_harvest(device, target):
    testcase = __name__.encode('utf-8')
    dpiRatio = monkeyutils.get_dpi_ratio(device, 480, 800)
    
    # Launch application.
    runComponent = target['package_name'] + '/' + target['launch_activity']
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(15)
    
    #Touch tostart
    device.touch(int(dpiRatio[0]*240), int(dpiRatio[1]*550), 'DOWN_AND_UP')
    MonkeyRunner.sleep(5)
    
    #harvest
    for y in [310,280,250,200]:
        dragStart   = (int(dpiRatio[0]*0), int(dpiRatio[1]*y))
        dragEnd     = (int(dpiRatio[0]*479), int(dpiRatio[1]*y))
        device.drag(dragStart, dragEnd, 2.0, 10)
        MonkeyRunner.sleep(2)
    
    #food
    food_pos_x = [50, 140, 240, 340, 430]
    device.touch(int(dpiRatio[0]*food_pos_x[2]), int(dpiRatio[1]*670), 'DOWN_AND_UP')
    MonkeyRunner.sleep(3)
    device.touch(int(dpiRatio[0]*340), int(dpiRatio[1]*540), 'DOWN_AND_UP')
    MonkeyRunner.sleep(5)
    
    #exit
    device.press('KEYCODE_BACK', 'DOWN_AND_UP' , "1")
    MonkeyRunner.sleep(5)
    device.press('KEYCODE_BACK', 'DOWN_AND_UP' , "1")
    MonkeyRunner.sleep(5)


target = {
    'package_name'      : 'jp.co.beeworks.funghiGardeningKit',
    'launch_activity'   : '.AdMobActivity'
}


class NamekoHarvest(unittest.TestCase):
    
    def test_nameko_harvest(self):
        serial = os.environ.get("serial")
        if serial:
            deviceIdList = [serial]
        else:
            deviceIdList = monkeyutils.get_adb_devices()
            if not deviceIdList:
                fail('Can not get serial or device-id-list.')
        
        for deviceId in deviceIdList:
            device = MonkeyRunner.waitForConnection(5, deviceId)
            if device:
                print "----\nConnect to " + monkeyutils.get_device_name(device)
                nameko_harvest(device, target)
            else:
                fail('Does not got device.')

if __name__ == '__main__':
    unittest.main()
