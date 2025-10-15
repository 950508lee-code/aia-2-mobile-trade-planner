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
    page_title="딥시그널 — AI Investment Agency",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/streamlit/streamlit',
        'Report a bug': 'https://github.com/streamlit/streamlit',
        'About': "# 딥시그널\n모바일에서도 사용 가능한 AI 투자 플랫폼"
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
    st.title("📊 딥시그널 (AI Investment Agency)")
    st.markdown("**AI 역할 기반 투자 의사결정 플랫폼**")
    
    # 탭 네비게이션
    tab_names = ["🎯 인트로", "� 투자상담매니저", "�📊 거시전략가", "💰 자산배분가", "🔍 섹터리서처", "📈 종목애널리스트", "🏆 CIO전략실", "⚡ Trade Planner"]
    tabs = st.tabs(tab_names)
    
    with tabs[0]:
        tab_intro()
    with tabs[1]:
        tab_consultant()
    with tabs[2]:
        tab_macro()
    with tabs[3]:
        tab_allocation()
    with tabs[4]:
        tab_sector()
    with tabs[5]:
        tab_analyst()
    with tabs[6]:
        tab_cio()
    with tabs[7]:
        tab_trade_planner()

def tab_consultant():
    """투자상담매니저 탭"""
    st.header("👥 투자상담매니저")
    st.markdown("**맞춤형 투자 전략을 위한 투자자 프로필 분석**")
    
    # 상담 진행 상태
    with st.expander("💼 투자 상담 진행 과정", expanded=True):
        st.markdown("""
        **🎯 상담 목표**: 투자자의 성향과 목표를 정확히 파악하여 최적의 투자 전략 수립
        
        **📋 상담 단계**:
        1. 투자 가용 자금 확인
        2. 투자 성향 및 리스크 허용도 분석  
        3. 선호 투자 시장 및 자산 파악
        4. 투자 목표 및 기간 설정
        5. 맞춤형 투자 전략 방향 제시
        """)
    
    # 투자자 기본 정보
    st.markdown("### 💰 투자 가용 자금")
    col1, col2 = st.columns(2)
    
    with col1:
        investment_amount = st.selectbox(
            "총 투자 가능 자산", 
            ["1천만원 미만", "1천만원 - 3천만원", "3천만원 - 5천만원", 
             "5천만원 - 1억원", "1억원 - 3억원", "3억원 이상"],
            index=2
        )
        
        monthly_saving = st.selectbox(
            "월 추가 투자 가능 금액",
            ["없음", "50만원 미만", "50만원 - 100만원", 
             "100만원 - 200만원", "200만원 - 500만원", "500만원 이상"],
            index=2
        )
    
    with col2:
        emergency_fund = st.selectbox(
            "비상 자금 준비 상태",
            ["없음", "생활비 3개월분", "생활비 6개월분", 
             "생활비 12개월분", "생활비 24개월분 이상"],
            index=2
        )
        
        debt_status = st.selectbox(
            "부채 상황",
            ["없음", "소액 (연소득 10% 미만)", "보통 (연소득 10-30%)", 
             "많음 (연소득 30-50%)", "과다 (연소득 50% 이상)"],
            index=1
        )
    
    # 투자 성향 분석
    st.markdown("### 📊 투자 성향 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_tolerance = st.radio(
            "투자 손실에 대한 허용도",
            ["매우 보수적 (손실 절대 불가)", 
             "보수적 (5% 이하 손실 허용)",
             "중립적 (10-15% 손실 허용)", 
             "적극적 (20-30% 손실 허용)",
             "공격적 (30% 이상 손실도 감수)"],
            index=2
        )
        
        investment_knowledge = st.selectbox(
            "투자 경험 및 지식 수준",
            ["초보자 (예적금만 경험)", "초급자 (펀드 투자 경험)", 
             "중급자 (주식 직접 투자)", "고급자 (파생상품 경험)", 
             "전문가 (포트폴리오 운용)"],
            index=1
        )
    
    with col2:
        investment_period = st.selectbox(
            "투자 예상 기간",
            ["6개월 이하", "6개월 - 1년", "1년 - 3년", 
             "3년 - 5년", "5년 - 10년", "10년 이상"],
            index=3
        )
        
        investment_goal = st.selectbox(
            "주요 투자 목적",
            ["안전한 자산 보전", "인플레이션 대응", "목돈 마련 (결혼, 주택)",
             "자녀 교육비", "노후 준비", "경제적 자유 달성"],
            index=2
        )
    
    # 선호 투자 시장
    st.markdown("### 🌍 선호 투자 시장 및 자산")
    
    col1, col2 = st.columns(2)
    
    with col1:
        preferred_market = st.multiselect(
            "선호하는 투자 시장 (복수 선택 가능)",
            ["국내 주식 (KOSPI, KOSDAQ)", "미국 주식 (S&P500, NASDAQ)", 
             "선진국 주식 (유럽, 일본)", "신흥국 주식", 
             "국내 채권", "해외 채권", "원자재 (금, 원유)", 
             "부동산 (REITs)", "암호화폐"],
            default=["국내 주식 (KOSPI, KOSDAQ)", "미국 주식 (S&P500, NASDAQ)"]
        )
        
        sector_preference = st.multiselect(
            "관심 있는 투자 섹터",
            ["IT/반도체", "바이오/헬스케어", "금융", "에너지/화학",
             "소비재", "자동차", "건설/부동산", "통신", "배터리/ESG"],
            default=["IT/반도체", "바이오/헬스케어"]
        )
    
    with col2:
        trading_style = st.radio(
            "선호하는 투자 스타일",
            ["장기 보유 (Buy & Hold)", "정기 적립 투자 (DCA)", 
             "시장 타이밍 투자", "단기 트레이딩", "혼합 스타일"],
            index=1
        )
        
        monitoring_frequency = st.selectbox(
            "포트폴리오 점검 빈도",
            ["매일", "주 1회", "월 1회", "분기별", "반기별", "연 1회"],
            index=2
        )
    
    # 투자 성향 분석 결과
    st.markdown("### 🎯 투자자 프로필 분석 결과")
    
    # 간단한 점수 계산 로직
    risk_scores = {"매우 보수적": 1, "보수적": 2, "중립적": 3, "적극적": 4, "공격적": 5}
    knowledge_scores = {"초보자": 1, "초급자": 2, "중급자": 3, "고급자": 4, "전문가": 5}
    period_scores = {"6개월 이하": 1, "6개월 - 1년": 2, "1년 - 3년": 3, 
                    "3년 - 5년": 4, "5년 - 10년": 5, "10년 이상": 6}
    
    total_score = (risk_scores.get(risk_tolerance, 3) + 
                  knowledge_scores.get(investment_knowledge, 2) + 
                  period_scores.get(investment_period, 3)) / 3
    
    if total_score <= 2:
        profile_type = "안전 추구형"
        profile_color = "🔵"
        recommended_allocation = {"주식": 30, "채권": 60, "현금": 10}
    elif total_score <= 3.5:
        profile_type = "균형 추구형"
        profile_color = "🟡"
        recommended_allocation = {"주식": 60, "채권": 30, "현금": 10}
    else:
        profile_type = "성장 추구형"
        profile_color = "🔴"
        recommended_allocation = {"주식": 80, "채권": 15, "현금": 5}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("투자자 유형", f"{profile_color} {profile_type}")
        st.write(f"**위험 허용도**: {risk_tolerance}")
        st.write(f"**투자 지식**: {investment_knowledge}")
    
    with col2:
        st.metric("투자 기간", investment_period)
        st.write(f"**투자 목적**: {investment_goal}")
        st.write(f"**투자 스타일**: {trading_style}")
    
    with col3:
        st.metric("종합 점수", f"{total_score:.1f}/5.0")
        st.write(f"**선호 시장**: {len(preferred_market)}개 시장")
        st.write(f"**관심 섹터**: {len(sector_preference)}개 섹터")
    
    # 추천 자산 배분
    st.markdown("### 📊 맞춤형 자산 배분 제안")
    
    fig = go.Figure(data=[go.Pie(
        labels=list(recommended_allocation.keys()),
        values=list(recommended_allocation.values()),
        hole=0.4,
        marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )])
    fig.update_layout(
        title=f"{profile_type} 추천 자산 배분",
        height=400
    )
    st.plotly_chart(fig)
    
    # 다음 단계 안내
    st.markdown("### 🚀 다음 단계")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 거시경제 분석 단계로", type="primary"):
            st.success("✅ 투자자 프로필이 설정되었습니다!")
            st.info("� 위의 '📊 거시전략가' 탭을 클릭하여 경제 환경 분석을 시작해주세요!")
    
    with col2:
        if st.button("🔄 프로필 다시 설정"):
            st.rerun()
    
    # 상담 요약
    with st.expander("📋 투자 상담 요약", expanded=False):
        st.markdown(f"""
        **👤 투자자 정보**
        - 투자 가능 자산: {investment_amount}
        - 월 추가 투자: {monthly_saving}
        - 비상 자금: {emergency_fund}
        
        **🎯 투자 성향**
        - 유형: {profile_color} {profile_type}
        - 위험 허용도: {risk_tolerance}
        - 투자 기간: {investment_period}
        - 투자 목적: {investment_goal}
        
        **🌍 투자 선호**
        - 선호 시장: {', '.join(preferred_market)}
        - 관심 섹터: {', '.join(sector_preference)}
        - 투자 스타일: {trading_style}
        
        **💡 추천 방향**
        - 주식 비중: {recommended_allocation['주식']}%
        - 채권 비중: {recommended_allocation['채권']}%
        - 현금 비중: {recommended_allocation['현금']}%
        """)

