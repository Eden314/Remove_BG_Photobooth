# Tách phông ảnh Windows

## Cấu trúc thư mục

- `src/`: mã Python của bộ tách ảnh và worker Photobooth.
- `docs/`: hướng dẫn sử dụng riêng cho từng gói portable.
- `RUN_*.bat`, `INSTALL.bat`, `BUILD_*.bat`: các lệnh chạy, cài đặt và đóng gói.
- `build/`, `.build_models/`, `.directml-build-env/`: tệp sinh ra trong quá trình build.
- `dist/`: các gói portable đã build.
- `Image/`, `CamVot/`: dữ liệu ảnh của dự án.

Dự án đóng gói hai ứng dụng độc lập bằng cùng một model `birefnet-general`:

| Ứng dụng | Dùng khi | Cách chạy |
|---|---|---|
| Remove_BG | Tách một ảnh hoặc một thư mục ảnh theo yêu cầu | Kéo ảnh/thư mục vào `RUN_REMOVE_BG_PORTABLE.bat` |
| Photobooth | Chạy liên tục, giữ model trong RAM/VRAM và tự xử lý ảnh mới | Chạy `RUN_PHOTOBOOTH_WATCH.bat "D:\Anh\Input"` |

Cả hai gói dùng ONNX Runtime DirectML để tăng tốc trên GPU DirectX 12 của nhiều
hãng (NVIDIA, AMD, Intel); nếu GPU/driver không hỗ trợ hoặc khởi tạo lỗi thì tự
chuyển sang CPU. DirectML yêu cầu Windows 10 phiên bản 1903 trở lên và driver GPU
phù hợp. Không cần cài CUDA Toolkit hay cuDNN.

## Dùng gói đã build

Lấy riêng thư mục `dist\Remove_BG` hoặc `dist\Photobooth` tùy chức năng. Mỗi
thư mục là một gói portable tự chứa Python runtime, thư viện DirectML và model.
Sao chép toàn bộ thư mục sang Windows x64; không cần cài Python hay pip.
Không tách riêng EXE khỏi thư mục `_internal`.

Photobooth theo dõi thư mục đầu vào. Phần mềm chụp ảnh cần lưu ảnh gốc vào đó;
khi tệp ảnh đã ghi xong, kết quả PNG xuất hiện trong `output_no_bg`. Giữ cửa sổ
Photobooth mở trong phiên, nhấn Ctrl+C để dừng. Model chỉ được nạp một lần mỗi
phiên chạy.

Hai gói có model và runtime riêng để có thể mang từng gói sang máy khác độc lập.
Model vẫn là BiRefNet General duy nhất; đổi backend không làm tăng độ chính xác
hay đảm bảo mọi vật thể cầm tay đều được giữ lại. DirectML có hỗ trợ rộng nhưng
tốc độ phụ thuộc GPU, driver và các phép toán được tăng tốc trên từng thiết bị.

## Build lại

Trên máy build cài Python 3.12 x64, chạy `INSTALL.bat` để cài môi trường xử lý,
tải model gốc rồi chạy `BUILD_PACKAGES.bat`. Hướng dẫn riêng nằm trong thư mục
[`docs`](docs/). Kết quả nằm trong
`dist\Remove_BG` và `dist\Photobooth`. Build cần khoảng 4 GB dung lượng trống.
