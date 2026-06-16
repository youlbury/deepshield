import cv2
import numpy as np
import os
from core.image_engine import ImageForensicsEngine

class VideoForensicsEngine:
    @staticmethod
    def temporal_consistency_check(video_path, fps=10):
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        if total_frames == 0: return {"error": "Invalid video"}

        if video_fps > 0:
            step = max(1, int(video_fps / fps))
        else:
            step = max(1, total_frames // 50)
        
        sample_frames = min(50, total_frames // step + 1)
        confidences = []
        frame_indices = []
        
        for i in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                temp_path = f"temp_frame_{i}.jpg"
                cv2.imwrite(temp_path, frame)
                res = ImageForensicsEngine.run_deep_scan(temp_path, model_type="hifi")
                confidences.append(res['confidence'])
                frame_indices.append(i)
                if os.path.exists(temp_path): os.remove(temp_path)
            
            if len(confidences) >= sample_frames:
                break

        cap.release()
        
        std_dev = np.std(confidences) if confidences else 0
        avg_confidence = np.mean(confidences) if confidences else 0
        
        jumps = []
        for i in range(1, len(confidences)):
            jump = abs(confidences[i] - confidences[i-1])
            jumps.append(jump)
        max_jump = max(jumps) if jumps else 0
        
        # 综合判定
        is_synthetic = avg_confidence > 0.5 or std_dev > 0.3 or max_jump > 0.4
        
        forgery_type = "None"
        anomalies = []
        if is_synthetic:
            if std_dev > 0.3:
                forgery_type = "Temporal Inconsistency (时序不一致)"
                anomalies.append(f"时序不稳定性: {std_dev:.4f} (>0.3)")
            elif max_jump > 0.4:
                forgery_type = "Frame Insertion/Deletion (帧插入/删除)"
                anomalies.append(f"最大帧间跳变: {max_jump:.4f} (>0.4)")
            else:
                forgery_type = "Deepfake Generation (深度伪造生成)"
                anomalies.append(f"平均置信度: {avg_confidence:.4f} (>0.5)")
        else:
            anomalies.append("未检测到明显时序异常")
        
        return {
            "is_synthetic": bool(is_synthetic),
            "avg_confidence": round(avg_confidence, 4),
            "temporal_instability": round(std_dev, 4),
            "max_frame_jump": round(max_jump, 4),
            "frames_analyzed": len(confidences),
            "total_frames": total_frames,
            "video_fps": round(video_fps, 2),
            "sample_fps": fps,
            "forgery_type": forgery_type,
            "anomalies": anomalies,
            "risk_level": VideoForensicsEngine._calculate_risk_level(avg_confidence, std_dev, max_jump)
        }
    
    @staticmethod
    def _calculate_risk_level(confidence, instability, jump):
        score = 0
        score += min(50, confidence * 50)
        score += min(30, instability * 100)
        score += min(20, jump * 50)
        return round(min(100, score), 2)