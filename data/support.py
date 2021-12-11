import random
import socket
import struct
import threading
import subprocess
import sys

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

    def tryssh(self, timeout, user, server):
        result = self.execute(f'timeout {timeout}s ssh {user}@{server}')
        if len(result) == 0:
            return False
        else:
            print(result)
            return True


    def sshscanner(self):
        while True:
            address = self.randomIP()
            didRespond = self.tryssh(self.timeoutSECONDS, "root", address)

            if not didRespond:

    # def commands(self):
    #     commandThread = threading.Thread(target=self.process())
    #     commandThread.join()
    #     commandThread.start()

                # print(f" {address} did not respond [PORT: 22]")
                self.failedAttempts+=1
            else:
                # print(f"\n {address} is responsive! [PORT: 22]")
                self.responsiveIPs.append(address)
            if self.stopscanner == True:
                break
            
        print(" Scanner Stopped.")
        print(f" Found {len(self.responsiveIPs)} Responsive Servers.")
        print(f" Failed {self.failedAttempts} times.")
        print(f"Log: {self.scanlogFile}")

    
    def process(self):
        c = Coloring()
        print(self.logo())
        while True:
            command = input(f"{c.cyan}Console{c.reset}:: ")
            parts = command.split(" ")
            if parts[0] == "scanner":
                try:
                    if parts[1] == "start":
                        scanner = threading.Thread(target=self.sshscanner)
                        scanner.daemon = True
                        scanner.start()
                        print(" [!] Scanner Thread Started.")
                    elif parts[1] == "stop":
                        self.stopscanner == True
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
                except:
                    print(" Scanner Syntax:")
                    print(" scanner start/stop/status")
                    print(" scanner timeout <interger_in_seconds>")
