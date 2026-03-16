# Khadas-Edge2
Khadas Edge2 NPU - AI 가속기 연구 

Khadas Edge2 OS : edge2-ubuntu-22.04-gnome-linux-5.10-fenix-1.6.2-240110                        
NPU version : RK3588     
RKNN Toolkit2 version : v0.9.0     
RKNN Runtime version : v1.3.0                 
PC Python version : 3.8    
Edge2 Python Version : 3.10   

------

####  NPU (Nenral Processing Unit)    
인공지능(AI)과 딥러닝 연산을 가속화하기 위해 특수하게 설계된 하드웨어 프로세서    
+ NPU는 고성능·저전력으로 설계되어 스마트폰, PC, 자율주행차 등 다양한 엣지 디바이스에서 AI 기능을 효율적으로 처리
+ CPU나 GPU의 부담을 줄여 전력 효율을 높이고 발열을 감소
####  RK3588
 

####  RK3588에 사용되는 프레임워크        
+ RKNN toolkit2
+ RKNN toolkit_lite2 
+ rknn model zoo              

####  호스트(PC)/rpi 둘 다 사용 한 이유   
PC의 컴파일 성능이 더 우수함           
컴파일은 호스트 가상환경에서, 추론은 Khadas Edge2 로컬에서 실행  

## PC 환경설정
1. Build Virtual Environment
```
sudo apt update
sudo apt install python3-dev python3-numpy
```
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```
```
conda create -n npu-env python=3.8
conda activate npu-env
conda init --all
conda deactivate
```
2. Get Convert Tool
```
git clone https://github.com/rockchip-linux/rknn-toolkit2.git
cd rknn-toolkit2/rknn-toolkit2
```
```
sudo apt-get install python3 python3-dev python3-pip
sudo apt-get install libxslt1-dev zlib1g-dev libglib2.0 libsm6 libgl1-mesa-glx libprotobuf-dev gcc cmake
pip3 install -r packages/requirements_cp38-1.6.0.txt
pip3 install packages/rknn_toolkit2-1.6.0+81f21f4d-cp38-cp38-linux_x86_64.whl
```


## Edge2 환경설정  
  
1. Toolkit 설치 
```
git clone https://github.com/khadas/edge2-npu
```
```
cd Python
sudo cp ../C++/runtime/librknn_api/aarch64/librknnrt.so /usr/lib
sudo apt update
sudo apt install -y python3-dev python3-pip python3-opencv python3-numpy
pip3 install ./wheel/rknn_toolkit_lite2-1.3.0-cp310-cp310-linux_aarch64.whl
```

------

1. RKNN Compile     
   See  [Compile](https://github.com/manjookim/Khadas-Edge2/tree/main/compile) for more details
2. Inference    
    See  [inference](https://github.com/manjookim/Khadas-Edge2/tree/main/inference) for more details                   
3. monitoring     
    See  [Monitoring](https://github.com/manjookim/Khadas-Edge2/tree/main/monitoring) for more details
4. accuracy     
   See  [accuracy](https://github.com/manjookim/Khadas-Edge2/tree/main/accuracy) for more details               




------
### References
https://github.com/khadas/edge2-npu    
https://github.com/airockchip/rknn_model_zoo     
https://github.com/airockchip/ultralytics_yolov8    
https://github.com/airockchip/rknn-toolkit2     
