import cv2
import numpy as np
import os

class ImageForensicsEngine:
    @staticmethod
    def compute_laplacian_pyramid(image_path, levels=3):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None: return 0.0, None
        
        pyramid_residuals = []
        current_img = img.astype(np.float32)
        
        for i in range(levels):
            blurred = cv2.GaussianBlur(current_img, (5, 5), 0)
            residual = cv2.absdiff(current_img, blurred)
            pyramid_residuals.append(residual)
            # 降采样进入下一层
            current_img = cv2.resize(current_img, (current_img.shape[1]//2, current_img.shape[0]//2))
        
        # 融合多尺度残差
        fused_residual = np.zeros_like(img, dtype=np.float32)
        for res in pyramid_residuals:
            resized_res = cv2.resize(res, (img.shape[1], img.shape[0]))
            fused_residual += resized_res
        
        anomaly_score = float(np.mean(fused_residual))
        return anomaly_score, fused_residual

    @staticmethod
    def generate_heatmap(residual_map):
        if residual_map is None: return None
        norm_map = cv2.normalize(residual_map, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = cv2.applyColorMap(norm_map.astype(np.uint8), cv2.COLORMAP_JET)
        return heatmap

    @staticmethod
    def run_deep_scan(image_path, model_type="hifi"):
        if model_type == "hifi":
            freq_score, residual_map = ImageForensicsEngine.compute_laplacian_pyramid(image_path)
            is_synthetic = freq_score > 10.0 
            confidence = min(0.99, freq_score / 12.0) if is_synthetic else max(0.01, 1.0 - (freq_score / 15.0))
            
            # 保存热力图用于取证报告
            heatmap_path = None
            if residual_map is not None:
                try:
                    os.makedirs("reports", exist_ok=True)
                    heatmap = ImageForensicsEngine.generate_heatmap(residual_map)
                    heatmap_path = os.path.join("reports", f"heatmap_{os.path.basename(image_path)}")
                    cv2.imwrite(heatmap_path, heatmap)
                except Exception as e:
                    print(f"Warning: Failed to save heatmap: {str(e)}")
            
            return {
                "is_synthetic": bool(is_synthetic),
                "confidence": round(confidence, 4),
                "multi_scale_anomaly": round(freq_score, 2),
                "heatmap_path": heatmap_path,
                "model_name": "HiFi-Net-MultiScale-Pyramid"
            }
        
        elif model_type == "cnnd":
            # CNND 风格检测（多尺度特征）
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return {"error": "无法读取图像", "model_name": "CNND-MultiScale"}
            
            scales = [3, 5, 7]
            anomalies = []
            
            for kernel_size in scales:
                blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
                residual = cv2.absdiff(img, blurred)
                anomalies.append(float(np.mean(residual)))
            
            avg_anomaly = np.mean(anomalies)
            is_fake = avg_anomaly > 10.0
            confidence = min(0.99, avg_anomaly / 18.0) if is_fake else max(0.01, 1.0 - (avg_anomaly / 25.0))
            
            return {
                "is_synthetic": bool(is_fake),
                "confidence": round(confidence, 4),
                "multi_scale_scores": [round(a, 2) for a in anomalies],
                "model_name": "CNND-MultiScale"
            }
        
        elif model_type == "exif":
            # EXIF 元数据分析
            from PIL import Image as PILImage
            
            try:
                img = PILImage.open(image_path)
                exif_data = img._getexif()
                
                suspicious_flags = []
                
                if exif_data:
                    software = exif_data.get(0x0131, "")
                    if "photoshop" in str(software).lower():
                        suspicious_flags.append("Photoshop detected")
                    
                    if not exif_data.get(0x010F):
                        suspicious_flags.append("Missing camera info")
                    
                    if exif_data.get(0x0132):
                        suspicious_flags.append("Modified timestamp found")
                
                has_suspicious = len(suspicious_flags) > 0
                confidence = min(0.95, 0.5 + len(suspicious_flags) * 0.15) if has_suspicious else 0.1
                
                return {
                    "is_synthetic": has_suspicious,
                    "confidence": round(confidence, 4),
                    "suspicious_flags": suspicious_flags,
                    "model_name": "EXIF-Forensics"
                }
            except Exception as e:
                return {
                    "is_synthetic": False,
                    "confidence": 0.0,
                    "error": str(e),
                    "model_name": "EXIF-Forensics"
                }
        
        else:
            # 默认使用 HiFi-Net
            return ImageForensicsEngine.run_deep_scan(image_path, model_type="hifi")