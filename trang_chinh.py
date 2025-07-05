import json

# Ma admin he thong (placeholder)
MA_ADMIN_HE_THONG = "ADMIN001" 

try:
    with open("co_giao.json", "r", encoding="utf-8") as file_gv:
        du_lieu_giao_vien = json.load(file_gv)
except FileNotFoundError:
    du_lieu_giao_vien = {"giao_vien": []}

try:
    with open("hoc_sinh.json", "r", encoding="utf-8") as file_hs:
        du_lieu_hoc_sinh = json.load(file_hs)
except FileNotFoundError:
    du_lieu_hoc_sinh = {
        "khoi_6": {"6-01": [], "6-02": []},
        "khoi_7": {"7-01": [], "7-02": []},
        "khoi_8": {"8-01": [], "8-02": []},
        "khoi_9": {"9-01": [], "9-02": []}
    }

try:
    with open("quan_ly_hoc_sinh.json", "r", encoding="utf-8") as file_ql:
        du_lieu_quan_ly = json.load(file_ql)
except FileNotFoundError:
    du_lieu_quan_ly = {"thoi_khoa_bieu": {}}

def cap_nhat_lai(du_lieu, ten_tep):
    with open(ten_tep, "w", encoding="utf-8") as file_ghi:
        json.dump(du_lieu, file_ghi, ensure_ascii=False, indent=4)

def them_moi_hoc_sinh(ma_hoc_sinh, ho_ten_hoc_sinh, que_quan, so_dien_thoai, khoi, lop):
    if khoi not in du_lieu_hoc_sinh or lop not in du_lieu_hoc_sinh[khoi]:
        print(f"Loi: Khoi '{khoi}' hoac lop '{lop}' khong ton tai.")
        return False

    for k, v_khoi in du_lieu_hoc_sinh.items():
        for l, ds_hs in v_khoi.items():
            for hs in ds_hs:
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    print(f"Loi: Ma hoc sinh {ma_hoc_sinh} da ton tai.")
                    return False

    hoc_sinh_moi = {
        "mahocsinh": ma_hoc_sinh,
        "hotenhocsinh": ho_ten_hoc_sinh,
        "quequan": que_quan,
        "sodt": so_dien_thoai,
        "so_tiet_nghi": 0,
        "diem_giua_ky": {},
        "diem_cuoi_ky": {},
        "diem_trung_binh": {}
    }
    du_lieu_hoc_sinh[khoi][lop].append(hoc_sinh_moi)
    cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
    print(f"Da them hoc sinh {ho_ten_hoc_sinh} (Ma: {ma_hoc_sinh}) vao lop {lop}.")
    return True

def xem_tim_kiem_hoc_sinh(ma_hoc_sinh=None, ho_ten=None, lop=None, khoi=None):
    ket_qua = []
    for k, v_khoi in du_lieu_hoc_sinh.items():
        if khoi and k != khoi:
            continue
        for l, ds_hs in v_khoi.items():
            if lop and l != lop:
                continue
            for hs in ds_hs:
                phu_hop_ma_hoc_sinh = (ma_hoc_sinh is None) or (hs.get("mahocsinh") == ma_hoc_sinh)
                phu_hop_ho_ten = (ho_ten is None) or (ho_ten.lower() in hs.get("hotenhocsinh", "").lower())

                if phu_hop_ma_hoc_sinh and phu_hop_ho_ten:
                    hs_copy = hs.copy()
                    hs_copy['khoi'] = k
                    hs_copy['lop'] = l
                    ket_qua.append(hs_copy)
    return ket_qua

def cap_nhat_thong_tin_hoc_sinh(ma_hoc_sinh, du_lieu_moi):
    for k, v_khoi in du_lieu_hoc_sinh.items():
        for l, ds_hs in v_khoi.items():
            for i, hs in enumerate(ds_hs):
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    for khoa, gia_tri in du_lieu_moi.items():
                        hs[khoa] = gia_tri
                    cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
                    print(f"Da cap nhat thong tin cho hoc sinh ma {ma_hoc_sinh}.")
                    return True
    print(f"Loi: Khong tim thay hoc sinh co ma {ma_hoc_sinh}.")
    return False

def xoa_hoc_sinh(ma_hoc_sinh):
    for k, v_khoi in list(du_lieu_hoc_sinh.items()):
        for l, ds_hs in list(v_khoi.items()):
            for i, hs in enumerate(ds_hs):
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    del du_lieu_hoc_sinh[k][l][i]
                    cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
                    print(f"Da xoa hoc sinh ma {ma_hoc_sinh} khoi lop {l}.")
                    return True
    print(f"Loi: Khong tim thay hoc sinh co ma {ma_hoc_sinh}.")
    return False

def xoa_hoc_sinh_theo_dieu_kien(gioi_han_so_tiet_nghi=25):
    danh_sach_hoc_sinh_da_xoa = []
    for k, v_khoi in list(du_lieu_hoc_sinh.items()):
        for l, ds_hs in list(v_khoi.items()):
            danh_sach_hoc_sinh_con_lai = []
            for hs in ds_hs:
                if hs.get("so_tiet_nghi", 0) > gioi_han_so_tiet_nghi:
                    danh_sach_hoc_sinh_da_xoa.append(hs["mahocsinh"])
                    print(f"Hoc sinh {hs['hotenhocsinh']} (Ma: {hs['mahocsinh']}) da bi xoa do so tiet nghi vuot qua {gioi_han_so_tiet_nghi} tiet.")
                else:
                    danh_sach_hoc_sinh_con_lai.append(hs)
            du_lieu_hoc_sinh[k][l] = danh_sach_hoc_sinh_con_lai
    
    if danh_sach_hoc_sinh_da_xoa:
        cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
        print("Da cap nhat file hoc_sinh.json sau khi xoa hoc sinh theo dieu kien.")
    else:
        print("Khong co hoc sinh nao bi xoa theo dieu kien.")
    return danh_sach_hoc_sinh_da_xoa

def xac_thuc_giao_vien(ma_giao_vien, so_dien_thoai):
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_giao_vien and gv.get("sodt") == so_dien_thoai:
            return gv
    return None

def tinh_diem_trung_binh_hoc_sinh(hoc_sinh):
    diem_giua_ky_mon = hoc_sinh.get("diem_giua_ky", {})
    diem_cuoi_ky_mon = hoc_sinh.get("diem_cuoi_ky", {})
    diem_trung_binh_mon = {}
    
    for mon_hoc in diem_giua_ky_mon.keys() | diem_cuoi_ky_mon.keys(): # Su dung toan tu hop tap hop |
        diem_giua = diem_giua_ky_mon.get(mon_hoc)
        diem_cuoi = diem_cuoi_ky_mon.get(mon_hoc)

        if diem_giua is not None and diem_cuoi is not None:
            diem_tb = (diem_giua * 0.4) + (diem_cuoi * 0.6)
            diem_trung_binh_mon[mon_hoc] = round(diem_tb, 2)
        elif diem_giua is not None:
            diem_trung_binh_mon[mon_hoc] = round(diem_giua * 0.4, 2)
        elif diem_cuoi is not None:
            diem_trung_binh_mon[mon_hoc] = round(diem_cuoi * 0.6, 2)
    
    hoc_sinh["diem_trung_binh"] = diem_trung_binh_mon

