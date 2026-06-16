from PIL import Image

class ExifGuard:
    @staticmethod
    def analyze_metadata(image_path):
        try:
            img = Image.open(image_path)
            exif = img._getexif()
            flags = []
            
            if exif:
                # 0x0131 是 Software 标签
                software = exif.get(0x0131, "")
                if "photoshop" in str(software).lower():
                    flags.append("Detected Photoshop Editing")
                
                # 0x010F 是 Make (相机制造商)
                if not exif.get(0x010F): 
                    flags.append("Missing Camera Manufacturer Info")
            
            return {
                "has_exif": bool(exif),
                "suspicious_flags": flags,
                "consistency_score": 1.0 if len(flags) == 0 else 0.6
            }
        except Exception as e:
            return {"error": f"Metadata extraction failed: {str(e)}"}
