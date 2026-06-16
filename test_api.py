"""
DeepShield 后端 API 测试脚本
用于验证检测引擎是否正常工作
"""
import requests
import os

# 配置
BASE_URL = "http://localhost:5001"
UPLOAD_DIR = "uploads"
TEST_IMAGE = "test.jpg"

def test_backend_health():
    """测试后端服务是否启动"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=3)
        print(f"[√] 后端服务正常 (状态码: {response.status_code})")
        return True
    except:
        print("[×] 后端服务未启动，请先运行 python app.py")
        return False

def test_image_detection():
    """测试图片检测功能"""
    # 检查测试文件是否存在
    test_file = os.path.join(UPLOAD_DIR, TEST_IMAGE)
    if not os.path.exists(test_file):
        print(f"[!] 测试文件不存在: {test_file}")
        print("    请将测试图片放入 uploads/ 目录并命名为 test.jpg")
        return False
    
    # 发送检测请求
    with open(test_file, 'rb') as f:
        files = {'file': (TEST_IMAGE, f)}
        data = {
            'model': 'hifi',
            'dataset': 'default',
            'threshold': 75
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/forensics/scan", files=files, data=data, timeout=30)
            
            if response.status_code != 200:
                print(f"[×] 检测失败 (状态码: {response.status_code})")
                print(f"    错误信息: {response.text}")
                return False
            
            result = response.json()
            
            # 验证返回数据结构
            if 'status' not in result:
                print("[×] 返回数据缺少 status 字段")
                return False
            
            if 'payload' not in result:
                print("[×] 返回数据缺少 payload 字段")
                print(f"    完整响应: {result}")
                return False
            
            if 'ai_analysis' not in result['payload']:
                print("[×] payload 中缺少 ai_analysis 字段")
                return False
            
            print("[√] 图片检测功能正常")
            print(f"    - 证据ID: {result.get('evidence_id', 'N/A')}")
            print(f"    - 风险评分: {result['payload'].get('risk_score', 'N/A')}")
            print(f"    - 是否伪造: {result['payload']['ai_analysis'].get('is_synthetic', 'N/A')}")
            return True
            
        except Exception as e:
            print(f"[×] 检测请求失败: {str(e)}")
            return False

def main():
    print("=" * 50)
    print("DeepShield 后端 API 测试")
    print("=" * 50)
    print()
    
    # 测试1: 后端健康检查
    if not test_backend_health():
        return
    
    print()
    
    # 测试2: 图片检测
    if not test_image_detection():
        print()
        print("提示: 如果测试失败，请检查:")
        print("  1. 后端服务是否正常运行")
        print("  2. uploads/ 目录是否有测试图片")
        print("  3. Python 依赖是否安装完整 (pip install -r requirements.txt)")
        return
    
    print()
    print("=" * 50)
    print("所有测试通过！后端 API 工作正常。")
    print("=" * 50)

if __name__ == "__main__":
    main()
