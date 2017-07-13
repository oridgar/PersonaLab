from flask import Flask, render_template
# from flask import Response
from personalab.drivers import conn
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
password = raw_input("enter password: ")
cloud = conn.PersonaLab(password=password)

@app.route('/',methods = ['GET'])
def hello():
    retval = ""
    vm_list = cloud.get_vms()
    #for vm in vm_list:
    #    retval += "server name: %s, type: %s\n" % vm.get_name(),vm.__class__.__name__
    return render_template("hello.html")

if __name__ == '__main__':
    app.run()