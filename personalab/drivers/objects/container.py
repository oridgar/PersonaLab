from docker import client
from personalab.drivers.objects.base import Vm

class Host(object):
    """
    :type cli: docker.client.Client
    """

    def __init__(self,url='unix://var/run/docker.sock'):
        self.cli = client.Client(base_url=url)

    def get_containers(self):
        container_list = []
        for container in self.cli.containers(all=True):
            container_list.append(Container(container, self.cli))
        return container_list

    def create_container(self, name, image='centos'):
        self.cli.create_container(image,name=name)


class Container(Vm):
    """
    :type docker_client: docker.client.Client
    """
    def __init__(self,base_object,docker_client):
        self.base_object = base_object
        self.docker_client = docker_client

    def start(self):
        self.docker_client.start(self.get_id())

    def stop(self):
        self.docker_client.stop(self.get_id())

    def restart(self):
        self.docker_client.restart(self.get_id())

    def get_name(self):
        return str(self.base_object['Names'][0]).replace('/','')

    def get_id(self):
        return str(self.base_object['Id'])

class Image(object):
    pass