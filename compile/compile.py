from rknn.api import RKNN

rknn = RKNN(verbose=True) 

# pre-process config
print('--> Config model')
rknn.config(mean_values=[[0, 0, 0]], std_values=[[255, 255, 255]], target_platform='rk3588')
print('done')

# Load ONNX model
print('--> Loading model')
ret = rknn.load_onnx(model='yolov8s-pose_fixed.onnx')
if ret != 0:
    print('Load model failed!')
    exit(ret)
print('done')

"""
# Load pytorch model
print('--> Loading model')
ret = rknn.load_pytorch(model='./resnet18.pt', input_size_list=[[1, 3, 224, 224]])
if ret != 0:
    print('Load model failed!')
    exit(ret)
print('done')
 
# Load tensorflow model
print('--> Loading model')
ret = rknn.load_tensorflow(tf_pb='./ssd_mobilenet_v1_coco_2017_11_17.pb',
                           inputs=['Preprocessor/sub'],
                           outputs=['concat', 'concat_1'],
                           input_size_list=[[300, 300, 3]])
if ret != 0:
    print('Load model failed!')
    exit(ret)
print('done')              
 
# Load caffe model
print('--> Loading model')
ret = rknn.load_caffe(model='./mobilenet_v2.prototxt', 
                      blobs='./mobilenet_v2.caffemodel')
if ret != 0:
    print('Load model failed!')
    exit(ret)
print('done')
 
# Load tensorflow lite model
print('--> Loading model')
ret = rknn.load_tflite(model='./mobilenet_v1.tflite')
if ret != 0:
    print('Load model failed!')
    exit(ret)
print('done')
 
# Load darknet model
print('--> Loading model')
ret = rknn.load_darknet(model='./yolov3-tiny.cfg',
                        weight='./yolov3.weights')
if ret != 0:
    print('Load model failed!')
    exit(ret)

"""

# Build model
print('--> Building model')
ret = rknn.build(do_quantization=True, dataset='./dataset.txt')
if ret != 0:
    print('Build model failed!')
    exit(ret)
print('done')

# Export RKNN model
print('--> Export rknn model')
ret = rknn.export_rknn(export_path='./yolov8s-pose_fixed.rknn')
if ret != 0:
    print('Export rknn model failed!')
    exit(ret)
print('done')


print('done')
