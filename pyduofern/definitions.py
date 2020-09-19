# coding=utf-8
#   python interface for dufoern usb stick
#   Copyright (C) 2017 Paul Görgen
#   Rough python re-write of the FHEM duofern modules by telekatz, also licensed under GPLv2
#   This re-write contains only negligible amounts of original code
#   apart from some comments to facilitate translation of the not-yet
#   translated parts of the original software. Modification dates are
#   documented as submits to the git repository of this code, currently
#   maintained at https://github.com/gluap/pyduofern.git

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

devices = {
    "40": "RolloTron Standard",
    "41": "RolloTron Comfort Slave",
    "42": "Rohrmotor-Aktor",
    "43": "Universalaktor",
    "46": "Steckdosenaktor",
    "47": "Rohrmotor Steuerung",
    "48": "Dimmaktor",
    "49": "Rohrmotor",
    "4b": "Connect-Aktor",
    "4C": "Troll Basis",
    "4e": "SX5",
    "61": "RolloTron Comfort Master",
    "62": "Super Fake Device",
    "65": "Bewegungsmelder",
    "69": "Umweltsensor",
    "70": "Troll Comfort DuoFern",
    "71": "Troll Comfort DuoFern (Lichtmodus)",
    "73": "Raumthermostat",
    "74": "Wandtaster 6fach 230V",
    "a0": "Handsender (6 Gruppen-48 Geraete)",
    "a1": "Handsender (1 Gruppe-48 Geraete)",
    "a2": "Handsender (6 Gruppen-1 Geraet)",
    "a3": "Handsender (1 Gruppe-1 Geraet)",
    "a4": "Wandtaster",
    "a5": "Sonnensensor",
    "a7": "Funksender UP",
    "a8": "HomeTimer",
    "aa": "Markisenwaechter",
    "ab": "Rauchmelder",
    "ad": "Wandtaster 6fach Bat",
}

sensorMsg = {
    "0701": {"name": "up", "chan": 6, "state": "Btn01"},
    "0702": {"name": "stop", "chan": 6, "state": "Btn02"},
    "0703": {"name": "down", "chan": 6, "state": "Btn03"},
    "0718": {"name": "stepUp", "chan": 6, "state": "Btn18"},
    "0719": {"name": "stepDown", "chan": 6, "state": "Btn19"},
    "071a": {"name": "pressed", "chan": 6, "state": "Btn1A"},
    "0713": {"name": "dawn", "chan": 5, "state": "dawn"},
    "0709": {"name": "dusk", "chan": 5, "state": "dusk"},
    "0708": {"name": "startSun", "chan": 5, "state": "on"},
    "070a": {"name": "endSun", "chan": 5, "state": "off"},
    "070d": {"name": "startWind", "chan": 5, "state": "on"},
    "070e": {"name": "endWind", "chan": 5, "state": "off"},
    "0711": {"name": "startRain", "chan": 5, "state": "on"},
    "0712": {"name": "endRain", "chan": 5, "state": "off"},
    "071c": {"name": "startTemp", "chan": 5, "state": "on"},
    "071d": {"name": "endTemp", "chan": 5, "state": "off"},
    "071e": {"name": "startSmoke", "chan": 5, "state": "on"},
    "071f": {"name": "endSmoke", "chan": 5, "state": "off"},
    "0720": {"name": "startMotion", "chan": 5, "state": "on"},
    "0721": {"name": "endMotion", "chan": 5, "state": "off"},
    "0723": {"name": "closeEnd", "chan": 5, "state": "off"},
    "0724": {"name": "closeStart", "chan": 5, "state": "on"},
    "0e01": {"name": "off", "chan": 6, "state": "Btn01"},
    "0e02": {"name": "off", "chan": 6, "state": "Btn02"},
    "0e03": {"name": "on", "chan": 6, "state": "Btn03"},
}

deadTimes = {
    0x00: "off",
    0x10: "short(160ms)",
    0x20: "long(480ms)",
    0x30: "individual",
}

closingTimes = {
    0x00: "off",
    0x01: "30",
    0x02: "60",
    0x03: "90",
    0x04: "120",
    0x05: "150",
    0x06: "180",
    0x07: "210",
    0x08: "240",
    0x09: "error",
    0x0A: "error",
    0x0B: "error",
    0x0C: "error",
    0x0D: "error",
    0x0E: "error",
    0x0F: "error",
}

openSpeeds = {
    0x00: "error",
    0x10: "11",
    0x20: "15",
    0x30: "19",
}