def nhap_diem_mon_hoc(ma_giao_vien, so_dien_thoai_gv, ma_hoc_sinh, ten_mon_hoc, diem_giua_ky=None, diem_cuoi_ky=None):
    thong_tin_giao_vien = xac_thuc_giao_vien(ma_giao_vien, so_dien_thoai_gv)
    if not thong_tin_giao_vien:
        print("Loi: Xac thuc giao vien khong thanh cong. Vui long kiem tra Ma giao vien va So dien thoai.")
        return False

    chuc_vu = thong_tin_giao_vien.get("chucvu")
    lop_chu_nhiem = thong_tin_giao_vien.get("lopchunhiem")
    mon_hoc_phu_trach = thong_tin_giao_vien.get("monhocphutrach", [])

    hoc_sinh_tim_thay = None
    khoi_hoc_sinh = None
    lop_hoc_sinh = None

    for k, v_khoi in du_lieu_hoc_sinh.items():
        for l, ds_hs in v_khoi.items():
            for i, hs in enumerate(ds_hs):
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    hoc_sinh_tim_thay = hs
                    khoi_hoc_sinh = k
                    lop_hoc_sinh = l
                    break
            if hoc_sinh_tim_thay:
                break
        if hoc_sinh_tim_thay:
            break

    if not hoc_sinh_tim_thay:
        print(f"Loi: Khong tim thay hoc sinh co ma {ma_hoc_sinh}.")
        return False

    if chuc_vu == "gvcn":
        if lop_hoc_sinh != lop_chu_nhiem:
            print(f"Loi: Giao vien {thong_tin_giao_vien['hotengiaovien']} khong phai chu nhiem lop {lop_hoc_sinh} cua hoc sinh {hoc_sinh_tim_thay['hotenhocsinh']}.")
            return False
    elif chuc_vu == "giáo viên bộ môn":
        if ten_mon_hoc not in mon_hoc_phu_trach:
            print(f"Loi: Giao vien {thong_tin_giao_vien['hotengiaovien']} khong phu trach mon {ten_mon_hoc}.")
            return False
    else:
        print(f"Loi: Chuc vu {chuc_vu} khong co quyen nhap diem.")
        return False

    if diem_giua_ky is not None:
        hoc_sinh_tim_thay["diem_giua_ky"][ten_mon_hoc] = diem_giua_ky
        print(f"Da cap nhat diem giua ky mon {ten_mon_hoc} cho HS {hoc_sinh_tim_thay['hotenhocsinh']} (Ma: {ma_hoc_sinh}): {diem_giua_ky}")
    
    if diem_cuoi_ky is not None:
        hoc_sinh_tim_thay["diem_cuoi_ky"][ten_mon_hoc] = diem_cuoi_ky
        print(f"Da cap nhat diem cuoi ky mon {ten_mon_hoc} cho HS {hoc_sinh_tim_thay['hotenhocsinh']} (Ma: {ma_hoc_sinh}): {diem_cuoi_ky}")

    tinh_diem_trung_binh_hoc_sinh(hoc_sinh_tim_thay)
    cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
    return True

def xem_bang_diem_ca_nhan(ma_hoc_sinh):
    hoc_sinh_tim_thay = None
    for k, v_khoi in du_lieu_hoc_sinh.items():
        for l, ds_hs in v_khoi.items():
            for hs in ds_hs:
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    hoc_sinh_tim_thay = hs
                    break
            if hoc_sinh_tim_thay:
                break
        if hoc_sinh_tim_thay:
            break

    if not hoc_sinh_tim_thay:
        print(f"Khong tim thay hoc sinh co ma {ma_hoc_sinh}.")
        return None

    print(f"\n--- Bang diem cua hoc sinh: {hoc_sinh_tim_thay['hotenhocsinh']} (Ma: {hoc_sinh_tim_thay['mahocsinh']}) ---")
    print("Mon hoc | Diem Giua Ky | Diem Cuoi Ky | Diem Trung Binh")
    print("--------------------------------------------------")

    tat_ca_mon_hoc = hoc_sinh_tim_thay.get("diem_giua_ky", {}).keys() | \
                       hoc_sinh_tim_thay.get("diem_cuoi_ky", {}).keys() | \
                       hoc_sinh_tim_thay.get("diem_trung_binh", {}).keys() # Su dung toan tu hop tap hop |

    if not tat_ca_mon_hoc:
        print("Chua co diem nao duoc nhap cho hoc sinh nay.")
        return hoc_sinh_tim_thay

    for mon_hoc in sorted(list(tat_ca_mon_hoc)):
        diem_giua = hoc_sinh_tim_thay.get("diem_giua_ky", {}).get(mon_hoc, 'N/A')
        diem_cuoi = hoc_sinh_tim_thay.get("diem_cuoi_ky", {}).get(mon_hoc, 'N/A')
        diem_tb = hoc_sinh_tim_thay.get("diem_trung_binh", {}).get(mon_hoc, 'N/A')
        print(f"{mon_hoc:<8} | {str(diem_giua):<12} | {str(diem_cuoi):<12} | {str(diem_tb):<15}")
    print("--------------------------------------------------")
    return hoc_sinh_tim_thay

def kiem_tra_va_xoa_hoc_sinh_nghi_qua_gioi_han(ma_hoc_sinh, gioi_han=12):
    hoc_sinh_tim_thay = None
    for k, v_khoi in du_lieu_hoc_sinh.items():
        for l, ds_hs in v_khoi.items():
            for hs in ds_hs:
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    hoc_sinh_tim_thay = hs
                    break
            if hoc_sinh_tim_thay:
                break
        if hoc_sinh_tim_thay:
            break

    if hoc_sinh_tim_thay and hoc_sinh_tim_thay.get("so_tiet_nghi", 0) > gioi_han:
        print(f"Canh bao: Hoc sinh {hoc_sinh_tim_thay['hotenhocsinh']} (Ma: {ma_hoc_sinh}) co so tiet nghi ({hoc_sinh_tim_thay['so_tiet_nghi']}) vuot qua gioi han ({gioi_han}).")
        xoa_hoc_sinh(ma_hoc_sinh)
        return True
    return False

def nhap_so_tiet_nghi(ma_giao_vien, so_dien_thoai_gv, ma_hoc_sinh, ten_mon_hoc, so_tiet_nghi_them):
    thong_tin_giao_vien = xac_thuc_giao_vien(ma_giao_vien, so_dien_thoai_gv)
    if not thong_tin_giao_vien:
        print("Loi: Xac thuc giao vien khong thanh cong. Vui long kiem tra Ma giao vien va So dien thoai.")
        return False

    chuc_vu = thong_tin_giao_vien.get("chucvu")
    mon_hoc_phu_trach = thong_tin_giao_vien.get("monhocphutrach", [])

    if chuc_vu != "giáo viên bộ môn":
        print(f"Loi: Chuc vu {chuc_vu} khong co quyen nhap so tiet nghi. Chi giao vien bo mon moi co quyen nay.")
        return False
    
    if ten_mon_hoc not in mon_hoc_phu_trach:
        print(f"Loi: Giao vien {thong_tin_giao_vien['hotengiaovien']} khong phu trach mon {ten_mon_hoc}.")
        return False

    hoc_sinh_tim_thay = None
    for k, v_khoi in du_lieu_hoc_sinh.items():
        for l, ds_hs in v_khoi.items():
            for i, hs in enumerate(ds_hs):
                if hs.get("mahocsinh") == ma_hoc_sinh:
                    hoc_sinh_tim_thay = hs
                    break
            if hoc_sinh_tim_thay:
                break
        if hoc_sinh_tim_thay:
            break

    if not hoc_sinh_tim_thay:
        print(f"Loi: Khong tim thay hoc sinh co ma {ma_hoc_sinh}.")
        return False
    
    hoc_sinh_tim_thay["so_tiet_nghi"] = hoc_sinh_tim_thay.get("so_tiet_nghi", 0) + so_tiet_nghi_them
    cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
    print(f"Da cap nhat so tiet nghi cho HS {hoc_sinh_tim_thay['hotenhocsinh']} (Ma: {ma_hoc_sinh}) mon {ten_mon_hoc}. Tong so tiet nghi: {hoc_sinh_tim_thay['so_tiet_nghi']}.")

    kiem_tra_va_xoa_hoc_sinh_nghi_qua_gioi_han(ma_hoc_sinh, gioi_han=12)
    return True

