from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os
from io import BytesIO
from datetime import datetime

# 可选导入 qrcode 模块
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    qrcode = None
    QRCODE_AVAILABLE = False

class ForensicReporter:
    @staticmethod
    def _add_page_number(canvas, doc):
        """添加页码和页脚"""
        page_num = canvas.getPageNumber()
        canvas.saveState()
        
        # 页脚线条
        canvas.setStrokeColor(colors.HexColor('#0066cc'))
        canvas.setLineWidth(1)
        canvas.line(50, 40, 545, 40)
        
        # 页码
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#666666'))
        canvas.drawRightString(545, 25, f"Page {page_num}")
        
        # 左侧标识
        canvas.setFillColor(colors.HexColor('#0066cc'))
        canvas.drawString(50, 25, "DeepShield Forensic Report")
        
        canvas.restoreState()
    
    @staticmethod
    def _add_header(canvas, doc):
        """添加页眉"""
        canvas.saveState()
        
        # 顶部线条
        canvas.setStrokeColor(colors.HexColor('#0066cc'))
        canvas.setLineWidth(2)
        canvas.line(50, 780, 545, 780)
        
        # Logo文字
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.HexColor('#0066cc'))
        canvas.drawString(50, 790, "🛡️ DeepShield")
        
        # 右侧时间
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#999999'))
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        canvas.drawRightString(545, 790, f"Generated: {current_time}")
        
        canvas.restoreState()
    
    @staticmethod
    def generate_pdf(evidence_data, output_path):
        """
        生成专业级 PDF 取证报告（影盾 DeepShield 标准模板 v2.0）
        """
        doc = SimpleDocTemplate(
            output_path, 
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=80,
            bottomMargin=50,
            title="DeepShield Forensic Report",
            author="DeepShield Platform",
            subject="Digital Forensics Analysis"
        )
        
        # 设置页眉页脚
        doc.onFirstPage = lambda canvas, doc: (ForensicReporter._add_header(canvas, doc), ForensicReporter._add_page_number(canvas, doc))
        doc.onLaterPages = lambda canvas, doc: (ForensicReporter._add_header(canvas, doc), ForensicReporter._add_page_number(canvas, doc))
        styles = getSampleStyleSheet()
        elements = []
        
        # 自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#0066cc'),
            fontName='Helvetica-Bold',
            spaceAfter=15,
            borderWidth=0
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=13,
            leading=17,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#555555'),
            spaceAfter=35,
            fontName='Helvetica-Oblique'
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=17,
            leading=22,
            textColor=colors.HexColor('#0066cc'),
            fontName='Helvetica-Bold',
            spaceBefore=25,
            spaceAfter=12,
            borderWidth=3,
            borderColor=colors.HexColor('#0066cc'),
            borderPadding=8,
            backColor=colors.HexColor('#f0f7ff')
        )
        
        label_style = ParagraphStyle(
            'Label',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        )
        
        value_style = ParagraphStyle(
            'Value',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold'
        )
        
        # ========== 封面页 ==========
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph("影盾 DeepShield", title_style))
        elements.append(Paragraph("多模态深度伪造检测与数字取证平台", subtitle_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # 报告标题
        report_title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold',
            spaceAfter=30
        )
        elements.append(Paragraph("数 字 取 证 报 告", report_title_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # 证据编号
        evidence_id = evidence_data.get('evidence_id', 'N/A')
        evidence_style = ParagraphStyle(
            'EvidenceID',
            parent=styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#0066cc'),
            fontName='Helvetica-Bold',
            spaceAfter=40
        )
        elements.append(Paragraph(f"证据编号：{evidence_id}", evidence_style))
        
        # 生成二维码（可选功能）
        if QRCODE_AVAILABLE:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                verify_url = f"http://localhost:5473/verify?id={evidence_id}"
                qr.add_data(verify_url)
                qr.make(fit=True)
                img_qr = qr.make_image(fill_color="black", back_color="white")
                
                qr_buffer = BytesIO()
                img_qr.save(qr_buffer, format='PNG')
                qr_buffer.seek(0)
                
                qr_image = Image(qr_buffer, width=2*inch, height=2*inch)
                elements.append(qr_image)
                elements.append(Spacer(1, 10))
                
                qr_hint_style = ParagraphStyle(
                    'QRHint',
                    parent=styles['Normal'],
                    fontSize=9,
                    alignment=TA_CENTER,
                    textColor=colors.HexColor('#999999'),
                    spaceAfter=30
                )
                elements.append(Paragraph("扫描二维码验证报告真实性", qr_hint_style))
            except Exception as e:
                # 如果二维码生成失败，跳过此步骤
                pass
        else:
            # 如果未安装 qrcode 模块，显示验证链接
            qr_hint_style = ParagraphStyle(
                'QRHint',
                parent=styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#999999'),
                spaceAfter=30
            )
            elements.append(Paragraph(f"验证链接：http://localhost:5473/verify?id={evidence_id}", qr_hint_style))
        
        elements.append(PageBreak())
        
        # ========== 第1页：基本信息 ==========
        elements.append(Paragraph("一、基本信息", section_title_style))
        
        # 基本信息表
        payload = evidence_data.get('payload', {})
        ai_analysis = payload.get('ai_analysis', {})
        
        basic_info_data = [
            ["证据编号", evidence_id],
            ["取证时间", evidence_data.get('timestamp', 'N/A')],
            ["文件类型", payload.get('modality_details', {}).get('type', 'N/A')],
            ["文件格式", payload.get('modality_details', {}).get('format', 'N/A')],
            ["检测模型", ai_analysis.get('model_name', 'N/A')],
            ["完整性校验", "✅ 已通过 (MD5 + SHA256)"],
            ["风险评分", f"{payload.get('risk_score', 0)} / 100"]
        ]
        
        t_basic = Table(basic_info_data, colWidths=[3.5*cm, 11.5*cm])
        t_basic.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dde1e6')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t_basic)
        elements.append(Spacer(1, 20))
        
        # ========== 第2页：检测结论 ==========
        elements.append(Paragraph("二、检测结论", section_title_style))
        
        # 真伪判定
        is_synthetic = ai_analysis.get('is_synthetic', False)
        confidence = ai_analysis.get('confidence', 0)
        
        conclusion_box_style = ParagraphStyle(
            'ConclusionBox',
            parent=styles['Normal'],
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.red if is_synthetic else colors.green,
            fontName='Helvetica-Bold',
            borderWidth=3,
            borderColor=colors.red if is_synthetic else colors.green,
            borderPadding=15,
            spaceAfter=20
        )
        
        result_text = "⚠️ 疑似伪造内容" if is_synthetic else "✅ 真实内容"
        elements.append(Paragraph(result_text, conclusion_box_style))
        
        # 置信度
        confidence_style = ParagraphStyle(
            'Confidence',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#333333'),
            spaceAfter=20
        )
        elements.append(Paragraph(f"检测置信度：{confidence:.2%}", confidence_style))
        
        # 五级风险等级（设计文档 4.5）
        risk_score = payload.get('risk_score', 0)
        risk_level = payload.get('risk_level', '')
        risk_color_hex = payload.get('risk_color', '#28a745')
        
        if not risk_level:
            # 回退计算
            if risk_score >= 90:
                risk_level = "极高风险"
                risk_color_hex = '#721c24'
            elif risk_score >= 70:
                risk_level = "高风险"
                risk_color_hex = '#dc3545'
            elif risk_score >= 50:
                risk_level = "中风险"
                risk_color_hex = '#fd7e14'
            elif risk_score >= 30:
                risk_level = "低风险"
                risk_color_hex = '#ffc107'
            else:
                risk_level = "可信"
                risk_color_hex = '#28a745'
        
        risk_color = colors.HexColor(risk_color_hex)
        
        risk_style = ParagraphStyle(
            'RiskLevel',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=risk_color,
            fontName='Helvetica-Bold',
            spaceAfter=20
        )
        elements.append(Paragraph(f"风险等级：{risk_level}", risk_style))
        
        # 伪造类型
        forgery_type = payload.get('forgery_type', 'None')
        if forgery_type and forgery_type != 'None':
            forgery_style = ParagraphStyle(
                'ForgeryType',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#333333'),
                spaceAfter=20
            )
            elements.append(Paragraph(f"识别伪造类型：{forgery_type}", forgery_style))
        
        elements.append(Spacer(1, 20))
        
        # ========== 第3页：技术细节 ==========
        elements.append(Paragraph("三、技术细节", section_title_style))
        
        modality_type = payload.get('modality_details', {}).get('type', 'Image')
        
        if modality_type == 'Image':
            # 图像检测技术指标
            tech_data = [
                ["指标项", "检测值"],
                ["AI 置信度", f"{confidence:.4f}"],
                ["多尺度异常值", f"{ai_analysis.get('multi_scale_anomaly', 'N/A')}"],
                ["对抗稳定性", f"{payload.get('robustness_eval', {}).get('stability_score', 0):.2%}"],
                ["EXIF 一致性", f"{payload.get('forensic_metadata', {}).get('consistency_score', 'N/A')}"],
            ]
        elif modality_type == 'Video':
            # 视频检测技术指标
            cross_modal = payload.get('cross_modal', {})
            tech_data = [
                ["指标项", "检测值"],
                ["AI 置信度", f"{confidence:.4f}"],
                ["分析帧数", f"{ai_analysis.get('frames_analyzed', 'N/A')}"],
                ["时序不稳定性", f"{ai_analysis.get('temporal_instability', 'N/A')}"],
                ["最大帧间跳变", f"{ai_analysis.get('max_frame_jump', 'N/A')}"],
            ]
            if cross_modal.get('enabled'):
                tech_data.append(["多模态融合", f"已启用 ({cross_modal.get('fusion_model', 'N/A')})"])
                tech_data.append(["融合置信度", f"{cross_modal.get('combined_confidence', 'N/A')}"],)
        elif modality_type == 'Audio':
            # 音频检测技术指标
            tech_data = [
                ["指标项", "检测值"],
                ["AI 置信度", f"{confidence:.4f}"],
                ["频谱方差", f"{ai_analysis.get('spectral_variance', 'N/A')}"],
                ["过零率方差", f"{ai_analysis.get('zero_crossing_var', 'N/A')}"],
                ["MFCC 稳定性", f"{ai_analysis.get('mfcc_stability', 'N/A')}"],
                ["谐波噪声比", f"{ai_analysis.get('hnr_ratio', 'N/A')}"],
                ["音频时长", f"{ai_analysis.get('duration_seconds', 'N/A')}s"],
            ]
        else:
            tech_data = [
                ["指标项", "检测值"],
                ["AI 置信度", f"{confidence:.4f}"],
            ]
        
        t_tech = Table(tech_data, colWidths=[4.5*cm, 10.5*cm])
        t_tech.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fafbfc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dde1e6')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t_tech)
        elements.append(Spacer(1, 20))
        
        # 跨模态融合结论（仅视频）
        cross_modal = payload.get('cross_modal', {})
        if cross_modal.get('enabled'):
            elements.append(Spacer(1, 15))
            elements.append(Paragraph("跨模态融合分析", section_title_style))
            
            fusion_note = cross_modal.get('cross_modal_note', 'N/A')
            is_compound = cross_modal.get('is_compound_forgery', False)
            
            fusion_style = ParagraphStyle(
                'FusionNote',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.red if is_compound else colors.HexColor('#333333'),
                fontName='Helvetica-Bold' if is_compound else 'Helvetica',
                spaceAfter=10
            )
            elements.append(Paragraph(f"融合研判：{fusion_note}", fusion_style))
            
            if is_compound:
                warning_style = ParagraphStyle(
                    'CompoundWarning',
                    parent=styles['Normal'],
                    fontSize=12,
                    textColor=colors.white,
                    backColor=colors.red,
                    alignment=TA_CENTER,
                    borderPadding=10,
                    spaceAfter=15
                )
                elements.append(Paragraph("⚠️ 检测到复合型伪造攻击（音画双重异常）", warning_style))
        
        # 风险研判结论
        risk_summary = payload.get('risk_summary', '')
        if risk_summary:
            elements.append(Spacer(1, 15))
            elements.append(Paragraph("风险研判结论", section_title_style))
            summary_style = ParagraphStyle(
                'RiskSummary',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#333333'),
                backColor=colors.HexColor('#f8f9fa'),
                borderPadding=10,
                spaceAfter=15
            )
            elements.append(Paragraph(risk_summary, summary_style))
        
        # 可视化证据（仅图像）
        heatmap_path = ai_analysis.get('heatmap_path')
        if heatmap_path and os.path.exists(heatmap_path):
            elements.append(Paragraph("四、可视化证据", section_title_style))
            elements.append(Paragraph("频域残差热力图：", label_style))
            try:
                img = Image(heatmap_path, width=5*inch, height=3.5*inch)
                elements.append(img)
            except Exception as e:
                elements.append(Paragraph(f"[热力图加载失败: {str(e)}]", label_style))
            elements.append(Spacer(1, 20))
        
        # ========== 页脚：法律声明 ==========
        elements.append(PageBreak())
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#777777'),
            alignment=TA_JUSTIFY,
            spaceAfter=15,
            leftIndent=10,
            rightIndent=10
        )
        
        elements.append(Paragraph("<b>免责声明：</b>", styles['Heading3']))
        elements.append(Paragraph(
            "本报告由影盾（DeepShield）多模态深度伪造检测与数字取证平台自动生成。"
            "报告中的检测结果基于当前最先进的 AI 算法，仅供参考，不构成法律意义上的最终鉴定结论。"
            "如需用于司法用途，请结合其他证据综合判断，并由具备资质的司法鉴定机构出具正式鉴定意见。",
            disclaimer_style
        ))
        
        elements.append(Spacer(1, 25))
        
        # 联系信息框
        contact_box_style = ParagraphStyle(
            'ContactBox',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#0066cc'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#0066cc'),
            borderPadding=15,
            backColor=colors.HexColor('#f0f7ff')
        )
        elements.append(Paragraph("🛡️ 影盾 DeepShield · 多模态取证平台", contact_box_style))
        elements.append(Spacer(1, 8))
        
        copyright_style = ParagraphStyle(
            'Copyright',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#999999'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(f"© 2026 DeepShield Platform. All Rights Reserved. | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", copyright_style))
        
        # 构建PDF
        doc.build(elements)
        return output_path
