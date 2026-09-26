import logging
import sys

try:
    import debugpy
    _HAS_DEBUGPY = False
except ImportError:
    _HAS_DEBUGPY = False

from google.protobuf.compiler import plugin_pb2
from google.protobuf import descriptor_pb2

from .generator import generate_file, generate_dunder_init

LOGGER = logging.getLogger(__name__)


def process_proto_file(
        module_name: str,
        file_descriptor: descriptor_pb2.FileDescriptorProto,
        response: plugin_pb2.CodeGeneratorResponse,
) -> tuple[list[str], list[str]]:
    LOGGER.info("Processing file: %s", file_descriptor.name)

    file = response.file.add()
    file.name = module_name + ".py"
    LOGGER.info("Creating new file: %s", file.name)

    file.content, classes, enums = generate_file(file_descriptor)

    return classes, enums


def process(
        request: plugin_pb2.CodeGeneratorRequest,
        response: plugin_pb2.CodeGeneratorResponse
) -> None:
    exports_by_module: dict[str, list[str]] = {}
    for file_descriptor in request.source_file_descriptors:
        module_name = file_descriptor.name[:-len(".proto")]
        classes, enums = process_proto_file(
            module_name, file_descriptor, response)
        exports_by_module[module_name] = classes + enums

    file = response.file.add()
    file.name = "__init__.py"
    LOGGER.info("Creating new file: %s", file.name)
    file.content = generate_dunder_init(exports_by_module)


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
