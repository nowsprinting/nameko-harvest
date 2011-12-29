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

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

# if running on Windows, set CURRENT_DIR_FOR_WIN value.
CURRENT_DIR_FOR_WIN = None #'H:\\HUB_Products\\workspace_android\\testterMonkeyrunner\\'
if CURRENT_DIR_FOR_WIN:
    import sys
    import os
    sys.path.append(CURRENT_DIR_FOR_WIN)
    os.chdir(CURRENT_DIR_FOR_WIN)
    os.system("cd "+CURRENT_DIR_FOR_WIN)

import monkeyutils


if CURRENT_DIR_FOR_WIN:
    monkeyutils.current_dir_for_win = CURRENT_DIR_FOR_WIN


def nameko_harvest(device, target):
    testcase = __name__.encode('utf-8')
    dpiRatio = monkeyutils.get_dpi_ratio(device, 480, 800)
    print '- ' + testcase + ' start!'
    
    # Launch application.
    runComponent = target['package_name'] + '/' + target['launch_activity']
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(15)
    
    #Touch tostart
    device.touch(int(dpiRatio[0]*240), int(dpiRatio[1]*550), 'DOWN_AND_UP')
    MonkeyRunner.sleep(5)
    
    #harvest
    for y in [310,280,250]:
        dragStart   = (int(dpiRatio[0]*0), int(dpiRatio[1]*y))
        dragEnd     = (int(dpiRatio[0]*479), int(dpiRatio[1]*y))
        device.drag(dragStart, dragEnd, 3.0, 10)
        MonkeyRunner.sleep(2)
    
    #food
    food_pos_x = [50, 140, 240, 340, 430]
    device.touch(int(dpiRatio[0]*food_pos_x[2]), int(dpiRatio[1]*670), 'DOWN_AND_UP')
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

def main():
    deviceIdList = monkeyutils.get_adb_devices()
    if not deviceIdList:
        print 'Connection device not found.'
        return
    
    for deviceId in deviceIdList:
        device = MonkeyRunner.waitForConnection(5, deviceId)
        if device:
            print "----\nConnect to " + monkeyutils.get_device_name(device)
            nameko_harvest(device, target)
            
    print "----\n"


if __name__ == '__main__':
    main()