"""
Try to connect to Simulink and send data to it through TCP/IP Connection. 
If the connection is successful, launch the Simulink model.
"""
import socket
import matlab.engine as m

TCP_IP = 'localhost'
TCP_PORT = 30001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
print('Waiting for Simulink to start')
s.listen(1)
conn, addr = s.accept()
print('Connection address: ', addr)


def launchSimulink():
    """
    Launch the Simulink model.
    """
    eng = m.start_matlab()
    eng.sim('Car.slx')
    pass

if __name__ == '__main__':
    launchSimulink()