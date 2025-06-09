import streamlit as st
from datetime import datetime, timedelta

# 🧊 ข้อมูลตู้ Limited
limited_banners = [
    {"name": "Summer", "start": (1, 15), "duration": 14},
    {"name": "Half Anniversary", "start": (4, 25), "duration": 14},
    {"name": "CN Banner", "start": (7, 25), "duration": 14},
    {"name": "Anniversary", "start": (10, 25), "duration": 14},
]

# 🧮 ฟังก์ชันคำนวณ Orundum และโรล
def calc_orundum(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    total_days = delta.days + 1

    orundum = 0
    tickets = 0
    rolls_from_banners = {}
    total_rolls_free = 0
    free_10_tickets = 0  # ตั๋วเปิดฟรี 10 โรล (แบบใช้ได้ตลอด)

    # คำนวณตู้ Limited ที่อยู่ในช่วง
    for banner in limited_banners:
        banner_start = datetime(start_date.year, banner["start"][0], banner["start"][1])
        banner_end = banner_start + timedelta(days=banner["duration"] - 1)

        # ตรวจสอบว่าตู้ตกในช่วงที่เลือก
        if banner_end < start_date or banner_start > end_date:
            continue

        effective_start = max(banner_start, start_date)
        effective_end = min(banner_end, end_date)
        duration = (effective_end - effective_start).days + 1

        rolls = min(duration, 14)  # ฟรี 1 โรล/วัน สูงสุด 14
        rolls += 10  # ตั๋วพิเศษเฉพาะช่วงตู้
        total_rolls_free += rolls
        rolls_from_banners[banner["name"]] = rolls
        free_10_tickets += 1  # ตั๋วเปิดฟรี 10 โรลแบบเก็บไว้ได้

    # คำนวณ Orundum รายวัน/สัปดาห์/รายเดือน
    for day_offset in range(total_days):
        current_day = start_date + timedelta(days=day_offset)

        orundum += 100  # รายวัน

        if current_day.weekday() == 0:  # จันทร์
            orundum += 500

        if current_day.weekday() == 1:  # อังคาร
            orundum += 1800

        if current_day.day == 1:  # วันที่ 1
            orundum += 600
            tickets += 4

    return orundum, tickets, total_rolls_free, free_10_tickets, total_days, rolls_from_banners


# ===============================
# 🌐 Streamlit Web App
# ===============================
st.title("🔮 ตัวช่วยคำนวณ Orundum – Arknights")

st.markdown("คำนวณจำนวนโรลที่คุณจะมีในช่วงเวลาที่กำหนด พร้อมรวมโรลฟรีจากตู้ Limited")

# 📅 อินพุตวันที่
start_date = st.date_input("เลือกวันเริ่มต้น", value=datetime.today())
end_date = st.date_input("เลือกวันสิ้นสุด", value=datetime(datetime.today().year, 12, 31))

# 💼 อินพุตทรัพยากรที่มี
existing_orundum = st.number_input("คุณมี Orundum อยู่แล้ว (ใส่จำนวน)", min_value=0, value=0)
existing_tickets = st.number_input("คุณมีตั๋วเปิดตู้กี่ใบ", min_value=0, value=0)

# 🚀 ปุ่มคำนวณ
if start_date > end_date:
    st.warning("⚠️ วันเริ่มต้นต้องมาก่อนหรือเท่ากับวันสิ้นสุด")
else:
    if st.button("คำนวณ"):
        orundum, tickets, rolls_from_free, free_10_tickets, total_days, banner_rolls = calc_orundum(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.min.time())
        )

        total_orundum = orundum + existing_orundum
        total_tickets = tickets + existing_tickets + free_10_tickets
        total_rolls = total_orundum // 600 + total_tickets + rolls_from_free

        st.success("✅ ผลลัพธ์การคำนวณ")
        st.markdown(f"""
        - 🗓️ รวมวัน : `{total_days} วัน`
        - 💎 Orundum ที่จะได้ต่อจากนี้ : `{orundum}`
        - 🎟️ ตั๋วที่จะได้ต่อจากนี้ : `{tickets}`
        - 🎁 โรลฟรีจากตู้ Limited (เฉพาะในช่วงตู้) : `{rolls_from_free}`
        - 🧧 ตั๋วเปิดฟรี 10 โรลแบบเก็บได้ : `{free_10_tickets}`
        - 📦 Orundum ที่คุณมี : `{existing_orundum}`
        - 📦 ตั๋วที่คุณมี : `{existing_tickets}`

        ### 🎯 รวมโรลทั้งหมดที่สามารถเปิดได้: `{total_rolls} โรล`
        """)

        if total_rolls >= 300:
            st.balloons()
            st.info("🎉 คุณสามารถการันตีในตู้ Limited ได้แล้ว (300 โรล)")
        else:
            rolls_needed = 300 - total_rolls
            orundum_needed = rolls_needed * 600
            st.info(f"คุณยังขาดอีก `{rolls_needed}` โรล เพื่อการันตีตู้ Limited หรือ Orundum `{orundum_needed}`")

        # 📊 รายละเอียดแยกตาม Banner
        with st.expander("📊 แสดงรายละเอียดเพิ่มเติม"):
            st.markdown("### 📌 รายละเอียด Orundum")
            weekly_missions = sum(1 for i in range(total_days)
                                  if (start_date + timedelta(days=i)).weekday() == 0) * 500
            annihilation = sum(1 for i in range(total_days)
                               if (start_date + timedelta(days=i)).weekday() == 1) * 1800
            monthly_bonus = sum(1 for i in range(total_days)
                                if (start_date + timedelta(days=i)).day == 1) * 600

            st.markdown(f"""
            - จากเควสรายวัน (100/วัน) : `{total_days * 100}`
            - จากเควสรายสัปดาห์ (500/สัปดาห์) : `{weekly_missions}`
            - จาก Annihilation (1800/สัปดาห์) : `{annihilation}`
            - โบนัสต้นเดือน (600/เดือน) : `{monthly_bonus}`
            """)

            st.markdown("### 📌 รายละเอียดตั๋ว")
            st.markdown(f"- ตั๋วจากโบนัสต้นเดือน (4 ใบ) : `{tickets}`")
            st.markdown(f"- ตั๋วเปิดฟรี 10 โรลแบบเก็บไว้ได้ : `{free_10_tickets}`")

            st.markdown("### 📌 โรลฟรีจากตู้ Limited (ภายในช่วงตู้เท่านั้น)")
            for banner_name, rolls in banner_rolls.items():
                st.markdown(f"- `{banner_name}`: {rolls} โรล")