def them_moi_giao_vien(ma_giao_vien, ho_ten_giao_vien, ngay_sinh, gioi_tinh, so_dien_thoai, email, chuc_vu, bang_cap, mon_hoc_phu_trach=None, lop_chu_nhiem=None):
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_giao_vien:
            print(f"Loi: Ma giao vien {ma_giao_vien} da ton tai.")
            return False
        if gv.get("email") == email and email is not None:
            print(f"Loi: Email {email} da ton tai.")
            return False

    if chuc_vu == "gvcn" and not lop_chu_nhiem:
        print("Loi: Giao vien chu nhiem phai co lop chu nhiem.")
        return False
    if chuc_vu == "giáo viên bộ môn" and not mon_hoc_phu_trach:
        print("Loi: Giao vien bo mon phai co mon hoc phu trach.")
        return False
    if chuc_vu != "gvcn" and lop_chu_nhiem:
        print("Canh bao: Chuc vu khong phai gvcn nhung co lop chu nhiem. Lop chu nhiem se duoc bo qua.")
        lop_chu_nhiem = None
    if chuc_vu != "giáo viên bộ môn" and mon_hoc_phu_trach:
        print("Canh bao: Chuc vu khong phai giao vien bo mon nhung co mon hoc phu trach. Mon hoc phu trach se duoc bo qua.")
        mon_hoc_phu_trach = []

    giao_vien_moi = {
        "magiaovien": ma_giao_vien,
        "hotengiaovien": ho_ten_giao_vien,
        "ngaysinh": ngay_sinh,
        "gioitinh": gioi_tinh,
        "sodt": so_dien_thoai,
        "email": email,
        "chucvu": chuc_vu,
        "bangcap": bang_cap,
        "monhocphutrach": mon_hoc_phu_trach if mon_hoc_phu_trach is not None else [],
        "lopchunhiem": lop_chu_nhiem,
        "thanh_tich": ""
    }
    du_lieu_giao_vien["giao_vien"].append(giao_vien_moi)
    cap_nhat_lai(du_lieu_giao_vien, "co_giao.json")
    print(f"Da them giao vien {ho_ten_giao_vien} (Ma: {ma_giao_vien}).")
    return True

def xem_tim_kiem_giao_vien(ma_giao_vien=None, ho_ten=None, chuc_vu=None, mon_hoc=None):
    ket_qua = []
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        phu_hop_ma = (ma_giao_vien is None) or (gv.get("magiaovien") == ma_giao_vien)
        phu_hop_ten = (ho_ten is None) or (ho_ten.lower() in gv.get("hotengiaovien", "").lower())
        phu_hop_chuc_vu = (chuc_vu is None) or (gv.get("chucvu", "").lower() == chuc_vu.lower())
        phu_hop_mon_hoc = (mon_hoc is None) or (mon_hoc in gv.get("monhocphutrach", []))

        if phu_hop_ma and phu_hop_ten and phu_hop_chuc_vu and phu_hop_mon_hoc:
            ket_qua.append(gv)
    return ket_qua

def cap_nhat_thong_tin_giao_vien(ma_giao_vien_can_cap_nhat, du_lieu_moi, ma_admin):
    if ma_admin != MA_ADMIN_HE_THONG:
        print("Loi: Ban khong co quyen quan tri de cap nhat thong tin giao vien.")
        return False

    for i, gv in enumerate(du_lieu_giao_vien.get("giao_vien", [])):
        if gv.get("magiaovien") == ma_giao_vien_can_cap_nhat:
            for khoa, gia_tri in du_lieu_moi.items():
                if khoa == "lopchunhiem" and gv.get("chucvu") != "gvcn" and gia_tri is not None:
                    print(f"Canh bao: Giao vien {gv['hotengiaovien']} khong phai gvcn, khong the cap nhat lop chu nhiem.")
                    continue
                if khoa == "monhocphutrach" and gv.get("chucvu") != "giáo viên bộ môn" and gia_tri:
                    print(f"Canh bao: Giao vien {gv['hotengiaovien']} khong phai giao vien bo mon, khong the cap nhat mon hoc phu trach.")
                    continue
                gv[khoa] = gia_tri
            cap_nhat_lai(du_lieu_giao_vien, "co_giao.json")
            print(f"Da cap nhat thong tin cho giao vien ma {ma_giao_vien_can_cap_nhat}.")
            return True
    print(f"Loi: Khong tim thay giao vien co ma {ma_giao_vien_can_cap_nhat}.")
    return False

def nhap_cap_nhat_thanh_tich_giao_vien(ma_giao_vien, thanh_tich_moi, ma_admin):
    if ma_admin != MA_ADMIN_HE_THONG:
        print("Loi: Ban khong co quyen quan tri de cap nhat thanh tich giao vien.")
        return False

    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_giao_vien:
            gv["thanh_tich"] = thanh_tich_moi
            cap_nhat_lai(du_lieu_giao_vien, "co_giao.json")
            print(f"Da cap nhat thanh tich cho giao vien {gv['hotengiaovien']} (Ma: {ma_giao_vien}).")
            return True
    print(f"Loi: Khong tim thay giao vien co ma {ma_giao_vien}.")
    return False

def phan_cong_gvcn(ma_giao_vien, lop_moi, ma_admin):
    if ma_admin != MA_ADMIN_HE_THONG:
        print("Loi: Ban khong co quyen quan tri de phan cong giao vien chu nhiem.")
        return False

    giao_vien_tim_thay = None
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_giao_vien:
            giao_vien_tim_thay = gv
            break
    
    if not giao_vien_tim_thay:
        print(f"Loi: Khong tim thay giao vien co ma {ma_giao_vien}.")
        return False
    
    if giao_vien_tim_thay.get("chucvu") != "gvcn":
        print(f"Loi: Giao vien {giao_vien_tim_thay['hotengiaovien']} khong phai la giao vien chu nhiem.")
        return False

    khoi_cua_lop = None
    for khoi_key, lop_data in du_lieu_hoc_sinh.items():
        if lop_moi in lop_data:
            khoi_cua_lop = khoi_key
            break
    
    if not khoi_cua_lop:
        print(f"Loi: Lop '{lop_moi}' khong ton tai trong du lieu hoc sinh.")
        return False

    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("lopchunhiem") == lop_moi and gv.get("magiaovien") != ma_giao_vien:
            print(f"Loi: Lop {lop_moi} da co giao vien chu nhiem ({gv['hotengiaovien']}).")
            return False

    giao_vien_tim_thay["lopchunhiem"] = lop_moi
    cap_nhat_lai(du_lieu_giao_vien, "co_giao.json")
    print(f"Da phan cong giao vien {giao_vien_tim_thay['hotengiaovien']} lam chu nhiem lop {lop_moi}.")
    return True

def phan_cong_gvbm(ma_giao_vien, mon_hoc_moi, ma_admin):
    if ma_admin != MA_ADMIN_HE_THONG:
        print("Loi: Ban khong co quyen quan tri de phan cong giao vien bo mon.")
        return False

    giao_vien_tim_thay = None
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_giao_vien:
            giao_vien_tim_thay = gv
            break
    
    if not giao_vien_tim_thay:
        print(f"Loi: Khong tim thay giao vien co ma {ma_giao_vien}.")
        return False
    
    if giao_vien_tim_thay.get("chucvu") != "giáo viên bộ môn":
        print(f"Loi: Giao vien {giao_vien_tim_thay['hotengiaovien']} khong phai la giao vien bo mon.")
        return False

    if mon_hoc_moi not in ["Toán", "Lý", "Anh"]:
        print(f"Loi: Mon hoc '{mon_hoc_moi}' khong hop le. Chi chap nhan 'Toan', 'Ly', 'Anh'.")
        return False

    if mon_hoc_moi not in giao_vien_tim_thay.get("monhocphutrach", []):
        giao_vien_tim_thay["monhocphutrach"].append(mon_hoc_moi)
        cap_nhat_lai(du_lieu_giao_vien, "co_giao.json")
        print(f"Da phan cong giao vien {giao_vien_tim_thay['hotengiaovien']} phu trach them mon {mon_hoc_moi}.")
        return True
    else:
        print(f"Canh bao: Giao vien {giao_vien_tim_thay['hotengiaovien']} da phu trach mon {mon_hoc_moi} roi.")
        return False

