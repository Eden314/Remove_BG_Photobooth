PHOTOBOOTH - GOI WORKER GIU MODEL SAN SANG

Chay:
  RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input"

Cho phan mem chup anh luu anh goc vao thu muc Input. Worker se doi anh ghi xong,
tu dong tach nen va xuat PNG vao Input\output_no_bg. Giu cua so worker mo suot
phien chup; nhan Ctrl+C khi ket thuc. Model/session duoc nap mot lan moi phien,
khong nap lai cho tung anh.

Goi nay chi co chuc nang Photobooth, dung model birefnet-general. Goi kem Python
runtime, thu vien, model va CUDA/cuDNN runtime. May dich Windows x64 khong can
cai Python, pip, rembg hay ONNX Runtime. Model da duoc dong goi, khong can tai
Internet. Giu toan bo thu muc, bao gom _internal.

May co NVIDIA GPU can driver NVIDIA tuong thich. Neu CUDA khong san sang,
chuong trinh tu chuyen sang CPU. Toc do phu thuoc GPU, driver va kich thuoc anh.