commands = {
    "remotePair": {"noArg": "06010000000000000000"},
    "remoteUnpair": {"noArg": "06020000000000000000"},
    "up": {"noArg": "0701tt00000000000000"},
    "stop": {"noArg": "07020000000000000000"},
    "down": {"noArg": "0703tt00000000000000"},
    "position": {"value": "0707ttnn000000000000"},
    "level": {"value": "0707ttnn000000000000"},
    "sunMode": {"on": "070801FF000000000000",
                "off": "070A0100000000000000"},
    "dusk": {"noArg": "070901FF000000000000"},
    "reversal": {"noArg": "070C0000000000000000"},
    "modeChange": {"noArg": "070C0000000000000000"},
    "windMode": {"on": "070D01FF000000000000",
                 "off": "070E0100000000000000"},
    "rainMode": {"on": "071101FF000000000000",
                 "off": "07120100000000000000"},
    "dawn": {"noArg": "071301FF000000000000"},
    "rainDirection": {"down": "071400FD000000000000",
                      "up": "071400FE000000000000"},
    "windDirection": {"down": "071500FD000000000000",
                      "up": "071500FE000000000000"},
    "tempUp": {"noArg": "0718tt00000000000000"},
    "tempDown": {"noArg": "0719tt00000000000000"},
    "toggle": {"noArg": "071A0000000000000000"},
    "slatPosition": {"value": "071B00000000nn000000"},
    "desired-temp": {"temp1": "0722tt0000wwww000000"},
    "sunAutomatic": {"on": "080100FD000000000000",
                     "off": "080100FE000000000000"},
    "sunPosition": {"value": "080100nn000000000000"},
    "ventilatingMode": {"on": "080200FD000000000000",
                        "off": "080200FE000000000000"},
    "ventilatingPosition": {"value": "080200nn000000000000"},
    "intermediateMode": {"on": "080200FD000000000000",
                         "off": "080200FE000000000000"},
    "intermediateValue": {"value": "080200nn000000000000"},
    "saveIntermediateOnStop": {"on": "080200FB000000000000",
                               "off": "080200FC000000000000"},
    "runningTime": {"value3": "0803nn00000000000000"},
    "timeAutomatic": {"on": "080400FD000000000000",
                      "off": "080400FE000000000000"},
    "duskAutomatic": {"on": "080500FD000000000000",
                      "off": "080500FE000000000000"},
    "manualMode": {"on": "080600FD000000000000",
                   "off": "080600FE000000000000"},
    "windAutomatic": {"on": "080700FD000000000000",
                      "off": "080700FE000000000000"},
    "rainAutomatic": {"on": "080800FD000000000000",
                      "off": "080800FE000000000000"},
    "dawnAutomatic": {"on": "080900FD000000000000",
                      "off": "080900FE000000000000"},
    "tiltInSunPos": {"on": "080C00FD000000000000",
                     "off": "080C00FE000000000000"},
    "tiltInVentPos": {"on": "080D00FD000000000000",
                      "off": "080D00FE000000000000"},
    "tiltAfterMoveLevel": {"on": "080E00FD000000000000",
                           "off": "080E00FE000000000000"},
    "tiltAfterStopDown": {"on": "080F00FD000000000000",
                          "off": "080F00FE000000000000"},
    "defaultSlatPos": {"value": "0810nn00000000000000"},
    "blindsMode": {"on": "081100FD000000000000",
                   "off": "081100FE000000000000"},
    "slatRunTime": {"value4": "0812nn00000000000000"},
    "motorDeadTime": {"off": "08130000000000000000",
                      "short": "08130100000000000000",
                      "long": "08130200000000000000"},
    "stairwellFunction": {"on": "081400FD000000000000",
                          "off": "081400FE000000000000"},
    "stairwellTime": {"value2": "08140000wwww00000000"},
    "reset": {"settings": "0815CB00000000000000",
              "full": "0815CC00000000000000"},
    "10minuteAlarm": {"on": "081700FD000000000000",
                      "off": "081700FE000000000000"},
    "automaticClosing": {"off": "08180000000000000000",
                         "30": "08180001000000000000",
                         "60": "08180002000000000000",
                         "90": "08180003000000000000",
                         "120": "08180004000000000000",
                         "150": "08180005000000000000",
                         "180": "08180006000000000000",
                         "210": "08180007000000000000",
                         "240": "08180008000000000000"},
    "2000cycleAlarm": {"on": "081900FD000000000000",
                       "off": "081900FE000000000000"},
    "openSpeed": {"11": "081A0001000000000000",
                  "15": "081A0002000000000000",
                  "19": "081A0003000000000000"},
    "backJump": {"on": "081B00FD000000000000",
                 "off": "081B00FE000000000000"},
    "temperatureThreshold1": {"temp2": "081E00000001nn000000"},
    "temperatureThreshold2": {"temp2": "081E0000000200nn0000"},
    "temperatureThreshold3": {"temp2": "081E000000040000nn00"},
    "temperatureThreshold4": {"temp2": "081E00000008000000nn"},
    "actTempLimit": {"1": "081Ett00001000000000",
                     "2": "081Ett00003000000000",
                     "3": "081Ett00005000000000",
                     "4": "081Ett00007000000000"},
    "on": {"noArg": "0E03tt00000000000000"},
    "off": {"noArg": "0E02tt00000000000000"},
}