def tao_chinh_sua_thoi_khoa_bieu(ma_admin, lop, ngay, danh_sach_tiet_hoc):
    if ma_admin != MA_ADMIN_HE_THONG:
        print("Loi: Ban khong co quyen quan tri de tao/chinh sua thoi khoa bieu.")
        return False

    khoi_cua_lop = None
    for k_hs, v_lop_hs in du_lieu_hoc_sinh.items():
        if lop in v_lop_hs:
            khoi_cua_lop = k_hs
            break
    if not khoi_cua_lop:
        print(f"Loi: Lop '{lop}' khong ton tai trong du lieu hoc sinh.")
        return False

    if lop not in du_lieu_quan_ly["thoi_khoa_bieu"]:
        du_lieu_quan_ly["thoi_khoa_bieu"][lop] = {}
    
    du_lieu_quan_ly["thoi_khoa_bieu"][lop][ngay] = []

    for tiet_hoc in danh_sach_tiet_hoc:
        ma_gv = tiet_hoc.get("ma_gv")
        ten_mon = tiet_hoc.get("mon")
        tiet = tiet_hoc.get("tiet")
        phong = tiet_hoc.get("phong")

        if not all([ma_gv, ten_mon, tiet, phong]):
            print(f"Loi: Thong tin tiet hoc thieu (ma_gv, mon, tiet, phong). Bo qua tiet hoc nay.")
            continue

        gv_tim_thay = None
        for gv in du_lieu_giao_vien.get("giao_vien", []):
            if gv.get("magiaovien") == ma_gv:
                gv_tim_thay = gv
                break
        
        if not gv_tim_thay:
            print(f"Loi: Khong tim thay giao vien co ma {ma_gv}. Bo qua tiet hoc.")
            continue
        
        if ten_mon not in gv_tim_thay.get("monhocphutrach", []):
            print(f"Loi: Giao vien {gv_tim_thay['hotengiaovien']} khong phu trach mon {ten_mon}. Bo qua tiet hoc.")
            continue
        
        trung_lich = False
        for l_khac, ngay_data in du_lieu_quan_ly["thoi_khoa_bieu"].items():
            if l_khac == lop:
                continue
            if ngay in ngay_data:
                for th_khac in ngay_data[ngay]:
                    if th_khac.get("ma_gv") == ma_gv and th_khac.get("tiet") == tiet:
                        print(f"Loi: Giao vien {gv_tim_thay['hotengiaovien']} da bi trung lich o lop {l_khac} vao ngay {ngay} tiet {tiet}. Bo qua tiet hoc nay.")
                        trung_lich = True
                        break
            if trung_lich:
                break
        if trung_lich:
            continue

        du_lieu_quan_ly["thoi_khoa_bieu"][lop][ngay].append(tiet_hoc)
    
    cap_nhat_lai(du_lieu_quan_ly, "quan_ly_hoc_sinh.json")
    print(f"Da cap nhat thoi khoa bieu cho lop {lop} ngay {ngay}.")
    return True

def xem_thoi_khoa_bieu(lop=None, ma_giao_vien=None):
    if not lop and not ma_giao_vien:
        print("Vui long cung cap ten lop hoac ma giao vien de xem thoi khoa bieu.")
        return None

    if lop:
        print(f"\n--- Thoi khoa bieu lop: {lop} ---")
        if lop in du_lieu_quan_ly["thoi_khoa_bieu"]:
            for ngay, ds_tiet_hoc in du_lieu_quan_ly["thoi_khoa_bieu"][lop].items():
                print(f"  {ngay}:")
                for tiet_hoc in ds_tiet_hoc:
                    print(f"    Tiet {tiet_hoc['tiet']}: {tiet_hoc['mon']} - GV: {tiet_hoc['ma_gv']} - Phong: {tiet_hoc['phong']}")
        else:
            print(f"  Chua co thoi khoa bieu cho lop {lop}.")
        return du_lieu_quan_ly["thoi_khoa_bieu"].get(lop)
    
    if ma_giao_vien:
        print(f"\n--- Lich day cua giao vien: {ma_giao_vien} ---")
        lich_day_gv = {}
        gv_hoten = "Khong tim thay"
        for gv in du_lieu_giao_vien.get("giao_vien", []):
            if gv.get("magiaovien") == ma_giao_vien:
                gv_hoten = gv.get("hotengiaovien")
                break

        print(f"Ten giao vien: {gv_hoten}")
        
        for lop_tkb, ngay_data in du_lieu_quan_ly["thoi_khoa_bieu"].items():
            for ngay, ds_tiet_hoc in ngay_data.items():
                for tiet_hoc in ds_tiet_hoc:
                    if tiet_hoc.get("ma_gv") == ma_giao_vien:
                        if ngay not in lich_day_gv:
                            lich_day_gv[ngay] = []
                        lich_day_gv[ngay].append({
                            "lop": lop_tkb,
                            "tiet": tiet_hoc['tiet'],
                            "mon": tiet_hoc['mon'],
                            "phong": tiet_hoc['phong']
                        })
        
        if lich_day_gv:
            for ngay in sorted(lich_day_gv.keys()):
                print(f"  {ngay}:")
                for tiet_day in sorted(lich_day_gv[ngay], key=lambda x: x['tiet']):
                    print(f"    Tiet {tiet_day['tiet']}: Lop {tiet_day['lop']} - Mon {tiet_day['mon']} - Phong {tiet_day['phong']}")
        else:
            print(f"  Giao vien {gv_hoten} chua co lich day nao.")
        return lich_day_gv

def xep_loai_hoc_luc(diem_trung_binh_chung):
    if diem_trung_binh_chung >= 8.0:
        return "Gioi"
    elif diem_trung_binh_chung >= 6.5:
        return "Kha"
    elif diem_trung_binh_chung >= 5.0:
        return "Trung binh"
    else:
        return "Yeu"

def bao_cao_hoc_luc_hoc_sinh_theo_lop(khoi, lop):
    if khoi not in du_lieu_hoc_sinh or lop not in du_lieu_hoc_sinh[khoi]:
        print(f"Loi: Khoi '{khoi}' or lop '{lop}' khong ton tai.")
        return []

    print(f"\n--- Bao cao hoc luc lop {lop}, khoi {khoi} ---")
    print(f"{'Ma HS':<8} | {'Ho Ten':<25} | {'Diem TB Chung':<15} | {'Xep Loai':<15}")
    print("-" * 70)

    ds_hoc_sinh_lop = du_lieu_hoc_sinh[khoi][lop]
    ket_qua_bao_cao = []

    for hs in ds_hoc_sinh_lop:
        diem_tb_cac_mon = hs.get("diem_trung_binh", {}).values()
        if diem_tb_cac_mon:
            diem_tb_chung = sum(diem_tb_cac_mon) / len(diem_tb_cac_mon)
            xep_loai = xep_loai_hoc_luc(diem_tb_chung)
        else:
            diem_tb_chung = "N/A"
            xep_loai = "Chua co diem"
        
        ket_qua_bao_cao.append({
            "mahocsinh": hs["mahocsinh"],
            "hotenhocsinh": hs["hotenhocsinh"],
            "diem_tb_chung": diem_tb_chung,
            "xep_loai": xep_loai
        })
        print(f"{hs['mahocsinh']:<8} | {hs['hotenhocsinh']:<25} | {str(diem_tb_chung):<15} | {xep_loai:<15}")
    print("-" * 70)
    return ket_qua_bao_cao

def bao_cao_tong_hop_diem_lop(khoi, lop):
    if khoi not in du_lieu_hoc_sinh or lop not in du_lieu_hoc_sinh[khoi]:
        print(f"Loi: Khoi '{khoi}' or lop '{lop}' khong ton tai.")
        return []

    print(f"\n--- Bang tong hop diem lop {lop}, khoi {khoi} ---")
    
    ds_hoc_sinh_lop = du_lieu_hoc_sinh[khoi][lop]
    
    tat_ca_mon_hoc = set()
    for hs in ds_hoc_sinh_lop:
        tat_ca_mon_hoc = tat_ca_mon_hoc | hs.get("diem_giua_ky", {}).keys()
        tat_ca_mon_hoc = tat_ca_mon_hoc | hs.get("diem_cuoi_ky", {}).keys()
        tat_ca_mon_hoc = tat_ca_mon_hoc | hs.get("diem_trung_binh", {}).keys()
    
    mon_hoc_sap_xep = sorted(list(tat_ca_mon_hoc))

    header = f"{'Ma HS':<8} | {'Ho Ten':<25}"
    for mon in mon_hoc_sap_xep:
        header += f" | {mon} GK | {mon} CK | {mon} TB"
    print(header)
    print("-" * (len(header) + 5 * len(mon_hoc_sap_xep)))

    ket_qua_bao_cao = []
    for hs in ds_hoc_sinh_lop:
        dong_du_lieu = f"{hs['mahocsinh']:<8} | {hs['hotenhocsinh']:<25}"
        hs_data = {
            "mahocsinh": hs["mahocsinh"],
            "hotenhocsinh": hs["hotenhocsinh"]
        }
        for mon in mon_hoc_sap_xep:
            diem_giua = hs.get("diem_giua_ky", {}).get(mon, 'N/A')
            diem_cuoi = hs.get("diem_cuoi_ky", {}).get(mon, 'N/A')
            diem_tb = hs.get("diem_trung_binh", {}).get(mon, 'N/A')
            dong_du_lieu += f" | {str(diem_giua):<7} | {str(diem_cuoi):<7} | {str(diem_tb):<7}"
            hs_data[f"{mon}_GK"] = diem_giua
            hs_data[f"{mon}_CK"] = diem_cuoi
            hs_data[f"{mon}_TB"] = diem_tb
        print(dong_du_lieu)
        ket_qua_bao_cao.append(hs_data)
    print("-" * (len(header) + 5 * len(mon_hoc_sap_xep)))
    return ket_qua_bao_cao

