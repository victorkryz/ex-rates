#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>

#include "fx_rates.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

using namespace currency_rates;

const std::string_view auth_token{"ex_rate_token"};

FxRatesClient::FxRatesClient(std::shared_ptr<Channel> channel)
    : stub_(ExRatesSvc::NewStub(channel)) {}

std::pair<grpc::Status, FxRatesClient::RatesMap> FxRatesClient::GetRates(const std::string& key)
{
    Request request;
    request.set_currency_code(key);

    ClientContext context;
    context.AddMetadata("authorization", "Bearer " + std::string(auth_token));

    Rates response;
    Status status = stub_->GetRates(&context, request, &response);

    std::pair<grpc::Status, RatesMap> result;
    auto& [result_status, rates_map] = result;

    if (status.ok())
    {
        const ::google::protobuf::RepeatedPtrField<::currency_rates::Rates_Rate>&
            vals = response.entries();

        auto it = vals.begin();
        while (it != vals.end())
        {
            const ::currency_rates::Rates_Rate& item = *(it++);
            rates_map.insert(std::make_pair<std::string, double>(item.currency().c_str(), item.value()));
        }
    }
    else
    {
        result_status = status;
    }

    return result;
}

std::unique_ptr<FxRatesClient>& FxRatesClient::CreateInstance(std::string endpoint)
{
    if (!classInstance)
    {
        classInstance.reset(new FxRatesClient(
            grpc::CreateChannel(endpoint, grpc::InsecureChannelCredentials())));
    }
    return classInstance;
}
