import qrcode

# 생성할 링크
link = "https://github.com/redspace9/openAPI_tlgja"

# QR 코드 생성
qr = qrcode.QRCode(
    version=1,  # QR 코드 크기
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # 오류 수정 수준
    box_size=10,  # 각 박스 크기
    border=4,  # 테두리 크기
)

# 링크를 QR 코드에 추가
qr.add_data(link)
qr.make(fit=True)

# 이미지를 생성
img = qr.make_image(fill='black', back_color='white')

# 이미지 저장
img.save("link_qr_code.png")

# 또는 이미지 보기
img.show()