import cv2 
import socket


class EEGReceiver:

    manager = None
    key = None
    
    frames_per_update = 1
    s = None
    hand_UI = False

    fresh_data = False
    
    def __init__(self, manager):
        print("Starting EEGReceiver")
        HOST=''
        PORT=8089

        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print ('Socket created')
        self.s.bind((HOST,PORT))
        print ('Socket bind complete')
        self.s.listen(10)
        print ('Socket now listening')
        conn,addr=self.s.accept()

        
        
        self.manager = manager
       
    

    def needsUpdate(self,steps):
        return self.fresh_data

    def quit(self):
        self.s.close()
        return 

    def _threaded_update(self):
        self.fresh_data = False
        print("here")
        #received = self.s.recv(4096)
        BUFF_SIZE   =4096
        data = b''
        while True:
            part = self.s.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        data_dict = json.loads(data)
        #received = received.decode("utf-8")
        print(data_dict)

        self.fresh_data = True
    
    def update(self):

        p = threading.Thread(target =self._threaded_update)
        p.start()
        

        return 


