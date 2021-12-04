from concurrent import futures
import logging

import grpc
import imagesend_pb2
import imagesend_pb2_grpc

# open image according to name, put the image to a imagelist and return
def open_image(image_name):
    imagelist = []
    with open(image_name+"1.jpg", 'rb') as f1:
        image1 = f1.read()
    imagelist.append(image1)
    with open(image_name+"2.jpg", 'rb') as f2:
        image2 = f2.read()
    imagelist.append(image2)
    return imagelist

class ImageSend(imagesend_pb2_grpc.ImageSendServicer):
    def Imagerequest(self, request, context):
        if request.image_name1 == "New York":
            # use function open new york images
            imagelist = open_image("New York")
            # send images to client
            return imagesend_pb2.images(images1 = imagelist[0], images2 = imagelist[1])
        elif request.image_name1 == "Los Angeles":
            imagelist = open_image("Los Angeles")
            return imagesend_pb2.images(images1 = imagelist[0], images2 = imagelist[1])
        elif request.image_name1 == "San Francisco":
            imagelist = open_image("San Francisco")
            return imagesend_pb2.images(images1 = imagelist[0], images2 = imagelist[1])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imagesend_pb2_grpc.add_ImageSendServicer_to_server(ImageSend(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()