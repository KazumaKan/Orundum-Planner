from datetime import datetime, timedelta

# กำหนดข้อมูลตู้ Limited
limited_banners = [
    {"name": "Summer", "start": (1, 15), "duration": 14},
    {"name": "Half Anniversary", "start": (4, 25), "duration": 14},
    {"name": "CN Banner", "start": (7, 25), "duration": 14},
    {"name": "Anniversary", "start": (10, 25), "duration": 14},
]

def calc_orundum(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    total_days = delta.days + 1

    orundum = 0
    tickets = 0
    rolls_from_free = 0

    for day_offset in range(total_days):
        current_day = start_date + timedelta(days=day_offset)

        # 2.1 รายวัน: 100 Orundum/วัน
        orundum += 100

        # 2.2 รายสัปดาห์: ทุกวันจันทร์เพิ่ม 500 Orundum
        if current_day.weekday() == 0:  # Monday
            orundum += 500

        # 2.3 Annihilation ทุกวันอังคาร (รวมเป็นสัปดาห์ละ 1800)
        if current_day.weekday() == 1:  # Tuesday
            orundum += 1800

        # 5. ทุกวันที่ 1 ของเดือน: 600 Orundum + 4 ใบเปิดตู้
        if current_day.day == 1:
            orundum += 600
            tickets += 4

        # 4. ตรวจสอบว่ามีตู้ Limited อยู่ในวันนั้นไหม
        for banner in limited_banners:
            banner_start = datetime(current_day.year, banner["start"][0], banner["start"][1])
            banner_end = banner_start + timedelta(days=banner["duration"] - 1)
            if banner_start <= current_day <= banner_end:
                if (banner_start == current_day):
                    rolls_from_free += 10  # 4.3 เปิดได้ฟรี 10 โรลเมื่อเริ่มตู้
                rolls_from_free += 1      # 4.2 โรลฟรีวันละ 1 โรล
            elif current_day > banner_end and (current_day - banner_end).days == 1:
                rolls_from_free += 10     # 4.4 ผ่านตู้แล้ว +10

    return orundum, tickets, rolls_from_free, total_days

if __name__ == "__main__":
    print("=== คำนวณ Orundum จากวันเริ่มต้นและวันสิ้นสุด ===")

    use_today = input("ใช้วันปัจจุบันเป็นวันเริ่มต้นหรือไม่? (y/n) : ").strip().lower()

    if use_today == 'y':
        start_date = datetime.today()
    else:
        start_input = input("กรุณาใส่วันเริ่มต้น (รูปแบบ: YYYY-MM-DD) : ").strip()
        try:
            start_date = datetime.strptime(start_input, "%Y-%m-%d")
        except ValueError:
            print("รูปแบบวันไม่ถูกต้อง ใช้วันปัจจุบันแทน")
            start_date = datetime.today()

    end_input = input("กรุณาใส่วันสิ้นสุด (รูปแบบ: YYYY-MM-DD): ").strip()
    try:
        end_date = datetime.strptime(end_input, "%Y-%m-%d")
    except ValueError:
        print("รูปแบบวันไม่ถูกต้อง ใช้วันสิ้นสุดเป็น 31 ธันวาคมของปีปัจจุบัน")
        end_date = datetime(start_date.year, 12, 31)

    if end_date < start_date:
        print("วันสิ้นสุดอยู่ก่อนวันเริ่มต้น จะสลับวันให้โดยอัตโนมัติ")
        start_date, end_date = end_date, start_date

    # ✅ รับข้อมูล Orundum และตั๋วที่ผู้ใช้มีอยู่แล้ว
    try:
        existing_orundum = int(input("คุณมี Orundum อยู่แล้วเท่าไหร่? : ").strip())
    except ValueError:
        existing_orundum = 0

    try:
        existing_tickets = int(input("คุณมีตั๋วเปิดตู้กี่ใบ? : ").strip())
    except ValueError:
        existing_tickets = 0

    orundum, tickets, rolls_from_free, total_days = calc_orundum(start_date, end_date)

    total_orundum = orundum + existing_orundum
    total_tickets = tickets + existing_tickets
    total_rolls = total_orundum // 600 + total_tickets + rolls_from_free

    print("\n=== ผลการคำนวณ ===")
    print(f"รวมวัน : {total_days}")
    print(f"Orundum ที่จะได้ต่อจากนี้ : {orundum}")
    print(f"ตั๋วที่จะได้ต่อจากนี้ : {tickets}")
    print(f"โรลฟรีจากตู้ Limited : {rolls_from_free}")
    print(f"Orundum ที่คุณมีอยู่ : {existing_orundum}")
    print(f"ตั๋วที่คุณมีอยู่ : {existing_tickets}")
    print(f"\n👉 รวม Orundum ทั้งหมด : {total_orundum}")
    print(f"👉 รวมตั๋วทั้งหมด : {total_tickets}")
    print(f"🎯 รวมโรลที่สามารถเปิดได้ : {total_rolls} โรล")
    print("\nขอบคุณที่ใช้ Orundum Planner!")