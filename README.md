# 🔮 Arknights Orundum Calculator – Streamlit Web App

A simple and interactive **Streamlit** web application for **Arknights** players to estimate the number of rolls they will have during a specific time period. It calculates Orundum earnings, recruitment tickets, and free pulls from Limited banners — helping players plan for future banners and guarantees.

---

## 📌 Features

- 🔢 **Daily Orundum calculation** (100 Orundum/day)
- 📆 **Weekly & Monthly bonuses**
  - Weekly Mission Bonus: +500 Orundum (every Monday)
  - Annihilation Reward: +1800 Orundum (every Tuesday)
  - Monthly Login Bonus: +600 Orundum and +4 tickets (every 1st of the month)
- 🎁 **Limited Banner tracking**
  - Calculates free daily pulls (up to 14) and 10-pull special tickets for each Limited banner
- 💼 **Customizable input**
  - Start/End date
  - Existing Orundum and tickets
- 📊 **Breakdown of all sources**
  - Detailed summary by source and banner
- 🎯 **Roll summary**
  - Shows total number of rolls available
  - Highlights whether 300-roll Limited banner pity is achievable
- 🎉 Animated effect if goal is met (Streamlit balloons!)

---

## 🧮 How It Works

The app calculates future resources based on the following logic :

### ✅ Daily and Event-Based Rewards

| Type                  | Value                |
|-----------------------|----------------------|
| Daily Login           | +100 Orundum/day     |
| Weekly Missions (Mon) | +500 Orundum         |
| Annihilation (Tue)    | +1800 Orundum        |
| 1st of Month Bonus    | +600 Orundum + 4 Tickets |

### 🧊 Limited Banners

The app tracks four main Limited banners:
- **Summer** – July 15 (14 days)
- **Half Anniversary** – April 25 (14 days)
- **CN Banner** – July 25 (14 days)
- **Anniversary** – October 25 (14 days)

Each banner gives:
- 🎁 **1 free pull per day** (up to 14)
- 🎟️ **1 special 10-pull ticket**

---

## 🚀 How to Run Locally

Make sure you have Python and Streamlit installed.

```bash
pip install streamlit
