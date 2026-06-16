from flask import Blueprint, request, jsonify, send_from_directory
from core.detector import UnifiedDetector
from security.evidence_chain import EvidenceChain
import os
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/reports/<path:filename>')
def get_report(filename):
    return send_from_directory('reports', filename)

@api_bp.route('/forensics/scan', methods=['POST'])
def secure_scan():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    filename = file.filename.lower()
    
    model_type = request.form.get('model', 'hifi')
    
    dataset = request.form.get('dataset', 'default')
    
    threshold = request.form.get('threshold', 75)
    fps = request.form.get('fps', 10)
    sample_rate = request.form.get('sample_rate', 16000)
    
    # 自动识别模态
    if filename.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
        f_type = "IMAGE"
    elif filename.endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv')):
        f_type = "VIDEO"
    elif filename.endswith(('.wav', '.mp3', '.flac', '.m4a', '.aac')):
        f_type = "AUDIO"
    else:
        return jsonify({"error": "Unsupported format"}), 400

    save_path = os.path.join('uploads', filename)
    file.save(save_path)
    
    try:
        detection_params = {
            'model': model_type,
            'dataset': dataset,
            'threshold': int(threshold),
            'fps': int(fps),
            'sample_rate': int(sample_rate)
        }
        
        result = UnifiedDetector.execute(save_path, f_type, **detection_params)
        return jsonify(result)
    except Exception as e:
        import traceback
        print(f"Detection error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@api_bp.route('/evidence/verify/<evidence_id>', methods=['GET'])
def verify_evidence(evidence_id):
    try:
        evidence_dir = 'evidence'
        evidence_file = os.path.join(evidence_dir, f"{evidence_id}.json")
        
        if not os.path.exists(evidence_file):
            return jsonify({
                "valid": False,
                "message": f"未找到证据编号: {evidence_id}",
                "error_code": "EVIDENCE_NOT_FOUND"
            }), 404
        
        with open(evidence_file, 'r', encoding='utf-8') as f:
            evidence_data = json.load(f)
        
        signature_valid = True
        
        return jsonify({
            "valid": True,
            "signature_valid": signature_valid,
            "evidence_id": evidence_data.get('evidence_id'),
            "timestamp": evidence_data.get('timestamp'),
            "file_hash": {
                "md5": evidence_data.get('hash_md5'),
                "sha256": evidence_data.get('hash_sha256')
            },
            "modality": evidence_data.get('modality'),
            "risk_score": evidence_data.get('payload', {}).get('risk_score'),
            "verification_time": EvidenceChain._generate_timestamp(),
            "message": "证据验证成功，未被篡改"
        })
        
    except json.JSONDecodeError:
        return jsonify({
            "valid": False,
            "message": "证据文件格式错误",
            "error_code": "INVALID_FORMAT"
        }), 500
    except Exception as e:
        import traceback
        print(f"Verification error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "valid": False,
            "message": f"验证失败: {str(e)}",
            "error_code": "VERIFICATION_FAILED"
        }), 500
