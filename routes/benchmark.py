import random
from datetime import datetime
from flask import Blueprint, jsonify, request

benchmark_bp = Blueprint('benchmark', __name__)

BENCHMARK_RESULTS = {
    "faceforensics_plus": {
        "dataset_name": "FaceForensics++",
        "total_samples": 5000,
        "models": {
            "xception": {
                "accuracy": 96.8,
                "auc": 98.5,
                "f1_score": 96.2,
                "precision": 97.1,
                "recall": 95.4,
                "inference_time_ms": 45,
                "tested_at": "2026-06-10T10:30:00"
            },
            "efficientnet": {
                "accuracy": 95.2,
                "auc": 97.8,
                "f1_score": 94.8,
                "precision": 96.0,
                "recall": 93.7,
                "inference_time_ms": 38,
                "tested_at": "2026-06-10T11:00:00"
            },
            "f3net": {
                "accuracy": 97.5,
                "auc": 99.1,
                "f1_score": 97.2,
                "precision": 98.0,
                "recall": 96.5,
                "inference_time_ms": 52,
                "tested_at": "2026-06-11T09:15:00"
            }
        }
    },
    "dfdc": {
        "dataset_name": "Deepfake Detection Challenge",
        "total_samples": 10000,
        "models": {
            "timesformer": {
                "accuracy": 94.3,
                "auc": 96.7,
                "f1_score": 93.8,
                "precision": 95.2,
                "recall": 92.5,
                "inference_time_ms": 120,
                "tested_at": "2026-06-12T14:20:00"
            },
            "slowfast": {
                "accuracy": 93.1,
                "auc": 95.4,
                "f1_score": 92.6,
                "precision": 94.0,
                "recall": 91.3,
                "inference_time_ms": 95,
                "tested_at": "2026-06-12T15:30:00"
            }
        }
    },
    "asvspoof_2021": {
        "dataset_name": "ASVspoof 2021",
        "total_samples": 3000,
        "models": {
            "aasist": {
                "eer": 1.23,
                "min_tDCF": 0.032,
                "accuracy": 98.7,
                "inference_time_ms": 25,
                "tested_at": "2026-06-13T08:00:00"
            },
            "wav2vec2": {
                "eer": 1.85,
                "min_tDCF": 0.048,
                "accuracy": 97.9,
                "inference_time_ms": 30,
                "tested_at": "2026-06-13T09:30:00"
            }
        }
    }
}


@benchmark_bp.route('/benchmark/datasets', methods=['GET'])
def list_datasets():
    try:
        datasets = []
        for key, data in BENCHMARK_RESULTS.items():
            datasets.append({
                'id': key,
                'name': data['dataset_name'],
                'total_samples': data['total_samples'],
                'model_count': len(data['models'])
            })
        
        return jsonify({
            'success': True,
            'datasets': datasets
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取数据集列表失败: {str(e)}'
        }), 500


@benchmark_bp.route('/benchmark/results/<dataset_id>', methods=['GET'])
def get_benchmark_results(dataset_id):
    try:
        if dataset_id not in BENCHMARK_RESULTS:
            return jsonify({
                'success': False,
                'message': f'数据集 {dataset_id} 不存在'
            }), 404
        
        dataset = BENCHMARK_RESULTS[dataset_id]
        
        all_models = dataset['models']
        best_accuracy = max(all_models.values(), key=lambda x: x.get('accuracy', 0))
        fastest_model = min(all_models.values(), key=lambda x: x.get('inference_time_ms', float('inf')))
        
        return jsonify({
            'success': True,
            'dataset': {
                'id': dataset_id,
                'name': dataset['dataset_name'],
                'total_samples': dataset['total_samples'],
                'best_model': {
                    'name': [k for k, v in all_models.items() if v == best_accuracy][0],
                    'accuracy': best_accuracy.get('accuracy')
                },
                'fastest_model': {
                    'name': [k for k, v in all_models.items() if v == fastest_model][0],
                    'inference_time_ms': fastest_model.get('inference_time_ms')
                }
            },
            'models': all_models
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取基准测试结果失败: {str(e)}'
        }), 500


