from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# --- DANH MỤC CHUẨN ---
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
NGU_HANH = {"Tý":"Thủy","Hợi":"Thủy","Dần":"Mộc","Mão":"Mộc","Tỵ":"Hỏa","Ngọ":"Hỏa","Thân":"Kim","Dậu":"Kim","Sửu":"Thổ","Thìn":"Thổ","Mùi":"Thổ","Tuất":"Thổ","Giáp":"Mộc","Ất":"Mộc","Bính":"Hỏa","Đinh":"Hỏa","Mậu":"Thổ","Kỷ":"Thổ","Canh":"Kim","Tân":"Kim","Nhâm":"Thủy","Quý":"Thủy"}
CAN_KY = {"Giáp":"Dần","Ất":"Thìn","Bính":"Tỵ","Đinh":"Mùi","Mậu":"Tỵ","Kỷ":"Mùi","Canh":"Thân","Tân":"Tuất","Nhâm":"Hợi","Quý":"Sửu"}

# Danh sách 12 Thần theo thứ tự chuẩn (Sử dụng "Thiên Không" thay cho "Thiên Phụ" theo hình mẫu)
THIEN_TUONG_NAMES = ["Quý Nhân", "Đằng Xà", "Chu Tước", "Lục Hợp", "Câu Trần", "Thanh Long", "Thiên Không", "Bạch Hổ", "Thái Thường", "Huyền Vũ", "Thái Âm", "Thiên Hậu"]

def get_full_luc_than(ngai_hanh, hao_hanh):
    rel = {"Huynh": "Huynh Đệ", "Tử": "Tử Tôn", "Tài": "Thê Tài", "Quan": "Quan Quỷ", "Phụ": "Phụ Mẫu"}
    mapping = {
        ("Mộc","Mộc"):"Huynh", ("Mộc","Hỏa"):"Tử", ("Mộc","Thổ"):"Tài", ("Mộc","Kim"):"Quan", ("Mộc","Thủy"):"Phụ",
        ("Hỏa","Hỏa"):"Huynh", ("Hỏa","Thổ"):"Tử", ("Hỏa","Kim"):"Tài", ("Hỏa","Thủy"):"Quan", ("Hỏa","Mộc"):"Phụ",
        ("Thổ","Thổ"):"Huynh", ("Thổ","Kim"):"Tử", ("Thổ","Thủy"):"Tài", ("Thổ","Mộc"):"Quan", ("Thổ","Hỏa"):"Phụ",
        ("Kim","Kim"):"Huynh", ("Kim","Thủy"):"Tử", ("Kim","Mộc"):"Tài", ("Kim","Hỏa"):"Quan", ("Kim","Thổ"):"Phụ",
        ("Thủy","Thủy"):"Huynh", ("Thủy","Mộc"):"Tử", ("Thủy","Hỏa"):"Tài", ("Thủy","Thổ"):"Quan", ("Thủy","Kim"):"Phụ"
    }
    short = mapping.get((ngai_hanh, hao_hanh), "")
    return rel.get(short, "")

def is_khac(active, passive):
    table = {"Kim":"Mộc", "Mộc":"Thổ", "Thổ":"Thủy", "Thủy":"Hỏa", "Hỏa":"Kim"}
    return table.get(NGU_HANH[active]) == NGU_HANH[passive]

