
from __future__ import print_function
import sys

import logging
import argparse

import grpc

sys.path.append('gen');
from gen import ex_rates_pb2
from gen import ex_rates_pb2_grpc

_AUTH_TOKEN = "ex_rate_token"
_AUTH_METADATA = (("authorization", f"Bearer {_AUTH_TOKEN}"),)

def run(code: str, service_host: str = "localhost"):
    with grpc.insecure_channel(f"{service_host}") as channel:
        stub = ex_rates_pb2_grpc.ExRatesSvcStub(channel)
        print(f"Connected to {service_host}")     
        print(f"Requesting for {code} ...")
        response = stub.GetRates(
            ex_rates_pb2.Request(currency_code=code),
            metadata=_AUTH_METADATA,
        )
        if len(response.entries) != 0:
            print(code, "rates received:")
            for item in sorted(response.entries, key=lambda entry: entry.currency):
                print(item.currency + ":",  item.value)     
        else:
            print("There are no rates for", code)     
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sends request to gRPC server for getting currency rate')
    parser.add_argument('--code', type=str, help='Specify currency code (i.g USD, EUR, UAH, ...)')
    parser.add_argument('--host', type=str, default="localhost:50051", help='Specify "ex-rates" service host)')
    args = parser.parse_args()

    if ( args.code ):
        logging.basicConfig()
        run(args.code, args.host)
    else:
        print("Insufficient parameters!")
