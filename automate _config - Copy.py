#Mejdoubi oussama

#WHAT DOES THE SCRIPT DO ?
#CONNECT TO A RANGE IF IP ADDRESSES USING SSH and push the config and it does generate a log file at the end where you can verify
#______condition 1 
#checkcking periodically if cpu_load in last 5 seconds is >40%
#______condition 2
#if only one port channel 1 is configured
#______condition 3
#if cpu_load>40% apply config on port_channel

from os import path,startfile
from re import findall, search
from time import sleep
from netmiko import ConnectHandler



config_commands = [
    "device-tracking policy DT_trunk_policy",
    "trusted-port",
    "device-role switch",
    "exit",
    "interface Port-channel1",
    "device-tracking attach-policy DT_trunk_policy",
    "exit"
]

c=0
def main():
    for n in range(103, 116):
        ip = f"10.126.2.{n}"
        print(f"Connecting to {ip}...")

        ###logging input and outputs
        with open("autopush_config.txt","W") as f:
            f.write(f"#########SSHING TO {ip}")

        try:
            conn = ConnectHandler(
            device_type="cisco_ios",
            ip=ip,
            username="username",
            password="your password",
            secret="your password"
            )

            ###logging input and outputs
            with open("autopush_config.txt","W") as f:
                f.write("########EXECUTING\n ENABLE")
            
            conn.enable()  # Go to privileged exec mode

            ###
            while True:
                print(f"CHECKING {ip} :: {c} times")
                output = conn.send_command("show processes cpu | include CPU")

                # Parse CPU utilization for 5 seconds
                match = search(r"CPU utilization for five seconds: (\d+)%", output)

                if match:
                    cpu_load = int(match.group(1))
                    print(f"CPU Load: {cpu_load}%")
                    if cpu_load > 40:
                        print("CPU load is acceptable.")
                        cpu_ok=True
                        ###logging input and outputs
                        with open("autopush_config.txt","W") as f:
                            f.write("#####INFO\t CPU IS OK")
                        break
                    else:
                        print("CPU load is high!")
                else:
                    print("Could not find CPU load info.")

                print("waiting 5 sec")
                sleep(5)
                c+=1


            ###logging input and outputs
            with open("autopush_config.txt","W") as f:
                f.write("########EXECUTING\n show etherchannel summary")
                
            ######checking if only one port channel 1 is configured
            output = conn.send_command("show etherchannel summary")

            ###logging input and outputs
            with open("autopush_config.txt","W") as f:
                f.write(f"####OUTPUT\n {output}")

            ###searching for Po+digit par exemple; Po1 ,Po10
            match = findall(r"Po(\d+)", output)
            if match:
                if len(match)==1:
                    ok=True
                else:
                    ok=False
                    ###logging input and outputs
                    with open("autopush_config.txt","W") as f:
                        f.write(f"there are other port channel groups {match}")
                    print(f"there are other port channel groups {match}")
            else:
                ok=False
                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write(f"there was no Port channel {match}")
                print(f"there was no Port channnel {match}")
            ######

            if all(ok,cpu_ok):
                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write(f"########EXECUTING\n {config_commands}")

                output = conn.send_config_set(config_commands)
                print(f"=== {ip} ===\n{output}\n")

                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write(f"####OUTPUT\n {output}")

                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write(f"########EXECUTING\n write memory")

                save_output = conn.send_command("write memory")
                print(f"Save config output:\n{save_output}\n")

                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write(f"####OUTPUT::\n {output}")
                
                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write("########EXECUTING::\n show running-config interface Port-channel1")

                # Verify config on Port-channel1
                verify_output = conn.send_command("show running-config interface Port-channel1")
                print(f"=== {ip} Port-channel1 Running Config ===\n{verify_output}\n")
                
                ###logging input and outputs
                with open("autopush_config.txt","W") as f:
                    f.write(f"####OUTPUT::\n {verify_output}")
                    
                #####verify if all commands has been pushed successfully
                for cmd in config_commands:
                    if cmd in verify_output:
                        print(f"{ip}: Config is done ✅")
                        ###logging input and outputs
                        with open("autopush_config.txt","W") as f:
                            f.write(f"####config_verify:: all commands has been pushed")
                    else:
                        print(f"{ip}: Config is missing ❌")
                        ###logging input and outputs
                        with open("autopush_config.txt","W") as f:
                            f.write(f"####config_verify:\n {cmd} hasn't been pushed")            
                print("disconnecting .....")
                conn.disconnect()
                print("exited")

        except Exception as e:
            print("connection Exception, check the log file")
            with open("autopush_config.txt","W") as f:
                f.write(f"########connection Exception\n {e}")


abs_path = path.abspath("autopush_config_log.txt")

print(f"DONE\n log file location:\n{abs_path}")

##opening the file
startfile(abs_path)  

if __name__ == "__main__":
    main()