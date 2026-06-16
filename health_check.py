#!/usr/bin/env python3
"""
DeepShield 系统健康检查脚本
用于验证所有模块是否正确安装和配置
"""

import sys
import os

def check_python_version():
    """检查 Python 版本"""
    print("🔍 检查 Python 版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f" Python 版本过低 (需要 3.8+)，当前: {version.major}.{version.minor}")
        return False

def check_dependencies():
    """检查关键依赖包"""
    print("\n🔍 检查依赖包...")
    
    packages = {
        'flask': 'Flask Web框架',
        'flask_cors': '跨域支持',
        'flask_sqlalchemy': '数据库ORM',
        'cv2': 'OpenCV视频处理',
        'numpy': '数值计算',
        'librosa': '音频处理',
        'PIL': '图像处理',
        'reportlab': 'PDF生成'
    }
    
    all_ok = True
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package:20s} - {description}")
        except ImportError:
            print(f"  ❌ {package:20s} - {description} (未安装)")
            all_ok = False
    
    return all_ok

def check_directories():
    """检查必要目录"""
    print("\n🔍 检查项目目录...")
    
    directories = [
        'uploads',
        'evidence',
        'reports',
        'core',
        'security',
        'services',
        'routes',
        'frontend'
    ]
    
    all_ok = True
    for directory in directories:
        path = os.path.join(os.path.dirname(__file__), directory)
        if os.path.exists(path):
            print(f"  ✅ {directory:20s}")
        else:
            print(f"  ❌ {directory:20s} (不存在)")
            all_ok = False
    
    return all_ok

def check_database():
    """检查数据库"""
    print("\n🔍 检查数据库...")
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'chovy_evidence.db')
    if os.path.exists(db_path):
        print(f"  ✅ 数据库文件存在")
        return True
    else:
        print(f"  ️  数据库文件不存在 (运行 init_db.py 初始化)")
        return False

def check_frontend():
    """检查前端配置"""
    print("\n 检查前端配置...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    checks = [
        ('package.json', 'npm 配置文件'),
        ('node_modules', 'npm 依赖'),
        ('vite.config.js', 'Vite 配置'),
        ('src/main.js', '入口文件'),
        ('src/App.vue', '主组件'),
        ('src/router/index.js', '路由配置')
    ]
    
    all_ok = True
    for file, description in checks:
        path = os.path.join(frontend_dir, file)
        if os.path.exists(path):
            print(f"  ✅ {file:25s} - {description}")
        else:
            print(f"  ❌ {file:25s} - {description} (缺失)")
            all_ok = False
    
    return all_ok

def check_model_config():
    """检查模型配置文件"""
    print("\n🔍 检查模型配置...")
    
    config_path = os.path.join(os.path.dirname(__file__), 'core', 'model_config.py')
    if os.path.exists(config_path):
        print(f"  ✅ model_config.py (专业模型配置)")
        return True
    else:
        print(f"  ❌ model_config.py (缺失)")
        return False

def main():
    print("=" * 60)
    print("  DeepShield 系统健康检查")
    print("=" * 60)
    
    results = []
    
    # 执行各项检查
    results.append(("Python 版本", check_python_version()))
    results.append(("依赖包", check_dependencies()))
    results.append(("项目目录", check_directories()))
    results.append(("数据库", check_database()))
    results.append(("前端配置", check_frontend()))
    results.append(("模型配置", check_model_config()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("  检查结果汇总")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {check_name:15s} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 所有检查通过！系统已准备就绪。")
        print("\n📝 下一步操作:")
        print("  1. 启动后端: python app.py")
        print("  2. 启动前端: cd frontend && npm run dev")
        print("  3. 访问系统: http://localhost:5473")
        return 0
    else:
        print("\n⚠️  部分检查失败，请根据提示修复后重试。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
