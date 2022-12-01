# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import imagesend_pb2 as imagesend__pb2


class ImageSendStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Imagerequest = channel.unary_unary(
                '/ImageSend/Imagerequest',
                request_serializer=imagesend__pb2.image_name.SerializeToString,
                response_deserializer=imagesend__pb2.images.FromString,
                )


class ImageSendServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Imagerequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageSendServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Imagerequest': grpc.unary_unary_rpc_method_handler(
                    servicer.Imagerequest,
                    request_deserializer=imagesend__pb2.image_name.FromString,
                    response_serializer=imagesend__pb2.images.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ImageSend', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageSend(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Imagerequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageSend/Imagerequest',
            imagesend__pb2.image_name.SerializeToString,
            imagesend__pb2.images.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)