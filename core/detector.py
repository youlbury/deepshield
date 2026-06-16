from core.image_engine import ImageForensicsEngine
from core.video_engine import VideoForensicsEngine
from core.audio_engine import AudioForensicsEngine
from core.cross_modal_fusion import CrossModalFusion
from core.risk_levels import classify_risk, get_risk_summary
from security.evidence_chain import EvidenceChain
from security.robustness import RobustnessEvaluator
from security.exif_guard import ExifGuard
from services.report_service import ForensicReporter
import os


class UnifiedDetector:
    @staticmethod
    def execute(file_path, modality, **kwargs):
        result = {}
        
        model_type = kwargs.get('model', 'xception')
        dataset = kwargs.get('dataset', 'default')
        threshold = kwargs.get('threshold', 75)
        fps = kwargs.get('fps', 10)
        sample_rate = kwargs.get('sample_rate', 16000)
        cross_modal = kwargs.get('cross_modal', True)
        
        if modality == "IMAGE":
            ai_data = ImageForensicsEngine.run_deep_scan(file_path, model_type=model_type)
            exif_data = ExifGuard.analyze_metadata(file_path)
            robustness = RobustnessEvaluator.test_jpeg_resilience(file_path)
            
            risk_score = UnifiedDetector._calculate_image_risk(ai_data, exif_data, robustness)
            
            risk_info = classify_risk(risk_score)
            forgery_type = ai_data.get("model_name", "Unknown")
            risk_summary = get_risk_summary(risk_info, forgery_type)
            
            result = {
                "ai_analysis": ai_data,
                "forensic_metadata": exif_data,
                "robustness_eval": robustness,
                "selected_model": model_type,
                "selected_dataset": dataset,
                "risk_score": risk_score,
                "risk_level": risk_info["label"],
                "risk_color": risk_info["color"],
                "risk_description": risk_info["description"],
                "risk_summary": risk_summary,
                "forgery_type": forgery_type,
                "modality_details": {
                    "type": "Image",
                    "format": file_path.split('.')[-1].upper(),
                    "threshold": threshold
                }
            }
            
        elif modality == "VIDEO":
            if cross_modal:
                # 多模态融合
                fusion_result = CrossModalFusion.detect_video_with_audio(
                    file_path, fps=fps, sample_rate=sample_rate
                )
                
                video_data = fusion_result["video_analysis"]
                audio_data = fusion_result["audio_analysis"]
                risk_score = video_data.get("risk_level", 0)
                
                if fusion_result["is_compound_forgery"]:
                    risk_score = min(100, risk_score * 1.3)
                
                risk_info = classify_risk(risk_score)
                forgery_type = fusion_result.get("cross_modal_note", "Unknown")
                risk_summary = get_risk_summary(risk_info, forgery_type)
                
                result = {
                    "ai_analysis": video_data,
                    "audio_analysis": audio_data,
                    "cross_modal": {
                        "enabled": True,
                        "combined_confidence": fusion_result["combined_confidence"],
                        "cross_modal_note": fusion_result["cross_modal_note"],
                        "is_compound_forgery": fusion_result["is_compound_forgery"],
                        "fusion_model": fusion_result["model_name"]
                    },
                    "selected_model": model_type,
                    "selected_dataset": dataset,
                    "risk_score": round(risk_score, 2),
                    "risk_level": risk_info["label"],
                    "risk_color": risk_info["color"],
                    "risk_description": risk_info["description"],
                    "risk_summary": risk_summary,
                    "forgery_type": forgery_type,
                    "modality_details": {
                        "type": "Video",
                        "format": file_path.split('.')[-1].upper(),
                        "fps": fps,
                        "cross_modal_fusion": True
                    }
                }
            else:
                video_data = VideoForensicsEngine.temporal_consistency_check(file_path, fps=fps)
                risk_score = video_data.get("risk_level", 0)
                risk_info = classify_risk(risk_score)
                forgery_type = video_data.get("forgery_type", "None")
                risk_summary = get_risk_summary(risk_info, forgery_type)
                
                result = {
                    "ai_analysis": video_data,
                    "cross_modal": {"enabled": False},
                    "selected_model": model_type,
                    "selected_dataset": dataset,
                    "risk_score": risk_score,
                    "risk_level": risk_info["label"],
                    "risk_color": risk_info["color"],
                    "risk_description": risk_info["description"],
                    "risk_summary": risk_summary,
                    "forgery_type": forgery_type,
                    "modality_details": {
                        "type": "Video",
                        "format": file_path.split('.')[-1].upper(),
                        "fps": fps,
                        "cross_modal_fusion": False
                    }
                }
                
        elif modality == "AUDIO":
            audio_data = AudioForensicsEngine.spectral_check(file_path, sample_rate=sample_rate)
            risk_score = audio_data.get("risk_level", 0)
            risk_info = classify_risk(risk_score)
            forgery_type = audio_data.get("forgery_type", "None")
            risk_summary = get_risk_summary(risk_info, forgery_type)
            
            result = {
                "ai_analysis": audio_data,
                "selected_model": model_type,
                "selected_dataset": dataset,
                "risk_score": risk_score,
                "risk_level": risk_info["label"],
                "risk_color": risk_info["color"],
                "risk_description": risk_info["description"],
                "risk_summary": risk_summary,
                "forgery_type": forgery_type,
                "modality_details": {
                    "type": "Audio",
                    "format": file_path.split('.')[-1].upper(),
                    "sample_rate": sample_rate
                }
            }
        
        # 生成证据链
        evidence = EvidenceChain.archive(file_path, {
            "modality": modality,
            "payload": result
        })
        
        report_path = None
        try:
            os.makedirs("reports", exist_ok=True)
            report_filename = f"report_{evidence['evidence_id']}.pdf"
            report_path = os.path.join("reports", report_filename)
            ForensicReporter.generate_pdf(evidence, report_path)
        except Exception as e:
            print(f"Warning: Failed to generate PDF report: {str(e)}")
            report_path = None
        
        return {
            "status": "SECURE_SCAN_COMPLETED",
            "evidence_id": evidence['evidence_id'],
            "modality": modality,
            "payload": result,
            "report_path": report_path,
            "timestamp": evidence['timestamp']
        }
    
    @staticmethod
    def _calculate_image_risk(ai_data, exif_data, robustness):
        score = 0
        
        # AI 置信度贡献 (40%)
        ai_confidence = ai_data.get("confidence", 0)
        score += ai_confidence * 40
        
        # EXIF 异常贡献 (30%)
        suspicious_flags = exif_data.get("suspicious_flags", [])
        score += min(30, len(suspicious_flags) * 10)
        
        # 对抗鲁棒性贡献 (30%)
        stability = robustness.get("stability_score", 1.0)
        score += (1 - stability) * 30
        
        return round(min(100, score), 2)