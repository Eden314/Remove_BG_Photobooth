# Tách phông ảnh Windows

Dự án đóng gói hai ứng dụng độc lập bằng cùng một model `birefnet-general`:

| Ứng dụng | Dùng khi | Cách chạy |
|---|---|---|
| Remove_BG | Tách một ảnh hoặc một thư mục ảnh theo yêu cầu | Kéo ảnh/thư mục vào `RUN_REMOVE_BG_PORTABLE.bat` |
| Photobooth | Chạy liên tục, giữ model trong RAM/VRAM và tự xử lý ảnh mới | Chạy `RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input"` |

## Dùng gói đã build

Lấy riêng thư mục `dist\Remove_BG` hoặc `dist\Photobooth` tùy chức năng. Mỗi
thư mục là một gói portable tự chứa Python runtime, thư viện, CUDA/cuDNN và
model. Sao chép toàn bộ thư mục sang Windows x64; không cần cài Python hay pip.
Không tách riêng EXE khỏi thư mục `_internal`.

Photobooth theo dõi thư mục đầu vào. Phần mềm chụp ảnh cần lưu ảnh gốc vào đó;
khi tệp ảnh đã ghi xong, kết quả PNG xuất hiện trong `output_no_bg`. Giữ cửa sổ
Photobooth mở trong phiên, nhấn Ctrl+C để dừng. Model chỉ được nạp một lần mỗi
phiên chạy.

Hai gói có model và runtime riêng để có thể mang từng gói sang máy khác độc lập.
Vì vậy tổng dung lượng của cả hai gói lớn hơn dùng một gói chung. Model vẫn là
BiRefNet General duy nhất; đổi cách đóng gói không làm tăng độ chính xác hay đảm
bảo mọi vật thể cầm tay đều được giữ lại.

## Build lại

Trên máy build cài Python 3.10 x64, chạy `INSTALL.bat` để cài môi trường xử lý,
tải model gốc rồi chạy `BUILD_PACKAGES.bat`. Kết quả nằm trong
`dist\Remove_BG` và `dist\Photobooth`. Build cần khoảng 10 GB dung lượng trống.
