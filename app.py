import streamlit as st

# 페이지 설정
st.set_page_config(page_title="부동산 수익 계산기", layout="centered")

st.title("🏠 부동산 수익 계산기")

# 초기 세션 상태 설정
if 'room_count_old' not in st.session_state:
    st.session_state.room_count_old = 1

# [건물 구매 금액]
building_price = st.number_input("건물 구매 금액 (원)", min_value=0, step=1000000, format="%d")
st.caption(f"💰 건물가 확인: **{building_price:,}** 원")

# [건물 관리비]
monthly_maintenance = st.number_input("월 건물 관리비 (원)", min_value=0, step=10000, format="%d")
st.caption(f"🛠 월 관리비 확인: **{monthly_maintenance:,}** 원")

st.divider()

# --- 일괄 적용 기능 ---
st.subheader("💰 월세 입력")
col_bulk1, col_bulk2 = st.columns([3, 1])

with col_bulk1:
    bulk_rent = st.number_input("일괄 적용할 월세 금액 (원)", min_value=0, step=10000, format="%d")

with col_bulk2:
    st.write(" ") 
    if st.button("모든 가구에 적용", use_container_width=True):
        for i in range(100): # 최대 100호실까지 초기화
            st.session_state[f"room_{i}"] = bulk_rent
        st.rerun()

# [건물에 있는 호실 수]
room_count = st.number_input("건물에 있는 호실 수", min_value=1, max_value=100, value=st.session_state.room_count_old)
st.session_state.room_count_old = room_count

# --- 각 호실별 입력 칸 ---
monthly_rents = []
cols = st.columns(2)

for i in range(room_count):
    if f"room_{i}" not in st.session_state:
        st.session_state[f"room_{i}"] = 0
        
    with cols[i % 2]:
        rent = st.number_input(
            f"{i+1}호실 월세 (원)", 
            min_value=0, 
            step=10000, 
            key=f"room_{i}", 
            format="%d" 
        )
        # 각 호실 입력창 바로 아래에 쉼표가 포함된 금액 표시 추가
        st.caption(f"└ **{rent:,}** 원")
        monthly_rents.append(rent)

st.divider()

# [계산하기] 버튼
if st.button("계산하기", type="primary", use_container_width=True):
    total_monthly_rent = sum(monthly_rents)
    annual_total_rent = total_monthly_rent * 12
    annual_total_maintenance = monthly_maintenance * 12
    final_annual_profit = annual_total_rent - annual_total_maintenance
    
    # --- 수익률 계산 ---
    roi = 0
    if building_price > 0:
        roi = round((final_annual_profit / building_price) * 100, 1)
    
    st.success("✅ 분석 완료")
    
    # 결과 표시
    c1, c2, c3 = st.columns(3)
    c1.metric("연간 총 월세", f"{annual_total_rent:,} 원")
    c2.metric("연간 총 관리비", f"- {annual_total_maintenance:,} 원")
    c3.metric("약 연간 수익률", f"{roi:.1f} %")
    
    st.divider()
    
    # 최종 요약
    st.subheader(f"📊 최종 연 순수익: {final_annual_profit:,} 원")
    st.info(f"💡 {building_price:,}원에 건물을 구매하여 연간 {final_annual_profit:,}원을 벌 경우, 투자 금액 대비 **약 연간 {roi:.1f}%**의 수익이 발생합니다.")
