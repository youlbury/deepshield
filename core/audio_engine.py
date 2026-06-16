import librosa
import numpy as np

class AudioForensicsEngine:
    @staticmethod
    def spectral_check(audio_path, sample_rate=16000):
        try:
            y, sr = librosa.load(audio_path, sr=sample_rate)
            duration = len(y) / sr
            
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            mfcc_std = np.std(mfccs, axis=1)
            
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            centroid_var = float(np.var(spectral_centroid))
            centroid_mean = float(np.mean(spectral_centroid))
            
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            zcr_var = float(np.var(zcr))
            
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            contrast_mean = float(np.mean(contrast))
            
            # 5. 谐波-噪声比 (HNR) - 新增特征
            try:
                hnr = librosa.effects.harmonic(y)
                hnr_ratio = float(np.mean(np.abs(hnr) / (np.abs(y) + 1e-8)))
            except:
                hnr_ratio = 0.0
            
            # 综合判定逻辑
            anomalies = []
            
            if centroid_var < 500:
                anomalies.append(f"Low spectral variance ({centroid_var:.2f} < 500)")
            
            if zcr_var > 0.1:
                anomalies.append(f"Abnormal zero-crossing rate ({zcr_var:.4f} > 0.1)")
            
            if np.mean(mfcc_std) < 0.5:
                anomalies.append(f"Unnatural MFCC stability ({np.mean(mfcc_std):.4f} < 0.5)")
            
            if hnr_ratio > 0.8 or hnr_ratio < 0.2:
                anomalies.append(f"Abnormal HNR ratio ({hnr_ratio:.4f})")
            
            # 计算综合置信度
            confidence_score = 0
            confidence_score += min(0.4, 500 / (centroid_var + 1) * 0.4)
            confidence_score += min(0.3, zcr_var * 3)
            confidence_score += min(0.2, (1 - np.mean(mfcc_std)) * 0.3)
            confidence_score += min(0.1, abs(0.5 - hnr_ratio) * 0.2)
            
            is_fake = len(anomalies) >= 2 or confidence_score > 0.6
            
            forgery_type = "None"
            if is_fake:
                if "Low spectral variance" in anomalies[0] if anomalies else False:
                    forgery_type = "TTS Synthesis (文本转语音合成)"
                elif "Abnormal zero-crossing rate" in anomalies[0] if anomalies else False:
                    forgery_type = "Audio Splicing (音频拼接)"
                elif "Abnormal HNR" in str(anomalies):
                    forgery_type = "Voice Cloning (语音克隆)"
                else:
                    forgery_type = "AI Generated Audio (AI生成音频)"
            
            return {
                "is_synthetic": bool(is_fake),
                "confidence": round(min(0.99, confidence_score), 4),
                "spectral_variance": round(centroid_var, 2),
                "zero_crossing_var": round(zcr_var, 4),
                "mfcc_stability": round(float(np.mean(mfcc_std)), 4),
                "hnr_ratio": round(hnr_ratio, 4),
                "duration_seconds": round(duration, 2),
                "sample_rate": sample_rate,
                "anomalies": anomalies,
                "forgery_type": forgery_type,
                "risk_level": AudioForensicsEngine._calculate_risk_level(confidence_score, len(anomalies)),
                "model_name": "Spectral-Guard-MultiFeature"
            }
        except Exception as e:
            import traceback
            print(f"Audio analysis error: {str(e)}")
            print(traceback.format_exc())
            return {
                "error": str(e),
                "is_synthetic": False,
                "confidence": 0.0,
                "anomalies": [f"Analysis failed: {str(e)}"],
                "model_name": "Spectral-Guard-MultiFeature",
                "risk_level": 0
            }
    
    @staticmethod
    def _calculate_risk_level(confidence, anomaly_count):
        score = confidence * 70
        score += min(30, anomaly_count * 10)
        return round(min(100, score), 2)