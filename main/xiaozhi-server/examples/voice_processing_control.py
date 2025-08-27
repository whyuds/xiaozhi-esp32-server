#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音处理开关控制示例
演示如何通过API控制语音处理功能
"""

import requests
import json
import time

class VoiceProcessingController:
    def __init__(self, server_host="localhost", server_port=8003):
        self.base_url = f"http://{server_host}:{server_port}"
        
    def get_status(self):
        """获取语音处理状态"""
        try:
            response = requests.get(f"{self.base_url}/api/voice_processing/status")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取状态失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def enable_voice_processing(self):
        """启用语音处理"""
        try:
            response = requests.post(
                f"{self.base_url}/api/voice_processing/toggle",
                json={"enabled": True},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
                return result
            else:
                print(f"启用失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def disable_voice_processing(self):
        """禁用语音处理"""
        try:
            response = requests.post(
                f"{self.base_url}/api/voice_processing/toggle",
                json={"enabled": False},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
                return result
            else:
                print(f"禁用失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def toggle_voice_processing(self):
        """切换语音处理状态"""
        try:
            response = requests.post(
                f"{self.base_url}/api/voice_processing/toggle",
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
                return result
            else:
                print(f"切换失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"请求失败: {e}")
            return None

def main():
    """主函数 - 演示语音处理控制"""
    controller = VoiceProcessingController()
    
    print("=== 语音处理控制演示 ===\n")
    
    # 1. 获取当前状态
    print("1. 获取当前状态...")
    status = controller.get_status()
    if status:
        print(f"   当前状态: {status['message']}")
    
    print()
    
    # 2. 禁用语音处理
    print("2. 禁用语音处理...")
    controller.disable_voice_processing()
    
    print()
    
    # 3. 确认禁用状态
    print("3. 确认禁用状态...")
    status = controller.get_status()
    if status:
        print(f"   当前状态: {status['message']}")
    
    print()
    
    # 4. 启用语音处理
    print("4. 启用语音处理...")
    controller.enable_voice_processing()
    
    print()
    
    # 5. 确认启用状态
    print("5. 确认启用状态...")
    status = controller.get_status()
    if status:
        print(f"   当前状态: {status['message']}")
    
    print()
    
    # 6. 演示切换功能
    print("6. 演示切换功能...")
    print("   第一次切换:")
    controller.toggle_voice_processing()
    
    print("   第二次切换:")
    controller.toggle_voice_processing()
    
    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    main()
