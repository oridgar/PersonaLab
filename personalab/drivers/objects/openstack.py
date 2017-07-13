from personalab.drivers.objects.base import Vm


class OpenStackVm(Vm):
    """
    :type base_object: novaclient.v2.servers.Server
    """

    def __init__(self,server):
        #super(self.__class__, self).__init__(server)
        self.base_object = server

    def start(self):
        self.base_object.start()

    def stop(self):
        self.base_object.stop()

    def restart(self):
        self.base_object.reboot()

    def reset(self):
        self.base_object.reboot(reboot_type='hard')

    def get_name(self):
        return self.base_object.name


