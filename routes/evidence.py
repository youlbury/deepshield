import hashlib
import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify

evidence_bp = Blueprint('evidence', __name__)

EVIDENCE_DB = {
    # 预置测试数据
    '111': {
        'evidence_id': '111',
        'file_hash': '54dac43ff78f8090a0dfbaab750576959f28cd95785fb1e3a88f43d2b9c7e6a1',
        'filename': 'test_image_001.jpg',
        'file_size': 245678,
        'timestamp': '2026-06-16T20:11:00',
        'model': 'HiFi_Net_v2.0',
        'risk_score': 0.85,
        'registered_at': '2026-06-16T20:11:30'
    },
    'ev_20260613_001': {
        'evidence_id': 'ev_20260613_001',
        'file_hash': 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
        'filename': 'suspicious_photo.png',
        'file_size': 512340,
        'timestamp': '2026-06-13T14:30:00',
        'model': 'CNN_Detection_v1.5',
        'risk_score': 0.92,
        'registered_at': '2026-06-13T14:30:45'
    },
    'IMG_20260615_001': {
        'evidence_id': 'IMG_20260615_001',
        'file_hash': 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567a',
        'filename': 'deepfake_face.jpg',
        'file_size': 387654,
        'timestamp': '2026-06-15T09:20:00',
        'model': 'Xception_v3.0',
        'risk_score': 0.78,
        'registered_at': '2026-06-15T09:20:30'
    },
    'VID_20260614_002': {
        'evidence_id': 'VID_20260614_002',
        'file_hash': 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567ab2',
        'filename': 'fake_video.mp4',
        'file_size': 15678900,
        'timestamp': '2026-06-14T16:45:00',
        'model': 'TimeSformer_v2.0',
        'risk_score': 0.95,
        'registered_at': '2026-06-14T16:45:30'
    },
    'AUD_20260616_003': {
        'evidence_id': 'AUD_20260616_003',
        'file_hash': 'd4e5f6789012345678901234567890abcdef1234567890abcdef1234567abc3',
        'filename': 'voice_clone.wav',
        'file_size': 2345678,
        'timestamp': '2026-06-16T11:30:00',
        'model': 'AASIST_v1.5',
        'risk_score': 0.88,
        'registered_at': '2026-06-16T11:30:30'
    },
    'TEST_REAL_001': {
        'evidence_id': 'TEST_REAL_001',
        'file_hash': 'e5f6789012345678901234567890abcdef1234567890abcdef1234567abcd4',
        'filename': 'authentic_photo.jpg',
        'file_size': 456789,
        'timestamp': '2026-06-16T14:00:00',
        'model': 'EfficientNet_v4.0',
        'risk_score': 0.12,
        'registered_at': '2026-06-16T14:00:30'
    }
}

