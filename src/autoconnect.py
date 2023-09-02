import time
import yaml
import pywifi

from os import path
from pywifi import const
from pythonping import ping

def connect_to_wifi(ssid, password):
    
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]

    ifaces.disconnect()

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    ifaces.remove_all_network_profiles()

    tmp_profile = ifaces.add_network_profile(profile)

    ifaces.connect(tmp_profile)

    print('🟢 Conexão estabelecida.')


def check_connection():
    hostname = 'www.google.com'
    connected = None

    try:
        response = ping(hostname, verbose=True)

        if response:
            connected = True
            print('✔ Conexão ativa.')

        else:
            connected = False
            print('✖ Conexão inativa.')

    except Exception as e:
        print(f'🔴 Erro ao verificar a conexão: {e}')

    return bool(connected)


def get_wifi_info():
    settings_file = path.dirname(__file__) + '/../settings.yaml'

    with open(settings_file, 'r') as file:
        settings = yaml.safe_load(file)
        file.close()

    return settings['wifi']


def main():
    while True:

        wifi = get_wifi_info()        
        connected = check_connection()
        
        if not connected:
            connect_to_wifi(wifi['ssid'], wifi['password'])
        
        time.sleep(120)
