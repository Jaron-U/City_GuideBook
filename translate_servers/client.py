import logging

import grpc
import translate_pb2
import translate_pb2_grpc


def run():
    content= input("Input the sentence you want to translate (English <=> Chinese): ")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = translate_pb2_grpc.GreeterStub(channel)
        response = stub.translate(translate_pb2.original_text(original_text1=content))
    print("translated: ", response.translated_text1)


if __name__ == '__main__':
    logging.basicConfig()
    run()
