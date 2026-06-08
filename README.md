
# $\color{MidnightBlue}\textit{\textbf{EX-Rates}}$


![Python](https://img.shields.io/badge/Python-v%203.7+-lightblue?logo=python) 
![gRPC](https://img.shields.io/badge/gRPC-v%201.64.1+-blueviolet)
![C++](https://img.shields.io/badge/C++-17-purple?logo=C++)
![cmake](https://img.shields.io/badge/cmake-3.30-brightgreen)


Ex-Rates is a gRPC-based currency exchange rate service.

The exchange rates are obtained from external exchange-rate providers and returned to clients through a gRPC API.


## Features
- [gRPC server implemented in Python](server)
- [Protobuf data definition](protos)
- JSON exchange-rate provider integration
- Multi-client project structure:
    - [Python client](client/py)
    - [C++ client](client/cpp) 
- [GitHub Actions CI pipeline](.github/workflows)

#### Prerequisites:
- Python 3.7 or higher
- Install Requests library (pip install requests)
- Install google protobuf (pip install protobuf)
- Install gRPC Python scaffold (*grpcio*, *grpcio-tools*) as it described in 
[*gRPC tutorial*](https://grpc.io/docs/languages/python/quickstart).


#### Run app:

-   Run the server:

    ```
     python ex_rates_svc.py
    ```
    Service listens port 50051

-   Run the client providing *currency code* like USD, EUR, UAH, GBP, etc. as a command line parameter,
    and optionally ip address of host where ex_rates_svc.py is launched (by default: localhost:50051)

    ```
     python ex_rates_clnt.py --code USD
     python ex_rates_clnt.py --code EUR --host ex-rates-service-ip:port
    ```
    The client prints the rates of the specified currency against to others


#### Update/generate gRPC code:

For (re)generation of gRPC code integrated into application use *grpc_tools*.    
Run it from the project's root directory:

```
python -m grpc_tools.protoc -I./protos --python_out=gen --pyi_out=gen --grpc_python_out=gen protos/ex-rates.proto
 ```
 The generated code drops into *gen* subfolder


## Building and Continuous Integration

The project uses GitHub Actions to:

- Run and test the Python client [Python Client GitHub Actions workflow](.github/workflows/linux-workflow-py-client.yml)
- Build, run and test the C++ client [C++ Client GitHub Actions workflow](.github/workflows/linux-workflow-cpp-client.yml)

