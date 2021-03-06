import argparse
import socket
import sys
from Round import *

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player:
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            # print data
            inp = data.split()
            timeleft = float(inp[-1])

            if timeleft > 5:
                if inp[0] == 'NEWGAME':
                    myName = inp[1]
                    oppAName = inp[2]
                    oppBName = inp[3]
                    

                elif inp[0] == 'NEWHAND':
                    #print inp
                    r = Round(inp, myName, oppAName, oppBName)
                    
                    
                elif inp[0] == 'GETACTION':
                    
                    r.parsePacket(inp)
                    action = r.getBestAction()
                    
                    
                    s.send(action + "\n")
                    #print("Action: " + action)

                elif inp[0] == "REQUESTKEYVALUES":
                    # At the end, the engine will allow your bot save key/value pairs.
                    # Send FINISH to indicate you're done.
                    s.send("FINISH\n")
            else:
                
                if inp[0] == 'NEWGAME':
                    pass
                    

                elif inp[0] == 'NEWHAND':
                    
                    pass
                    
                    
                elif inp[0] == 'GETACTION':
                    counter = 0
                    for test in inp:
                        if test == '0' or test == '1' or test == '2' or test == '3' or test == '4' or test == '5' or test == '6' or test == '7':
                            location = counter
                        counter += 1
                    legalActions = inp[location+1:len(inp)-1]
                    
                    for act in legalActions:
                        a = act.split(':')
                        if a[0] == 'RAISE':
                            action = 'RAISE:' + a[2]
                        elif a[0] == 'BET':
                            action = 'BET:' + a[2]
                        else:
                            action = 'CHECK'
                    
                    
                    s.send(action + "\n")
                    #print("Action: " + action)

                elif inp[0] == "REQUESTKEYVALUES":
                    # At the end, the engine will allow your bot save key/value pairs.
                    # Send FINISH to indicate you're done.
                    s.send("FINISH\n")
            

            
            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!

            
        s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
        #print 'Connected!', args.port
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
