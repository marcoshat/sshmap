import random
import socket
import struct
import threading
import subprocess
import sys
import os

class Coloring:

    reset = ""
    red = ""
    green = ""
    yellow = ""
    blue = ""
    magenta = ""
    cyan = ""
    white = ""

    machineOs = str(sys.platform).lower()


    # def getServerStatus(self, serverAddress):
    #     machineOs = self.machineOs
    #     if "linux" in machineOs or "ox x" in machineOs:
    #         result = subprocess.run([f"ping -c 1 {serverAddress}"], stdout=subprocess.PIPE, shell=True)
    #         if "0% packet loss" in str(result.stdout):
    #             return True
    #         else:
    #             return False
    #     elif "win32" in machineOs or "windows" in machineOs:
    #         result = subprocess.run([f"ping /n 1 {serverAddress}"], stdout=subprocess.PIPE, shell=True)
    #         if "0% packet loss" in str(result.stdout):
    #             return True
    #         else:
    #             return False

    if 'linux' in str(sys.platform).lower() or 'os x' in str(sys.platform).lower():
        reset = "\u001b[0m"
        red = "\u001b[31m"
        green = "\u001b[32m"
        yellow = "\u001b[33m"
        blue = "\u001b[34m"
        magenta = "\u001b[35m"
        cyan = "\u001b[36m"
        white = "\u001b[37m"
    else:
        print("This program runs on linux systems!! SSH timeout requires a linux shell!")
        exit(1)

class Cracker:

    timeoutSECONDS = 8
    responsiveIPs = []
    failedAttempts = 0
    stopscanner = False
    scanlogFile = "scan.log"
    userlist = ["root"]
    
    scannerport = 22

    def logo(self):
        c = Coloring()
        logo = c.cyan+"""
            ███████╗███████╗██╗  ██╗███╗   ███╗ █████╗ ██████╗ 
            ██╔════╝██╔════╝██║  ██║████╗ ████║██╔══██╗██╔══██╗
            ███████╗███████╗███████║██╔████╔██║███████║██████╔╝
            ╚════██║╚════██║██╔══██║██║╚██╔╝██║██╔══██║██╔═══╝ 
            ███████║███████║██║  ██║██║ ╚═╝ ██║██║  ██║██║     
            ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝   
        """+c.reset

        return logo


    def execute(self, command):
        result = subprocess.run([command], stdout=subprocess.PIPE, shell=True)
        return result.stdout

    def randomIP(self):
        return str(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    def tryssh(self, timeout, user, server, port=0):
        if port == 0:
            result = self.execute(f'timeout {timeout}s ssh {user}@{server}')
        else:
            result = self.execute(f'timeout {timeout}s ssh {user}@{server} -p {port}')
        if len(result) == 0:
            return False
        else:
            print(result)
            return True


    def sshscanner(self, userlist, port=0):
        while True:
            global stopscanner
            address = self.randomIP()

            for user in userlist:
                didRespond = self.tryssh(self.timeoutSECONDS, "root", address, self.scannerport)

                if not didRespond:
                    # print(f" {address} did not respond [PORT: 22]")
                    self.failedAttempts+=1
                else:
                    # print(f"\n {address} is responsive! [PORT: 22]")
                    self.responsiveIPs.append(address)
                if self.stopscanner:
                    print(" Stopped scanner.")
                    print(" Scanner Stopped.")
                    print(f" Found {len(self.responsiveIPs)} Responsive Servers.")
                    print(f" Failed {self.failedAttempts} times.")
                    print(f"Log: {self.scanlogFile}")
                    break

    def process(self):
        c = Coloring()
        print(self.logo())
        
        scanner = threading.Thread(target=self.sshscanner, args=(self.userlist,))
        while True:
            command = input(f"{c.cyan}Console{c.reset}:: ")
            parts = command.split(" ")
            if parts[0] == "scanner":
                try:
                    if parts[1] == "start":
                        self.stopscanner = False
                        scanner.daemon = True
                        scanner.start()
                        print(" [!] Scanner Thread Started.")
                    elif parts[1] == "stop":
                        # print(" Stopping scanner.")
                        self.stopscanner == True
                        scanner.do_run = False
                        # scanner.join()
                    elif parts[1] == "status":
                        print(f" Found {len(self.responsiveIPs)} Responsive Servers.")
                        print(f" Failed {self.failedAttempts} times.")
                        print(" Continuing...")
                    elif parts[1] == "timeout":
                        try:
                            test = int(parts[2])
                            self.timeoutSECONDS = test
                            print(f" Changed SSH timeout to: {self.timeoutSECONDS}.")
                        except:
                            print(" Timeout must be a interger in seconds.")
                    elif parts[1] == "port":
                        try:
                            test = int(parts[2])
                            self.scannerport = test
                            print(f" Changed Scanner port to: {self.scannerport}.")
                        except:
                            print(" Port must be an interger.")
                    elif parts[1] == "adduser":
                        self.userlist.append(parts[2])
                        print(f" Will now also check login for {parts[2]} as well as: ")
                        for user in self.userlist:
                            print(f"  {user}")
                    elif parts[1] == "rmuser":
                        for user in self.userlist:
                            if user == parts[2]:
                                index = self.userlist.index(parts[2])
                                self.userlist.pop(index)
                                print(f" Removed {parts[2]}")
                                print(" Users in List:")
                                for user in self.userlist:
                                    print(f"  {user}")
                    elif parts[1] == "log":
                        if os.path.isdir(parts[2]):
                            print(" Already exists. Overwrite (o) or append? (a):", end="")
                            res = input("")
                            if res.lower() == "o":
                                print(" Overwriting...")
                                f = open(parts[2], "w")
                                f.write("")
                                f.close()
                                self.scanlogFile = parts[2]
                                print(f" Changed Log File to: {self.scanlogFile}.")
                            elif res.lower() == "a":
                                self.scanlogFile = parts[2]
                                print(f" Changed Log File to: {self.scanlogFile}.")


                except:
                    print(" Scanner Syntax:")
                    print(" scanner start/stop/status")
                    print(" scanner timeout <interger_in_seconds>")
                    print(" Scanner port <new_op_port>")
                    print(" scanner adduser/rmuser <user_to_add>")
                    print(" scanner log <new_log_file>")
