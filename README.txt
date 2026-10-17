HUONG DAN TACH PHONG CHAN DUNG

1. Cai Python 3.10 - 3.12 (ban 64-bit, tick "Add python.exe to PATH").
2. Chay INSTALL.bat mot lan.
3. Keo mot tep anh hoac thu muc anh vao RUN_REMOVE_BG.bat.
4. Anh PNG trong suot nam trong thu muc output_no_bg ben canh anh goc.

Mac dinh dung birefnet-general, xu ly tren GPU NVIDIA neu da cai dat bang
INSTALL.bat. May co RTX 3050 Ti se duoc chay bang GPU thay vi CPU. Model duoc
tai trong lan chay dau tien, can ket noi Internet. Alpha matting da duoc bo
vi co the lam vien bi loi pixel; chuong trinh chi khu loang mau vien.
Anh goc khong doi.

Neu muon uu tien toc do hon nua, chon ban nhe:
  RUN_REMOVE_BG.bat "D:\Anh" --model birefnet-general-lite

Neu chu the la chan dung va can thu model uu tien nguoi:
  RUN_REMOVE_BG.bat "D:\Anh" --model birefnet-portrait

Neu can so sanh voi model cu:
  RUN_REMOVE_BG.bat "D:\Anh" --model isnet-general-use

Khi bat dau, dong "Xu ly bang" se cho biet dang dung GPU NVIDIA hay CPU.

Ho tro JPG, JPEG, PNG, WEBP, BMP. Ket qua PNG co kenh alpha trong suot.
Khong co mo hinh nao bao dam giu dung moi vat the trong moi anh; model tong quat
co the giu vat cam tay tot hon nhung cung co the giu them mot phan nen.
