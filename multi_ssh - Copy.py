#MEJDOUBI oussama
#MULTI & single SSH using putty
##semi-auto config push - with intercative CLI

import subprocess


multi=False


inp = input("enter net address + range \tEX 10.10.10.101-200  OR 10.10.10.101\n:")
base_addr  = ".".join(inp.split(".")[0:3]) # get first 3 bytes of IPV4

if "-" in inp:
    multi=True
    start,end= inp.split(".")[-1].split("-")


###cisco 9600 config
""""
en
your enable password
conf t
device-tracking policy DT_trunk_policy
trusted-port
device-role switch
!
interface Po 1
device-tracking attach-policy DT_trunk_policy
!
do show running int po 1

exit
exit
exit
!
"""

username = "itadmin"   # <-- change this


if multi:
    for i in range(int(start),int(end)+1):
        ip = f"{base_addr}.{i}"
        print(f"wanna ssh to {ip} ?")
        inp = input("yes or no (y/n):\nquit (q):")

        if inp=="yes" or inp=="y" or inp=="Y":
            cmd = ["putty.exe", "-ssh", f"{username}@{ip}","-pw", "your password"]
            cmd = subprocess.Popen(cmd)
        if inp=="quit" or "q":
            break
        else:
            pass
else:
    print(f"wanna ssh to {inp} ?")
    inp = input("yes or no | y/n:")
    if inp=="yes" or inp=="y" or inp=="Y":
        cmd = ["putty.exe", "-ssh", f"{username}@{inp}","-pw", "you password"]
        cmd = subprocess.Popen(cmd)