def bao_cao_hoc_sinh_nghi_nhieu(gioi_han_nghi=5):
    print(f"\n--- Danh sach hoc sinh nghi hoc nhieu (tren {gioi_han_nghi} tiet) ---")
    print(f"{'Ma HS':<8} | {'Ho Ten':<25} | {'Lop':<8} | {'Khoi':<8} | {'So Tiet Nghi':<15}")
    print("-" * 75)

    ket_qua_bao_cao = []
    for khoi_key, lop_data in du_lieu_hoc_sinh.items():
        for lop_key, ds_hs in lop_data.items():
            for hs in ds_hs:
                so_tiet_nghi = hs.get("so_tiet_nghi", 0)
                if so_tiet_nghi > gioi_han_nghi:
                    ket_qua_bao_cao.append({
                        "mahocsinh": hs["mahocsinh"],
                        "hotenhocsinh": hs["hotenhocsinh"],
                        "lop": lop_key,
                        "khoi": khoi_key,
                        "so_tiet_nghi": so_tiet_nghi
                    })
                    print(f"{hs['mahocsinh']:<8} | {hs['hotenhocsinh']:<25} | {lop_key:<8} | {khoi_key:<8} | {so_tiet_nghi:<15}")
    if not ket_qua_bao_cao:
        print("Khong co hoc sinh nao nghi hoc vuot qua gioi han.")
    print("-" * 75)
    return ket_qua_bao_cao

def thong_ke_giao_vien_theo_chuc_vu():
    print("\n--- Thong ke giao vien theo chuc vu ---")
    thong_ke = {}
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        chuc_vu = gv.get("chucvu", "Khong xac dinh")
        thong_ke[chuc_vu] = thong_ke.get(chuc_vu, 0) + 1
    
    print(f"{'Chuc Vu':<20} | {'So Luong':<10}")
    print("-" * 35)
    for cv, sl in thong_ke.items():
        print(f"{cv:<20} | {sl:<10}")
    print("-" * 35)
    return thong_ke

def thong_ke_giao_vien_theo_mon_hoc():
    print("\n--- Thong ke giao vien theo mon hoc ---")
    thong_ke = {}
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        mon_hoc_phu_trach = gv.get("monhocphutrach", [])
        if not mon_hoc_phu_trach and gv.get("chucvu") == "giáo viên bộ môn":
            thong_ke["Chua phan cong mon"] = thong_ke.get("Chua phan cong mon", 0) + 1
        else:
            for mon in mon_hoc_phu_trach:
                thong_ke[mon] = thong_ke.get(mon, 0) + 1
    
    print(f"{'Mon Hoc':<20} | {'So Luong Giao Vien':<20}")
    print("-" * 45)
    for mon, sl in thong_ke.items():
        print(f"{mon:<20} | {sl:<20}")
    print("-" * 45)
    return thong_ke

# --- V. Cac chuc nang khac ---

def xac_thuc_quyen_dac_biet(ma_xac_thuc, chuc_vu_yeu_cau):
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_xac_thuc:
            if gv.get("chucvu") == chuc_vu_yeu_cau or gv.get("chucvu") == "hieu truong" or gv.get("chucvu") == "hieu pho":
                return True
    return False

def thong_bao_va_canh_bao(ma_giao_vien_xac_thuc, lop_can_duyet):
    gv_info = None
    for gv in du_lieu_giao_vien.get("giao_vien", []):
        if gv.get("magiaovien") == ma_giao_vien_xac_thuc:
            gv_info = gv
            break
    
    if not gv_info:
        print("Loi: Ma giao vien xac thuc khong hop le.")
        return False
    
    chuc_vu = gv_info.get("chucvu")
    lop_chu_nhiem = gv_info.get("lopchunhiem")

    if chuc_vu == "gvcn" and lop_can_duyet != lop_chu_nhiem:
        print(f"Loi: Giao vien {gv_info['hotengiaovien']} khong phai chu nhiem lop {lop_can_duyet}.")
        return False
    elif chuc_vu not in ["hieu truong", "hieu pho", "gvcn"]:
        print(f"Loi: Chuc vu {chuc_vu} khong co quyen thong bao va canh bao.")
        return False

    print(f"\n--- Duyet ket qua va thong bao canh bao cho lop {lop_can_duyet} ---")
    
    khoi_cua_lop = None
    for k_hs, v_lop_hs in du_lieu_hoc_sinh.items():
        if lop_can_duyet in v_lop_hs:
            khoi_cua_lop = k_hs
            break
    
    if not khoi_cua_lop:
        print(f"Loi: Lop '{lop_can_duyet}' khong ton tai trong du lieu hoc sinh.")
        return False

    ds_hoc_sinh_lop = du_lieu_hoc_sinh[khoi_cua_lop][lop_can_duyet]

    for hs in ds_hoc_sinh_lop:
        diem_tb_cac_mon = hs.get("diem_trung_binh", {})
        canh_bao_diem = []
        for mon, diem_tb in diem_tb_cac_mon.items():
            if diem_tb < 5.0:
                canh_bao_diem.append(f"{mon}: {diem_tb}")
        
        if canh_bao_diem:
            print(f"Hoc sinh {hs['hotenhocsinh']} (Ma: {hs['mahocsinh']}) co diem duoi 5 o cac mon: {', '.join(canh_bao_diem)}")
        else:
            print(f"Hoc sinh {hs['hotenhocsinh']} (Ma: {hs['mahocsinh']}) co ket qua tot.")
    print("--- Hoan tat duyet ket qua ---")
    return True

