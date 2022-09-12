from netmiko import ConnectHandler
R1 ={
    'device_type': 'cisco_ios',
    'host': 'x.x.x.x',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}

commands = ['crypto isakmp key XXX address X.X.X.X',
            'interface Tunnel',
            'ip address X.X.X.X X.X.X.X',
            'tunnel source X.X.X.X',
            'tunnel destination X.X.X.X',
            'tunnel mode ipsec ipv4',
            'tunnel protection ipsec profile IPSEC_PROFILE_LLEP',
            'shutdown',
            'no shutdown',
            'exit']

R2 = R1.copy()
commands1 = commands.copy()

numero_tunnel = '1'

#Definifion origen destino del tunnel
print("---------------------------Definifion origen destino del tunnel---------------------------")
equipo_origen = input("coloque la direccion de ip de equipo origen del tunel :")
equipo_destino = input("coloque la direccion de ip de equipo destino del tunel :")

#Definicion clave interna del tunnel
print("---------------------------Definicion clave interna del tunnell---------------------------")
ip_origen = input("coloque la direccion de ip de origen del tunel :")
ip_destino = input("coloque la direccion de ip de destino del tunel :")

clave_tunnel = input("coloque la clave simetrica del tunnel :")
commands [0] = 'crypto isakmp key ' + clave_tunnel + ' address ' + ip_destino
commands1 [0] = 'crypto isakmp key ' + clave_tunnel + ' address ' + ip_origen


#---------------------Definicion ip interna del tunnel------------------------------------
commands [1] = 'interface Tunnel' + numero_tunnel
commands [2] = 'ip address 192.168.' + numero_tunnel + '.1 255.255.255.252'
commands [3] = 'tunnel source ' + ip_origen
commands [4] = 'tunnel destination ' + ip_destino


commands1 [1] = 'interface Tunnel' + numero_tunnel
commands1 [2] = 'ip address 192.168.' + numero_tunnel + '.2 255.255.255.252'
commands1 [3] = 'tunnel source ' + ip_destino
commands1 [4] = 'tunnel destination ' + ip_origen


#----------------------Definicion de conexion ssh a equipos----------------------------
R1['host'] = equipo_origen
R2['host'] = equipo_destino

print("------------------------------------------------------------------------")
net_connect = ConnectHandler(**R1)
net_connect.enable()
net_connect.config_mode()

net_connect.send_config_from_file(config_file="comandos.txt")
net_connect.config_mode()
outline = net_connect.send_config_set(commands)
print(outline)

net_connect.disconnect

print("------------------------------------------------------------------------")
net_connect = ConnectHandler(**R2)
net_connect.enable()
net_connect.config_mode()

net_connect.send_config_from_file(config_file="comandos.txt")
net_connect.config_mode()
outline = net_connect.send_config_set(commands1)
print(outline)

net_connect.disconnect
