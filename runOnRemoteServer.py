"""Tornado TCP echo server/client demo."""

from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer
import functools
import uuid

needConn = False
connOk = False
tempConn = None
connMap = {}

@gen.coroutine
def cliEcho(streamS,streamC):
    while True:
        d1 = yield streamC.read_bytes(1)
        if len(d1)!=0:
            break
    
    data =  streamC._read_buffer
    l = len(data)
    d2 = yield streamC.read_bytes(l-1)
    yield streamS.write(d1+d2)
    
@gen.coroutine
def run_client(streamS,streamC,k):
    while True:
        try:
            yield cliEcho(streamS,streamC)
        except StreamClosedError:
            print("server " + " left.")
            global connMap
            connMap[k] = False
            break


   
    
class EchoServer(TCPServer):
    clients = set()    
    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, fileno = address
        print("Incoming connection from " + ip)
        EchoServer.clients.add(address)
        global needConn,connOk,tempConn
        needConn = True
        while not connOk:
            yield gen.sleep(0.5)
        k,streamCli = tempConn
        tempConn = None
        connOk = False        
        print 'client ok'
        IOLoop.instance().add_callback(functools.partial(run_client,stream,streamCli,k))
        while True:
            try:
                yield self.echo(stream,streamCli)
            except StreamClosedError:
                print("Client " + str(address) + " left.")
                EchoServer.clients.remove(address)
                global connMap
                connMap[k] = False
                break

    @gen.coroutine
    def echo(self, stream,streamCli):
        while True:
            d1 = yield stream.read_bytes(1)
            if len(d1)!=0:
                break
        data =  stream._read_buffer
        l = len(data)
        d2 = yield stream.read_bytes(l-1)
        yield streamCli.write(d1+d2)
        
class EchoServerC(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        global needConn,connOk,tempConn,connMap    
        ip, fileno = address
        print("Incoming connection from " + ip)
        if not needConn:
            stream.close()
            return
        k = str(uuid.uuid1())
        connMap[k] = True
        tempConn = k,stream
        connOk = True
        needConn = False
        while connMap[k]:
            yield gen.sleep(1)
        del connMap[k]
        stream.close()
       
  
def start_server():
    serverForHome = EchoServer()  
    serverForCompany = EchoServerC()  
    ip = '192.168.199.126'
    ip = '45.77.214.165'
    serverForHome.listen(8888,ip)
    serverForCompany.listen(8889,ip)
  

   
        

if __name__ == "__main__":

    start_server()
    IOLoop.instance().start()
