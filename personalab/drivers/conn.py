import os_client_config
import libvirt
#from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import personalab.drivers.objects.container
import personalab.drivers.objects.libvirt
import personalab.drivers.objects.openstack
import logging
from personalab.utils import utils



Base = declarative_base()

class Cloud(Base):
    __tablename__ = 'cloud'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    type = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    username = Column(String(250), nullable=True)
    project_name = Column(String(250), nullable=True)
    region_name = Column(String(250), nullable=True)

#person_id = Column(Integer, ForeignKey('person.id'))
#person = relationship(Person)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.


class PersonaLab(object):
    def __init__(self, password, api_version='3.0'):

        #DB
        logger = logging.getLogger('PersonaLab')
        logger.info('Connecting to sqlite database')
        db = create_engine('sqlite:///db/sqlalchemy_example.db')
        Base.metadata.create_all(db)
        DBSession = sessionmaker(bind=db)
        self.session = DBSession()
        #Import clouds if there are no clouds
        if self.session.query(Cloud).all() == []:
            cloud_configs = utils.get_config("config/personalab.conf")
            local_cloud = Cloud(name='localhost',type='libvirt',url='qemu:///system')
            
            remote_cloud = Cloud(
                name = cloud_configs.get('public-cloud', 'name'),
                type = cloud_configs.get('public-cloud', 'type'),
                url = cloud_configs.get('public-cloud', 'url'),
                username = cloud_configs.get('public-cloud', 'username'),
                project_name = cloud_configs.get('public-cloud', 'project_name'),
                region_name=cloud_configs.get('public-cloud', 'region_name')
            )
            local_container = Cloud(name='local-docker',type='docker',url='unix://var/run/docker.sock')
            self.session.add(local_cloud)
            #self.session.commit()
            self.session.add(remote_cloud)
            #self.session.commit()
            self.session.add(local_container)
            self.session.commit()


        for cloud in self.get_clouds():
            if (cloud.type == 'openstack'):
                # self.op_connection = os_client_config.make_client(
                #     'compute',
                #     version=api_version,
                #     #auth_url='https://%s:13000' % server,
                #     auth_url='%s:13000' % cloud.url,
                #     username=username,
                #     password=password,
                #     project_name=project_name,
                #     region_name=region_name)
                self.op_connection = os_client_config.make_client(
                    'compute',
                    version=api_version,
                    auth_url='%s:13000' % cloud.url,
                    username=cloud.username,
                    password=password,
                    project_name=cloud.project_name,
                    region_name=cloud.region_name)
            elif (cloud.type == 'libvirt'):
                # self.libvirt_conn = libvirt.open("qemu:///system")
                # if self.libvirt_conn is None:
                #     print 'Failed to open connection to the hypervisor'
                self.libvirt_conn = libvirt.open(cloud.url)
                if self.libvirt_conn is None:
                    print 'Failed to open connection to the hypervisor'
            elif (cloud.type == 'docker'):
                self.docker_conn = personalab.drivers.objects.container.Host(cloud.url)

    #Getters

    def get_clouds(self):
        return self.session.query(Cloud).all()

    def get_vms(self):
        a = []
        for server in self.op_connection.servers.list():
            a.append(personalab.drivers.objects.openstack.OpenStackVm(server))

        try:
            dom_list = self.libvirt_conn.listAllDomains()
        except:
            print 'Failed to find domains'

        # print "Domain 0: id %d running %s" % (dom0.ID(), dom0.OSType())
        for curr_dom in dom_list:
            a.append(personalab.drivers.objects.libvirt.LibVirtVm(curr_dom))

        for curr_container in self.docker_conn.get_containers():
            a.append(curr_container)

        return a

    #Creation

    def create_container(self,name):
        self.docker_conn.create_container(name)

    def close(self):
        self.libvirt_conn.close()
        
    def add_os_cloud(self,name, cloud_type, url, username, project_name, region_name):
        new_cloud = Cloud(name=name, type=cloud_type, url=url,
                             username=username, project_name=project_name, region_name=region_name)
        self.session.add(new_cloud)
        self.session.commit()