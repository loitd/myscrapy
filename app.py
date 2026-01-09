from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# --- DANH MỤC CHUẨN ---
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
NGU_HANH = {"Tý":"Thủy","Hợi":"Thủy","Dần":"Mộc","Mão":"Mộc","Tỵ":"Hỏa","Ngọ":"Hỏa","Thân":"Kim","Dậu":"Kim","Sửu":"Thổ","Thìn":"Thổ","Mùi":"Thổ","Tuất":"Thổ","Giáp":"Mộc","Ất":"Mộc","Bính":"Hỏa","Đinh":"Hỏa","Mậu":"Thổ","Kỷ":"Thổ","Canh":"Kim","Tân":"Kim","Nhâm":"Thủy","Quý":"Thủy"}
# Cung ký: Nơi Can ngày "ngụ" trên Địa bàn
CAN_KY = {"Giáp":"Dần","Ất":"Thìn","Bính":"Tỵ","Đinh":"Mùi","Mậu":"Tỵ","Kỷ":"Mùi","Canh":"Thân","Tân":"Tuất","Nhâm":"Hợi","Quý":"Sửu"}

# Danh sách 12 Thần chuẩn (Thiên tướng)
THIEN_TUONG_NAMES = ["Quý Nhân", "Đằng Xà", "Chu Tước", "Lục Hợp", "Câu Trần", "Thanh Long", "Thiên Không", "Bạch Hổ", "Thái Thường", "Huyền Vũ", "Thái Âm", "Thiên Hậu"]

def get_full_luc_than(ngai_hanh, hao_hanh):
    """Xác định mối quan hệ Lục thân dựa trên Ngũ hành sinh khắc"""
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
    """Kiểm tra quan hệ khắc giữa hai hào"""
    table = {"Kim":"Mộc", "Mộc":"Thổ", "Thổ":"Thủy", "Thủy":"Hỏa", "Hỏa":"Kim"}
    return table.get(NGU_HANH[active]) == NGU_HANH[passive]