def tab_intro():
    """인트로 탭"""
    st.header("🎯 딥시그널 — AI 투자 에이전시")
    
    # 메인 비전
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin: 20px 0;">
        <h2>🤖 8명의 투자전문 AI와 함께하는 단계별 의사결정</h2>
        <p style="font-size: 18px; margin: 10px 0;">각 분야 전문가 AI가 순차적으로 분석하여 최적의 투자 전략을 도출합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.markdown("""
        ### 🎯 **왜 딥시그널인가?**
        
        **🧠 집단지성 의사결정**: 8명의 전문 AI가 각각의 전문 영역에서 분석하고 토론하여 편향을 제거합니다
        
        **📊 데이터 기반 객관성**: 감정적 판단을 배제하고 순수 데이터와 알고리즘으로 투자 결정을 내립니다
        
        **🎨 개인 맞춤형**: 투자자의 성향, 목표, 자금 규모를 반영한 완전 개인화된 포트폴리오를 제안합니다
        
        **⚡ 실시간 실행**: 분석부터 매매 타이밍까지 원스톱으로 실제 투자 실행을 지원합니다
        """)
    
    with col2:
        st.markdown("""
        ### 💼 **8명의 전문 AI팀**
        
        **👥 투자상담매니저**  
        *투자자 성향 분석*
        
        **📊 거시전략가**  
        *글로벌 경제 분석*
        
        **💰 자산배분가**  
        *포트폴리오 최적화*
        
        **🔍 섹터리서처**  
        *산업별 투자기회 발굴*
        
        **📈 종목애널리스트**  
        *개별 종목 심층분석*
        
        **🏆 CIO전략실**  
        *최종 전략 확정*
        
        **⚡ 트레이드플래너**  
        *매매 타이밍 최적화*
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 프로세스 플로우
    st.markdown("### 🔄 **투자 의사결정 프로세스**")
    
    process_steps = [
        ("👥", "투자 프로필링", "성향·목표·자금 분석"),
        ("📊", "거시환경 진단", "경제 시나리오 설정"),
        ("💰", "자산배분 설계", "리스크 최적화"),
        ("🔍", "섹터 발굴", "성장동력 분석"),
        ("📈", "종목 선별", "개별 기업 분석"),
        ("🏆", "전략 확정", "포트폴리오 완성"),
        ("⚡", "실행 계획", "매매 타이밍 설정")
    ]
    
    cols = st.columns(7)
    for i, (icon, title, desc) in enumerate(process_steps):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border: 2px solid #f0f2f6; border-radius: 10px; height: 120px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 24px;">{icon}</div>
                <div style="font-weight: bold; font-size: 12px; margin: 5px 0;">{title}</div>
                <div style="font-size: 10px; color: #666;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if i < len(process_steps) - 1:
            st.markdown("<div style='text-align: center; margin: 10px 0;'>→</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 핵심 특징
    st.markdown("### ✨ **핵심 경쟁력**")
    
    features = [
        ("🎯", "정밀 타겟팅", "투자자별 맞춤형 전략", "#4CAF50"),
        ("🔬", "과학적 분석", "AI 기반 객관적 판단", "#2196F3"), 
        ("⚡", "즉시 실행", "분석부터 매매까지 원스톱", "#FF9800"),
        ("📱", "언제 어디서", "모바일 접근 24/7 가능", "#9C27B0")
    ]
    
    cols = st.columns(4)
    for i, (icon, title, desc, color) in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: {color}15; border-left: 4px solid {color}; border-radius: 5px;">
                <div style="font-size: 30px; margin-bottom: 10px;">{icon}</div>
                <div style="font-weight: bold; color: {color}; margin-bottom: 5px;">{title}</div>
                <div style="font-size: 14px; color: #666;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 시작하기 버튼 (중앙 정렬, 더 임팩트 있게)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3 style="color: #667eea; margin-bottom: 15px;">🚀 당신만의 투자 전략을 찾아보세요</h3>
            <p style="color: #666; margin-bottom: 20px;">8명의 AI 전문가가 단계별로 최적의 투자 솔루션을 제안합니다</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎯 AI 투자 여정 시작하기", type="primary", use_container_width=True):
            st.success("✅ 투자상담매니저와의 상담이 시작됩니다!")
            st.info("👆 위의 '👥 투자상담매니저' 탭을 클릭하여 투자 프로필 설정을 시작해주세요!")
            st.markdown("""
            <script>
            setTimeout(function() {
                var tabs = parent.document.querySelectorAll('[data-testid="stTabs"] button');
                if (tabs.length > 1) {
                    tabs[1].click();
                }
            }, 1000);
            </script>
            """, unsafe_allow_html=True)

def tab_macro():
    """거시전략가 탭"""
    st.header("📊 거시전략가")
    st.markdown("**글로벌 경제 환경 분석 및 투자 전략 수립**")
    
    # 현재 거시경제 지표
    st.markdown("### 🌍 주요 거시경제 지표")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("미국 기준금리", "5.25%", "-0.25%")
        st.metric("한국 기준금리", "3.50%", "0.00%")
    
    with col2:
        st.metric("미국 CPI", "3.2%", "-0.3%")
        st.metric("한국 CPI", "3.1%", "+0.1%")
    
    with col3:
        st.metric("달러/원 환율", "1,320원", "+15원")
        st.metric("WTI 유가", "$87.5", "+$2.3")
    
    with col4:
        st.metric("VIX 공포지수", "18.5", "-2.1")
        st.metric("미국 10년 국채", "4.6%", "+0.1%")
    
    # 거시 환경 시나리오 분석
    st.markdown("### 📈 거시 환경 시나리오 분석")
    
    scenarios = {
        "� 소프트랜딩 시나리오 (확률 40%)": {
            "description": "인플레이션 안정화, 경기 둔화 없이 금리 정상화",
            "implications": "성장주 회복, 기술주 선호, 장기 채권 매력도 증가",
            "recommended_assets": {"성장주": 45, "가치주": 25, "채권": 20, "현금": 10}
        },
        "� 경기둔화 시나리오 (확률 35%)": {
            "description": "고금리 지속으로 경기 둔화, 기업 실적 부진",
            "implications": "방어주 선호, 배당주 매력, 단기 채권 비중 확대",
            "recommended_assets": {"방어주": 35, "배당주": 30, "채권": 25, "현금": 10}
        },
        "🔴 재인플레이션 시나리오 (확률 25%)": {
            "description": "인플레이션 재상승, 추가 금리 인상 압력",
            "implications": "실물자산 선호, 에너지/원자재 투자, 변동금리 채권",
            "recommended_assets": {"원자재": 30, "에너지": 25, "실물자산": 25, "현금": 20}
        }
    }
    
    selected_scenario = st.selectbox(
        "투자 전략의 기준이 될 거시 시나리오를 선택하세요:",
        list(scenarios.keys())
    )
    
    scenario_data = scenarios[selected_scenario]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📝 시나리오 설명**")
        st.write(scenario_data["description"])
        st.markdown(f"**💡 투자 시사점**")
        st.write(scenario_data["implications"])
    
    with col2:
        # 시나리오별 추천 자산배분 시각화
        fig = go.Figure(data=[go.Pie(
            labels=list(scenario_data["recommended_assets"].keys()),
            values=list(scenario_data["recommended_assets"].values()),
            hole=0.4
        )])
        fig.update_layout(title=f"시나리오별 추천 자산배분")
        st.plotly_chart(fig)
    
    # 지역별 시장 전망
    st.markdown("### 🌏 지역별 시장 전망")
    
    market_outlook = {
        "🇺🇸 미국": {"outlook": "중립", "score": 75, "reason": "기업실적 견조하나 밸류에이션 부담"},
        "🇰🇷 한국": {"outlook": "긍정", "score": 80, "reason": "반도체 업사이클, 저평가 매력"},
        "🇨🇳 중국": {"outlook": "신중", "score": 45, "reason": "부동산 리스크, 정책 불확실성"},
        "🇪🇺 유럽": {"outlook": "중립", "score": 60, "reason": "에너지 안정화, 경기 회복 지연"},
        "🌏 신흥국": {"outlook": "긍정", "score": 70, "reason": "달러 약세 기대, 원자재 수혜"}
    }
    
    for region, data in market_outlook.items():
        with st.expander(f"{region} 시장 전망", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                if data["score"] >= 70:
                    outlook_color = "🟢"
                elif data["score"] >= 50:
                    outlook_color = "🟡"
                else:
                    outlook_color = "🔴"
                
                st.metric("투자 매력도", f"{data['score']}/100")
                st.write(f"**전망**: {outlook_color} {data['outlook']}")
                st.write(f"**근거**: {data['reason']}")
            
            with col2:
                # 가격 차트 시뮬레이션
                days = pd.date_range('2024-01-01', periods=50, freq='D')
                trend = 1 if data["score"] > 60 else -1 if data["score"] < 50 else 0
                prices = 100 + np.cumsum(np.random.normal(trend*0.3, 1.5, 50))
                
                fig = px.line(x=days, y=prices, title=f"{region} 시장 추이")
                fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig)
    
    # 투자 전략 결론
    st.markdown("### 🎯 거시전략가 결론")
    
    if "소프트랜딩" in selected_scenario:
        st.success("🚀 위험자산 확대 전략: 성장주와 기술주 중심의 공격적 포트폴리오")
        strategy_recommendation = "성장주 위주 적극 투자"
    elif "둔화" in selected_scenario:
        st.warning("🛡️ 방어적 자산배분: 배당주와 채권 중심의 안정적 포트폴리오")
        strategy_recommendation = "방어주 위주 안정 투자"
    else:
        st.error("⚠️ 인플레이션 헤지: 실물자산과 원자재 중심의 인플레이션 대응 포트폴리오")
        strategy_recommendation = "실물자산 위주 헤지 투자"
    
    # 다음 단계 안내
    if st.button("💰 자산배분 최적화 단계로", type="primary"):
        st.success("✅ 거시 환경 분석이 완료되었습니다!")
        st.info(f"🔄 자산배분가 탭에서 '{strategy_recommendation}' 전략을 바탕으로 구체적인 포트폴리오를 구성해보세요.")

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