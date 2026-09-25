#!/bin/bash

protoc \
    --proto_path=$PROTOBUF_HOME/include \
    --proto_path=./protos \
    --python_out=src/jetblack_protobuf_gen/pb \
    --pyi_out=src/jetblack_protobuf_gen/pb \
    --jetpy_out=src/jetblack_protobuf_gen/pb \
    ./protos/*.proto