def quan_ly_lop_hoc(chuc_nang, ma_hieu_truong=None, ma_hieu_pho=None, ma_gvbm=None, khoi=None, lop=None, lop_moi=None, ma_hoc_sinh=None):
    if not (xac_thuc_quyen_dac_biet(ma_hieu_truong, "hieu truong") and
            xac_thuc_quyen_dac_biet(ma_hieu_pho, "hieu pho") and
            xac_thuc_quyen_dac_biet(ma_gvbm, "giáo viên bộ môn")):
        print("Loi: Can xac thuc bo ba Hieu truong, Hieu pho va Giao vien bo mon de thuc hien chuc nang quan ly lop hoc.")
        return False

    if chuc_nang == "them":
        if khoi not in du_lieu_hoc_sinh:
            print(f"Loi: Khoi '{khoi}' khong ton tai. Khong the them lop.")
            return False
        if lop in du_lieu_hoc_sinh[khoi]:
            print(f"Loi: Lop '{lop}' da ton tai trong khoi '{khoi}'.")
            return False
        du_lieu_hoc_sinh[khoi][lop] = []
        cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
        print(f"Da them lop {lop} vao khoi {khoi}.")
        return True
    
    elif chuc_nang == "sua":
        if khoi not in du_lieu_hoc_sinh or lop not in du_lieu_hoc_sinh[khoi]:
            print(f"Loi: Lop '{lop}' trong khoi '{khoi}' khong ton tai.")
            return False
        if not lop_moi:
            print("Loi: Vui long cung cap ten lop moi de sua.")
            return False
        if lop_moi in du_lieu_hoc_sinh[khoi]:
            print(f"Loi: Ten lop moi '{lop_moi}' da ton tai trong khoi '{khoi}'.")
            return False
        
        du_lieu_hoc_sinh[khoi][lop_moi] = du_lieu_hoc_sinh[khoi].pop(lop)
        cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
        print(f"Da doi ten lop {lop} thanh {lop_moi} trong khoi {khoi}.")
        return True

    elif chuc_nang == "xoa":
        if khoi not in du_lieu_hoc_sinh or lop not in du_lieu_hoc_sinh[khoi]:
            print(f"Loi: Lop '{lop}' trong khoi '{khoi}' khong ton tai.")
            return False
        if du_lieu_hoc_sinh[khoi][lop]:
            print(f"Loi: Lop {lop} van con hoc sinh. Khong the xoa lop co hoc sinh.")
            return False
        del du_lieu_hoc_sinh[khoi][lop]
        cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
        print(f"Da xoa lop {lop} khoi khoi {khoi}.")
        return True

    elif chuc_nang == "chuyen_lop_hoc_sinh":
        if not ma_hoc_sinh or not lop_moi or not khoi:
            print("Loi: Vui long cung cap ma hoc sinh, lop moi va khoi moi de chuyen lop.")
            return False
        
        hs_tim_thay = None
        lop_cu = None
        khoi_cu = None
        
        for k_cu, v_khoi_cu in du_lieu_hoc_sinh.items():
            for l_cu, ds_hs_cu in v_khoi_cu.items():
                for i, hs in enumerate(ds_hs_cu):
                    if hs.get("mahocsinh") == ma_hoc_sinh:
                        hs_tim_thay = hs
                        lop_cu = l_cu
                        khoi_cu = k_cu
                        break
                if hs_tim_thay:
                    break
            if hs_tim_thay:
                break
        
        if not hs_tim_thay:
            print(f"Loi: Khong tim thay hoc sinh co ma {ma_hoc_sinh}.")
            return False
        
        if khoi not in du_lieu_hoc_sinh or lop_moi not in du_lieu_hoc_sinh[khoi]:
            print(f"Loi: Lop moi '{lop_moi}' trong khoi '{khoi}' khong ton tai.")
            return False
        
        if lop_cu == lop_moi and khoi_cu == khoi:
            print(f"Canh bao: Hoc sinh {hs_tim_thay['hotenhocsinh']} da o trong lop {lop_moi} cua khoi {khoi} roi.")
            return False

        # Xoa hoc sinh khoi lop cu
        du_lieu_hoc_sinh[khoi_cu][lop_cu].remove(hs_tim_thay)
        # Them hoc sinh vao lop moi
        du_lieu_hoc_sinh[khoi][lop_moi].append(hs_tim_thay)
        cap_nhat_lai(du_lieu_hoc_sinh, "hoc_sinh.json")
        print(f"Da chuyen hoc sinh {hs_tim_thay['hotenhocsinh']} (Ma: {ma_hoc_sinh}) tu lop {lop_cu} khoi {khoi_cu} sang lop {lop_moi} khoi {khoi}.")
        return True

    else:
        print("Loi: Chuc nang quan ly lop hoc khong hop le.")
        return False

def quan_ly_mon_hoc(chuc_nang, ma_hieu_truong=None, ma_hieu_pho=None, ma_gvbm=None, ten_mon=None, ten_mon_moi=None):
    if not (xac_thuc_quyen_dac_biet(ma_hieu_truong, "hieu truong") and
            xac_thuc_quyen_dac_biet(ma_hieu_pho, "hieu pho") and
            xac_thuc_quyen_dac_biet(ma_gvbm, "giáo viên bộ môn")):
        print("Loi: Can xac thuc bo ba Hieu truong, Hieu pho va Giao vien bo mon de thuc hien chuc nang quan ly mon hoc.")
        return False

    cac_mon_hoc_hien_co = ["Toán", "Lý", "Anh"] # Danh sach cac mon hoc co dinh

    if chuc_nang == "them":
        if not ten_mon:
            print("Loi: Vui long cung cap ten mon hoc can them.")
            return False
        if ten_mon in cac_mon_hoc_hien_co:
            print(f"Loi: Mon hoc '{ten_mon}' da ton tai.")
            return False
        cac_mon_hoc_hien_co.append(ten_mon)
        print(f"Da them mon hoc '{ten_mon}'.")
        # Trong thuc te, can cap nhat vao mot file/database luu tru mon hoc
        return True
    
    elif chuc_nang == "sua":
        if not ten_mon or not ten_mon_moi:
            print("Loi: Vui long cung cap ten mon hoc cu va ten mon hoc moi de sua.")
            return False
        if ten_mon not in cac_mon_hoc_hien_co:
            print(f"Loi: Mon hoc '{ten_mon}' khong ton tai.")
            return False
        if ten_mon_moi in cac_mon_hoc_hien_co and ten_mon_moi != ten_mon:
            print(f"Loi: Ten mon hoc moi '{ten_mon_moi}' da ton tai.")
            return False
        
        vi_tri = cac_mon_hoc_hien_co.index(ten_mon)
        cac_mon_hoc_hien_co[vi_tri] = ten_mon_moi
        print(f"Da doi ten mon hoc '{ten_mon}' thanh '{ten_mon_moi}'.")
        # Trong thuc te, can cap nhat vao mot file/database luu tru mon hoc
        return True

    elif chuc_nang == "xoa":
        if not ten_mon:
            print("Loi: Vui long cung cap ten mon hoc can xoa.")
            return False
        if ten_mon not in cac_mon_hoc_hien_co:
            print(f"Loi: Mon hoc '{ten_mon}' khong ton tai.")
            return False
        
        cac_mon_hoc_hien_co.remove(ten_mon)
        print(f"Da xoa mon hoc '{ten_mon}'.")
        # Trong thuc te, can cap nhat vao mot file/database luu tru mon hoc
        return True
    else:
        print("Loi: Chuc nang quan ly mon hoc khong hop le.")
        return False

# --- Menu chinh ---
def hien_thi_menu():
    print("\n--- HE THONG QUAN LY TRUONG HOC ---")
    print("1. Quan ly Hoc sinh")
    print("2. Quan ly Giao vien")
    print("3. Quan ly Lich hoc (Thoi khoa bieu)")
    print("4. Bao cao va Thong ke")
    print("5. Cac chuc nang khac")
    print("0. Thoat")

