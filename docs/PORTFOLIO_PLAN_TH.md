# แผน GitHub ก่อนฝึกงาน: Web Development + Applied AI

เป้าหมายคือแสดงว่าเขียนเว็บ เชื่อม API/ฐานข้อมูล และนำโมเดลมาใช้กับปัญหาจริงได้ พร้อมอธิบายข้อจำกัดและดูแลระบบหลังนำขึ้นใช้งาน งานวิเคราะห์ข้อมูลและกราฟเป็นส่วนช่วยตรวจคุณภาพโมเดลและสื่อสารผล ไม่จำเป็นต้องวางตัวเป็น Data Analyst เพียงสายเดียว

ทักษะเหล่านี้ช่วยเตรียมสมัครงานที่ตรงเป้าหมายได้ แต่เงินเดือนขึ้นกับตำแหน่ง บริษัท ประสบการณ์ และการสัมภาษณ์ ไม่มีจำนวน repo หรือเทคโนโลยีใดรับประกันรายได้

## สิ่งที่ตรวจพบจริง

อ่าน public README, package.json และโครงสร้างไฟล์ผ่าน GitHub แล้ว ยังไม่ได้รันโปรเจกต์เหล่านี้ จึงแยกคำอธิบายใน README ออกจากผลการทดสอบจริง

