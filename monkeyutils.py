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
import commands
import subprocess
import os
import re


# for Windows.
current_dir_for_win = ''


def get_adb_devices():
    """Return connect devices form 'adb devices' command. """
    deviceIdPattern = re.compile('^(\w+)\tdevice$')
    deviceIds = []
    commandResponse = commands.getoutput('adb devices')
    for current in commandResponse.splitlines():
        matcher = deviceIdPattern.match(current)
        if matcher:
            deviceIds.append(matcher.group(1))
    return deviceIds


def get_dpi_ratio(device, testcaseWidth, testcaseHeight):
    """Return dpi ratio, device.width / testcaseWidth. """
    deviceWidth = device.getProperty('display.width')
    wRatio = float(deviceWidth) / testcaseWidth
    deviceHeight = device.getProperty('display.height')
    hRatio = float(deviceHeight) / testcaseHeight
    return (wRatio, hRatio)


def get_device_name(device):
    """Return device model name + android version. """
    model = device.getProperty('build.model').encode('utf-8')
    ver = device.getProperty('build.version.release').encode('utf-8')
    return model.replace(' ', '_') + "_" + ver


def take_and_compare_snapshot(device, testcase, filename):
    """Take snapshot and compare to snapshot_expected image. """
    ssDir = current_dir_for_win + 'snapshot/' + get_device_name(device) + "/" + testcase
    exDir = current_dir_for_win + 'snapshot_expected/' + get_device_name(device) + "/" + testcase
    cpDir = current_dir_for_win + 'snapshot_compare/' + get_device_name(device) + "/" + testcase
    ssFile = ssDir + "/" + filename + ".png"
    exFile = exDir + "/" + filename + ".png"
    cpFile = cpDir + "/" + filename + ".png"
    
    # Take snapshot
    try:
        os.makedirs(ssDir)
    except OSError:
        pass
    ss = device.takeSnapshot()
    ss.writeToFile(ssFile, 'png')
    
    # sameAs
    expected = None #MonkeyRunner.loadImageFromFile(exFile)
    if expected:
        # sameAs
        if ss.sameAs(expected, 0.9):
            print '  - take snapshot: ' + filename + ' same as expected image.'
        else:
            print '  - take snapshot: ' + filename + ' NOT same as expected image.'
    else:
        print '  - take snapshot: ' + filename
    
    # Compare(need ImageMagick)
    if os.path.exists(exFile):
        try:
            os.makedirs(cpDir)
        except OSError:
            pass
        try:
            subprocess.call(["compare", exFile, ssFile, cpFile])
        except OSError:
            pass
