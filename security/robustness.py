import io
from PIL import Image
from core.image_engine import ImageForensicsEngine
import os

class RobustnessEvaluator:
    @staticmethod
    def test_jpeg_resilience(image_path):
        try:
            # 原始检测
            original_res = ImageForensicsEngine.run_deep_scan(image_path)
            
            img = Image.open(image_path)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=50)
            buffer.seek(0)
            
            temp_path = "temp_attack.jpg"
            with open(temp_path, 'wb') as f: 
                f.write(buffer.read())
            
            attacked_res = ImageForensicsEngine.run_deep_scan(temp_path)
            if os.path.exists(temp_path): os.remove(temp_path)
            
            stability_score = 1.0 - abs(original_res['confidence'] - attacked_res['confidence'])
            
            return {
                "attack_type": "JPEG_Compression_Q50",
                "stability_score": round(stability_score, 4),
                "original_conf": original_res['confidence'],
                "attacked_conf": attacked_res['confidence']
            }
        except Exception as e:
            return {"error": str(e)}
