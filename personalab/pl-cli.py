#from ansible.module_utils import cloud

import personalab.drivers.conn
import sys
import getpass


def main():
    password = raw_input("enter password: ")
    # password = getpass.getpass('enter password: ')
    cloud = personalab.drivers.conn.PersonaLab(password=password)

    while True:
        command = raw_input("(personalab):> ")

        if command in ["exit", "quit"]:
            break

        command_words = command.split()
        if len(command_words) == 3:
            (action, resource_type, resource_name) = command_words
        elif len(command_words) == 2:
            (action, resource_type) = command_words

        # Validations
        if action not in ["get", "stop", "start", "restart", "reset", "create"]:
            print ("unknown action %s" % action)
            continue
        if resource_type not in ["vm","container"]:
            print ("unknown resource type %s" % resource_type)
            continue


        if resource_type == "container":
            if action == "create":
                if len(resource_name) < 1:
                    print("no name for container")
                else:
                    cloud.create_container(resource_name)

        #Perform actions
        elif resource_type == "vm":
            if action == "get":
                vm_list = cloud.get_vms()
                for vm in vm_list:
                    print ("server name: {}, type: {}".format(vm.get_name(), vm.__class__.__name__))
            else:
                for vm in cloud.get_vms():
                    if vm.get_name() == resource_name:
                        if action == "stop":
                            vm.stop()
                        elif action == "start":
                            vm.start()
                        elif action == "restart":
                            print ("restarting vm %s" % resource_name)
                            vm.restart()
                        elif action == "reset":
                            print ("resetting vm %s" % resource_name)
                            vm.reset()


                            # print (vm.base_object.state())
                            # for curr_attr in dir(vm.base_object):
                            #     print(curr_attr)
                            # curr_dom.destroy()
                            # if vm.get_name() == 'cirros-test':
                            #   vm.start()

    return


if __name__ == '__main__':
    main()
    sys.exit(0)
