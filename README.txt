HUONG DAN TACH PHONG CHAN DUNG

1. Cai Python 3.10 - 3.12 (ban 64-bit, tick "Add python.exe to PATH").
2. Chay INSTALL.bat mot lan.
3. Keo mot tep anh hoac thu muc anh vao RUN_REMOVE_BG.bat.
4. Anh PNG trong suot nam trong thu muc output_no_bg ben canh anh goc.

Mac dinh dung birefnet-general de giu nguoi va cac vat the nhu vat cam tay.
Lan chay dau tien se tai model AI, can ket noi Internet. Xu ly cung bat khu
loang mau vien de giam vien mau nen tren toc, quan ao va chi tiet mem.
Anh goc khong doi.

Neu chu the la chan dung va can thu model uu tien nguoi:
  RUN_REMOVE_BG.bat "D:\Anh" --model birefnet-portrait

Neu hinh dang mep (vi du toc) bi cat hoac mep cung, thu tinh chinh alpha:
  RUN_REMOVE_BG.bat "D:\Anh" --alpha-matting

Alpha matting cham hon; hay doi chieu ket qua tren nen sang va nen toi.
Neu can so sanh voi model cu:
  RUN_REMOVE_BG.bat "D:\Anh" --model isnet-general-use

Ho tro JPG, JPEG, PNG, WEBP, BMP. Ket qua PNG co kenh alpha trong suot.
Khong co mo hinh nao bao dam giu dung moi vat the trong moi anh; model tong quat
co the giu vat cam tay tot hon nhung cung co the giu them mot phan nen.
