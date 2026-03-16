#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import time
import re
import datetime

def get_npu_util():
    """Edge2 NPU(RK3588)의 3개 코어 사용량을 각각 읽어옵니다."""
    npu_path = '/sys/kernel/debug/rknpu/load'
    # 초기값 설정
    core_utils = {'Core0': 0.0, 'Core1': 0.0, 'Core2': 0.0}
    
    try:
        if os.path.exists(npu_path):
            with open(npu_path, 'r') as f:
                content = f.read().strip()
                # "NPU load:  Core0:  10%, Core1:   5%, Core2:   0%" 형태에서 각 숫자 추출
                # f-string이나 정규식으로 각 코어별 숫자를 매칭
                matches = re.findall(r'Core\d:\s*(\d+)%', content)
                if matches and len(matches) >= 3:
                    core_utils['Core0'] = float(matches[0])
                    core_utils['Core1'] = float(matches[1])
                    core_utils['Core2'] = float(matches[2])
    except Exception:
        pass
    return core_utils

def get_cpu_and_mem_stats():
    stats = {}
    try:
        # 메모리 정보
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            stats['mem_total_kb'] = int(re.search(r'MemTotal:\s+(\d+)', meminfo).group(1))
            stats['mem_available_kb'] = int(re.search(r'MemAvailable:\s+(\d+)', meminfo).group(1))
        # CPU 정보
        with open('/proc/stat', 'r') as f:
            cpu_times = [int(x) for x in f.readline().split()[1:]]
            stats['cpu_total_time'] = sum(cpu_times)
            stats['cpu_idle_time'] = cpu_times[3]
    except Exception:
        return None
    return stats

def calculate_cpu_usage(prev, curr):
    if not prev or not curr: return 0.0
    total_diff = curr['cpu_total_time'] - prev['cpu_total_time']
    idle_diff = curr['cpu_idle_time'] - prev['cpu_idle_time']
    return 100.0 * (1 - idle_diff / total_diff) if total_diff > 0 else 0.0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-period", type=float, default=1.0)
    args = parser.parse_args()

    log_dir = "/home/khadas/monitoring/logs"
    os.makedirs(log_dir, exist_ok=True) # 폴더가 없으면 생성

    current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    log_filename = f"monitor-{current_date_str}.log"
    log_filepath = os.path.join(log_dir, log_filename)

    prev_stats = get_cpu_and_mem_stats()
    print(f"Monitoring started... Logging to {log_filepath}")

    try:
        while True:
            # 날짜 바뀜 체크
            new_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            if new_date_str != current_date_str:
                current_date_str = new_date_str
                log_filepath = os.path.join(log_dir, f"monitor-{current_date_str}.log")

            curr_stats = get_cpu_and_mem_stats()
            if not curr_stats:
                time.sleep(args.update_period)
                continue

            # 자원 계산
            cpu_util = calculate_cpu_usage(prev_stats, curr_stats)
            mem_used = curr_stats['mem_total_kb'] - curr_stats['mem_available_kb']
            mem_util = 100.0 * (mem_used / curr_stats['mem_total_kb'])

            npu_dict = get_npu_util()
            npu_str = f"Core0:{npu_dict['Core0']:2.0f}%, Core1: {npu_dict['Core1']:2.0f}%, Core2: {npu_dict['Core2']:2.0f}%"
            log_msg = (
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] "
                f"NPU: {npu_str}%, CPU: {cpu_util:4.1f}%, Mem: {mem_util:4.1f}%"
            )
            
            # 파일 기록 및 실시간 출력 (디버깅용)
            with open(log_filepath, "a") as f:
                f.write(log_msg + "\n")
            print(log_msg) 

            prev_stats = curr_stats
            time.sleep(args.update_period)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        error_path = os.path.join(log_dir, f"error-{current_date_str}.log")
        with open(error_path, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Error: {e}\n")
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
