"""Tornado TCP echo server/client demo."""

from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer
import functools

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
def run_client(streamS,streamC):
    while True:
        try:
            yield cliEcho(streamS,streamC)
        except StreamClosedError:
            print("server " + " left.")
            streamC.close()
            streamS.close()
            break
        
    
@gen.coroutine
def handle_stream():
    while True:
        ip = '192.168.199.126'
        ip = '45.77.214.165'        
        yield gen.sleep(3)
        streamCli = yield TCPClient().connect(ip, 8889)
        stream = yield TCPClient().connect('192.168.199.126', 5900)
        print 'client ok'
        IOLoop.instance().add_callback(functools.partial(run_client,stream,streamCli))
        IOLoop.instance().add_callback(functools.partial(run_client,streamCli,stream))
    




   
        

if __name__ == "__main__":

    IOLoop.instance().run_sync(handle_stream)
