class ComponentManager:
    
    component_dict = {}
    step = 0
    current_frame = None

    def __init__(self):
        print("Initializing Component Manager")

    def addComponent(self,name,c):
        self.component_dict[name] = c

    def update(self,frame):
        
        self.current_frame = frame
        for c in self.component_dict.items():
            if c[1].needsUpdate(self.step):
                c[1].update()

        self.step+=1

    def quit(self):
        print("exiting")
        for c in self.component_dict.items():
            c[1].quit()
        exit()
    
            