def solve_luc_nham(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
    # Tính Can Chi ngày dựa trên mốc tham chiếu
    ref = datetime(2026, 1, 5)
    diff = (dt.date() - ref.date()).days
    can_d = THIEN_CAN[(5 + diff) % 10]
    chi_d = DIA_CHI[(3 + diff) % 12]
    gio_chi = DIA_CHI[((dt.hour + 1) // 2) % 12]
    
    # Xác định Nguyệt Tướng tự động theo lịch tiết khí 2026
    nt_data = [("01-20","Tý"),("02-18","Hợi"),("03-20","Tuất"),("04-20","Dậu"),("05-21","Thân"),("06-21","Mùi"),("07-23","Ngọ"),("08-23","Tỵ"),("09-23","Thìn"),("10-23","Mão"),("11-22","Dần"),("12-22","Sửu")]
    md = dt.strftime("%m-%d")
    nt_chi = "Sửu"
    for d, c in nt_data:
        if md >= d: nt_chi = c

    # 1. Lập Thiên Bàn: Nguyệt tướng gia trên giờ chiêm
    offset = (DIA_CHI.index(nt_chi) - DIA_CHI.index(gio_chi)) % 12
    thien_ban = {DIA_CHI[i]: DIA_CHI[(i + offset) % 12] for i in range(12)}

    # 2. Lập Tứ Khóa
    ck = CAN_KY[can_d] # Cung ký của Can ngày
    k1 = (thien_ban[ck], can_d) # Khóa 1: Thiên bàn trên cung ký của Can
    k2 = (thien_ban[k1[0]], k1[0]) # Khóa 2: Thiên bàn trên hào Khóa 1
    k3 = (thien_ban[chi_d], chi_d) # Khóa 3: Thiên bàn trên Chi ngày
    k4 = (thien_ban[k3[0]], k3[0]) # Khóa 4: Thiên bàn trên hào Khóa 3
    
    # 3. Tìm Tam Truyền theo phép Cửu Cách (Ưu tiên Tặc Khắc -> Dao Sát)
    so_truyen = None
    ten_khoa = "Tặc Khắc Khóa"
    
    # Kiểm tra trạng thái Thiên bàn
    if offset == 6: ten_khoa = "Phản Ngâm Khóa"
    elif offset == 0: ten_khoa = "Phục Ngâm Khóa"

    for k in [k4, k3, k2, k1]: 
        if is_khac(k[1], k[0]): # Hạ khắc Thượng
            so_truyen = k[0]
            break
    if not so_truyen:
        for k in [k4, k3, k2, k1]: 
            if is_khac(k[0], k[1]): # Thượng khắc Hạ
                so_truyen = k[0]
                break
    if not so_truyen: # Dao Sát
        for k in [k4, k3, k2]:
            if is_khac(can_d, k[0]) or is_khac(k[0], can_d): 
                so_truyen = k[0]
                ten_khoa = "Dao Sát Khóa"
                break
    if not so_truyen: so_truyen = k1[0] # Mặc định

    trung = thien_ban[so_truyen]
    mat = thien_ban[trung]

    # 4. Xác định Tuần Không
    giap_idx = (DIA_CHI.index(chi_d) - THIEN_CAN.index(can_d)) % 12
    tuan_khong = [DIA_CHI[(giap_idx - 2) % 12], DIA_CHI[(giap_idx - 1) % 12]]

    # 5. An Thiên Tướng (Quý Nhân khởi theo ngày/đêm và can ngày)
    is_day = 6 <= dt.hour < 18
    qn_map = {"Giáp": ("Sửu", "Mùi"), "Mậu": ("Sửu", "Mùi"), "Canh": ("Sửu", "Mùi"), "Ất": ("Tý", "Thân"), "Kỷ": ("Tý", "Thân"), "Bính": ("Hợi", "Dậu"), "Đinh": ("Hợi", "Dậu"), "Nhâm": ("Tỵ", "Mão"), "Quý": ("Tỵ", "Mão"), "Tân": ("Ngọ", "Dần")}
    qn_heaven = qn_map[can_d][0] if is_day else qn_map[can_d][1]
    qn_earth = next(k for k, v in thien_ban.items() if v == qn_heaven)
    nghich = qn_earth in ["Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất"]
    thien_tuong = {DIA_CHI[(DIA_CHI.index(qn_heaven) + ((-i if nghich else i))) % 12]: n for i, n in enumerate(THIEN_TUONG_NAMES)}

    # 6. Lời phán tự động
    loi_phan = []
    if ten_khoa == "Phản Ngâm Khóa": loi_phan.append("Sự việc lặp lại, đi rồi lại về. Bệnh cũ tái phát, lòng người không thuận.")
    if thien_tuong.get(so_truyen) == "Huyền Vũ": loi_phan.append("Cảnh báo: Có sự lừa dối, mờ ám hoặc hao tài ngầm.")
    if so_truyen in tuan_khong: loi_phan.append("Khởi đầu hư ảo, không có thực lực, chỉ là lời hứa suông.")

    return {
        "can_d": can_d, "chi_d": chi_d, "nt": nt_chi, "gio": gio_chi,
        "ck": ck, # Truyền cung ký của Can ngày để giao diện highlight
        "ten_khoa": ten_khoa, "loi_phan": loi_phan,
        "tu_khoa": [k1, k2, k3, k4],
        "tam_truyen": [
            {"chi": so_truyen, "lt": get_full_luc_than(NGU_HANH[can_d], NGU_HANH[so_truyen]), "tt": thien_tuong.get(so_truyen), "is_khong": so_truyen in tuan_khong},
            {"chi": trung, "lt": get_full_luc_than(NGU_HANH[can_d], NGU_HANH[trung]), "tt": thien_tuong.get(trung), "is_khong": trung in tuan_khong},
            {"chi": mat, "lt": get_full_luc_than(NGU_HANH[can_d], NGU_HANH[mat]), "tt": thien_tuong.get(mat), "is_khong": mat in tuan_khong}
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