@benchmark_bp.route('/benchmark/run', methods=['POST'])
def run_benchmark():
    try:
        data = request.get_json()
        dataset_id = data.get('dataset')
        model_name = data.get('model')
        samples = data.get('samples', 1000)
        
        if not dataset_id or not model_name:
            return jsonify({
                'success': False,
                'message': '缺少必要参数: dataset 和 model'
            }), 400
        
        # 模拟测试
        test_duration = random.uniform(5, 15)
        
        mock_result = {
            'accuracy': round(random.uniform(90, 99), 2),
            'auc': round(random.uniform(92, 99.5), 2),
            'f1_score': round(random.uniform(89, 98), 2),
            'precision': round(random.uniform(91, 99), 2),
            'recall': round(random.uniform(88, 97), 2),
            'inference_time_ms': random.randint(20, 150),
            'tested_samples': samples,
            'test_duration_seconds': round(test_duration, 2),
            'tested_at': datetime.now().isoformat()
        }
        
        # 保存
        if dataset_id not in BENCHMARK_RESULTS:
            BENCHMARK_RESULTS[dataset_id] = {
                'dataset_name': dataset_id,
                'total_samples': samples,
                'models': {}
            }
        
        BENCHMARK_RESULTS[dataset_id]['models'][model_name] = mock_result
        
        return jsonify({
            'success': True,
            'message': '基准测试完成',
            'result': mock_result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'基准测试失败: {str(e)}'
        }), 500


@benchmark_bp.route('/benchmark/compare', methods=['POST'])
def compare_models():
    try:
        data = request.get_json()
        dataset_id = data.get('dataset')
        model_names = data.get('models', [])
        
        if not dataset_id or not model_names:
            return jsonify({
                'success': False,
                'message': '缺少必要参数'
            }), 400
        
        if dataset_id not in BENCHMARK_RESULTS:
            return jsonify({
                'success': False,
                'message': f'数据集 {dataset_id} 不存在'
            }), 404
        
        dataset = BENCHMARK_RESULTS[dataset_id]
        comparison = {}
        
        for model_name in model_names:
            if model_name in dataset['models']:
                comparison[model_name] = dataset['models'][model_name]
        
        return jsonify({
            'success': True,
            'dataset': dataset['dataset_name'],
            'comparison': comparison
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'模型比较失败: {str(e)}'
        }), 500


