from generate_mac import generate_mac
import random

z = 0

while z < 2:
    coinToss = random.randint(0, 1)

    if random.randint(0, 4) == 0:
        userHexString = generate_mac.total_random().replace(":", " ")
        wifiHexString = generate_mac.total_random().replace(":", " ")
    else:
        userHexString = "Wrong"
        wifiHexString = "Wrong"
    locations = ['5172a-clwa-2144', "Incorrect Location"]

    wifistr = f'2023-08-07 07:47:15.470435      DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (4075268204) 471 days, 16:11:22.04    SNMPv2-MIB::snmpTrapOID.0 = OID: SNMPv2-SMI::enterprises.14179.2.6.3.1   SNMPv2-SMI::enterprises.14179.2.6.2.35.0 = Hex-STRING: {wifiHexString}       SNMPv2-SMI::enterprises.14179.2.6.2.36.0 = INTEGER: 0   SNMPv2-SMI::enterprises.14179.2.6.2.37.0 = INTEGER: 2   SNMPv2-SMI::enterprises.14179.2.6.2.43.0 = IpAddress: 0.0.0.0   SNMPv2-SMI::enterprises.14179.2.6.2.34.0 = Hex-STRING: {userHexString}        SNMPv2-SMI::enterprises.14179.2.6.2.39.0 = ""   SNMPv2-SMI::enterprises.14179.2.2.1.1.3.0 = STRING:  "{locations[coinToss]}"'

    timestamp = wifistr[0: 26]

    wifiHexIndex = wifistr.find('Hex-STRING') + 12
    wifiHex = wifistr[wifiHexIndex: wifiHexIndex+17]

    userHexIndex = wifistr.rfind('Hex-STRING') + 12
    userHex = wifistr[userHexIndex: userHexIndex+17]

    locationIndex = wifistr.rfind('STRING') + 10
    location = wifistr[locationIndex: -1]

    def checkStr(location, user):
        location = location[:4]
        #checks if first 4 chars of location string is a number which seems to be consitent throughout all locations
        try:
            x = 0
            int(location)
            #secondary protection where even if location is correct if the mac address of the user doesnt have 5 spaces (as all mac addresses do) it will throw an error
            for i in range(0, len(user)):
                if user[i] == " ":
                    x += 1
            if x != 5:
                raise ValueError("Broken String")
            else:
                print(userHex)
        except:
            print('broken string')

    checkStr(location, userHex)
    z += 1