wCmds = {
    "interval": {"enable": 0x80, "min": 1, "max": 100, "offset": 0,
                 "reg": 7, "byte": 0, "size": 1, "count": 1,
                 "mask": 0xff, "shift": 0},
    "DCF": {"enable": 0x02, "min": 0, "max": 0, "offset": 0,
            "reg": 7, "byte": 1, "size": 1, "count": 1,
            "mask": 0x02, "shift": 0},
    "timezone": {"enable": 0x00, "min": 0, "max": 23, "offset": 0,
                 "reg": 7, "byte": 4, "size": 1, "count": 1,
                 "mask": 0xff, "shift": 0},
    "latitude": {"enable": 0x00, "min": 0, "max": 90, "offset": 0,
                 "reg": 7, "byte": 5, "size": 1, "count": 1,
                 "mask": 0xff, "shift": 0},
    "longitude": {"enable": 0x00, "min": -90, "max": 90, "offset": 256,
                  "reg": 7, "byte": 7, "size": 1, "count": 1,
                  "mask": 0xff, "shift": 0},
    "triggerWind": {"enable": 0x20, "min": 1, "max": 31, "offset": 0,
                    "reg": 6, "byte": 0, "size": 1, "count": 5,
                    "mask": 0x7f, "shift": 0},
    "triggerRain": {"enable": 0x80, "min": 0, "max": 0, "offset": 0,
                    "reg": 6, "byte": 0, "size": 1, "count": 1,
                    "mask": 0x80, "shift": 0},
    "triggerTemperature": {"enable": 0x80, "min": -40, "max": 80, "offset": 40,
                           "reg": 6, "byte": 5, "size": 1, "count": 5,
                           "mask": 0xff, "shift": 0},
    "triggerDawn": {"enable": 0x10000000, "min": 1, "max": 100, "offset": -1,
                    "reg": 0, "byte": 0, "size": 4, "count": 5,
                    "mask": 0x1000007F, "shift": 0},
    "triggerDusk": {"enable": 0x20000000, "min": 1, "max": 100, "offset": -1,
                    "reg": 0, "byte": 0, "size": 4, "count": 5,
                    "mask": 0x201FC000, "shift": 14},
    "triggerSun": {"enable": 0x20000000, "min": 1, "max": 0x3FFFFFFF, "offset": 0,
                   "reg": 3, "byte": 0, "size": 4, "count": 5,
                   "mask": 0x3FFFFFC0, "shift": 0},
    "triggerSunDirection": {"enable": 0x00, "min": 1, "max": 0xFF, "offset": 0,
                            "reg": 3, "byte": 1, "size": 4, "count": 5,
                            "mask": 0x000000FF, "shift": 0},
    "triggerSunHeight": {"enable": 0x00, "min": 1, "max": 0x1FFF, "offset": 0,
                         "reg": 3, "byte": 1, "size": 4, "count": 5,
                         "mask": 0x00001F80, "shift": 0},
}

commandsStatus = {
    "getStatus": "0F",
    "getWeather": "13",
    "getTime": "10",
}

setsBasic = {
    "reset:settings,full": "",
    "remotePair:noArg": "",
    "remoteUnpair:noArg": "",
}

setsDefaultRollerShutter = {
    "getStatus:noArg": "",
    "up:noArg": "",
    "down:noArg": "",
    "stop:noArg": "",
    "toggle:noArg": "",
    "dusk:noArg": "",
    "dawn:noArg": "",
    "sunMode:on,off": "",
    "position:slider,0,1,100": "",
    "sunPosition:slider,0,1,100": "",
    "ventilatingPosition:slider,0,1,100": "",
    "dawnAutomatic:on,off": "",
    "duskAutomatic:on,off": "",
    "manualMode:on,off": "",
    "sunAutomatic:on,off": "",
    "timeAutomatic:on,off": "",
    "ventilatingMode:on,off": "",
}

setsRolloTube = {
    "windAutomatic:on,off": "",
    "rainAutomatic:on,off": "",
    "windDirection:up,down": "",
    "rainDirection:up,down": "",
    "windMode:on,off": "",
    "rainMode:on,off": "",
    "reversal:on,off": "",
}

