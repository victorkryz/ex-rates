
#include <cstdlib>
#include <iostream>
#include <string>

#include <cxxopts.hpp>

#include "fx_rates.h"

constexpr auto app_name = APP_NAME;
constexpr auto app_version = APP_VERSION;

struct CommandLineOptions
{
    std::string code{"USD"};
    std::string host{"localhost:50051"};
};

CommandLineOptions process_arguments(int argc, char* argv[]);

int main(int argc, char* argv[])
{
    int exit_code = 0;
    const auto arguments = process_arguments(argc, argv);

    {
        auto& client = FxRatesClient::CreateInstance(arguments.host);
        auto result = client->GetRates(arguments.code);
        const auto& [status, rates_map] = result;

        if (status.ok())
        {
            for (const auto& entry : rates_map)
            {
                auto [currency, rate] = entry;
                std::cout << currency << ": " << rate << std::endl;
            }
        }
        else
        {
            std::cerr << "Error: " << status.error_code() << ": " << status.error_message() << std::endl;
            exit_code = 1;
        }
    }

    return exit_code;
}

CommandLineOptions process_arguments(int argc, char* argv[])
{
    cxxopts::Options options(app_name, "Exchange rates client");

    // clang-format off
    options.add_options()("c, code", "Currency code", cxxopts::value<std::string>()->default_value("USD"))
                         ("H, host", "Server endpoint", cxxopts::value<std::string>()->default_value("localhost:50051"))
                         ("h, help", "Show usage");
    // clang-format on

    const auto result = options.parse(argc, argv);

    if (result.count("help") != 0)
    {
        std::cout << options.help() << std::endl;
        std::exit(0);
    }

    return {
        result["code"].as<std::string>(),
        result["host"].as<std::string>()};
}
