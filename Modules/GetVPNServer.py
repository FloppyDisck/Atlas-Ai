import os, json, requests

#NOTE: This program only works if you remove SUDO priviledges from openvpn
#Perfect tutorial https://askubuntu.com/questions/159007/how-do-i-run-specific-sudo-commands-without-a-password

class GetVPNServer:
    def __init__(self, ServiceProvider):
        self.ServiceProvider = ServiceProvider

    def getServer(self, location):
        if self.ServiceProvider == 'NordVPN':
            #https://nordvpn.com/api/server
            #get json, every link has a 2 letter header
            request = 'https://nordvpn.com/api/server/stats'
            try:
                nordServers = json.loads(requests.get(request).text)
            except Exception as e:
                print(e)
                return None

            minimum = []
            for server, load in nordServers.items():
                if location == server[:2] and (minimum == [] or (load['percent'] < minimum[1] and minimum[1] > 50)):
                    minimum = [server, load['percent']]
            
            self.server = minimum[0]
            return minimum

    def startVPN(self, user, passwd):
        #Get Username and password and then launch terminal
        #Create text file with user on one line and passwd on the other
        #authPass = get Path to text file

        #Create temp login file
        fileName = 'tempLogin.text'
        directory = os.path.dirname(os.path.abspath(__file__))
        authPass = directory + '/' + fileName
        print(directory)
        loginFile = open(authPass, 'w+')
        loginFile.write(user + '\n')
        loginFile.write(passwd)
        loginFile.close()

        command = 'openvpn --config /etc/openvpn/ovpn_udp/{}.udp.ovpn --auth-user-pass {}'.format(self.server, authPass)
        os.system(command)
        os.remove(authPass)

if __name__ == "__main__":
    nordServer = GetVPNServer('NordVPN')
    server = nordServer.getServer('us')
    print(server)
    nordServer.startVPN('generiEmail@gmail.com', 'passwordBlah')
    #print(os.system('cd /etc/openvpn/ovpn_udp/ && openvpn {}.udp.ovpn'.format(nordServer[0])))
    