def menu_quan_ly_hoc_sinh():
    while True:
        print("\n--- QUAN LY HOC SINH ---")
        print("1. Them moi hoc sinh")
        print("2. Xem/Tim kiem hoc sinh")
        print("3. Cap nhat thong tin hoc sinh")
        print("4. Xoa hoc sinh")
        print("5. Xoa hoc sinh theo dieu kien (nghi > 25 tiet)")
        print("6. Nhap diem mon hoc")
        print("7. Xem bang diem ca nhan")
        print("8. Nhap so tiet nghi")
        print("0. Quay lai Menu chinh")
        
        lua_chon = input("Nhap lua chon cua ban: ")

        if lua_chon == '1':
            ma_hs = int(input("Nhap ma hoc sinh: "))
            ho_ten = input("Nhap ho ten hoc sinh: ")
            que_quan = input("Nhap que quan: ")
            sdt = input("Nhap so dien thoai phu huynh: ")
            khoi = input("Nhap khoi (vd: khoi_6): ")
            lop = input("Nhap lop (vd: 6-01): ")
            them_moi_hoc_sinh(ma_hs, ho_ten, que_quan, sdt, khoi, lop)
        elif lua_chon == '2':
            ma_hs = input("Nhap ma hoc sinh (bo qua neu khong tim theo ma): ")
            ho_ten = input("Nhap ho ten hoc sinh (bo qua neu khong tim theo ten): ")
            lop = input("Nhap lop (bo qua neu khong tim theo lop): ")
            khoi = input("Nhap khoi (bo qua neu khong tim theo khoi): ")
            
            ma_hs = int(ma_hs) if ma_hs else None
            ket_qua = xem_tim_kiem_hoc_sinh(ma_hs, ho_ten, lop, khoi)
            if ket_qua:
                print("\nKet qua tim kiem:")
                for hs in ket_qua:
                    print(f"Ma: {hs.get('mahocsinh')}, Ten: {hs.get('hotenhocsinh')}, Lop: {hs.get('lop')}, Khoi: {hs.get('khoi')}")
            else:
                print("Khong tim thay hoc sinh nao.")
        elif lua_chon == '3':
            ma_hs = int(input("Nhap ma hoc sinh can cap nhat: "))
            du_lieu_moi = {}
            new_name = input("Nhap ho ten moi (bo qua neu khong doi): ")
            if new_name: du_lieu_moi["hotenhocsinh"] = new_name
            new_quequan = input("Nhap que quan moi (bo qua neu khong doi): ")
            if new_quequan: du_lieu_moi["quequan"] = new_quequan
            new_sodt = input("Nhap so dien thoai moi (bo qua neu khong doi): ")
            if new_sodt: du_lieu_moi["sodt"] = new_sodt
            
            if du_lieu_moi:
                cap_nhat_thong_tin_hoc_sinh(ma_hs, du_lieu_moi)
            else:
                print("Khong co thong tin nao de cap nhat.")
        elif lua_chon == '4':
            ma_hs = int(input("Nhap ma hoc sinh can xoa: "))
            xoa_hoc_sinh(ma_hs)
        elif lua_chon == '5':
            gioi_han = int(input("Nhap so tiet nghi gioi han de xoa (mac dinh 25): ") or 25)
            xoa_hoc_sinh_theo_dieu_kien(gioi_han)
        elif lua_chon == '6':
            ma_gv = input("Nhap ma giao vien: ")
            sdt_gv = input("Nhap so dien thoai giao vien: ")
            ma_hs = int(input("Nhap ma hoc sinh: "))
            ten_mon = input("Nhap ten mon hoc (Toan, Ly, Anh): ")
            diem_gk = input("Nhap diem giua ky (bo qua neu khong co): ")
            diem_ck = input("Nhap diem cuoi ky (bo qua neu khong co): ")
            
            diem_gk = float(diem_gk) if diem_gk else None
            diem_ck = float(diem_ck) if diem_ck else None
            
            nhap_diem_mon_hoc(ma_gv, sdt_gv, ma_hs, ten_mon, diem_gk, diem_ck)
        elif lua_chon == '7':
            ma_hs = int(input("Nhap ma hoc sinh can xem bang diem: "))
            xem_bang_diem_ca_nhan(ma_hs)
        elif lua_chon == '8':
            ma_gv = input("Nhap ma giao vien bo mon: ")
            sdt_gv = input("Nhap so dien thoai giao vien: ")
            ma_hs = int(input("Nhap ma hoc sinh: "))
            ten_mon = input("Nhap ten mon hoc (Toan, Ly, Anh): ")
            so_tiet = int(input("Nhap so tiet nghi them: "))
            nhap_so_tiet_nghi(ma_gv, sdt_gv, ma_hs, ten_mon, so_tiet)
        elif lua_chon == '0':
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")

def menu_quan_ly_giao_vien():
    while True:
        print("\n--- QUAN LY GIAO VIEN ---")
        print("1. Them moi giao vien")
        print("2. Xem/Tim kiem giao vien")
        print("3. Cap nhat thong tin giao vien (Chi admin he thong)")
        print("4. Nhap/Cap nhat thanh tich giao vien (Chi admin he thong)")
        print("5. Phan cong giao vien chu nhiem (Chi admin he thong)")
        print("6. Phan cong giao vien bo mon (Chi admin he thong)")
        print("0. Quay lai Menu chinh")

        lua_chon = input("Nhap lua chon cua ban: ")

        if lua_chon == '1':
            ma_gv = input("Nhap ma giao vien: ")
            ho_ten = input("Nhap ho ten giao vien: ")
            ngay_sinh = input("Nhap ngay sinh (YYYY-MM-DD): ")
            gioi_tinh = input("Nhap gioi tinh: ")
            sdt = input("Nhap so dien thoai: ")
            email = input("Nhap email: ")
            chuc_vu = input("Nhap chuc vu (gvcn/giáo viên bộ môn/hieu truong/hieu pho): ")
            bang_cap = input("Nhap bang cap: ")
            mon_hoc = input("Nhap mon hoc phu trach (cach nhau boi dau phay, bo qua neu khong phai gvbm): ").split(',') if chuc_vu == "giáo viên bộ môn" else None
            lop_cn = input("Nhap lop chu nhiem (bo qua neu khong phai gvcn): ") if chuc_vu == "gvcn" else None
            them_moi_giao_vien(ma_gv, ho_ten, ngay_sinh, gioi_tinh, sdt, email, chuc_vu, bang_cap, mon_hoc, lop_cn)
        elif lua_chon == '2':
            ma_gv = input("Nhap ma giao vien (bo qua neu khong tim theo ma): ")
            ho_ten = input("Nhap ho ten giao vien (bo qua neu khong tim theo ten): ")
            chuc_vu = input("Nhap chuc vu (bo qua neu khong tim theo chuc vu): ")
            mon_hoc = input("Nhap mon hoc phu trach (bo qua neu khong tim theo mon): ")
            
            ket_qua = xem_tim_kiem_giao_vien(ma_gv, ho_ten, chuc_vu, mon_hoc)
            if ket_qua:
                print("\nKet qua tim kiem:")
                for gv in ket_qua:
                    print(f"Ma: {gv.get('magiaovien')}, Ten: {gv.get('hotengiaovien')}, Chuc vu: {gv.get('chucvu')}, Mon: {gv.get('monhocphutrach')}, Lop CN: {gv.get('lopchunhiem')}")
            else:
                print("Khong tim thay giao vien nao.")
        elif lua_chon == '3':
            ma_admin = input(f"Nhap ma admin he thong ({MA_ADMIN_HE_THONG}) de xac thuc: ")
            ma_gv_cap_nhat = input("Nhap ma giao vien can cap nhat: ")
            du_lieu_moi = {}
            new_sdt = input("Nhap so dien thoai moi (bo qua neu khong doi): ")
            if new_sdt: du_lieu_moi["sodt"] = new_sdt
            new_email = input("Nhap email moi (bo qua neu khong doi): ")
            if new_email: du_lieu_moi["email"] = new_email
            new_chucvu = input("Nhap chuc vu moi (bo qua neu khong doi): ")
            if new_chucvu: du_lieu_moi["chucvu"] = new_chucvu
            
            cap_nhat_thong_tin_giao_vien(ma_gv_cap_nhat, du_lieu_moi, ma_admin)
        elif lua_chon == '4':
            ma_admin = input(f"Nhap ma admin he thong ({MA_ADMIN_HE_THONG}) de xac thuc: ")
            ma_gv = input("Nhap ma giao vien can cap nhat thanh tich: ")
            thanh_tich = input("Nhap thanh tich moi: ")
            nhap_cap_nhat_thanh_tich_giao_vien(ma_gv, thanh_tich, ma_admin)
        elif lua_chon == '5':
            ma_admin = input(f"Nhap ma admin he thong ({MA_ADMIN_HE_THONG}) de xac thuc: ")
            ma_gv = input("Nhap ma giao vien can phan cong chu nhiem: ")
            lop_cn = input("Nhap lop chu nhiem moi: ")
            phan_cong_gvcn(ma_gv, lop_cn, ma_admin)
        elif lua_chon == '6':
            ma_admin = input(f"Nhap ma admin he thong ({MA_ADMIN_HE_THONG}) de xac thuc: ")
            ma_gv = input("Nhap ma giao vien can phan cong bo mon: ")
            mon_hoc = input("Nhap mon hoc moi (Toan/Ly/Anh): ")
            phan_cong_gvbm(ma_gv, mon_hoc, ma_admin)
        elif lua_chon == '0':
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")

