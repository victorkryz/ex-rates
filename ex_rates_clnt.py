
from __future__ import print_function
import sys

import logging
import argparse

import grpc

sys.path.append('gen');
from gen import ex_rates_pb2
from gen import ex_rates_pb2_grpc

def run(code: str):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ex_rates_pb2_grpc.ExRatesSvcStub(channel)
        response = stub.GetRates(ex_rates_pb2.Request(currency_code=code))
        if len(response.entries) != 0:
            print(code, "rates received:")
            for item in response.entries:
                print(item.currency + ":",  item.value)     
        else:
            print("There are no rates for", code)     
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sends request to gRPC server for getting currency rate')
    parser.add_argument('code', type=str, help='Specify currency code (i.g USD, EUR, UAH, ...)')
    args = parser.parse_args()

    if ( args.code ):
        print("Requesting for", args.code, "...")
        logging.basicConfig()
        run(args.code)
    else:
        print("Insufficient parameters!")
