import streamlit as st

# 페이지 설정
st.set_page_config(page_title="부동산 수익 계산기", layout="centered")

st.title("🏠 부동산 수익 계산기")

# 초기 세션 상태 설정
if 'room_count_old' not in st.session_state:
    st.session_state.room_count_old = 1

# [건물 구매 금액] - format="%,d"를 사용해 천 단위 쉼표 강제
building_price = st.number_input("건물 구매 금액 (원)", min_value=0, step=1000000, format="%d")
st.caption(f"💰 입력된 금액: **{building_price:,}** 원")

# [건물 관리비]
monthly_maintenance = st.number_input("월 건물 관리비 (원)", min_value=0, step=10000, format="%d")
st.caption(f"🛠 월 관리비: **{monthly_maintenance:,}** 원 (연간 총 {monthly_maintenance * 12:,} 원 차감)")

# [건물에 있는 호실 수]
room_count = st.number_input("건물에 있는 호실 수", min_value=1, max_value=100, value=st.session_state.room_count_old)
st.session_state.room_count_old = room_count

st.divider()

# --- 일괄 적용 기능 ---
st.subheader("💰 월세 입력")
col_bulk1, col_bulk2 = st.columns([3, 1])

with col_bulk1:
    # 여기서 입력하는 값도 쉼표가 보이게 설정
    bulk_rent = st.number_input("일괄 적용할 월세 금액 (원)", min_value=0, step=10000, format="%d")

with col_bulk2:
    st.write(" ") # 레이아웃 정렬용
    if st.button("모든 가구에 적용", use_container_width=True):
        for i in range(room_count):
            st.session_state[f"room_{i}"] = bulk_rent
        st.rerun()

# --- 각 호실별 입력 칸 ---
monthly_rents = []
cols = st.columns(2)

for i in range(room_count):
    # 세션 상태에 값이 없으면 0으로 초기화
    if f"room_{i}" not in st.session_state:
        st.session_state[f"room_{i}"] = 0
        
    with cols[i % 2]:
        # format="%d"를 통해 입력창에 쉼표 표시
        rent = st.number_input(
            f"{i+1}호실 월세 (원)", 
            min_value=0, 
            step=10000, 
            key=f"room_{i}", 
            format="%d" 
        )
        monthly_rents.append(rent)

st.divider()

# [계산하기] 버튼
if st.button("계산하기", type="primary", use_container_width=True):
    total_monthly_rent = sum(monthly_rents)
    annual_total_rent = total_monthly_rent * 12
    annual_total_maintenance = monthly_maintenance * 12
    final_annual_profit = annual_total_rent - annual_total_maintenance
    
    st.success("✅ 연간 수익 계산 완료")
    
    # 메트릭 결과값에도 쉼표 표시 (:,)
    c1, c2, c3 = st.columns(3)
    c1.metric("월세 합계 (1달)", f"{total_monthly_rent:,} 원")
    c2.metric("연간 총 관리비", f"- {annual_total_maintenance:,} 원")
    c3.metric("최종 연간 수익", f"{final_annual_profit:,} 원")
    
    st.info(f"💡 연간 총 월세 {annual_total_rent:,}원에서 연간 총 관리비 {annual_total_maintenance:,}원을 제외한 순수익입니다.")