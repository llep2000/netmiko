#........................................................................
#..                    Academia Cisco Fermin Toro                      ..
#..                       Derechos reservados                          ..
#..                        Developer Llep A.                           ..
#..                            Ver. 0.0.1                              ..
#..                                                                    ..
#........................................................................

#libreria de conexion netmiko
from netmiko import ConnectHandler

#diccionario de parametros de conexion
sw ={
    'device_type': 'cisco_ios',
    'host': 'x.x.x.x',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}

#arreglo de comando para ingresar a una interface
port =[
    'interface fastEthernet 0/',
    'switchport access vlan'
]

#arreglo configuracion basica de seguridad de puertos de acceso
portsecurity =[
    'interface fastEthernet 0/',
    'spanning-tree portfast',
    'spanning-tree bpduguard enable',
    'switchport port-security',
    'switchport port-security maximum 1',
    'switchport port-security violation shutdown',
    'switchport port-security mac-address sticky'
]

#arreglo de comandos protocolo vtp
vtp = [
    'vtp mode server',
    'vtp password cisco',
    'vtp domain cisco'
]


#Variable de opcion para configurar varios swith
OpVariosSw = 'S'

#Bucle para configurar varios swith
while OpVariosSw == 's' or OpVariosSw == 'S':

    #indicacion de ip de swith a configurar 
    equipo = input("coloque la direccion de ip del equipo a configurar ")

    sw['host'] = equipo

    #apertura de conexion ssh con el equipo
    net_connect = ConnectHandler(**sw)
    net_connect.enable()
    net_connect.config_mode()

    #ejecucion arreglo comandos vtp
    net_connect.send_config_set(vtp)

    #ejecucion archivo externo comandos vlan
    net_connect.send_config_from_file(config_file="comandosSw.txt")

    Op = input("Desea confirurar los puertos de acceso? (s/n) ")

    #bucle configuracion puertos
    while Op == 's' or Op == 'S':
        Puerto = input("Coloque numero del puerto ")
        Vlanid = input("Coloque vlan Id del puerto ")

        port[0] = 'interface fastEthernet 0/' + Puerto
        port[1] = 'switchport access vlan ' + Vlanid

        outline = net_connect.send_config_set(vtp)
        print(outline)
        outline = net_connect.send_config_set(port)
        print(outline)

        Op1 = input("Desea aplicar seguridad a este puerto? (s/n)")

        if Op1 == 'S' or Op1 == 's':
            portsecurity[0] = 'interface fastEthernet 0/' + Puerto
            outline = net_connect.send_config_set(portsecurity)
            print(outline)
            
        Op = input("Desea confirurar otro puertos de acceso? (s/n)")

    
    OpVariosSw = input("Desea confirurar otro Swith de acceso? (s/n) ")

    #cierre de conexion ssh
    net_connect.disconnect