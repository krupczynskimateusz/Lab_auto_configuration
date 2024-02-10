# Lab managment
Script for uploading basic startup configuration to devices in the created laboratory like turn on ssh, configure interfaces for connectivity etc. 

Currently supports:
- Server:
  - GNS3 with external connection *add.1.
- Devices:
  - vIOS


Menu:
- [1] Show projects - shows the list of projects stored on the server.
- [2] Set project - set project that will be downloaded on local machine to work with it.
- [3] Download project - projects must be downloaded before script execution.
- [4] Execute - executes the script. Creates device objects, connects via telnet and prints the necessary commands.
- [5] Execute free - executes script without server and telnet connection.
- [6] Exit - exit.
  
Configuration:
- Basic_config:
  - Hostname setting.
  - Setting the domain "lab.home".
  - Adding user "cisco".
- Configure SSH:
  - RSA 2048-bit key generation.
  - Setting vty.
- Set up management interface:
  - Creates vrf mgmt.
  - Sets the last interface in the created vrf and assigns it an address from the pool of management addresses.
  - Adds a default route for management.
- Configure interfaces:
  - Assigns an IP address via the device interface:
    - When connecting Router-a to Router-b, the interfaces will be set as follows:
      IP 10.x.y.z, where x is the   lower number of device a or b, y is the higher number of device a or b, and z is the number of the device for which the configuration is generated.
    - In case of connection to multi-access networks (works only for gns3 switch), the interface will receive the address:
      IP 10.0.x.z, where x is the subnet assigned to the switch, and z is the device for which the configuration is generated.
- Create loopback:
  - Add interface loopback 0 with address 1.1.1.x, where x is device number. 

      
Plans for the future:
- Automate authorization using an RSA key.
- Adding options menu with configuration to choose from.
- OSPF.


Know issue:
- No option to choose what we want to configure.
- After enabling the VIOS device, you need to telnet to it and click Enter. iOS starts in some weird mode with telnet, but you can't enter any characters. I don't yet know how to click the physical "Enter" on a remote connection. If you know how to do it, please let me know :P.
- Probably many issue in validation of config file. Still it is version 0.1.
- Optymalization.


Addnotation:
- add.1: You can generate configurations in the form of Python lists when you specify the path to the gns3 project in the local path option in the config.ini file.
  
