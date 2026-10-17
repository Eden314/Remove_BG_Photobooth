HUONG DAN TACH PHONG CHAN DUNG

1. Cai Python 3.10 - 3.12 (ban 64-bit, tick "Add python.exe to PATH").
2. Chay INSTALL.bat mot lan.
3. Keo mot tep anh hoac thu muc anh vao RUN_REMOVE_BG.bat.
4. Anh PNG trong suot nam trong thu muc output_no_bg ben canh anh goc.

Mac dinh dung model birefnet-general. Chuong trinh chay tren GPU NVIDIA neu CUDA
san sang, neu khong se tu chuyen sang CPU. Model duoc tai mot lan va luu trong
cache; lan dau can Internet. Anh goc khong doi.

Neu AI xoa nham mot vat can giu (vi du may anh dang cam), tao mot tep mask
den-trang cung kich thuoc voi anh: to trang len vat can giu, de nen mau den.
Sau do chay:
  RUN_REMOVE_BG.bat "D:\Anh\ChânDung6.jpg" --keep-mask "D:\Anh\ChânDung6-keep.png"
Vung trang trong mask se duoc giu lai; vung den van theo ket qua AI. Co the dung
Paint.NET, GIMP hoac phan mem ve co lop de to mask. Mask cung co the co mau xam
de tao vien mem. Cach nay sua dung anh cu the, khong can huan luyen lai model.

De xu ly nhieu anh bang mot lan nap model, dua ca thu muc vao RUN_REMOVE_BG.bat.
De dung photobooth va nap model mot lan cho ca phien chup, chay:
  RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input"
De ung dung chup anh vao thu muc Input; PNG duoc tao trong Input\output_no_bg.
Giu cua so worker mo; nhan Ctrl+C de dung. Cua so in thoi gian nap model/session
va thoi gian xu ly moi anh de tach ro phan khoi dong voi phan suy luan.

Toc do tuy thuoc model, GPU va driver; khong the bao dam duoi 10 giay tren moi
may. Dung che do WATCH de giu session trong RAM/VRAM, khong khoi dong lai app
cho tung tam anh. CUDA Graph chua bat vi driver/model tren may build loi capture.

Ho tro JPG, JPEG, PNG, WEBP, BMP. Ket qua PNG co kenh alpha trong suot.
Khong co mo hinh nao bao dam giu dung moi vat the trong moi anh; model tong quat
co the giu vat cam tay tot hon nhung cung co the giu them mot phan nen.
