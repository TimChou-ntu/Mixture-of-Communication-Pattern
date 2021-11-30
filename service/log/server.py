import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse
import threading

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt


history = []

mqttip = "127.0.0.1"
mqttport = 1883

class LogHistoryServicer(log_pb2_grpc.LogHistoryServicer):

    def __init__(self):
        pass

    def getHistory(self, request, context):
        print("get request")
        print(history)
        response = log_pb2.LogResponse()
        for h in history:
            x = h.split('_')
            print(x)
            x0 = x[0][1:]
            x1 = x[1][:-1]
            print(x0,x1)
            response.value.append(int(x0))
            response.value.append(int(x1))

        return response

def on_message(client, obj, msg):
    print("ON message")
    print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
    history.append(msg.payload.decode('utf-8'))


class Subscriber():

    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.client.on_message = on_message
        self.client.connect(host=mqttip, port=mqttport)
        self.client.subscribe('log', 0)
        
    def run(self):
        print(f"subscribe to host {mqttip}:{mqttport}")
        try:
            self.client.loop_forever()
        except KeyboardInterrupt as e:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8888, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogHistoryServicer()
    sub = Subscriber()
    log_pb2_grpc.add_LogHistoryServicer_to_server(servicer, server)
    t = threading.Thread(target=sub.run)
    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        t.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
