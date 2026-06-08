cmake_minimum_required(VERSION 3.21)

project(
    ex-rates
    VERSION 1.0.0
    LANGUAGES CXX
)

include(FetchContent)

FetchContent_Declare(
    cxxopts
    GIT_REPOSITORY https://github.com/jarro2783/cxxopts.git
    GIT_TAG v3.2.1
)

FetchContent_GetProperties(cxxopts)
if(NOT cxxopts_POPULATED)
    FetchContent_MakeAvailable(cxxopts)
endif()

set(APP_TARGET ex_rates_clnt)
set(PROTO_TARGET ex_rates_proto)

option(USE_SYSTEM_PROTOBUF "Use Ubuntu/system Protobuf module mode" OFF)

if(USE_SYSTEM_PROTOBUF)
    find_package(Protobuf REQUIRED) # CMake FindProtobuf.cmake
else()
    find_package(Protobuf CONFIG REQUIRED) # ProtobufConfig.cmake from SDK/prefix
endif()

message(STATUS "Protobuf version: ${Protobuf_VERSION}")
message(STATUS "Protobuf protoc: ${Protobuf_PROTOC_EXECUTABLE}")
message(STATUS "gRPC version: ${gRPC_VERSION}")

find_package(gRPC CONFIG REQUIRED)

set(PROTO_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../..//protos")
set(PROTO_FILE "${PROTO_DIR}/ex-rates.proto")
set(GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")

set(PROTO_SRCS "${GENERATED_DIR}/ex-rates.pb.cc")
set(PROTO_HDRS "${GENERATED_DIR}/ex-rates.pb.h")
set(GRPC_SRCS "${GENERATED_DIR}/ex-rates.grpc.pb.cc")
set(GRPC_HDRS "${GENERATED_DIR}/ex-rates.grpc.pb.h")

add_custom_command(
    OUTPUT
    "${PROTO_SRCS}"
    "${PROTO_HDRS}"
    "${GRPC_SRCS}"
    "${GRPC_HDRS}"
    COMMAND protobuf::protoc
    ARGS
    "--proto_path=${PROTO_DIR}"
    "--cpp_out=${GENERATED_DIR}"
    "--grpc_out=${GENERATED_DIR}"
    "--plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>"
    "${PROTO_FILE}"
    DEPENDS
    "${PROTO_FILE}"
    protobuf::protoc
    gRPC::grpc_cpp_plugin
    COMMENT "Generating C++ sources from ${PROTO_FILE}"
    VERBATIM
)

add_library(${PROTO_TARGET}
    "${PROTO_SRCS}"
    "${PROTO_HDRS}"
    "${GRPC_SRCS}"
    "${GRPC_HDRS}"
)

target_include_directories(${PROTO_TARGET}
    PUBLIC
    "${GENERATED_DIR}"
)

target_link_libraries(${PROTO_TARGET}
    PUBLIC
    gRPC::grpc++
    protobuf::libprotobuf
)

add_executable(${APP_TARGET}
    src/fx_rates.cpp
    src/main.cpp
)

target_compile_features(${APP_TARGET}
    PRIVATE
    cxx_std_17
)

target_compile_definitions(${APP_TARGET}
    PRIVATE
    APP_NAME="${APP_TARGET}"
    APP_VERSION="${PROJECT_VERSION}"
)

target_include_directories(${APP_TARGET}
    PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_link_libraries(${APP_TARGET}
    PRIVATE
    cxxopts::cxxopts
    ${PROTO_TARGET}
)

include(GNUInstallDirs)

install(TARGETS ${APP_TARGET}
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
)
