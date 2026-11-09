Bộ công cụ scan

Trước khi sử dụng cần cài đặt các thư viện: 
    pip install -r requirements.txt

Hướng dẫn sử dụng chung: 
    python main.py -h

Hướng dẫn sử dụng các tính năng:
    - Local: python main.py [-t threads] Local -h 
    - Web: python main.py [-t threads] Web -h 
    - Network: python main.py [-t threads] Network -h 

Mô tả tính năng: 
    - Local: Scan port và service của máy tính, có thể in ra hoặc đưa vào file tùy lựa chọn
    - Web: Scan các service của trang web, brute-force sub-domains và uri trang web dựa trên wordlist có sẵn
    - Network: Scan port và service các máy tính trong mạng (demo có thể dùng máy ảo)