import netmiko

f = open("ip_ASR_nangcap.txt","r")
data_host = f.read()
data_host = data_host.strip()
data_host_lst = data_host.split(",")
f.close()

for IP_lo0 in data_host_lst:
    device_info = {
        "host": IP_lo0,
        "port": 22,
        "username": "tdhuy",
        "password": "muahoado1C",
        "device_type": "cisco_ios"
        }
    try:
        print("Connecting to {}...".format(device_info["host"]))
        conn = netmiko.ConnectHandler(**device_info)
    except:
	    print ("Fail to connect to: ", IP_lo0)
    else:
        check_exist = conn.send_command(f"dir disk0:/ | inc ASR9K-iosxr-px-k9-6.5.3.tar",use_textfsm=True)
        #print (check_exist.find("ASR9K-iosxr-px-k9-6.5.3.tar"))
        if (check_exist.find("ASR9K-iosxr-px-k9-6.5.3.tar")) != (-1):
        #if check_exist[0]["name"] == "ASR9K-iosxr-px-k9-6.5.3.tar":
            print ("IOS has been copied already!")
        else:
            print ("Copying, please wait ...")	        
            output=conn.send_command_timing("copy ftp://backup:backup@222.253.207.242/ASR9K-iosxr-px-k9-6.5.3.tar disk0:/ASR9K-iosxr-px-k9-6.5.3.tar")
            if "Destination" in output:
                output += conn.send_command_timing("\n")
            conn.send_command("\n",expect_string=r"#")
            #check MD5
            print ("Checking MD5 ...")
            command = f"show md5 file /disk0:/ASR9K-iosxr-px-k9-6.5.3.tar"
            try:
                #print (conn.find_prompt())
                md5 =conn.send_command (command,use_textfsm=True)
                x = md5.find("f8851a6ec81b8f99b8609e487dc4f959")
                if md5[x::] == "f8851a6ec81b8f99b8609e487dc4f959":
                    print ("MD5 checking is OK.")
                else:
                    print ("Something is wrong, please check!")
            except:
                print ("Something is wrong in {}, please check!".format(device_info["host"]))
        conn.disconnect()		
        print("Done!")
print ("Finish!")