@evidence_bp.route('/evidence/verify', methods=['POST'])
def verify_evidence():
    try:
        data = request.get_json()
        evidence_id = data.get('evidence_id')
        
        if not evidence_id:
            return jsonify({
                'success': False,
                'message': '缺少证据ID'
            }), 400
        
        # 模式1: 验证已注册证据
        if evidence_id in EVIDENCE_DB:
            evidence_record = EVIDENCE_DB[evidence_id]
            
            file_hash_provided = data.get('file_hash')
            hash_verified = True
            hash_match = True
            
            if file_hash_provided:
                stored_hash = evidence_record.get('file_hash')
                hash_match = (file_hash_provided == stored_hash)
                hash_verified = True
            else:
                hash_verified = False
                hash_match = None
            
            timestamp_provided = data.get('timestamp')
            timestamp_verified = True
            timestamp_match = True
            
            if timestamp_provided:
                stored_timestamp = evidence_record.get('timestamp')
                # 允许5分钟误差
                time_diff = abs(datetime.fromisoformat(timestamp_provided) - 
                              datetime.fromisoformat(stored_timestamp))
                timestamp_match = time_diff.total_seconds() < 300
            else:
                timestamp_verified = False
                timestamp_match = None
            
            # 综合结果
            all_verified = hash_match and timestamp_match if (hash_verified and timestamp_verified) else False
            
            verification_result = {
                'success': True,
                'evidence_id': evidence_id,
                'verification_status': 'VERIFIED' if all_verified else 'FAILED',
                'details': {
                    'hash_verification': {
                        'verified': hash_verified,
                        'match': hash_match,
                        'stored_hash': evidence_record.get('file_hash'),
                        'provided_hash': file_hash_provided
                    },
                    'timestamp_verification': {
                        'verified': timestamp_verified,
                        'match': timestamp_match,
                        'stored_timestamp': evidence_record.get('timestamp'),
                        'provided_timestamp': timestamp_provided
                    },
                    'metadata': {
                        'original_filename': evidence_record.get('filename'),
                        'file_size': evidence_record.get('file_size'),
                        'detection_model': evidence_record.get('model'),
                        'risk_score': evidence_record.get('risk_score')
                    }
                },
                'verified_at': datetime.now().isoformat()
            }
            
            return jsonify(verification_result), 200
        
        # 模式2: 创建新证据记录（如果提供了文件哈希）
        else:
            file_hash_provided = data.get('file_hash')
            
            if not file_hash_provided:
                return jsonify({
                    'success': False,
                    'message': '证据不存在于数据库中，且未提供文件哈希。请先上传文件进行检测。',
                    'verification_status': 'NOT_FOUND'
                }), 404
            
            # 创建新的证据记录
            new_evidence = {
                'evidence_id': evidence_id,
                'file_hash': file_hash_provided,
                'filename': data.get('filename', 'unknown_file'),
                'file_size': data.get('file_size', 0),
                'timestamp': data.get('timestamp', datetime.now().isoformat()),
                'model': data.get('model', 'Unknown'),
                'risk_score': data.get('risk_score', 0.0),
                'registered_at': datetime.now().isoformat()
            }
            
            # 保存到数据库
            EVIDENCE_DB[evidence_id] = new_evidence
            
            verification_result = {
                'success': True,
                'evidence_id': evidence_id,
                'verification_status': 'NEW_EVIDENCE',
                'message': '新证据已注册到系统',
                'details': {
                    'hash_verification': {
                        'verified': True,
                        'match': True,
                        'stored_hash': file_hash_provided,
                        'provided_hash': file_hash_provided
                    },
                    'timestamp_verification': {
                        'verified': True,
                        'match': True,
                        'stored_timestamp': new_evidence['timestamp'],
                        'provided_timestamp': data.get('timestamp')
                    },
                    'metadata': {
                        'original_filename': new_evidence['filename'],
                        'file_size': new_evidence['file_size'],
                        'detection_model': new_evidence['model'],
                        'risk_score': new_evidence['risk_score']
                    }
                },
                'verified_at': datetime.now().isoformat()
            }
            
            return jsonify(verification_result), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'验证失败: {str(e)}'
        }), 500


@evidence_bp.route('/evidence/register', methods=['POST'])
def register_evidence():
    try:
        data = request.get_json()
        evidence_id = data.get('evidence_id')
        
        if not evidence_id:
            return jsonify({
                'success': False,
                'message': '缺少证据ID'
            }), 400
        
        # 保存记录
        EVIDENCE_DB[evidence_id] = {
            'evidence_id': evidence_id,
            'file_hash': data.get('file_hash'),
            'filename': data.get('filename'),
            'file_size': data.get('file_size'),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'model': data.get('model'),
            'risk_score': data.get('risk_score'),
            'registered_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': '证据注册成功',
            'evidence_id': evidence_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500


@evidence_bp.route('/evidence/calculate_hash', methods=['POST'])
def calculate_hash():
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': '未找到上传文件'
            }), 400
        
        file = request.files['file']
        
        sha256_hash = hashlib.sha256()
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
        
        file_hash = sha256_hash.hexdigest()
        
        return jsonify({
            'success': True,
            'file_hash': file_hash,
            'algorithm': 'SHA-256',
            'filename': file.filename,
            'file_size': file.content_length
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'哈希计算失败: {str(e)}'
        }), 500


@evidence_bp.route('/evidence/list', methods=['GET'])
def list_evidence():
    try:
        evidence_list = []
        for eid, record in EVIDENCE_DB.items():
            evidence_list.append({
                'evidence_id': record['evidence_id'],
                'filename': record.get('filename'),
                'timestamp': record.get('timestamp'),
                'risk_score': record.get('risk_score'),
                'model': record.get('model')
            })
        
        return jsonify({
            'success': True,
            'total': len(evidence_list),
            'evidence_list': evidence_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取列表失败: {str(e)}'
        }), 500
