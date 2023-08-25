import hashlib
import uuid
import psycopg2

wifistr = '2023-08-07 07:47:15.470435      DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (4075268204) 471 days, 16:11:22.04    SNMPv2-MIB::snmpTrapOID.0 = OID: SNMPv2-SMI::enterprises.14179.2.6.3.1   SNMPv2-SMI::enterprises.14179.2.6.2.35.0 = Hex-STRING: F8 4F 57 41 5D 50        SNMPv2-SMI::enterprises.14179.2.6.2.36.0 = INTEGER: 0   SNMPv2-SMI::enterprises.14179.2.6.2.37.0 = INTEGER: 2   SNMPv2-SMI::enterprises.14179.2.6.2.43.0 = IpAddress: 0.0.0.0   SNMPv2-SMI::enterprises.14179.2.6.2.34.0 = Hex-STRING: 5C 52 30 98 DA 53        SNMPv2-SMI::enterprises.14179.2.6.2.39.0 = ""   SNMPv2-SMI::enterprises.14179.2.2.1.1.3.0 = STRING:  "5172a-clwa-2144"'

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
            print('broken string')
    except:
        print('broken string')

checkStr(location, userHex)

#print(timestamp)
#print(wifiHex)
#print(location)
#print(userHex)

salt =  uuid.uuid4().hex

userHex = hashlib.sha256(salt.encode() + userHex.encode()).hexdigest()
print(userHex)

psql = psycopg2.connect("user=postgres password=samrith123 dbname=wifi")

cursor = psql.cursor()

cursor.execute('INSERT INTO info VALUES(%s, %s, %s, %s)', (timestamp, wifiHex, userHex, location))

psql.commit()
cursor.close()
psql.close()