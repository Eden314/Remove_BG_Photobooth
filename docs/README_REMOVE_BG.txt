REMOVE_BG - GOI TACH ANH DOC LAP

Ke mot tep anh hoac thu muc anh vao RUN_REMOVE_BG_PORTABLE.bat.
PNG nen trong suot duoc tao trong thu muc output_no_bg ben canh anh goc.

Goi nay chi co chuc nang tach anh theo yeu cau, dung model birefnet-general.
Goi kem Python runtime, thu vien DirectML va model. GPU DirectX 12 duoc uu tien;
neu DirectML khong kha dung, chuong trinh tu chuyen sang CPU. May dich Windows
x64 khong can cai Python, pip, rembg hay ONNX Runtime. Model da duoc dong goi,
khong can tai Internet. Giu toan bo thu muc, bao gom _internal.

DirectML can Windows 10 phien ban 1903 tro len va driver GPU tuong thich.
Khong can cai CUDA Toolkit/cuDNN. Goi nay khong theo doi thu muc lien tuc.
