"""Hand-authored educational fixtures, not customer records.

Each semantic family stays in one split. English and Thai paraphrases of the
same request therefore cannot leak across train/dev/test.
"""

FAMILIES = {
    "account": [
        ("password", "train", ["I forgot my account password and need a reset", "Please help reset the password for my login", "ลืมรหัสผ่านบัญชี ขอเปลี่ยนรหัสผ่านใหม่", "ช่วยรีเซ็ตรหัสผ่านเพื่อเข้าบัญชีให้หน่อย"]),
        ("locked", "train", ["My account is locked after too many login attempts", "Unlock my account so I can sign in", "บัญชีถูกล็อกหลังใส่รหัสผิดหลายครั้ง", "เข้าบัญชีไม่ได้ ระบบแจ้งว่าบัญชีถูกล็อก"]),
        ("email", "train", ["Change the email address on my account", "My account email address is no longer active", "ขอเปลี่ยนอีเมลที่ผูกกับบัญชีผู้ใช้", "อีเมลบัญชีเก่าใช้ไม่ได้ อยากแก้ไขอีเมล"]),
        ("profile", "train", ["How do I edit my account profile name", "Update the phone number in my user profile", "แก้ไขชื่อและเบอร์โทรในโปรไฟล์บัญชีตรงไหน", "ต้องการอัปเดตข้อมูลส่วนตัวของบัญชีผู้ใช้"]),
        ("delete", "train", ["I want to delete my account permanently", "Please close my user account and remove my profile", "ต้องการลบบัญชีผู้ใช้ถาวร", "ช่วยปิดบัญชีและลบข้อมูลโปรไฟล์ให้ด้วย"]),
        ("signin", "train", ["I cannot sign in to my account with my password", "Login says my account credentials are invalid", "เข้าสู่ระบบบัญชีไม่ได้ทั้งที่รหัสผ่านถูกต้อง", "ล็อกอินบัญชีแล้วแจ้งว่าข้อมูลผู้ใช้ไม่ถูกต้อง"]),
        ("verification", "dev", ["The account verification email never arrived", "I need a new verification code to activate my account", "ไม่ได้รับอีเมลยืนยันบัญชีผู้ใช้", "ขอรหัสยืนยันเพื่อเปิดใช้งานบัญชีอีกครั้ง"]),
        ("twofactor", "dev", ["I lost my phone and cannot verify my account login", "Help restore account access with two factor authentication", "มือถือหายจึงรับรหัสเข้าบัญชีไม่ได้", "ต้องการกู้คืนบัญชีที่เปิดยืนยันตัวตนสองขั้นตอน"]),
        ("register", "test", ["I cannot create a new user account", "Registration will not let me open an account", "สมัครบัญชีผู้ใช้ใหม่ไม่ได้", "สร้างบัญชีใหม่แล้วระบบไม่ให้ลงทะเบียน"]),
        ("username", "test", ["Where can I change my account username", "My login username is wrong in my account settings", "ต้องการเปลี่ยนชื่อผู้ใช้ของบัญชี", "ชื่อที่ใช้ล็อกอินผิด แก้ไขในบัญชีตรงไหน"]),
    ],
    "billing": [
        ("duplicate", "train", ["My card was charged twice for one payment", "There are two charges for the same order on my bill", "บัตรถูกหักเงินซ้ำสองครั้งสำหรับคำสั่งซื้อเดียว", "ชำระเงินแล้วโดนเรียกเก็บเงินซ้ำในบิล"]),
        ("refund", "train", ["When will my payment refund reach my bank", "I paid but need a refund of the charge", "เงินที่ชำระไปจะคืนเข้าบัญชีธนาคารเมื่อไร", "ขอคืนเงินค่าบริการที่ชำระไปแล้ว"]),
        ("invoice", "train", ["Please send an invoice for my payment", "I need the receipt and billing invoice", "ขอใบเสร็จรับเงินและใบแจ้งหนี้", "ชำระเงินแล้วต้องการเอกสารใบกำกับภาษี"]),
        ("declined", "train", ["My credit card payment keeps getting declined", "The bank rejected my payment at checkout", "ชำระเงินด้วยบัตรเครดิตไม่ผ่าน", "ธนาคารปฏิเสธการชำระเงินตอนจ่ายเงิน"]),
        ("subscription", "train", ["Cancel my subscription before the next payment", "Stop charging my card for the monthly subscription", "ขอยกเลิกสมาชิกก่อนตัดเงินรอบถัดไป", "หยุดหักค่าบริการรายเดือนจากบัตรให้ด้วย"]),
        ("paymentmethod", "train", ["How can I update the card used for billing", "Can I pay this bill by bank transfer", "เปลี่ยนบัตรที่ใช้ชำระเงินค่าบริการได้อย่างไร", "ใบแจ้งหนี้นี้จ่ายเงินด้วยการโอนได้ไหม"]),
        ("overcharge", "dev", ["The amount charged is higher than the invoice total", "Why is the payment amount on my bill incorrect", "ยอดเงินที่ถูกหักมากกว่าราคาในใบแจ้งหนี้", "บิลเรียกเก็บเงินผิดจำนวน ช่วยตรวจยอดชำระ"]),
        ("coupon", "dev", ["My discount was missing when the payment was charged", "The coupon did not reduce the bill at payment", "ตอนชำระเงินส่วนลดไม่ถูกหักจากยอดบิล", "ใช้คูปองแล้วแต่ยอดเรียกเก็บเงินยังราคาเต็ม"]),
        ("tax", "test", ["Explain the extra tax charge on my billing invoice", "Why does my payment receipt include this tax amount", "ค่าภาษีที่เพิ่มในใบแจ้งหนี้คิดอย่างไร", "ใบเสร็จชำระเงินมีภาษีเพิ่มมาจากอะไร"]),
        ("installment", "test", ["Can this payment be split into monthly installments", "I want to pay my bill in installments with my card", "ยอดชำระเงินนี้แบ่งจ่ายรายเดือนได้ไหม", "อยากผ่อนชำระบิลผ่านบัตรเครดิต"]),
    ],
    "delivery": [
        ("late", "train", ["My parcel delivery is three days late", "The package has not arrived by the delivery date", "พัสดุจัดส่งล่าช้าเกินกำหนดสามวัน", "ถึงวันส่งสินค้าแล้วแต่ยังไม่ได้รับพัสดุ"]),
        ("tracking", "train", ["Where is the tracking number for my parcel", "The shipment tracking page does not show my package", "ขอเลขติดตามพัสดุที่จัดส่ง", "ติดตามสถานะขนส่งของสินค้าได้ที่ไหน"]),
        ("address", "train", ["Please change the delivery address before shipment", "The parcel is going to the wrong delivery address", "ขอเปลี่ยนที่อยู่จัดส่งก่อนส่งสินค้า", "พัสดุกำลังไปผิดที่อยู่ ต้องแก้ที่อยู่จัดส่ง"]),
        ("missing", "train", ["Tracking says delivered but my parcel is missing", "The courier marked my package delivered and I received nothing", "ขนส่งแจ้งว่าส่งแล้วแต่ไม่พบพัสดุ", "สถานะจัดส่งสำเร็จแต่ยังไม่ได้รับสินค้า"]),
        ("damaged", "train", ["My delivered parcel arrived with a broken product", "The package was damaged during shipping", "พัสดุที่ได้รับเสียหายระหว่างขนส่ง", "กล่องบุบและสินค้าแตกตอนจัดส่งมาถึง"]),
        ("wrongitem", "train", ["The delivered package contains the wrong product", "My shipment has a different item from my order", "พัสดุที่ส่งมาเป็นสินค้าผิดรายการ", "ได้รับสินค้าคนละอย่างกับที่สั่งจัดส่ง"]),
        ("courier", "dev", ["How can I contact the courier delivering my parcel", "The delivery driver cannot find my house", "ติดต่อพนักงานขนส่งที่นำพัสดุมาส่งได้ไหม", "คนส่งสินค้าหาที่อยู่บ้านไม่เจอ"]),
        ("return", "dev", ["I need the shipping label to return this parcel", "Where do I send the package for a product return", "ขอใบปะหน้าขนส่งสำหรับส่งคืนสินค้า", "ต้องส่งพัสดุคืนสินค้าไปที่อยู่ไหน"]),
        ("dispatch", "test", ["Has my order been shipped or is the parcel still waiting", "When will the warehouse dispatch my package for delivery", "คำสั่งซื้อส่งออกจากคลังหรือยัง รอพัสดุอยู่", "คลังสินค้าจะส่งพัสดุออกเมื่อไร"]),
        ("shippingfee", "test", ["What is the shipping fee to deliver this parcel upcountry", "How much does express package delivery cost", "ค่าขนส่งพัสดุไปต่างจังหวัดราคาเท่าไร", "ส่งสินค้าด่วนมีค่าจัดส่งเท่าไร"]),
    ],
    "technical": [
        ("crash", "train", ["The app crashes every time I open the dashboard", "Your website shows an error and closes unexpectedly", "แอปเด้งปิดเองทุกครั้งที่เปิดหน้าแดชบอร์ด", "เว็บแสดงข้อผิดพลาดแล้วปิดเองตลอด"]),
        ("blank", "train", ["The website loads a blank white screen", "The app screen stays empty after loading", "เปิดเว็บไซต์แล้วหน้าจอขาวโหลดไม่ขึ้น", "แอปโหลดเสร็จแล้วหน้าจอว่างเปล่า"]),
        ("upload", "train", ["File upload fails with a server error in the app", "I cannot upload a photo because the website errors", "อัปโหลดไฟล์ในเว็บไม่ได้ ระบบขึ้นข้อผิดพลาด", "แอปอัปโหลดรูปไม่สำเร็จและแจ้งเซิร์ฟเวอร์ผิดพลาด"]),
        ("slow", "train", ["The website is very slow and keeps freezing", "The app dashboard takes forever to load", "เว็บไซต์ช้ามากและค้างตลอด", "หน้าแดชบอร์ดแอปโหลดช้าผิดปกติ"]),
        ("api", "train", ["The API integration returns an internal server error", "My app cannot connect to your API endpoint", "เชื่อมต่อ API ไม่สำเร็จ ระบบแจ้งเซิร์ฟเวอร์ผิดพลาด", "แอปเรียก API แล้วได้รับข้อความ error"]),
        ("button", "train", ["The save button in the app does not respond", "Clicking the website submit button does nothing", "กดปุ่มบันทึกในแอปแล้วไม่ตอบสนอง", "ปุ่มส่งข้อมูลบนเว็บไซต์กดแล้วไม่มีอะไรเกิดขึ้น"]),
        ("video", "dev", ["The video player in the app freezes with an error", "The website cannot play video and shows a black screen", "แอปเล่นวิดีโอไม่ได้ หน้าจอค้างขึ้น error", "วิดีโอบนเว็บไซต์เป็นจอดำและไม่เล่น"]),
        ("connection", "dev", ["The app keeps showing a connection error on good wifi", "The website disconnects with a network error", "แอปแจ้งเชื่อมต่อผิดพลาดทั้งที่ไวไฟปกติ", "เว็บไซต์หลุดและขึ้นข้อผิดพลาดเครือข่าย"]),
        ("browser", "test", ["The website layout is broken in my mobile browser", "The app page does not display correctly on Safari", "หน้าเว็บไซต์แสดงผลผิดพลาดบนเบราว์เซอร์มือถือ", "เปิดเว็บในซาฟารีแล้วหน้าจอแสดงผลไม่ถูกต้อง"]),
        ("export", "test", ["The app fails to export a file and shows an error", "The website download report button gets stuck", "แอปส่งออกไฟล์ไม่ได้และแจ้งข้อผิดพลาด", "กดดาวน์โหลดรายงานในเว็บแล้วระบบค้าง"]),
    ],
}

UNKNOWN = {
    "dev": ["What is the weather in Bangkok today", "Write a poem about a blue mountain", "Recommend a recipe for green curry", "วันนี้อากาศที่เชียงใหม่เป็นอย่างไร", "แต่งกลอนเกี่ยวกับดวงจันทร์ให้หน่อย", "ขอสูตรทำผัดกะเพราให้อร่อย"],
    "test": ["Who won the football match yesterday", "Teach me how to play the guitar", "How many planets are in the solar system", "ช่วยแนะนำสถานที่เที่ยวทะเล", "แมวชอบนอนวันละกี่ชั่วโมง", "สอนเล่นเปียโนเพลงง่ายให้หน่อย"],
}


def ticket_rows():
    rows = []
    for label, families in FAMILIES.items():
        for family, split, texts in families:
            for index, text in enumerate(texts):
                rows.append({"id": f"{label}-{family}-{index + 1}", "label": label,
                             "family": f"{label}/{family}", "split": split,
                             "language": "en" if index < 2 else "th", "text": text})
    return rows
