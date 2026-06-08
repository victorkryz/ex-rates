#pragma once

#include <memory>
#include <string>
#include <map>

#include <grpcpp/grpcpp.h>

#include "ex-rates.grpc.pb.h"

namespace currency_rates = currates;

class FxRatesClient
{
public:
    using RatesMap = std::map<std::string, double>;
    static std::unique_ptr<FxRatesClient>& CreateInstance(std::string endpoint = "localhost:50051");
    std::pair<grpc::Status, RatesMap> GetRates(const std::string& key);

private:
    inline static std::unique_ptr<FxRatesClient> classInstance;
    FxRatesClient(std::shared_ptr<grpc::Channel> channel);

private:
    std::unique_ptr<currency_rates::ExRatesSvc::Stub> stub_;
};
