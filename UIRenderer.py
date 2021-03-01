import cv2 

class UIRenderer:

    manager = None
    key = None
    
    frames_per_update = 1

    
    def __init__(self, manager):
        print("Starting Renderer")
        self.manager = manager
        cv2.namedWindow("frame")
    

    def needsUpdate(self,steps):
        return True

    def quit(self):
        return 

    
    def update(self):

        frame = self.manager.current_frame
        
        self.key = cv2.waitKey(1)
        
        cv2.imshow("frame",frame)

        return 


