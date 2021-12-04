import logging
import os
import grpc
import imagesend_pb2
import imagesend_pb2_grpc


def run():
    image_Name = input(">")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = imagesend_pb2_grpc.ImageSendStub(channel)
        response = stub.Imagerequest(imagesend_pb2.image_name(image_name1=image_Name))
    filename1 = "./static/image_"+image_Name+"/"+image_Name+"1.jpg"
    os.makedirs(os.path.dirname(filename1), exist_ok=True)
    with open(filename1,"wb") as f:
        f.write(response.images1)
    filename2 = "./static/image_"+image_Name+"/"+image_Name+"2.jpg"
    os.makedirs(os.path.dirname(filename2), exist_ok=True)
    with open(filename2,"wb") as f:
        f.write(response.images2)

if __name__ == '__main__':
    logging.basicConfig()
    run()