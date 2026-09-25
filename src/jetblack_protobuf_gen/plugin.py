import logging
import sys

try:
    import debugpy
    _HAS_DEBUGPY = False
except ImportError:
    _HAS_DEBUGPY = False

from google.protobuf.compiler import plugin_pb2
from google.protobuf import descriptor_pb2

from .generator import generate_file

LOGGER = logging.getLogger(__name__)


def process_proto_file(
        file_descriptor: descriptor_pb2.FileDescriptorProto,
        response: plugin_pb2.CodeGeneratorResponse,
) -> None:
    LOGGER.info("Processing file: %s", file_descriptor.name)

    file = response.file.add()
    file.name = file_descriptor.name[:-len(".proto")] + ".py"
    LOGGER.info("Creating new file: %s", file.name)

    file.content = generate_file(file_descriptor)


def process(
        request: plugin_pb2.CodeGeneratorRequest,
        response: plugin_pb2.CodeGeneratorResponse
) -> None:
    for proto_file in request.source_file_descriptors:
        process_proto_file(proto_file, response)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)ss - %(message)s"
    )

    # Wait for the debugger to attach
    if _HAS_DEBUGPY:
        debugpy.listen(5678)
        LOGGER.info("Wait for debugger to attach")
        debugpy.wait_for_client()

    request = plugin_pb2.CodeGeneratorRequest.FromString(
        sys.stdin.buffer.read())

    response = plugin_pb2.CodeGeneratorResponse()

    process(request, response)

    sys.stdout.buffer.write(response.SerializeToString())


if __name__ == "__main__":
    main()
