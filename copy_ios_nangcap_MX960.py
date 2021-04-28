import netmiko
from netmiko import ConnectHandler
import json
confirm = "y"

def check_re_master():
   output_re0 = net_connect.send_command("show chassis environment routing-engine 0 | display json")  
   if output_re0[-8::] == "{master}":
        output_re0 = output_re0.rstrip("{master}")
   output_re0_json = json.loads(output_re0)
   #print (output_re0)
   output_re0_json = output_re0_json["environment-component-information"][0]['environment-component-item'][0]['state'][0]['data']
	#
   output_re1 = net_connect.send_command("show chassis environment routing-engine 1 | display json")  
   if output_re1[-8::] == "{master}":
        output_re1 = output_re1.rstrip("{master}")
   output_re1_json = json.loads(output_re1)
   output_re1_json = output_re1_json["environment-component-information"][0]['environment-component-item'][0]['state'][0]['data']
   if (output_re0_json[0:6] == "Online") and (output_re0_json[0:6] == "Online"):
        #print ("Both of 2 cards are online.")
        if output_re0_json[7::] == "Master":
            #print ("RE0 is Master Card")
            master_card = "re0"
        elif output_re1_json[7::] == "Master":
            #print ("RE1 is Master Card")
            master_card = "re1"
   else:
        #print ("Only 1 card online!")
        master_card = "null_1"
   return master_card
	
while True:
    if confirm == "n":
        break
    IP_lo0 = input("Please enter your IP lo0(quit/exit to finish): ")
    if IP_lo0 != "exit" and IP_lo0 != "quit":
    #    
        device_info={
        "device_type":"juniper",
        "host":IP_lo0,
        "username":"tdhuy",
        "password":"muahoado1C",
        }
        net_connect = ConnectHandler(**device_info)
        try:
            print("Connecting to {} ...".format(device_info["host"]))
            net_connect = netmiko.ConnectHandler(**device_info)
        except:
            print ("Fail to connect to: ", IP_lo0)
        else:
            master_card = check_re_master()
            print("Copying from ftp to {} ...".format(master_card))
            output=net_connect.send_command("file copy ftp://backup:backup@222.253.207.242/text.txt /var/tmp/text.txt",expect_string=r"transferring")  
            
            #print (master_card)
            if master_card == "re0":
                print("Copying from RE0 to RE1 ...")
                output=net_connect.send_command("file copy /var/tmp/text.txt re1:/var/tmp/text.txt",expect_string=r">") 
            elif master_card == "re1":
                print("Copying from re1 to re0 ...")
                output=net_connect.send_command("file copy /var/tmp/text.txt re0:/var/tmp/text.txt",expect_string=r">") 				
            print("Copy IOS finish!")
            net_connect.disconnect()          
        confirm = input("Tiếp tục chứ nhỉ? (y/n)")
    #   
    else:
        break