setsTroll = {
    "windAutomatic:on,off": "",
    "rainAutomatic:on,off": "",
    "windDirection:up,down": "",
    "rainDirection:up,down": "",
    "windMode:on,off": "",
    "rainMode:on,off": "",
    "runningTime:slider,0,1,150": "",
    "motorDeadTime:off,short,long": "",
    "reversal:on,off": "",
}

setsBlinds = {
    "tiltInSunPos:on,off": "",
    "tiltInVentPos:on,off": "",
    "tiltAfterMoveLevel:on,off": "",
    "tiltAfterStopDown:on,off": "",
    "defaultSlatPos:slider,0,1,100": "",
    "slatRunTime:slider,0,100,5000": "",
    "slatPosition:slider,0,1,100": "",
}

setsSwitchActor = {
    "getStatus:noArg": "",
    "dawnAutomatic:on,off": "",
    "duskAutomatic:on,off": "",
    "manualMode:on,off": "",
    "sunAutomatic:on,off": "",
    "timeAutomatic:on,off": "",
    "sunMode:on,off": "",
    "modeChange:on,off": "",
    "stairwellFunction:on,off": "",
    "stairwellTime:slider,0,10,3200": "",
    "on:noArg": "",
    "off:noArg": "",
    "dusk:noArg": "",
    "dawn:noArg": "",
}

setsUmweltsensor = {
    "getStatus:noArg": "",
    "getWeather:noArg": "",
    "getTime:noArg": "",
}

setsUmweltsensor00 = {
    "getWeather:noArg": "",
    "getTime:noArg": "",
    "getConfig:noArg": "",
    "writeConfig:noArg": "",
    "DCF:on,off": "",
    "interval:off,1,2,3,4,5,6,7,8,9,10,15,20,30,40,50,60,70,80,90,100": "",
    "latitude": "",
    "longitude": "",
    "timezone": "",
    "time:noArg": "",
    "triggerDawn": "",
    "triggerDusk": "",
    "triggerRain:on,off": "",
    "triggerSun": "",
    "triggerSunDirection": "",
    "triggerSunHeight": "",
    "triggerTemperature": "",
    "triggerWind": "",
}

setsUmweltsensor01 = {
    "windAutomatic:on,off": "",
    "rainAutomatic:on,off": "",
    "windDirection:up,down": "",
    "rainDirection:up,down": "",
    "windMode:on,off": "",
    "rainMode:on,off": "",
    "runningTime:slider,0,1,100": "",
    "reversal:on,off": "",
}

setsSX5 = {
    "getStatus:noArg": "",
    "up:noArg": "",
    "down:noArg": "",
    "stop:noArg": "",
    "position:slider,0,1,100": "",
    "ventilatingPosition:slider,0,1,100": "",
    "manualMode:on,off": "",
    "timeAutomatic:on,off": "",
    "ventilatingMode:on,off": "",
    "10minuteAlarm:on,off": "",
    "automaticClosing:off,30,60,90,120,150,180,210,240": "",
    "2000cycleAlarm:on,off": "",
    "openSpeed:11,15,19": "",
    "backJump:on,off": "",
}

setsDimmer = {
    "getStatus:noArg": "",
    "level:slider,0,1,100": "",
    "on:noArg": "",
    "off:noArg": "",
    "dawnAutomatic:on,off": "",
    "duskAutomatic:on,off": "",
    "manualMode:on,off": "",
    "sunAutomatic:on,off": "",
    "timeAutomatic:on,off": "",
    "sunMode:on,off": "",
    "modeChange:on,off": "",
    "stairwellFunction:on,off": "",
    "stairwellTime:slider,0,10,3200": "",
    "runningTime:slider,0,1,255": "",
    "intermediateMode:on,off": "",
    "intermediateValue:slider,0,1,100": "",
    "saveIntermediateOnStop:on,off": "",
    "dusk:noArg": "",
    "dawn:noArg": "",
}

tempSetList = "4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5,25.0,25.5,26.0,26.5,27.0,27.5,28.0,28.5,29.0,29.5,30.0"

setsThermostat = {
    "getStatus:noArg": "",
    "tempUp:noArg": "",
    "tempDown:noArg": "",
    "manualMode:on,off": "",
    "timeAutomatic:on,off": "",
    "temperatureThreshold1:$tempSetList": "",
    "temperatureThreshold2:$tempSetList": "",
    "temperatureThreshold3:$tempSetList": "",
    "temperatureThreshold4:$tempSetList": "",
    "actTempLimit:0,1,2,3": "",
    "desired-temp:$tempSetList": "",
}
