import numpy as np
from ComponentManager import *
from UIRenderer import *
from EEGReceiver import *

if __name__ == "__main__":
    manager = ComponentManager()
    manager.addComponent("UIRenderer", UIRenderer(manager))
    manager.addComponent("EEGReceiver",EEGReceiver(manager))
    frame = np.zeros((640,480,3))
    while True:
        try:
            manager.update(frame)
        except KeyboardInterrupt:
            manager.quit()
            
   