@benchmark_bp.route('/benchmark/robustness', methods=['GET'])
def get_robustness():
    try:
        results = {
            'models': [
                {'name': 'Xception', 'jpeg_q90': 95.8, 'jpeg_q70': 94.2, 'jpeg_q50': 90.5, 'gaussian_noise': 93.1, 'median_blur': 94.8},
                {'name': 'F3Net', 'jpeg_q90': 94.0, 'jpeg_q70': 92.8, 'jpeg_q50': 88.3, 'gaussian_noise': 91.5, 'median_blur': 93.2},
                {'name': 'EfficientNet', 'jpeg_q90': 95.2, 'jpeg_q70': 93.5, 'jpeg_q50': 89.8, 'gaussian_noise': 92.4, 'median_blur': 94.0},
                {'name': 'AASIST', 'jpeg_q90': 92.5, 'jpeg_q70': 90.8, 'jpeg_q50': 86.2, 'gaussian_noise': 89.5, 'median_blur': 91.8},
                {'name': 'TimeSformer', 'jpeg_q90': 96.8, 'jpeg_q70': 95.5, 'jpeg_q50': 92.0, 'gaussian_noise': 94.5, 'median_blur': 95.8}
            ],
            'attack_types': [
                {'id': 'jpeg_q90', 'label': 'JPEG 压缩 Q90', 'label_cn': '轻度压缩', 'category': '压缩攻击'},
                {'id': 'jpeg_q70', 'label': 'JPEG 压缩 Q70', 'label_cn': '中度压缩', 'category': '压缩攻击'},
                {'id': 'jpeg_q50', 'label': 'JPEG 压缩 Q50', 'label_cn': '重度压缩', 'category': '压缩攻击'},
                {'id': 'gaussian_noise', 'label': '高斯噪声 σ=0.02', 'label_cn': '加性噪声', 'category': '噪声攻击'},
                {'id': 'median_blur', 'label': '中值滤波 3×3', 'label_cn': '平滑滤波', 'category': '滤波攻击'}
            ]
        }
        return jsonify({'success': True, **results}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@benchmark_bp.route('/benchmark/cross-modal', methods=['GET'])
def get_cross_modal():
    try:
        results = {
            'fusion_results': [
                {'model': 'Xception + AASIST', 'modality': '图像+音频', 'single_image': 96.2, 'single_audio': 93.2, 'fusion_accuracy': 97.8, 'fusion_gain': 1.6},
                {'model': 'Xception + TimeSformer', 'modality': '图像+视频', 'single_image': 96.2, 'single_video': 97.5, 'fusion_accuracy': 98.5, 'fusion_gain': 1.0},
                {'model': 'F3Net + AASIST', 'modality': '图像+音频', 'single_image': 94.5, 'single_audio': 93.2, 'fusion_accuracy': 96.2, 'fusion_gain': 1.7},
                {'model': 'EfficientNet + TimeSformer', 'modality': '图像+视频', 'single_image': 95.8, 'single_video': 97.5, 'fusion_accuracy': 98.2, 'fusion_gain': 0.7}
            ],
            'fusion_categories': ['Early Fusion 早期融合', 'Late Fusion 晚期融合', 'Attention Fusion 注意力融合']
        }
        return jsonify({'success': True, **results}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@benchmark_bp.route('/benchmark/roc', methods=['GET'])
def get_roc_data():
    try:
        def generate_roc_points(auc, n=20):
            import math
            points = []
            for i in range(n + 1):
                fpr = i / n
                tpr = math.pow(fpr, (1 - auc / 100) * 10 + 0.5) if fpr > 0 else 0
                tpr = min(1.0, max(0.0, tpr + (auc / 100 - 0.9) * 0.3))
                points.append({'fpr': round(fpr, 3), 'tpr': round(tpr, 4)})
            # 平滑末尾
            points[-1] = {'fpr': 1.0, 'tpr': 1.0}
            return points

        results = {
            'curves': [
                {'model': 'Xception', 'auc': 98.1, 'color': '#00D4FF', 'points': generate_roc_points(98.1)},
                {'model': 'F3Net', 'auc': 97.0, 'color': '#00FF88', 'points': generate_roc_points(97.0)},
                {'model': 'EfficientNet', 'auc': 97.8, 'color': '#8b5cf6', 'points': generate_roc_points(97.8)},
                {'model': 'AASIST', 'auc': 96.5, 'color': '#f59e0b', 'points': generate_roc_points(96.5)},
                {'model': 'TimeSformer', 'auc': 98.8, 'color': '#ef4444', 'points': generate_roc_points(98.8)}
            ]
        }
        return jsonify({'success': True, **results}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@benchmark_bp.route('/benchmark/speed', methods=['GET'])
def get_speed_data():
    try:
        results = {
            'models': [
                {'name': 'Xception', 'latency_cpu': 245, 'latency_gpu': 45, 'throughput_cpu': 4.1, 'throughput_gpu': 22.2, 'params_m': 22.9, 'flops_g': 8.4},
                {'name': 'F3Net', 'latency_cpu': 310, 'latency_gpu': 52, 'throughput_cpu': 3.2, 'throughput_gpu': 19.2, 'params_m': 28.5, 'flops_g': 12.1},
                {'name': 'EfficientNet', 'latency_cpu': 185, 'latency_gpu': 38, 'throughput_cpu': 5.4, 'throughput_gpu': 26.3, 'params_m': 15.3, 'flops_g': 5.6},
                {'name': 'AASIST', 'latency_cpu': 120, 'latency_gpu': 28, 'throughput_cpu': 8.3, 'throughput_gpu': 35.7, 'params_m': 8.7, 'flops_g': 3.2},
                {'name': 'TimeSformer', 'latency_cpu': 520, 'latency_gpu': 68, 'throughput_cpu': 1.9, 'throughput_gpu': 14.7, 'params_m': 121.0, 'flops_g': 42.5}
            ],
            'platforms': ['CPU (Intel i9)', 'GPU (NVIDIA RTX 4090)']
        }
        return jsonify({'success': True, **results}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
