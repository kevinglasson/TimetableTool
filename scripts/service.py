import zerorpc
import control


class mainRPC(object):
    def start(self, username, passwword, calendar_name, token):
        # control.main(username, passwword, calendar_name, token)
        return 'Successfully Completed'


s = zerorpc.Server(mainRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()