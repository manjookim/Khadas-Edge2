import onnx

# 1. 아까 성공적으로 뽑은 ONNX 로드
model = onnx.load('../model/yolov8s-pose.onnx')

# 2. 모델의 모든 노드를 돌면서 MaxPool의 dilations 속성 제거
for node in model.graph.node:
    if node.op_type == 'MaxPool':
        # dilations 속성이 있는지 확인하고 삭제
        for i, attr in enumerate(node.attribute):
            if attr.name == 'dilations':
                node.attribute.pop(i)
                print(f"Fixed MaxPool node: {node.name}")

# 3. 수정된 모델 저장
onnx.save(model, 'yolov8s-pose_fixed.onnx')
print("준비 완료! 이제 yolov8s_fixed.onnx 파일을 사용해 RKNN으로 변환하세요.")
