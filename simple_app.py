"""
AIA 2.0 — Simple Demo Version
Python 3.14 호환성을 위한 간단한 데모 버전
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="AIA 2.0 — AI Investment Agency",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit',
        'Report a bug': 'https://github.com/streamlit/streamlit',
        'About': "# AIA 2.0\n모바일에서도 사용 가능한 AI 투자 플랫폼"
    }
)

def format_money(value):
    """통화 형식으로 포맷팅"""
    if value >= 100000000:  # 1억 이상
        return f"{value/100000000:.1f}억원"
    elif value >= 10000:  # 1만 이상
        return f"{value/10000:.0f}만원"
    else:
        return f"{value:,.0f}원"

def format_percent(value):
    """소수를 퍼센트로 변환"""
    return f"{value*100:.1f}%" if value < 1 else f"{value:.1f}%"

def main():
    """메인 애플리케이션"""
    
    # 상단 제목
    st.title("🏦 AIA 2.0 — Dual-Team AI Investment Agency")
    st.markdown("**AI 역할 기반 투자 의사결정 플랫폼 (Mobile Ready)**")
    
    # 모바일 접근 안내
    with st.expander("📱 모바일 접근 방법", expanded=False):
        st.markdown("""
        **🌐 외부에서 접근하는 방법:**
        
        1. **같은 Wi-Fi 네트워크**: `http://192.168.55.106:8501`
        2. **모바일 핫스팟**: 컴퓨터를 모바일 핫스팟에 연결 후 모바일에서 접근
        3. **포트 포워딩**: 공유기 설정에서 8501 포트 열기
        
        **💡 팁**: 모바일에서 북마크에 저장하면 앱처럼 사용 가능!
        """)
    
    # 탭 네비게이션
    tab_names = ["🎯 인트로", "📊 거시전략가", "💰 자산배분가", "🔍 섹터리서처", "📈 종목애널리스트", "🏆 CIO전략실", "⚡ Trade Planner"]
    tabs = st.tabs(tab_names)
    
    with tabs[0]:
        tab_intro()
    with tabs[1]:
        tab_macro()
    with tabs[2]:
        tab_allocation()
    with tabs[3]:
        tab_sector()
    with tabs[4]:
        tab_analyst()
    with tabs[5]:
        tab_cio()
    with tabs[6]:
        tab_trade_planner()

def tab_intro():
    """인트로 탭"""
    st.header("🎯 AIA 2.0 — 듀얼팀 AI 투자 에이전시")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 플랫폼 개요
        
        **AIA 2.0**는 AI 역할 기반 투자 의사결정 플랫폼으로, 
        전문 투자팀의 역할을 AI가 수행하여 체계적인 투자 전략을 제공합니다.
        
        ### 📋 7단계 투자 프로세스
        
        1. **🎯 인트로**: 플랫폼 소개 및 투자자 프로필 설정
        2. **📊 거시전략가**: 경제 환경 분석 및 시장 전망
        3. **💰 자산배분가**: 리스크 성향별 포트폴리오 구성
        4. **🔍 섹터리서처**: 유망 섹터 및 테마 선별
        5. **📈 종목애널리스트**: 개별 종목 분석 및 추천
        6. **🏆 CIO전략실**: 최종 포트폴리오 확정
        7. **⚡ Trade Planner**: 모멘텀+RSI 기반 매매 전략
        """)
    
    with col2:
        st.markdown("""
        ### 💡 핵심 특징
        
        ✅ **AI 역할 분담**: 각 단계별 전문 AI 에이전트  
        ✅ **체계적 프로세스**: 거시→미시→실행 단계별 접근  
        ✅ **실용적 전략**: 모멘텀+RSI 기반 단순 매매 신호  
        ✅ **개인 맞춤형**: 리스크 성향 및 투자 목표 반영  
        
        ### 🎯 모멘텀+RSI 전략
        
        복잡한 팩터모델 대신 **검증된 기술적 지표 조합**을 활용:
        
        - **RSI 지표 (50%)**: 과매수/과매도 구간 판별
        - **단기 모멘텀 (30%)**: 20일 이동평균 기준 
        - **장기 모멘텀 (20%)**: 60일 이동평균 기준
        
        **🟢 매수 신호**: RSI 30-40 + 모멘텀 상승  
        **🔴 매도 신호**: RSI 70+ + 모멘텀 둔화
        """)
    
    # 시작하기 버튼
    st.markdown("---")
    if st.button("🚀 투자 여정 시작하기", type="primary"):
        st.success("✅ 거시전략가 탭으로 이동하여 투자를 시작해보세요!")

