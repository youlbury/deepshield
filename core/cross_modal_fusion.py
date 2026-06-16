class CrossModalFusion:

    @staticmethod
    def detect_video_with_audio(video_path, fps=10, sample_rate=16000):
        from core.video_engine import VideoForensicsEngine
        from core.audio_engine import AudioForensicsEngine

        video_result = VideoForensicsEngine.temporal_consistency_check(video_path, fps=fps)
        audio_result = AudioForensicsEngine.spectral_check(video_path, sample_rate=sample_rate)


        video_conf = video_result.get("avg_confidence", 0)
        audio_conf = audio_result.get("confidence", 0)

        # 融合策略
        combined_confidence = max(video_conf, audio_conf)
        is_compound = False
        cross_modal_note = ""

        if video_conf > 0.5 and audio_conf > 0.5:
            # 双模态均异常 → 复合型伪造
            combined_confidence = min(0.99, combined_confidence * 1.2)
            is_compound = True
            cross_modal_note = "复合型伪造：画面+音频双重异常，疑似AI换脸+AI配音组合攻击"
        elif video_conf > 0.5 and audio_conf <= 0.3:
            cross_modal_note = "画面异常但音频正常，疑似视频换脸/帧篡改"
        elif audio_conf > 0.5 and video_conf <= 0.3:
            cross_modal_note = "音频异常但画面正常，疑似后期AI配音/音频拼接"
        elif abs(video_conf - audio_conf) > 0.4:
            cross_modal_note = "音画不一致：置信度差异显著，疑似后期配音或画面替换"
            combined_confidence = max(video_conf, audio_conf) * 1.1
        else:
            cross_modal_note = "音画一致性正常，未发现跨模态异常"

        return {
            "combined_confidence": round(min(0.99, combined_confidence), 4),
            "video_analysis": video_result,
            "audio_analysis": audio_result,
            "cross_modal_note": cross_modal_note,
            "is_compound_forgery": is_compound,
            "fusion_strategy": "attention_weighted",
            "model_name": "CrossModal-Fusion-Detector"
        }