def solve_luc_nham(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
    # Mốc chuẩn: 2026-01-05 là Kỷ Mão
    ref = datetime(2026, 1, 5)
    diff = (dt.date() - ref.date()).days
    can_d = THIEN_CAN[(5 + diff) % 10]
    chi_d = DIA_CHI[(3 + diff) % 12]
    gio_chi = DIA_CHI[((dt.hour + 1) // 2) % 12]
    
    # Tự động tính Nguyệt Tướng theo 2026
    nt_data = [("01-20","Tý"),("02-18","Hợi"),("03-20","Tuất"),("04-20","Dậu"),("05-21","Thân"),("06-21","Mùi"),("07-23","Ngọ"),("08-23","Tỵ"),("09-23","Thìn"),("10-23","Mão"),("11-22","Dần"),("12-22","Sửu")]
    md = dt.strftime("%m-%d")
    nt_chi = "Sửu"
    for d, c in nt_data:
        if md >= d: nt_chi = c

    # Thiên Bàn (Heavenly Plate)
    offset = (DIA_CHI.index(nt_chi) - DIA_CHI.index(gio_chi)) % 12
    thien_ban = {DIA_CHI[i]: DIA_CHI[(i + offset) % 12] for i in range(12)}

    # Tứ Khóa
    ck = CAN_KY[can_d]
    k1 = (thien_ban[ck], can_d)
    k2 = (thien_ban[k1[0]], k1[0])
    k3 = (thien_ban[chi_d], chi_d)
    k4 = (thien_ban[k3[0]], k3[0])
    
    # Tìm Tam Truyền
    so_truyen = None
    for k in [k4, k3, k2, k1]: 
        if is_khac(k[1], k[0]): so_truyen = k[0]; break
    if not so_truyen:
        for k in [k4, k3, k2, k1]: 
            if is_khac(k[0], k[1]): so_truyen = k[0]; break
    if not so_truyen: 
        for k in [k4, k3, k2]:
            if is_khac(can_d, k[0]) or is_khac(k[0], can_d): so_truyen = k[0]; break
    if not so_truyen: so_truyen = k1[0]

    trung = thien_ban[so_truyen]
    mat = thien_ban[trung]

    # --- CHỈNH SỬA AN THIÊN TƯỚNG ---
    
    # 1. Xác định Quý Nhân theo Ngày/Đêm (Day/Night)
    # Quy tắc: Giáp Mậu Canh Ngưu Dương, Ất Kỷ Thử Hầu Hương...
    is_day = 6 <= dt.hour < 18
    qn_map = {
        "Giáp": ("Sửu", "Mùi"), "Mậu": ("Sửu", "Mùi"), "Canh": ("Sửu", "Mùi"),
        "Ất": ("Tý", "Thân"), "Kỷ": ("Tý", "Thân"),
        "Bính": ("Hợi", "Dậu"), "Đinh": ("Hợi", "Dậu"),
        "Nhâm": ("Tỵ", "Mão"), "Quý": ("Tỵ", "Mão"),
        "Tân": ("Ngọ", "Dần")
    }
    qn_heavenly_pos = qn_map[can_d][0] if is_day else qn_map[can_d][1]
    
    # 2. Xác định chiều xoay (Thuận/Nghịch) dựa trên vị trí Quý Nhân trên ĐỊA BÀN
    # Tìm xem Quý Nhân (trên Thiên Bàn) đang đóng ở cung nào của Địa Bàn
    qn_on_earthly_pos = ""
    for dia, thien in thien_ban.items():
        if thien == qn_heavenly_pos:
            qn_on_earthly_pos = dia
            break
            
    # Theo quy tắc: Nếu Quý Nhân tại Địa Bàn thuộc cung Hợi -> Thìn: Thuận. Tỵ -> Tuất: Nghịch.
    nghich = qn_on_earthly_pos in ["Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất"]
    
    # 3. An 12 Thần lên Thiên Bàn
    idx_qn_heaven = DIA_CHI.index(qn_heavenly_pos)
    thien_tuong = {}
    for i, name in enumerate(THIEN_TUONG_NAMES):
        # Nếu Thuận: +i, Nếu Nghịch: -i
        pos = (idx_qn_heaven - i) % 12 if nghich else (idx_qn_heaven + i) % 12
        thien_tuong[DIA_CHI[pos]] = name

    return {
        "can_d": can_d, "chi_d": chi_d, "nt": nt_chi, "gio": gio_chi,
        "tu_khoa": [k1, k2, k3, k4],
        "tam_truyen": [
            {"chi": so_truyen, "lt": get_full_luc_than(NGU_HANH[can_d], NGU_HANH[so_truyen]), "tt": thien_tuong.get(so_truyen)},
            {"chi": trung, "lt": get_full_luc_than(NGU_HANH[can_d], NGU_HANH[trung]), "tt": thien_tuong.get(trung)},
            {"chi": mat, "lt": get_full_luc_than(NGU_HANH[can_d], NGU_HANH[mat]), "tt": thien_tuong.get(mat)}
        ],
        "thien_ban": thien_ban, "thien_tuong": thien_tuong
    }

@app.route("/", methods=["GET", "POST"])
def index():
    dt = request.form.get("dt", datetime.now().strftime("%Y-%m-%dT%H:%M"))
    res = solve_luc_nham(dt)
    return render_template("index.html", res=res, dt=dt)

if __name__ == "__main__":
    app.run(debug=True)