# assets — รูปที่ตั้งไว้ในแอป

| ไฟล์ | ใช้ทำอะไร |
| --- | --- |
| `profile.jpg` (หรือ `.png` / `.jpeg` / `.webp`) | **รูปประจำตัวผู้ดูแลระบบ** — ตั้งไว้ครั้งเดียว โชว์เป็นวงกลมที่ sidebar ทุกหน้า |

- นามสกุลที่รองรับ: `.png` `.jpg` `.jpeg` `.webp` (ไม่เกิน 8 MB)
- ตั้งรูปได้ 2 วิธี: วางไฟล์ที่ `assets/profile.jpg` หรือกดอัปโหลดในหน้า **Admin / Setup**
- รูปจะถูกอ่านเป็น base64 ฝังในหน้าเว็บ จึงไม่ต้องมี public URL
- ถ้า deploy บน Streamlit Cloud ต้อง `git add assets` แล้ว commit/push รูปถึงจะติดไปตอน redeploy