| Repo | หลักฐานที่เห็น | สิ่งที่ควรเติม |
| --- | --- | --- |
| [sweet_pos_project](https://github.com/nnt2525/sweet_pos_project) | README และ package.json มี Next.js/TypeScript, Express, Prisma/MySQL; README อธิบาย auth, สั่งซื้อ และ admin dashboard | ภาพจริง, demo, แผนภาพระบบ, บทบาทที่ทำเอง และผลทดสอบเส้นทางสั่งซื้อ |
| [AI-Emergency-Voice-Rescuer_Raspberry_pi](https://github.com/nnt2525/AI-Emergency-Voice-Rescuer_Raspberry_pi) | มี Python backend, MQTT receiver, model และ [คู่มือ Pi](https://github.com/nnt2525/AI-Emergency-Voice-Rescuer_Raspberry_pi/blob/main/pi_zero/README_HARDWARE.md); ไม่มี README ที่ root | วิธีรันครบระบบ, ที่มา/สิทธิ์ใช้ข้อมูล, วิธีแบ่งชุดข้อมูล, ผลประเมิน และขอบเขตการใช้งานต้นแบบ |
| [agriagent_farming](https://github.com/nnt2525/agriagent_farming) | README ระบุ hackathon prototype: Go API, Next.js dashboard, mock mode; ระบุชัดว่า auth ยังเป็น static, CV ยังไม่ต่อ และ relay เป็น stub | demo ที่แสดง mock/จริงชัดเจน, unit ของ sensor, กราฟเวลา, การประเมิน rule baseline เทียบโมเดล และสถานะงานที่ยังไม่เสร็จ |
| [foodscanweb](https://github.com/nnt2525/foodscanweb) | README ระบุงาน Backend Development/Database Design ของผู้ใช้ และอธิบายกราฟโภชนาการ; ช่อง Preview ยังเป็นชื่อหน้า | ภาพจริง, แหล่งข้อมูลรายชุด, SQL ตัวอย่าง และแก้การตั้งค่า test: [backend package.json](https://github.com/nnt2525/foodscanweb/blob/main/nutrition-app/backend/package.json) มี `test: jest` แต่ไม่ประกาศ Jest ใน dependencies ที่อ่าน |

[node.js](https://github.com/nnt2525/node.js) และ [mock_AI_voice_detection](https://github.com/nnt2525/mock_AI_voice_detection) ว่างตาม API; [webtech.github](https://github.com/nnt2525/webtech.github) มีเพียง README ชื่อ repo ควรเอาพื้นที่ pin ไปให้โปรเจกต์ที่เปิดดูผลงานได้ ส่วน bio, contribution count และ pin ในภาพเป็นข้อมูลจากภาพที่ส่งมา ไม่ได้ตรวจสถานะสดของหน้า profile

## จัดลำดับงานและ pin

**โปรเจกต์เดิม 3 ตัวที่ควรทุ่มเวลาก่อน:** `sweet_pos_project` สำหรับพื้นฐาน full stack, `AI-Emergency-Voice-Rescuer_Raspberry_pi` สำหรับการใช้โมเดล และ `agriagent_farming` สำหรับ API/IoT/dashboard ไม่ต้องเพิ่ม AI ให้ทุก repo จนโจทย์เดิมซับซ้อนเกินจำเป็น

ลำดับ pin ที่เสนอเมื่อแต่ละตัวพร้อม:

1. **[applied-ai-web-lab](https://github.com/nnt2525/applied-ai-web-lab)** — เว็บ 3 สไตล์ใน repo เดียว พร้อมโมเดลคัดแยกข้อความและ regression ที่ฝึกจริง มี baseline/evaluation; ข้อมูลสาธิตทั้งหมดและยังเป็น educational prototype
2. **[sweet_pos_project](https://github.com/nnt2525/sweet_pos_project)** — งาน full stack หลัก
3. **[AI-Emergency-Voice-Rescuer_Raspberry_pi](https://github.com/nnt2525/AI-Emergency-Voice-Rescuer_Raspberry_pi)** — งานใช้โมเดลหลัก หลังเติม README และผลประเมิน
4. **[agriagent_farming](https://github.com/nnt2525/agriagent_farming)** — dashboard และระบบ event-driven โดยติดป้าย prototype
5. **[foodscanweb](https://github.com/nnt2525/foodscanweb)** — ผลงานกลุ่มที่ระบุส่วนรับผิดชอบชัด
6. **[esp32_LED_web](https://github.com/nnt2525/esp32_LED_web)** — pin สำรองหลังเติม README, wiring และ demo; มีโค้ดจริงแต่ควรจัดไฟล์ build ที่ไม่จำเป็นออกก่อนนำเสนอ

ไม่จำเป็นต้องเติมครบ 6 ทันที เริ่มจาก 3–4 ตัวที่มี demo และอธิบายโค้ดได้ก่อน หากยังไม่ทำ gallery ให้เว้นช่องไว้ ไม่ต้องสร้าง repo ว่างเพื่อให้ครบจำนวน

## แผน 4 สัปดาห์

แผนนี้สมมติมีเวลาประมาณ 10–15 ชั่วโมงต่อสัปดาห์ เลือกทำงานหลักทีละชิ้นและลดฟีเจอร์เมื่อเวลาไม่พอ

| สัปดาห์ | สิ่งที่ทำ | หลักฐานที่ต้องได้ |
| --- | --- | --- |
| 1: พื้นฐานเว็บ | เลือกเส้นทางผู้ใช้หนึ่งเส้นใน Sweet POS; ทบทวน HTML semantics, responsive CSS, TypeScript, form validation, loading/error/empty state และ keyboard navigation | ภาพ desktop/mobile, README ที่ระบุส่วนที่ทำ และอธิบายการไหลของข้อมูลจาก UI ไป API ได้ |
| 2: API + DB | ตรวจ schema/ความสัมพันธ์, validation, auth/สิทธิ์, transaction ที่จำเป็น และข้อมูล seed; เพิ่ม tests สำหรับกรณีสำคัญ เช่น สิทธิ์ admin, จำนวนสินค้าไม่ถูกต้อง และยอดรวม; ตั้ง CI ให้รัน checks ที่ใช้ได้จริง | เริ่มจาก clean clone ได้ด้วยคำสั่งใน README, `.env.example` ไม่มี secret, tests ผ่าน และมี API request/response ตัวอย่าง |
| 3: โมเดล + การประเมิน | ใน applied-ai-web-lab หรือ AI Emergency กำหนด input/output และ baseline; ตรวจข้อมูลซ้ำ/สิทธิ์ใช้ข้อมูล; แบ่ง train/validation/test ก่อนปรับโมเดล โดยกันผู้พูด/อุปกรณ์/ช่วงเวลาซ้ำข้ามชุดเมื่อเกี่ยวข้อง | บันทึก seed และวิธี split, metrics บน test ที่ไม่ใช้จูน, confusion matrix/ตัวอย่างผิดพลาด, เปรียบเทียบ baseline; บอกชัดว่าใช้โมเดลสำเร็จรูป ปรับจูน หรือฝึกเอง |
| 4: เชื่อมระบบ + deploy | เชื่อมเว็บ → API → inference → response; เพิ่ม timeout/ข้อจำกัด input/error state; deploy demo, ตรวจ config/log ที่ไม่เผยข้อมูลส่วนตัว และทดสอบจากเครื่องใหม่ | ลิงก์ demo จริง, วิดีโอสั้น, CI ผ่าน, architecture และ known limitations; ทำหน้า gallery เพิ่มเฉพาะเมื่อเส้นทางหลักเสร็จแล้ว |

สำหรับข้อมูลเสียง ให้แยกผู้พูดหรือ session ระหว่างชุดข้อมูลตามโจทย์ เพื่อหลีกเลี่ยงผลประเมินที่ดูดีจากข้อมูลคล้ายกันเกินไป ถ้าจำนวนข้อมูลยังน้อยให้รายงานตามจริง และใช้คำว่า prototype ไม่อ้างว่าใช้ช่วยชีวิตหรือทดแทนระบบฉุกเฉินได้

## README ของแต่ละโปรเจกต์

ใช้ลำดับ: ปัญหาและผู้ใช้ → ภาพ/demo → สิ่งที่ทำเอง/ทีม → architecture → วิธีรันและ seed → วิธีทดสอบ → ผลประเมิน/ข้อจำกัด → แหล่งข้อมูลและ license

แยก `Implemented`, `Mock/demo` และ `Planned` ให้ตรงกับโค้ด ตัวเลข เช่น accuracy, latency หรือจำนวนผู้ใช้ ให้ใส่เฉพาะที่วัดได้จริง พร้อมวิธีวัดและวันที่ หลีกเลี่ยง badge ที่สื่อว่า tests ผ่านทั้งที่ยังไม่มี workflow

## ร่าง GitHub bio และ profile README

Bio ที่นำไปปรับใช้ได้:

> Student developer | TypeScript & Python | Learning full-stack web development and applied AI

ร่าง README สำหรับ repo ชื่อ `nnt2525/nnt2525` (เผยแพร่เมื่อผู้ใช้พร้อม):

```markdown
# Hi, I'm NNT

I'm a student interested in web development and applied AI.
I work with TypeScript, JavaScript, and Python, and I'm improving how I build APIs, databases, and model-backed web applications.

## Selected projects

- [Sweet POS](https://github.com/nnt2525/sweet_pos_project) — a full-stack sweet shop project.
- [AI Emergency Voice Rescuer](https://github.com/nnt2525/AI-Emergency-Voice-Rescuer_Raspberry_pi) — an audio/AI prototype with a Raspberry Pi component.
- [AgriAgent](https://github.com/nnt2525/agriagent_farming) — a smart farming hackathon prototype with a web dashboard.
- [NutriTrack](https://github.com/nnt2525/foodscanweb) — a team nutrition tracking project; my documented role covers backend development and database design.

## Current focus

- Building usable, responsive web interfaces and reliable APIs.
- Evaluating model behavior and documenting limitations.
- Writing reproducible setup steps and meaningful tests.

Project READMEs describe the current implementation and unfinished parts.
```

เพิ่ม applied-ai-web-lab และ demo หลังมี URL จริง ใส่ช่องทางติดต่อเฉพาะที่ต้องการเปิดเผยต่อสาธารณะ

## เตรียมอธิบายตอนสัมภาษณ์

- อธิบายใน 60 วินาทีได้ว่าใครมีปัญหาอะไร เว็บรับ input อย่างไร และโมเดลช่วยตรงไหน
- เปิดโค้ดไล่เส้นทาง UI → API → DB/โมเดล → response พร้อมอธิบายเหตุผลของการออกแบบ
- ระบุว่าตนเองทำอะไร เพื่อนทำอะไร และส่วนใดนำจาก starter/library/model เดิม
- อธิบาย baseline, data leakage, metric ที่เลือก และตัวอย่างที่โมเดลทายผิดได้ ไม่จำเฉพาะค่า accuracy
- สาธิต error case อย่างน้อยหนึ่งกรณี เช่น API timeout, input ไม่ถูกต้อง หรือข้อมูลไม่พอ
- อธิบายการใช้ AI อย่างตรงไปตรงมา เช่น “ใช้ AI ช่วยร่าง/หาบั๊กในส่วนนี้ แล้วตรวจ diff ทดสอบกรณีนี้ และปรับเหตุผลนี้เอง” ไม่อ้างว่าเขียนเองทั้งหมด
- เตรียมเปลี่ยนเงื่อนไขหรือแก้บั๊กเล็ก ๆ ต่อหน้าได้ และชี้ข้อจำกัด/งานถัดไปโดยไม่อ้างว่าระบบพร้อม production หากยังไม่ได้พิสูจน์

เอกสารนี้เป็นแผนและร่างข้อความ ยังไม่ได้แก้ profile, pin หรือ repository ใดบน GitHub
