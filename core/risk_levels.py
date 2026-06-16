
RISK_LEVELS = {
    "trusted": {
        "range": (0, 30),
        "label": "可信",
        "label_en": "Trusted",
        "color": "#28a745",
        "color_name": "绿色",
        "description": "无明显伪造特征，内容为原生文件",
        "action": "无需处理"
    },
    "low": {
        "range": (30, 50),
        "label": "低风险",
        "label_en": "Low Risk",
        "color": "#ffc107",
        "color_name": "黄色",
        "description": "疑似轻微编辑、局部可疑特征，无恶意风险",
        "action": "建议人工复核"
    },
    "medium": {
        "range": (50, 70),
        "label": "中风险",
        "label_en": "Medium Risk",
        "color": "#fd7e14",
        "color_name": "橙色",
        "description": "明确局部篡改、简单拼接，存在误导风险",
        "action": "需要进一步验证"
    },
    "high": {
        "range": (70, 90),
        "label": "高风险",
        "label_en": "High Risk",
        "color": "#dc3545",
        "color_name": "红色",
        "description": "大面积伪造、核心内容篡改，存在舆情风险",
        "action": "强烈建议阻断传播"
    },
    "critical": {
        "range": (90, 100),
        "label": "极高风险",
        "label_en": "Critical Risk",
        "color": "#721c24",
        "color_name": "深红色",
        "description": "全文件AI生成、人脸/语音克隆，存在诈骗、抹黑等高危害风险",
        "action": "立即阻断并报警"
    }
}


def classify_risk(score):
    score = max(0, min(100, float(score)))

    for level_key, info in RISK_LEVELS.items():
        low, high = info["range"]
        if low <= score < high:
            return {
                "level": level_key,
                "label": info["label"],
                "label_en": info["label_en"],
                "color": info["color"],
                "color_name": info["color_name"],
                "description": info["description"],
                "action": info["action"],
                "score": score
            }

    # score == 100 归入 critical
    critical = RISK_LEVELS["critical"]
    return {
        "level": "critical",
        "label": critical["label"],
        "label_en": critical["label_en"],
        "color": critical["color"],
        "color_name": critical["color_name"],
        "description": critical["description"],
        "action": critical["action"],
        "score": score
    }


def get_risk_summary(risk_info, forgery_type="None"):
    label = risk_info["label"]
    score = risk_info["score"]
    desc = risk_info["description"]
    action = risk_info["action"]

    summary = f"【{label}】风险评分 {score}/100。"
    summary += f"{desc}。"

    if forgery_type and forgery_type != "None":
        summary += f"识别伪造类型：{forgery_type}。"

    summary += f"建议处置：{action}。"

    return summary


def get_all_levels():
    return [
        {
            "level": key,
            "label": info["label"],
            "range": f"{info['range'][0]}% ~ {info['range'][1]}%",
            "color": info["color"],
            "color_name": info["color_name"],
            "description": info["description"]
        }
        for key, info in RISK_LEVELS.items()
    ]
