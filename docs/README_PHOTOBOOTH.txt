PHOTOBOOTH - GOI WORKER GIU MODEL SAN SANG

Neu chay tu ma nguon tren may co Python 3.12 x64, chay INSTALL.bat mot lan.
Moi truong rieng .photobooth-env se duoc tao. Sau do chay launcher ben duoi;
model tu tai trong lan chay dau tien va can ket noi Internet.

Chay:
  RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input"

Anh da co trong Input luc worker khoi dong se bi bo qua. Chi anh duoc them sau
khi worker chay moi duoc xu ly. Worker doi anh ghi xong, tu dong tach nen va
xuat PNG vao Input\output_no_bg. Giu cua so worker mo suot
phien chup; nhan Ctrl+C khi ket thuc. Model/session duoc nap mot lan moi phien,
khong nap lai cho tung anh.

Goi nay chi co chuc nang Photobooth, dung model birefnet-general. Goi kem Python
runtime, thu vien DirectML va model. GPU DirectX 12 duoc uu tien; neu DirectML
khong kha dung, chuong trinh tu chuyen sang CPU. May dich Windows x64 khong can
cai Python, pip, rembg hay ONNX Runtime. Model da duoc dong goi, khong can tai
Internet. Giu toan bo thu muc, bao gom _internal.

DirectML can Windows 10 phien ban 1903 tro len va driver GPU tuong thich.
Khong can cai CUDA Toolkit/cuDNN. Toc do phu thuoc GPU, driver va kich thuoc anh.