def menu_quan_ly_lich_hoc():
    while True:
        print("\n--- QUAN LY LICH HOC ---")
        print("1. Tao/Chinh sua thoi khoa bieu (Chi admin he thong)")
        print("2. Xem thoi khoa bieu theo lop")
        print("3. Xem lich day theo giao vien")
        print("0. Quay lai Menu chinh")

        lua_chon = input("Nhap lua chon cua ban: ")

        if lua_chon == '1':
            ma_admin = input(f"Nhap ma admin he thong ({MA_ADMIN_HE_THONG}) de xac thuc: ")
            lop = input("Nhap lop can tao/chinh sua TKB: ")
            ngay = input("Nhap ngay (vd: Thu Hai): ")
            danh_sach_tiet_hoc = []
            while True:
                tiet = input("Nhap tiet hoc (vd: 1, 2, ... hoac 'xong' de ket thuc): ")
                if tiet.lower() == 'xong':
                    break
                mon = input("Nhap ten mon: ")
                ma_gv = input("Nhap ma giao vien: ")
                phong = input("Nhap phong hoc: ")
                danh_sach_tiet_hoc.append({"tiet": int(tiet), "mon": mon, "ma_gv": ma_gv, "phong": phong})
            tao_chinh_sua_thoi_khoa_bieu(ma_admin, lop, ngay, danh_sach_tiet_hoc)
        elif lua_chon == '2':
            lop = input("Nhap lop can xem thoi khoa bieu: ")
            xem_thoi_khoa_bieu(lop=lop)
        elif lua_chon == '3':
            ma_gv = input("Nhap ma giao vien can xem lich day: ")
            xem_thoi_khoa_bieu(ma_giao_vien=ma_gv)
        elif lua_chon == '0':
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")

def menu_bao_cao_thong_ke():
    while True:
        print("\n--- BAO CAO VA THONG KE ---")
        print("1. Bao cao hoc luc hoc sinh theo lop")
        print("2. Bang tong hop diem lop")
        print("3. Bao cao hoc sinh nghi nhieu")
        print("4. Thong ke giao vien theo chuc vu")
        print("5. Thong ke giao vien theo mon hoc")
        print("0. Quay lai Menu chinh")

        lua_chon = input("Nhap lua chon cua ban: ")

        if lua_chon == '1':
            khoi = input("Nhap khoi (vd: khoi_6): ")
            lop = input("Nhap lop (vd: 6-01): ")
            bao_cao_hoc_luc_hoc_sinh_theo_lop(khoi, lop)
        elif lua_chon == '2':
            khoi = input("Nhap khoi (vd: khoi_6): ")
            lop = input("Nhap lop (vd: 6-01): ")
            bao_cao_tong_hop_diem_lop(khoi, lop)
        elif lua_chon == '3':
            gioi_han = int(input("Nhap gioi han so tiet nghi (mac dinh 5): ") or 5)
            bao_cao_hoc_sinh_nghi_nhieu(gioi_han)
        elif lua_chon == '4':
            thong_ke_giao_vien_theo_chuc_vu()
        elif lua_chon == '5':
            thong_ke_giao_vien_theo_mon_hoc()
        elif lua_chon == '0':
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")

def menu_cac_chuc_nang_khac():
    while True:
        print("\n--- CAC CHUC NANG KHAC ---")
        print("1. Thong bao va Canh bao (GVCN/Hieu truong/Hieu pho)")
        print("2. Quan ly Lop hoc (Hieu truong/Hieu pho/GVBM)")
        print("3. Quan ly Mon hoc (Hieu truong/Hieu pho/GVBM)")
        print("0. Quay lai Menu chinh")

        lua_chon = input("Nhap lua chon cua ban: ")

        if lua_chon == '1':
            ma_gv_xac_thuc = input("Nhap ma giao vien cua ban: ")
            lop_duyet = input("Nhap lop can duyet ket qua: ")
            thong_bao_va_canh_bao(ma_gv_xac_thuc, lop_duyet)
        elif lua_chon == '2':
            print("\n--- QUAN LY LOP HOC ---")
            print("a. Them lop")
            print("b. Sua ten lop")
            print("c. Xoa lop")
            print("d. Chuyen lop hoc sinh")
            chuc_nang_ql_lop = input("Chon chuc nang (a/b/c/d): ")
            
            ma_ht = input(f"Nhap ma Hieu truong ({MA_ADMIN_HE_THONG}): ")
            ma_hp = input(f"Nhap ma Hieu pho ({MA_ADMIN_HE_THONG}): ")
            ma_gvbm = input(f"Nhap ma Giao vien bo mon ({MA_ADMIN_HE_THONG}): ")

            if chuc_nang_ql_lop == 'a':
                khoi = input("Nhap khoi (vd: khoi_6): ")
                lop = input("Nhap ten lop moi: ")
                quan_ly_lop_hoc("them", ma_ht, ma_hp, ma_gvbm, khoi=khoi, lop=lop)
            elif chuc_nang_ql_lop == 'b':
                khoi = input("Nhap khoi (vd: khoi_6): ")
                lop_cu = input("Nhap ten lop cu: ")
                lop_moi = input("Nhap ten lop moi: ")
                quan_ly_lop_hoc("sua", ma_ht, ma_hp, ma_gvbm, khoi=khoi, lop=lop_cu, lop_moi=lop_moi)
            elif chuc_nang_ql_lop == 'c':
                khoi = input("Nhap khoi (vd: khoi_6): ")
                lop = input("Nhap ten lop can xoa: ")
                quan_ly_lop_hoc("xoa", ma_ht, ma_hp, ma_gvbm, khoi=khoi, lop=lop)
            elif chuc_nang_ql_lop == 'd':
                ma_hs = int(input("Nhap ma hoc sinh can chuyen: "))
                khoi_moi = input("Nhap khoi moi (vd: khoi_6): ")
                lop_moi = input("Nhap lop moi (vd: 6-01): ")
                quan_ly_lop_hoc("chuyen_lop_hoc_sinh", ma_ht, ma_hp, ma_gvbm, ma_hoc_sinh=ma_hs, khoi=khoi_moi, lop_moi=lop_moi)
            else:
                print("Chuc nang khong hop le.")

        elif lua_chon == '3':
            print("\n--- QUAN LY MON HOC ---")
            print("a. Them mon hoc")
            print("b. Sua ten mon hoc")
            print("c. Xoa mon hoc")
            chuc_nang_ql_mon = input("Chon chuc nang (a/b/c): ")

            ma_ht = input(f"Nhap ma Hieu truong ({MA_ADMIN_HE_THONG}): ")
            ma_hp = input(f"Nhap ma Hieu pho ({MA_ADMIN_HE_THONG}): ")
            ma_gvbm = input(f"Nhap ma Giao vien bo mon ({MA_ADMIN_HE_THONG}): ")

            if chuc_nang_ql_mon == 'a':
                ten_mon = input("Nhap ten mon hoc moi: ")
                quan_ly_mon_hoc("them", ma_ht, ma_hp, ma_gvbm, ten_mon=ten_mon)
            elif chuc_nang_ql_mon == 'b':
                ten_mon_cu = input("Nhap ten mon hoc cu: ")
                ten_mon_moi = input("Nhap ten mon hoc moi: ")
                quan_ly_mon_hoc("sua", ma_ht, ma_hp, ma_gvbm, ten_mon=ten_mon_cu, ten_mon_moi=ten_mon_moi)
            elif chuc_nang_ql_mon == 'c':
                ten_mon = input("Nhap ten mon hoc can xoa: ")
                quan_ly_mon_hoc("xoa", ma_ht, ma_hp, ma_gvbm, ten_mon=ten_mon)
            else:
                print("Chuc nang khong hop le.")
        elif lua_chon == '0':
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")

def main():
    while True:
        hien_thi_menu()
        lua_chon_chinh = input("Nhap lua chon cua ban: ")

        if lua_chon_chinh == '1':
            menu_quan_ly_hoc_sinh()
        elif lua_chon_chinh == '2':
            menu_quan_ly_giao_vien()
        elif lua_chon_chinh == '3':
            menu_quan_ly_lich_hoc()
        elif lua_chon_chinh == '4':
            menu_bao_cao_thong_ke()
        elif lua_chon_chinh == '5':
            menu_cac_chuc_nang_khac()
        elif lua_chon_chinh == '0':
            print("Cam on ban da su dung he thong. Tam biet!")
            break
        else:
            print("Lua chon khong hop le. Vui long chon lai.")

if __name__ == "__main__":
    main()
