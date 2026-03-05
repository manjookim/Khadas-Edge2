import os
import cv2
import numpy as np
import time
from rknnlite.api import RKNNLite

# --- 설정 ---
MODEL_PATH = '/home/khadas/models/yolov8s-pose_fixed.rknn'
DATASET_PATH = '/home/khadas/dataset/coco/val2017_100' # 이미지 폴더 경로
INPUT_SIZE = 640

def measure_coco_performance():
    rknn_lite = RKNNLite()
    
    # 모델 로드 및 초기화
    if rknn_lite.load_rknn(MODEL_PATH) != 0:
        return
    if rknn_lite.init_runtime() != 0:
        return

    img_files = [f for f in os.listdir(DATASET_PATH) if f.endswith(('.jpg', '.png'))]
    print(f"Total images found: {len(img_files)}")

    pre_times = []   # 전처리 시간
    npu_times = []   # NPU 순수 추론 시간
    total_times = [] # 전체 시간 (전처리 + 추론)

    # 예열 (Warm-up) - 10장
    for i in range(10):
        dummy_img = np.zeros((INPUT_SIZE, INPUT_SIZE, 3), dtype=np.uint8)
        rknn_lite.inference(inputs=[dummy_img])

    print("Starting Inference on COCO val2017...")
    
    for filename in img_files:
        img_path = os.path.join(DATASET_PATH, filename)
        
        # 1. 전처리 (CPU)
        start_pre = time.perf_counter()
        orig_img = cv2.imread(img_path)
        img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (INPUT_SIZE, INPUT_SIZE))
        end_pre = time.perf_counter()
        
        # 2. NPU 추론
        start_npu = time.perf_counter()
        outputs = rknn_lite.inference(inputs=[img])
        end_npu = time.perf_counter()
        
        # 시간 기록
        pre_t = (end_pre - start_pre) * 1000
        npu_t = (end_npu - start_npu) * 1000
        
        pre_times.append(pre_t)
        npu_times.append(npu_t)
        total_times.append(pre_t + npu_t)

    # 결과 요약
    avg_pre = np.mean(pre_times)
    avg_npu = np.mean(npu_times)
    avg_total = np.mean(total_times)
    
    print('\n' + '='*40)
    print(f" Dataset: COCO val2017 ({len(img_files)} images)")
    print(f" Average Pre-process (CPU): {avg_pre:.2f} ms")
    print(f" Average Inference (NPU)  : {avg_npu:.2f} ms")
    print(f" Average End-to-End       : {avg_total:.2f} ms")
    print("-" * 40)
    print(f" Pure NPU FPS : {1000/avg_npu:.2f}")
    print(f" Real-world FPS: {1000/avg_total:.2f}")
    print('='*40)

    rknn_lite.release()

if __name__ == '__main__':
    measure_coco_performance()