def tab_macro():
    """거시전략가 탭"""
    st.header("📊 거시전략가")
    st.markdown("**글로벌 경제 환경 분석 및 투자 전략 수립**")
    
    # 투자자 프로필 설정
    with st.expander("👤 투자자 프로필 설정", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            investment_amount = st.slider("투자 가능 자산 (만원)", 100, 10000, 3000, 100)
            risk_level = st.selectbox("투자 성향", ["안전형", "안정형", "중립형", "적극형", "공격형"])
            
        with col2:
            investment_period = st.selectbox("투자 기간", ["1년 이하", "1-3년", "3-5년", "5년 이상"])
            market_preference = st.selectbox("선호 시장", ["국내", "해외", "혼합"])
    
    # 거시 분석
    st.markdown("### 🌍 현재 거시 환경 분석")
    
    macro_scenarios = [
        "📈 경기 회복 시나리오 - 금리 안정화, 성장주 선호",
        "⚖️ 균형 성장 시나리오 - 적절한 분산투자, 밸류+그로스",
        "📉 경기 둔화 시나리오 - 방어적 투자, 배당주/채권 비중 확대"
    ]
    
    selected_scenario = st.radio("선택할 거시 시나리오:", macro_scenarios)
    
    # 시나리오별 추천
    if "회복" in selected_scenario:
        st.success("🚀 성장주 위주의 공격적 포트폴리오를 추천합니다.")
        recommended_allocation = {"주식": 70, "채권": 20, "현금": 10}
    elif "둔화" in selected_scenario:
        st.warning("🛡️ 방어적 자산 비중을 늘린 안정적 포트폴리오를 추천합니다.")
        recommended_allocation = {"주식": 40, "채권": 40, "현금": 20}
    else:
        st.info("⚖️ 균형잡힌 분산 포트폴리오를 추천합니다.")
        recommended_allocation = {"주식": 60, "채권": 30, "현금": 10}
    
    # 추천 자산배분 시각화
    fig = go.Figure(data=[go.Pie(
        labels=list(recommended_allocation.keys()),
        values=list(recommended_allocation.values()),
        hole=0.4
    )])
    fig.update_layout(title="거시 환경 기반 추천 자산배분")
    st.plotly_chart(fig)

def tab_allocation():
    """자산배분가 탭"""
    st.header("💰 자산배분가")
    st.markdown("**리스크 성향 기반 포트폴리오 구성**")
    
    # 포트폴리오 전략 선택
    allocation_strategies = [
        "보수형 포트폴리오 (주식 30%, 채권 60%, 현금 10%)",
        "균형형 포트폴리오 (주식 60%, 채권 30%, 현금 10%)",
        "성장형 포트폴리오 (주식 80%, 채권 15%, 현금 5%)"
    ]
    
    selected_strategy = st.selectbox("포트폴리오 전략 선택:", allocation_strategies)
    
    # 백테스팅 결과 (더미 데이터)
    st.markdown("### 📊 포트폴리오 백테스팅 결과")
    
    # 수익률 시뮬레이션
    dates = pd.date_range('2020-01-01', '2024-12-31', freq='ME')
    returns = np.random.normal(0.008, 0.04, len(dates)).cumsum()
    
    df = pd.DataFrame({
        'Date': dates,
        'Cumulative_Return': returns
    })
    
    fig = px.line(df, x='Date', y='Cumulative_Return', title='포트폴리오 누적 수익률')
    st.plotly_chart(fig)
    
    # 성과 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("연 평균 수익률", "8.5%")
    with col2:
        st.metric("최대 손실", "-12.3%")
    with col3:
        st.metric("변동성", "15.2%")
    with col4:
        st.metric("샤프 비율", "1.25")

def tab_sector():
    """섹터리서처 탭"""
    st.header("🔍 섹터리서처")
    st.markdown("**유망 섹터 및 투자 테마 분석**")
    
    # 섹터별 전망
    sectors = [
        {"name": "🔋 배터리/이차전지", "score": 85, "trend": "강한 상승", "reason": "전기차 확산, ESG 트렌드"},
        {"name": "🤖 AI/반도체", "score": 90, "trend": "매우 강한 상승", "reason": "AI 혁명, 데이터센터 수요"},
        {"name": "💊 바이오/헬스케어", "score": 75, "trend": "상승", "reason": "고령화, 정밀의료 발전"},
        {"name": "🏭 전통 제조업", "score": 45, "trend": "보합", "reason": "경기 민감, 구조적 변화"},
        {"name": "🏠 부동산/건설", "score": 35, "trend": "하락", "reason": "고금리, 공급과잉 우려"}
    ]
    
    # 섹터 선택
    st.markdown("### 📈 투자 섹터 선택")
    
    for sector in sectors:
        with st.expander(f"{sector['name']} (점수: {sector['score']}/100)", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**투자 매력도**: {sector['score']}/100")
                st.write(f"**추세**: {sector['trend']}")
                st.write(f"**핵심 동력**: {sector['reason']}")
                
            with col2:
                # 가격 차트 시뮬레이션
                days = pd.date_range('2024-01-01', periods=100, freq='D')
                if sector['score'] > 70:
                    prices = 100 + np.random.normal(0.5, 2, 100).cumsum()
                elif sector['score'] > 50:
                    prices = 100 + np.random.normal(0.1, 1.5, 100).cumsum()
                else:
                    prices = 100 + np.random.normal(-0.2, 1.8, 100).cumsum()
                
                fig = px.line(x=days, y=prices, title=f"{sector['name']} 가격 추이")
                fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig)
    
    # 선택된 섹터
    selected_sectors = st.multiselect(
        "투자할 섹터를 선택하세요:",
        [sector['name'] for sector in sectors],
        default=[sectors[0]['name'], sectors[1]['name']]
    )
    
    if selected_sectors:
        st.success(f"✅ 선택된 섹터: {', '.join(selected_sectors)}")

def tab_analyst():
    """종목애널리스트 탭"""
    st.header("📈 종목애널리스트")
    st.markdown("**개별 종목 분석 및 추천**")
    
    # 추천 종목 리스트
    stocks = [
        {"code": "005930", "name": "삼성전자", "sector": "반도체", "target_return": 15.5, "risk": "중간"},
        {"code": "000660", "name": "SK하이닉스", "sector": "반도체", "target_return": 22.3, "risk": "높음"},
        {"code": "373220", "name": "LG에너지솔루션", "sector": "배터리", "target_return": 28.7, "risk": "높음"},
        {"code": "207940", "name": "삼성바이오로직스", "sector": "바이오", "target_return": 18.2, "risk": "중간"},
        {"code": "035720", "name": "카카오", "sector": "IT서비스", "target_return": 12.1, "risk": "중간"}
    ]
    
    # 종목 선택
    st.markdown("### 🎯 AI 추천 종목")
    
    for stock in stocks:
        with st.expander(f"{stock['name']} ({stock['code']})", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("목표 수익률", f"{stock['target_return']}%")
                st.write(f"**섹터**: {stock['sector']}")
                st.write(f"**리스크**: {stock['risk']}")
                
            with col2:
                # RSI 지표 시뮬레이션
                rsi = np.random.randint(25, 75)
                if rsi < 30:
                    rsi_status = "🟢 과매도 (매수)"
                elif rsi > 70:
                    rsi_status = "🔴 과매수 (매도)"
                else:
                    rsi_status = "🟡 중립"
                
                st.metric("RSI", f"{rsi}", help=rsi_status)
                
                # 모멘텀 시뮬레이션
                momentum = np.random.randint(-15, 20)
                momentum_status = "🟢 상승" if momentum > 0 else "🔴 하락"
                st.metric("모멘텀", f"{momentum:+}%", help=momentum_status)
                
            with col3:
                # 매수 신호 점수
                signal_score = max(0, min(100, 50 + (70-rsi) + momentum))
                
                if signal_score >= 70:
                    signal_status = "🟢 강한 매수"
                    signal_color = "green"
                elif signal_score >= 40:
                    signal_status = "🟡 보통 매수"
                    signal_color = "orange"
                else:
                    signal_status = "🔴 대기"
                    signal_color = "red"
                
                st.metric("종합 신호", f"{signal_score}점")
                st.markdown(f"**{signal_status}**")
    
    # 선택된 종목
    selected_stocks = st.multiselect(
        "포트폴리오에 포함할 종목을 선택하세요:",
        [f"{stock['name']} ({stock['code']})" for stock in stocks],
        default=[f"{stocks[0]['name']} ({stocks[0]['code']})", f"{stocks[1]['name']} ({stocks[1]['code']})"]
    )
    
    if selected_stocks:
        st.success(f"✅ 선택된 종목: {', '.join(selected_stocks)}")

def tab_cio():
    """CIO전략실 탭"""
    st.header("🏆 CIO전략실")
    st.markdown("**최종 포트폴리오 확정 및 리뷰**")
    
    # 최종 포트폴리오 생성
    if st.button("🎯 최종 포트폴리오 생성", type="primary"):
        
        # 더미 포트폴리오 데이터
        portfolio = {
            "국내주식": 45,
            "해외주식": 25, 
            "국내채권": 20,
            "해외채권": 5,
            "현금": 5
        }
        
        investment_amount = 3000  # 3천만원
        
        st.markdown("### 🎯 최종 포트폴리오")
        
        # 포트폴리오 시각화
        fig = go.Figure(data=[go.Pie(
            labels=list(portfolio.keys()),
            values=list(portfolio.values()),
            hole=0.4
        )])
        fig.update_layout(title="최종 자산배분")
        st.plotly_chart(fig)
        
        # 상세 배분
        st.markdown("### 💰 상세 투자 배분")
        
        for asset, weight in portfolio.items():
            amount = investment_amount * weight / 100
            st.write(f"• **{asset} {weight}%**: {format_money(amount * 10000)}")
        
        # 예상 성과
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("예상 수익률", "12.5%")
        with col2:
            st.metric("예상 변동성", "16.8%")
        with col3:
            st.metric("샤프 비율", "1.35")
        with col4:
            st.metric("최대 손실", "-18.5%")
        
        st.success("🎉 포트폴리오가 성공적으로 확정되었습니다! 이제 Trade Planner로 진행하여 실제 매수/매도 전략을 수립해보세요.")

def tab_trade_planner():
    """Trade Planner 탭"""
    st.header("⚡ Trade Planner")
    st.markdown("**모멘텀 + RSI 지표 기반 단순하고 실용적인 매매 전략**")
    
    # 전략 개요
    with st.expander("📈 **모멘텀+RSI 전략 개요**", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🎯 핵심 전략**
            • **RSI 지표**: 과매수/과매도 구간 판별
            • **모멘텀**: 20일/60일 이동평균 기준 추세 확인
            • **복합신호**: RSI + 모멘텀 조합으로 정확도 향상
            
            **✅ 매수 신호**
            • RSI 30-40 + 모멘텀 상승 전환
            • RSI 과매도 + 20일선 골든크로스
            • 장기 모멘텀 지지 + 단기 반등
            """)
        
        with col2:
            st.markdown("""
            **📊 신호 가중치**
            • RSI 신호: 50% (과매수/과매도 판별)
            • 단기 모멘텀: 30% (20일선 기준)
            • 장기 모멘텀: 20% (60일선 기준)
            
            **❌ 매도 신호**
            • RSI 70 이상 + 모멘텀 둔화
            • RSI 80 이상 강제 매도
            • 모멘텀 하락 전환 + RSI 피크
            """)
    
    # 투자 전략 설정
    st.markdown("### 🎯 투자 실행 전략")
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment_method = st.selectbox(
            "투자 실행 방식",
            ["일시불 투자", "분할 매수 (DCA)", "하락시 점진 매수", "기술적 타이밍"]
        )
        
        execution_period = st.selectbox(
            "투자 실행 기간",
            ["즉시 실행", "1주일 내", "1개월 내", "3개월 내", "6개월 내"]
        )
    
    with col2:
        rebalancing_cycle = st.selectbox(
            "리밸런싱 주기",
            ["분기별 (3개월)", "반기별 (6개월)", "연간 (12개월)", "편차 20% 도달시", "시장 상황 변화시"]
        )
        
        risk_management = st.selectbox(
            "위험 관리 방식",
            ["스톱로스 -20%", "스톱로스 -15%", "시장상황 모니터링", "장기 보유", "변동성 기준 조정"]
        )
    
    # 종목별 매매 신호
    st.markdown("### 🎯 선별 종목 매매 신호")
    
    demo_stocks = [
        {"name": "삼성전자", "code": "005930", "rsi": 35, "momentum": 8.5, "signal": 72},
        {"name": "SK하이닉스", "code": "000660", "rsi": 28, "momentum": 12.3, "signal": 85},
        {"name": "LG에너지솔루션", "code": "373220", "rsi": 65, "momentum": -3.2, "signal": 25}
    ]
    
    for stock in demo_stocks:
        with st.expander(f"📈 {stock['name']} ({stock['code']})", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("현재가", format_money(50000 + np.random.randint(-10000, 10000)))
                
                rsi_status = "🟢 과매도" if stock['rsi'] < 30 else "🔴 과매수" if stock['rsi'] > 70 else "🟡 중립"
                st.metric("RSI 지표", f"{stock['rsi']:.1f}", help=rsi_status)
            
            with col2:
                momentum_color = "🟢" if stock['momentum'] > 0 else "🔴"
                st.metric("20일선 모멘텀", f"{stock['momentum']:+.1f}%", help=f"{momentum_color} {'상승' if stock['momentum'] > 0 else '하락'} 추세")
                
                momentum_strength = "강함" if abs(stock['momentum']) > 10 else "보통" if abs(stock['momentum']) > 5 else "약함"
                st.metric("모멘텀 강도", momentum_strength)
            
            with col3:
                if stock['signal'] >= 70:
                    signal_status = "🟢 강한 매수"
                elif stock['signal'] >= 40:
                    signal_status = "🟡 보통 매수"
                else:
                    signal_status = "🔴 대기/매도"
                st.metric("종합 신호", signal_status)
    
    # 매매 체크리스트
    st.markdown("### ✅ 트레이딩 실행 체크리스트")
    
    checklist = [
        "증권계좌 투자금 입금 완료",
        "각 자산별 매수 주문 가격 설정", 
        "손절/목표가 주문 등록",
        "분할매수 일정 캘린더 등록",
        "포트폴리오 모니터링 알림 설정",
        "리밸런싱 주기 알림 설정"
    ]
    
    for i, item in enumerate(checklist):
        st.checkbox(item, key=f"checklist_{i}")
    
    # 완료 버튼
    if st.button("🚀 모멘텀+RSI 트레이딩 계획 완료!", type="primary"):
        st.balloons()
        st.success("🎉 축하합니다! 단순하고 실용적인 모멘텀+RSI 투자 전략이 수립되었습니다.")
        st.markdown("""
        ### 🎯 다음 단계 안내
        
        1. **실행**: RSI + 모멘텀 신호에 따라 단계별 투자 시작
        2. **모니터링**: 매일 RSI 지표와 모멘텀 추세 확인  
        3. **조정**: RSI 과매수/과매도 + 모멘텀 변화에 따른 포지션 조정
        4. **리밸런싱**: 분기별 장기 모멘텀 사이클 점검 및 재배분
        
        **💡 모멘텀+RSI 전략 성공 팁:**
        - RSI 30-40 구간에서 모멘텀 상승 확인 후 매수
        - RSI 70 이상에서 모멘텀 둔화시 단계적 매도
        - 감정보다는 지표 신호를 신뢰하고 일관성 유지
        - 장기 모멘텀과 단기 RSI의 조화로운 매매 타이밍 포착
        """)

if __name__ == "__main__":
    main()