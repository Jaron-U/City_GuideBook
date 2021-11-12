from concurrent import futures
import logging
import urllib.request
import urllib.parse
import json

import grpc
import translate_pb2
import translate_pb2_grpc

class Translate(translate_pb2_grpc.GreeterServicer):
    def translate(self, request, context):
        url = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        data = {}
        data['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['i'] = request.original_text1
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['ue'] = 'UTF-8'
        data['typoResult'] = 'true'
        data = urllib.parse.urlencode(data).encode()

        response = urllib.request.urlopen(url, data)

        html = response.read().decode()
        html = json.loads(html)

        result = html["translateResult"][0][0]["tgt"]
        return translate_pb2.translated_text(translated_text1 = result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translate_pb2_grpc.add_GreeterServicer_to_server(Translate(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()