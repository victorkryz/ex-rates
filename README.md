
# $\color{MidnightBlue}\textit{\textbf{EX-Rates}}$


![Python](https://img.shields.io/badge/Python-v%203.7+-lightblue?logo=python) 
![gRPC](https://img.shields.io/badge/gRPC-v%201.64.1+-blueviolet)

Small Python client/server app that communicates by gRPC protocol and provides currency exchange rates

#### Prerequisites:
- Python 3.7 or higher
- Install gRPC Python scaffold (*grpcio*, *grpcio-tools*) as it described in 
[*gRPC tutorial*](https://grpc.io/docs/languages/python/quickstart).


#### Run app:

-   Run the server:

    ```
     python ex_rates_svc.py
    ```

-   Run the client providing *currency code* like USD, EUR, UAH, GBP, etc. as a command line parameter:

    ```
     python ex_rates_clnt.py USD
    ```
    The client prints the rates of the specified currency against to others


#### Update/generate gRPC code:

For (re)generation of gRPC code integrated into application use *grpc_tools*.    
Run it from the project's root directory:

```
python -m grpc_tools.protoc -I./protos --python_out=gen --pyi_out=gen --grpc_python_out=gen protos/ex-rates.proto
 ```
 The generated code drops into *gen* subfolder