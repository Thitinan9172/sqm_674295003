from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Image as RLImage)

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Lab01_674295003_ฐิตินันท์-คงไสยะ.pdf"
FONT = r"C:\Windows\Fonts\LeelawUI.ttf"
pdfmetrics.registerFont(TTFont("Leelawadee", FONT))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ThaiTitle", parent=styles["Title"], fontName="Leelawadee", fontSize=20, leading=29, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="ThaiHead", parent=styles["Heading1"], fontName="Leelawadee", fontSize=15, leading=21, textColor=colors.HexColor("#17365D"), spaceBefore=10, spaceAfter=7))
styles.add(ParagraphStyle(name="ThaiSub", parent=styles["Heading2"], fontName="Leelawadee", fontSize=12, leading=18, textColor=colors.HexColor("#17365D"), spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="ThaiBody", parent=styles["BodyText"], fontName="Leelawadee", fontSize=10.5, leading=17, alignment=TA_LEFT, spaceAfter=7))
styles.add(ParagraphStyle(name="ThaiSmall", parent=styles["BodyText"], fontName="Leelawadee", fontSize=8.7, leading=12.5))

def p(text, style="ThaiBody"):
    return Paragraph(text, styles[style])

def heading(text):
    return p(text, "ThaiHead")

def table(rows, widths):
    formatted = [[p(cell, "ThaiSmall") for cell in row] for row in rows]
    t = Table(formatted, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B4C6E7")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7FAFF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t

def evidence_image(filename, width):
    path = ROOT / "evidence" / filename
    image = RLImage(str(path))
    ratio = image.imageHeight / image.imageWidth
    image.drawWidth = width
    image.drawHeight = width * ratio
    return image

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Leelawadee", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm, f"Lab 1 | การจัดการคุณภาพซอฟต์แวร์ | หน้า {doc.page}")
    canvas.restoreState()

story = [
    Spacer(1, 3.5 * cm),
    p("รายงาน Lab 1", "ThaiTitle"),
    p("วิเคราะห์กรณีความล้มเหลวของซอฟต์แวร์", "ThaiTitle"),
    Spacer(1, 1.0 * cm),
    p("กรณีศึกษา: Knight Capital Group - เหตุขัดข้องของระบบซื้อขายหลักทรัพย์", "ThaiHead"),
    Spacer(1, 1.0 * cm),
    p("รายวิชา 4663335 การจัดการคุณภาพซอฟต์แวร์"),
    p("รหัสนักศึกษา: 674295003"),
    p("ชื่อ-สกุล: ฐิตินันท์ คงไสยะ"),
    p("GitHub: https://github.com/Thitinan9172/sqm_674295003"),
    PageBreak(),
    heading("1. สรุปเหตุการณ์และผลกระทบ"),
    p("วันที่ 1 สิงหาคม 2012 Knight Capital Americas LLC ปล่อยการปรับปรุงระบบ SMARS เพื่อรองรับ Retail Liquidity Program ของตลาดหลักทรัพย์นิวยอร์ก (NYSE) แต่การติดตั้งโค้ดไม่ครบทุกเซิร์ฟเวอร์ ทำให้เซิร์ฟเวอร์หนึ่งเครื่องยังมีโค้ดเก่าที่ไม่ควรถูกเรียกใช้งานอยู่ เมื่อระบบเริ่มทำงาน โค้ดเก่านี้ถูกกระตุ้นและส่งคำสั่งซื้อขายจำนวนมากโดยไม่ตั้งใจ"),
    p("เหตุการณ์ดำเนินอยู่ประมาณ 45 นาที ก่อนที่บริษัทจะหยุดระบบได้ บริษัทสะสมสถานะหลักทรัพย์โดยไม่ตั้งใจในระดับหลายพันล้านดอลลาร์สหรัฐ และเกิดความเสียหายมากกว่า 460 ล้านดอลลาร์สหรัฐ เหตุการณ์นี้กระทบตลาด ผู้ลงทุน และความน่าเชื่อถือขององค์กร [1]"),
    heading("2. การจำแนกปัญหาตามคุณลักษณะคุณภาพ"),
    table([
        ["คุณลักษณะ", "ปัญหาที่พบ", "เหตุผล"],
        ["Functional suitability", "ระบบส่งคำสั่งซื้อขายที่ไม่ตรงกับความประสงค์", "หน้าที่หลักของระบบคือส่งคำสั่งซื้อขายอย่างถูกต้อง แต่โค้ดเก่าสร้างคำสั่งผิดพลาด"],
        ["Reliability", "ระบบผิดพลาดต่อเนื่องจนต้องหยุด", "ความผิดพลาดจากเซิร์ฟเวอร์เดียวทำให้เกิดคำสั่งซื้อขายผิดปกติซ้ำ ๆ"],
        ["Maintainability", "โค้ดเก่ายังคงอยู่ในระบบผลิตจริง", "การจัดการโค้ดและการติดตั้งทำให้ตรวจสอบเวอร์ชันได้ยาก"],
        ["Operational control", "ไม่มีการจำกัดความเสียหายอย่างเพียงพอ", "ควรมีวงเงินจำกัด การแจ้งเตือน และปุ่มหยุดฉุกเฉิน"],
    ], [3.1 * cm, 5.0 * cm, 8.0 * cm]),
    heading("3. การป้องกันและตรวจพบในวงจรการพัฒนา"),
    table([
        ["ระยะ SDLC", "QA: ป้องกัน", "QC: ตรวจพบ"],
        ["ความต้องการและวางแผน", "กำหนดวงเงินซื้อขายและเงื่อนไขหยุดระบบ", "ทบทวนข้อกำหนดกับทีมธุรกิจและกำกับดูแล"],
        ["ออกแบบ", "ออกแบบ circuit breaker, kill switch และ version control", "Design review ของกรณีคำสั่งผิดปกติ"],
        ["พัฒนา", "มาตรฐานลบโค้ดเลิกใช้และ peer review", "Code review หาโค้ดเก่าและ feature flag ที่เสี่ยง"],
        ["ทดสอบ", "แผน end-to-end ที่ใกล้ระบบจริง", "Integration และ regression test ทุกเซิร์ฟเวอร์"],
        ["ติดตั้ง", "deployment checklist และการอนุมัติ", "ตรวจเวอร์ชัน/ไฟล์ทุกเครื่องก่อนเปิดใช้"],
        ["ปฏิบัติการ", "นโยบาย monitoring และ incident response", "เฝ้าระวังคำสั่งผิดปกติและทดสอบ kill switch"],
    ], [3.0 * cm, 6.4 * cm, 6.7 * cm]),
    PageBreak(),
    heading("4. บทวิเคราะห์"),
    p("สาเหตุหลักไม่ได้เกิดจากข้อผิดพลาดในโค้ดเพียงบรรทัดเดียว แต่เกิดจากการควบคุมคุณภาพของกระบวนการปล่อยซอฟต์แวร์ที่ไม่เพียงพอ บริษัทติดตั้งเวอร์ชันใหม่ไม่ครบทุกเซิร์ฟเวอร์ ปล่อยให้โค้ดเก่าคงอยู่ และไม่มีการควบคุมหรือขั้นตอนตอบสนองต่อสัญญาณผิดปกติที่เพียงพอ [1]"),
    p("ในมุม QC ทีมควรตรวจพบปัญหาจากการทดสอบการติดตั้งทุกเซิร์ฟเวอร์ การตรวจสอบเวอร์ชันหลัง deploy และการทดสอบระบบแบบ end-to-end ส่วน QA ควรวางมาตรฐาน deployment, code retirement, peer review, change approval และ incident response ตั้งแต่ต้น เหตุการณ์นี้แสดงให้เห็นว่า QA ช่วยป้องกันข้อบกพร่องจากกระบวนการ ขณะที่ QC ช่วยค้นพบข้อบกพร่องในผลิตภัณฑ์และการติดตั้งก่อนจะส่งผลต่อผู้ใช้"),
    heading("5. ข้อเสนอแนะ"),
    p("1. ทำ deployment แบบอัตโนมัติและยืนยัน hash/เวอร์ชันของซอฟต์แวร์ทุกเครื่องก่อนเปิดใช้<br/>2. ใช้ code review และ change approval สำหรับการเปลี่ยนแปลงที่มีความเสี่ยงสูง<br/>3. ลบหรือปิดกั้นโค้ดที่เลิกใช้แล้ว พร้อมบันทึกรายการโค้ดและ feature flag ที่เหลืออยู่<br/>4. ทดสอบแบบ integration และ regression บนสภาพแวดล้อมที่เหมือนระบบจริง รวมถึงกรณี rollback<br/>5. กำหนด trading limit, circuit breaker, dashboard และ kill switch ที่เจ้าหน้าที่ใช้งานได้ทันที"),
    heading("6. หลักฐาน GitHub และ Git"),
    p("Repository: sqm_674295003<br/>URL: https://github.com/Thitinan9172/sqm_674295003"),
    p("ภาพที่ 1 ผลการตรวจสอบเวอร์ชัน Git"),
    evidence_image("git-version.png", 13.6 * cm),
    Spacer(1, 0.3 * cm),
    p("ภาพที่ 2 GitHub repository sqm_674295003 และไฟล์ในโฟลเดอร์ lab01/"),
    evidence_image("github-repository.png", 16.4 * cm),
    Spacer(1, 0.3 * cm),
    p("ก่อนส่ง ให้เพิ่มภาพหน้าประวัติ commit ที่แสดงการ commit รายงาน Lab 1 โดยเปิด https://github.com/Thitinan9172/sqm_674295003/commits/main"),
    heading("7. การใช้ AI"),
    p("ใช้ Codex ช่วยค้นหาแหล่งอ้างอิงทางการ วางโครงร่าง และตรวจความชัดเจนของภาษา ผู้จัดทำตรวจสอบข้อเท็จจริงกับเอกสารของ SEC และเรียบเรียงเนื้อหารายงานนี้เอง โดยต้องแนบภาพหรือสำเนาบทสนทนานี้ในภาคผนวกก่อนส่งตามนโยบายรายวิชา"),
    heading("อ้างอิง"),
    p("[1] U.S. Securities and Exchange Commission. (2013, October 16). <i>SEC charges Knight Capital with violations of market access rule</i>. https://www.sec.gov/newsroom/press-releases/2013-222"),
    p("[2] U.S. Securities and Exchange Commission. (2013). <i>In the matter of Knight Capital Americas LLC, Release No. 34-70694</i>. https://www.sec.gov/litigation/admin/2013/34-70694.pdf"),
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=1.55 * cm, leftMargin=1.55 * cm, topMargin=1.6 * cm, bottomMargin=1.7 * cm, title="Lab 1 - Knight Capital")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
