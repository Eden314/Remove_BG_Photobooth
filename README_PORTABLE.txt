AI TACH PHONG - GOI PORTABLE CHO WINDOWS x64

CACH DUNG MOT LAN
1. Giai nen ca thu muc AI_Tach_Phong vao may Windows x64.
2. Ke tep anh hoac thu muc anh vao RUN_REMOVE_BG_PORTABLE.bat.
3. PNG nen trong suot duoc tao trong thu muc output_no_bg ben canh anh goc.

CHE DO PHOTOBOOTH (GIU MODEL LUON SAN SANG)
1. Chay RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input".
2. De ung dung chup anh vao thu muc Input; ket qua tu dong xuat vao
   Input\output_no_bg.
3. Giu cua so worker mo trong suot phien chup; nhan Ctrl+C de dung.
   Worker nap model mot lan, khong nap lai cho moi tam anh.

Goi da kem Python runtime, cac thu vien can thiet, model birefnet-general FP32
va ban FP16 toi uu cho GPU, cung CUDA/cuDNN runtime. May dich khong can cai
Python, pip, rembg hay ONNX Runtime. Model duoc dong goi nen khong tai Internet.
GPU NVIDIA dung ban FP16; CPU dung model FP32 goc.

May co NVIDIA GPU can co driver NVIDIA tuong thich. Neu CUDA khong san sang,
chuong trinh tu chuyen sang CPU; khong can cai CUDA Toolkit rieng.
May khong co GPU NVIDIA van co the xu ly bang CPU, nhung se cham hon.
De ep dung CPU tren may co GPU, them --cpu vao lenh chay EXE.

Goi mac dinh can Windows x64; khong chay truc tiep tren macOS/Linux. Goi chiem
khoang 4.2 GiB sau khi giai nen; phai giu toan bo thu muc AI_Tach_Phong, bao
gom _internal.

Thoi gian tung anh hien trong cua so. Nap model/session mat thoi gian rieng;
che do photobooth giu session trong RAM/VRAM de tranh nap lai moi tam anh.
Toc do suy luan tuy thuoc GPU/driver; khong the bao dam duoi 10 giay tren moi PC.

Luu y: model van co the nhan dien sai mot so vat the. Dong goi khong lam model
chinh xac hon. Neu can cuu vat AI xoa nham, su dung --keep-mask nhu README.txt.
