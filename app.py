import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Thai Savings Comparison", page_icon="💰", layout="centered")

# --- 2. DATA (ACCOUNTS) ---
ACCOUNTS = [
    {
        "bank": "KKP Bank",
        "account": "FIN SAVE by KKP",
        "emoji": "🔥",
        "tiers": [
            {"min": 0, "max": 500_000, "rate": 1.70},
            {"min": 500_000, "max": float("inf"), "rate": 0.50},
        ],
        "highlight_rate": 1.70,
        "badge": "Highest Rate",
    },
    {
        "bank": "CIMB Thai",
        "account": "Speed D+ Savings",
        "emoji": "⚡",
        "tiers": [
            {"min": 0, "max": 10_000, "rate": 0.50},
            {"min": 10_000, "max": 200_000, "rate": 1.30},
            {"min": 200_000, "max": 2_000_000, "rate": 1.60},
            {"min": 2_000_000, "max": 5_000_000, "rate": 1.60},
            {"min": 5_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "highlight_rate": 1.60,
        "badge": "Big Bag Approved",
    },
    {
        "bank": "SCB",
        "account": "SCB Easy Savings",
        "emoji": "💜",
        "tiers": [
            {"min": 0, "max": 2_000_000, "rate": 1.50},
            {"min": 2_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "highlight_rate": 1.50,
        "badge": "Most Popular",
    },
    {
        "bank": "LH Bank",
        "account": "M Choice Digital",
        "emoji": "🌿",
        "tiers": [
            {"min": 0, "max": 5_000_000, "rate": 1.50},
            {"min": 5_000_000, "max": float("inf"), "rate": 0.50},
        ],
        "highlight_rate": 1.50,
        "badge": "Biggest Cap",
    },
    {
        "bank": "Krungsri Kept",
        "account": "Grow Savings",
        "emoji": "🌸",
        "tiers": [
            {"min": 0, "max": 5_000_000, "rate": 1.45},
            {"min": 5_000_000, "max": float("inf"), "rate": 0.25},
        ],
        "highlight_rate": 1.45,
        "badge": "Auto-Save Vibes",
    },
]

# --- 3. LOGIC (CALCULATION) ---
def calculate_interest(account, amount):
    yearly = 0.0
    remaining = amount
    for tier in account["tiers"]:
        if remaining <= 0:
            break
        tier_range = tier["max"] - tier["min"]
        tier_amount = min(remaining, tier_range)
        if tier_amount > 0:
            yearly += tier_amount * tier["rate"] / 100
            remaining -= tier_amount
    
    monthly = yearly / 12
    # ภาษีหัก ณ ที่จ่าย 15% หากดอกเบี้ยรวมเกิน 20,000 บาท
    tax_exempt = yearly <= 20_000
    net_yearly = yearly if tax_exempt else yearly * 0.85
    return {
        "yearly": round(yearly, 2),
        "monthly": round(monthly, 2),
        "net_yearly": round(net_yearly, 2),
        "tax_exempt": tax_exempt,
    }

# --- 4. UI (STREAMLIT) ---
st.title("💰 Savings Comparison Thailand")
st.write("เปรียบเทียบดอกเบี้ยเงินฝากดิจิทัล พร้อมคำนวณภาษีหัก ณ ที่จ่ายอัตโนมัติ")

# ช่องกรอกจำนวนเงิน
amount = st.number_input("ใส่จำนวนเงินฝากของคุณ (บาท):", min_value=0.0, value=100000.0, step=10000.0)

if amount > 0:
    results = []
    for acc in ACCOUNTS:
        interest = calculate_interest(acc, amount)
        results.append({
            "Bank": f"{acc['emoji']} {acc['bank']}",
            "Account": acc["account"],
            "Highlight Rate": f"{acc['highlight_rate']}%",
            "Yearly (Gross)": interest["yearly"],
            "Monthly": interest["monthly"],
            "Net Yearly (After Tax)": interest["net_yearly"],
            "Tax Status": "✅ Exempt" if interest["tax_exempt"] else "⚠️ 15% Tax Applied"
        })

    # เรียงลำดับตามดอกเบี้ยรายปี
    df = pd.DataFrame(results).sort_values(by="Yearly (Gross)", ascending=False)

    # แสดงผลตาราง
    st.subheader("📊 ผลการคำนวณ")
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Yearly (Gross)": st.column_config.NumberColumn(format="฿%.2f"),
            "Monthly": st.column_config.NumberColumn(format="฿%.2f"),
            "Net Yearly (After Tax)": st.column_config.NumberColumn(format="฿%.2f"),
        }
    )

    # คำแนะนำเพิ่มเติม
    best_bank = df.iloc[0]
    st.success(f"📌 แนะนำ: **{best_bank['Bank']}** ให้ผลตอบแทนสูงสุดที่ **฿{best_bank['Yearly (Gross)']:,.2f}** ต่อปี")

st.divider()
st.caption("หมายเหตุ: ข้อมูลนี้เป็นการคำนวณโดยประมาณการตาม Tier ดอกเบี้ยเบื้องต้นเท่านั้น โปรดตรวจสอบเงื่อนไขล่าสุดจากธนาคารอีกครั้ง")
