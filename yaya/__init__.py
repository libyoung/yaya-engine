from .deviceaction import *
from .uiobjectaction import *
from .adbfunction import *
from .device import *
from .devicemanage import *
from .frameworkkey import *
from .flow import Flow
from .configparser import *
from .testtemplate import * 
from .otherdatastruct import *
from .cmdlineparser import *
from .xmlfile import *
from .logdatatojson import *
from .create_xlsx import *
'''
################################################
# Flow Engine Framework
################################################
Flow = flow.Flow
################################################
# Flow Engine Framework Key
################################################
NOT = frameworkkey.NOT
FOR = frameworkkey.FOR
SWITCH = frameworkkey.SWITCH
################################################
# Device Management
################################################
#SwitchSDevice = devicemanage.SwitchSDevice
#SwitchMDevice = devicemanage.SwitchMDevice
################################################
# Device Key
################################################
Home = deviceaction.Home
Back = deviceaction.Back
Point = deviceaction.Point
Enter = deviceaction.Enter
Recent = deviceaction.Recent
Power = deviceaction.Power
Menu = deviceaction.Menu
Search = deviceaction.Search
'''
################################################
# ADB Function
################################################
#OpenAPP = adbfunction.OpenAPP
#IsInCall = adbfunction.IsInCall
#InCallStay = adbfunction.InCallStay
#IsRinging = adbfunction.IsRinging
CallAnswer = CallAnswer()
EndCall = EndCall()
'''
################################################
# UIObject Action
################################################
#IsGone = uiobjectaction.Gone
#IsExists = uiobjectaction.Exists
Click = uiobjectaction.Click
LongClick = uiobjectaction.LongClick
Input = uiobjectaction.Input
Vert = uiobjectaction.Vert
Swipe = uiobjectaction.Swipe
Drag = uiobjectaction.Drag
Gesture = uiobjectaction.Gesture
################################################
# Test Template
################################################
TestTemplate = testtemplate.TestTemplate
Ready = testtemplate.Ready
################################################
# Config Parser
################################################
Get = configparser.get
Stci = configparser.stci
'''