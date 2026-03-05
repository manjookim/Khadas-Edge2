import sys
import os

# 1. 수정된 소스 코드가 있는 경로를 시스템 경로 맨 앞에 추가 (매우 중요!)
# 본인의 실제 경로로 확인해 주세요.
sys.path.insert(0, '/home/mjss/mountp/edge2/ultralytics')

try:
    from ultralytics import YOLO
    import torch
    print("수정된 Ultralytics 로딩 완료!")
except ImportError as e:
    print(f"로딩 실패: {e}")
    sys.exit(1)

# 2. 모델 로드 및 변환
model_path = '/home/mjss/edge2/model/yolov8s-pose.pt' # 본인의 pt 파일 경로
model = YOLO(model_path)

print("ONNX 변환을 시작합니다...")
# format='onnx'로 설정하면 우리가 head.py에 넣은 'is_in_onnx_export'가 작동합니다.
success = model.export(format='onnx', opset=12, simplify=True)

if success:
    print(f"변환 성공! 파일 위치: {success}")
else:
    print("변환에 실패했습니다. 로그를 확인하세요.")
