#!/bin/bash

protoc \
    --proto_path=$PROTOBUF_HOME/include \
    --proto_path=./protos \
    --python_out=src/protobuf_ex1/pb \
    --pyi_out=src/protobuf_ex1/pb \
    --jetpy_out=src/protobuf_ex1/pb \
    ./protos/*.proto
