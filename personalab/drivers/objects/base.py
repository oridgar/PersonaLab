class Vm(object):
    #def __init__(self, base_object):
        #self.base_object = base_object

    def start(self):
        return NotImplemented

    def stop(self):
        return NotImplemented

    def restart(self):
        return NotImplemented

    def reset(self):
        return NotImplemented

    def get_base_object(self):
        return self.base_object