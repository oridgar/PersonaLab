from personalab.drivers.objects.base import Vm


class LibVirtVm(Vm):
    """
    :type base_object: libvirt.virDomain
    """

    def __init__(self,domain):
        #self.base_object = libvirt.virDomain()
        self.base_object = domain
        #super(self.__class__, self).__init__(domain)

    def start(self):
        self.base_object.create()

    def stop(self):
        self.base_object.destroy()

    def restart(self):
        self.base_object.reboot()

    def reset(self):
        self.base_object.reset()

    def get_name(self):
        return self.base_object.name()