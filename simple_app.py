import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 페이지 설정
st.set_page_config(
    page_title="딥시그널 AI 투자 플랫폼",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 모바일 최적화 CSS
st.markdown("""
<style>
    /* 전체 레이아웃 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* 모바일 첫번째 최적화 - 제목 */
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.3;
    }
    
    /* 진행 표시줄 */
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .progress-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .progress-bar {
        background: #e0e0e0;
        border-radius: 15px;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        border-radius: 15px;
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* AI 전문가 카드 */
    .expert-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .expert-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 6px 12px rgba(31,119,180,0.2);
        transform: translateY(-2px);
    }
    
    .expert-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .expert-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .expert-desc {
        font-size: 1.6rem;
        color: #666;
        line-height: 1.4;
    }
    
    /* 프로세스 단계 카드 */
    .process-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #1f77b4;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .process-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .process-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .process-desc {
        font-size: 1.4rem;
        color: #666;
        line-height: 1.3;
    }
    
    /* 네비게이션 버튼 */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.8rem;
        }
        .subtitle {
            font-size: 1.6rem;
        }
        .expert-title {
            font-size: 1.6rem;
        }
        .expert-desc {
            font-size: 1.3rem;
        }
        .process-title {
            font-size: 1.5rem;
        }
        .process-desc {
            font-size: 1.2rem;
        }
    }
    
    /* Streamlit 기본 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 컨텐츠 영역 폰트 크기 증가 */
    .stMarkdown {
        font-size: 1.6rem;
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        font-size: 1.8rem;
        font-weight: bold;
        height: 60px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# 단계별 이름 정의
STEP_NAMES = [
    "🏠 AI 소개",
    " 투자상담매니저",
    "📊 시장전략가", 
    "💰 자산배분전문가",
    "🔍 산업리서처",
    "📈 종목분석가"
]

def show_progress_bar():
    """진행 상황 표시"""
    progress = (st.session_state.current_step + 1) / len(STEP_NAMES)
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-title">{STEP_NAMES[st.session_state.current_step]}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress*100}%"></div>
        </div>
        <div style="text-align: center; font-size: 1.4rem; color: #666; margin-top: 0.5rem;">
            {st.session_state.current_step + 1} / {len(STEP_NAMES)} 단계
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_navigation(current_step):
    """각 페이지별 맞춤 네비게이션 버튼"""
    # 각 단계별 다음 버튼 텍스트 정의
    next_button_texts = [
        "👥 투자상담 시작하기 ➡️",  # AI 소개
        "📊 시장분석 보기 ➡️",  # 투자상담매니저
        "💰 자산배분 보기 ➡️",  # 시장전략가
        "🔍 산업분석 보기 ➡️",  # 자산배분전문가
        "📈 종목추천 보기 ➡️",  # 산업리서처
        "🎆 분석 완료!"  # 종목분석가
    ]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_step > 0:
            if st.button("⬅️ 이전", use_container_width=True, type="secondary"):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col3:
        if st.session_state.current_step < len(STEP_NAMES) - 1:
            next_text = next_button_texts[current_step]
            if st.button(next_text, use_container_width=True, type="primary"):
                st.session_state.current_step += 1
                st.rerun()

# =============================================================================
# 각 단계별 함수들 (6단계로 단순화)
# =============================================================================

def step_ai_intro():
    """1단계: AI 소개"""
    st.markdown('<div class="main-title">🤖 딥시그널 AI 투자 플랫폼</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">8명의 AI 투자전문가가 함께하는 똑똑한 투자</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI 전문가 소개 (모바일 최적화: 2열 배치)
    experts = [
        ("👥", "투자상담매니저", "투자성향과 목표를 분석하여 맞춤형 투자전략을 제시합니다"),
        ("📊", "시장전략가", "거시경제와 시장 동향을 분석하여 투자 방향을 제시합니다"),
        ("💰", "자산배분전문가", "리스크 관리와 포트폴리오 최적화를 통한 자산배분을 설계합니다"),
        ("🔍", "산업리서처", "산업별 트렌드와 성장성을 분석하여 유망 섹터를 발굴합니다"),
        ("📈", "종목분석가", "개별 종목의 기술적/기본적 분석을 통해 투자 기회를 찾습니다"),
        ("⚡", "매매전략가", "모멘텀과 RSI 지표를 활용한 최적의 매매 타이밍을 제공합니다"),
        ("🏆", "포트폴리오매니저", "전체 포트폴리오의 성과를 모니터링하고 리밸런싱을 관리합니다"),
        ("🎯", "투자컨설턴트", "종합적인 투자 자문과 개인별 맞춤 솔루션을 제공합니다")
    ]
    
    # 2열 배치
    for i in range(0, len(experts), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(experts):
                icon, title, desc = experts[i + j]
                with col:
                    st.markdown(f"""
                    <div class="expert-card">
                        <div class="expert-icon">{icon}</div>
                        <div class="expert-title">{title}</div>
                        <div class="expert-desc">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")

def step_consultant():
    """투자상담매니저"""
    st.markdown('<div class="main-title">👥 투자상담매니저</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">맞춤형 투자 전략을 위한 상담</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 상담 진행
    with st.container():
        st.markdown("### 💼 1. 기본 투자 정보")
        
        col1, col2 = st.columns(2)
        with col1:
            investment_experience = st.selectbox(
                "투자 경험은?",
                ["투자 초보 (1년 미만)", "초급자 (1-3년)", "중급자 (3-7년)", "고급자 (7년 이상)"],
                key="experience"
            )
        
        with col2:
            target_return = st.selectbox(
                "목표 수익률은?",
                ["안정형 (3-5%)", "균형형 (5-10%)", "성장형 (10-15%)", "공격형 (15% 이상)"],
                key="target_return"
            )
    
    st.markdown("---")
    
    st.markdown("### ⚖️ 2. 리스크 성향")
    
    col1, col2 = st.columns(2)
    with col1:
        risk_tolerance = st.selectbox(
            "손실 허용 한도는?",
            ["매우 보수적 (5% 미만)", "보수적 (5-10%)", "보통 (10-20%)", "적극적 (20% 이상)"],
            key="risk_tolerance"
        )
    
    with col2:
        investment_style = st.selectbox(
            "투자 스타일은?",
            ["안정성 중시", "균형 추구", "성장성 중시", "고수익 추구"],
            key="investment_style"
        )
    
    st.markdown("---")
    
    st.markdown("### 📅 3. 투자 목표")
    
    col1, col2 = st.columns(2)
    with col1:
        investment_period = st.selectbox(
            "투자 기간은?",
            ["단기 (1년 미만)", "중기 (1-3년)", "장기 (3-5년)", "초장기 (5년 이상)"],
            key="investment_period"
        )
    
    with col2:
        investment_purpose = st.selectbox(
            "투자 목적은?",
            ["여유자금 운용", "노후 준비", "목돈 마련", "기타"],
            key="investment_purpose"
        )
    
    st.markdown("---")
    
    st.markdown("### 🎨 4. AI 전략 스타일")
    
    ai_strategy = st.selectbox(
        "선호하는 AI 전략은?",
        [
            "🛡️ 안전 우선형 - 리스크 최소화 전략",
            "⚖️ 균형 추구형 - 안정성과 수익성의 조화", 
            "📈 성장 추구형 - 트렌드 기반 성장주 중심",
            "⚡ 모멘텀형 - 기술적 분석 기반 단기 전략"
        ],
        key="ai_strategy"
    )
    
    # 분석 결과 자동 저장
    st.session_state.user_profile = {
        'experience': investment_experience,
        'target_return': target_return,
        'risk_tolerance': risk_tolerance,
        'investment_style': investment_style,
        'investment_period': investment_period,
        'investment_purpose': investment_purpose,
        'ai_strategy': ai_strategy
    }
    
    st.success("✅ 투자성향 분석이 완료되었습니다!")
    st.info("💡 다음 단계에서 시장전략가가 현재 시장 상황을 분석해드립니다.")

def step_market_analyst():
    """5단계: 시장전략가"""
    st.markdown('<div class="main-title">📊 시장전략가</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">거시경제 분석 및 시장 전망</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 시장 개요
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 코스피", "2,580.50", "12.30 (0.48%)")
    with col2:
        st.metric("💱 달러/원", "1,340.50", "-8.20 (-0.61%)")
    with col3:
        st.metric("🏛️ 기준금리", "3.50%", "동결")
    
    st.markdown("---")
    
    # 시장 분석
    st.markdown("### 🔍 현재 시장 분석")
    
    # 차트 데이터 생성
    dates = pd.date_range(start='2024-01-01', end='2024-10-15', freq='D')
    kospi_data = 2400 + np.cumsum(np.random.randn(len(dates)) * 5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=kospi_data,
        mode='lines',
        name='KOSPI',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title="코스피 지수 추이 (2024년)",
        xaxis_title="날짜",
        yaxis_title="지수",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 섹터별 전망
    st.markdown("### 🎯 섹터별 투자 전망")
    
    sectors = [
        ("💻 IT/반도체", "긍정적", "AI 붐과 반도체 슈퍼사이클 진입"),
        ("🏭 제조업", "보통", "글로벌 경기 둔화 우려 상존"),
        ("🏦 금융", "긍정적", "금리 인상 효과 지속"),
        ("⚡ 에너지", "주의", "유가 변동성 확대"),
        ("🏥 바이오", "긍정적", "신약 파이프라인 기대감"),
        ("🏢 부동산", "부정적", "금리 상승과 규제 강화")
    ]
    
    for i in range(0, len(sectors), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(sectors):
                sector, outlook, reason = sectors[i + j]
                
                color = {"긍정적": "🟢", "보통": "🟡", "주의": "🟠", "부정적": "🔴"}[outlook]
                
                with col:
                    st.markdown(f"""
                    <div style="background: white; border: 2px solid #e0e0e0; border-radius: 10px; 
                                padding: 1.5rem; margin: 0.5rem 0; text-align: center;">
                        <h4>{sector}</h4>
                        <p>{color} {outlook}</p>
                        <p style="font-size: 0.9rem; color: #666;">{reason}</p>
                    </div>
                    """, unsafe_allow_html=True)

def step_asset_allocator():
    """6단계: 자산배분전문가"""
    st.markdown('<div class="main-title">💰 자산배분전문가</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">최적화된 포트폴리오 구성</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 사용자 프로필 기반 추천
    if st.session_state.user_profile:
        risk_level = st.session_state.user_profile.get('risk_tolerance', '보통 (10-20%)')
        
        if "매우 보수적" in risk_level:
            portfolio = {"현금/예금": 40, "채권": 40, "주식": 15, "대안투자": 5}
        elif "보수적" in risk_level:
            portfolio = {"현금/예금": 20, "채권": 50, "주식": 25, "대안투자": 5}
        elif "보통" in risk_level:
            portfolio = {"현금/예금": 10, "채권": 30, "주식": 50, "대안투자": 10}
        else:  # 적극적
            portfolio = {"현금/예금": 5, "채권": 15, "주식": 65, "대안투자": 15}
    else:
        portfolio = {"현금/예금": 10, "채권": 30, "주식": 50, "대안투자": 10}
    
    # 파이 차트
    fig = px.pie(
        values=list(portfolio.values()),
        names=list(portfolio.keys()),
        title="추천 자산배분 포트폴리오"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 자산별 상세 설명
    st.markdown("### 📋 자산별 투자 전략")
    
    asset_details = [
        ("💰 현금/예금", f"{portfolio['현금/예금']}%", "유동성 확보 및 기회 대기"),
        ("📈 채권", f"{portfolio['채권']}%", "안정적 수익과 포트폴리오 방어"),
        ("📊 주식", f"{portfolio['주식']}%", "장기 성장 동력 확보"),
        ("🔮 대안투자", f"{portfolio['대안투자']}%", "분산투자 효과 극대화")
    ]
    
    for detail in asset_details:
        asset, ratio, desc = detail
        st.markdown(f"**{asset}** ({ratio}): {desc}")

def step_sector_researcher():
    """7단계: 산업리서처"""
    st.markdown('<div class="main-title">🔍 산업리서처</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">유망 섹터 발굴 및 분석</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 추천 섹터 TOP 5
    st.markdown("### 🏆 이달의 추천 섹터 TOP 5")
    
    recommended_sectors = [
        ("🤖 AI/빅데이터", "매우 높음", "+18.5%", "ChatGPT 열풍과 AI 반도체 수요 급증"),
        ("⚡ 2차전지", "높음", "+12.3%", "전기차 시장 확대와 ESG 투자 증가"),
        ("🏥 바이오헬스", "높음", "+15.7%", "고령화 사회와 헬스케어 디지털화"),
        ("🛡️ 사이버보안", "보통", "+8.9%", "디지털 전환 가속화와 보안 위협 증가"),
        ("🌱 친환경에너지", "보통", "+6.4%", "탄소중립 정책과 재생에너지 확산")
    ]
    
    for i, (sector, level, return_rate, reason) in enumerate(recommended_sectors, 1):
        color = {"매우 높음": "#ff4444", "높음": "#ff8800", "보통": "#44aa44"}[level]
        
        st.markdown(f"""
        <div style="background: white; border-left: 5px solid {color}; padding: 1rem; margin: 1rem 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h4>#{i} {sector} <span style="color: {color};">({level})</span></h4>
            <p><strong>기대수익률:</strong> <span style="color: green;">{return_rate}</span></p>
            <p><strong>투자근거:</strong> {reason}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 섹터 성과 차트
    st.markdown("### 📊 섹터별 성과 비교 (최근 3개월)")
    
    sectors_perf = pd.DataFrame({
        '섹터': ['AI/빅데이터', '2차전지', '바이오헬스', '사이버보안', '친환경에너지', '전통제조', '금융'],
        '수익률(%)': [18.5, 12.3, 15.7, 8.9, 6.4, -2.1, 3.8]
    })
    
    fig = px.bar(
        sectors_perf, 
        x='섹터', 
        y='수익률(%)',
        color='수익률(%)',
        color_continuous_scale='RdYlGn',
        title="섹터별 3개월 수익률"
    )
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

def step_stock_analyzer():
    """8단계: 종목분석가"""
    st.markdown('<div class="main-title">📈 종목분석가</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">모멘텀 + RSI 기반 종목 추천</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 추천 종목 (모멘텀 + RSI 분석)
    st.markdown("### 🎯 AI 추천 종목 TOP 10")
    
    recommended_stocks = [
        ("삼성전자", "005930", "반도체", 68500, "+2.3%", "매수", 45, "상승모멘텀 지속"),
        ("SK하이닉스", "000660", "반도체", 98200, "+1.8%", "매수", 42, "메모리 반등 기대"),
        ("NAVER", "035420", "IT서비스", 185000, "+3.1%", "매수", 38, "AI 플랫폼 강화"),
        ("카카오", "035720", "IT서비스", 51800, "-0.5%", "관망", 55, "횡보 구간 진입"),
        ("LG에너지솔루션", "373220", "2차전지", 425000, "+1.2%", "매수", 48, "전기차 수요 증가"),
        ("삼성바이오로직스", "207940", "바이오", 750000, "+0.8%", "매수", 52, "위탁생산 확대"),
        ("현대차", "005380", "자동차", 178000, "-1.2%", "관망", 58, "전기차 전환 과도기"),
        ("포스코홀딩스", "005490", "철강", 385000, "+2.5%", "매수", 44, "원자재 반등"),
        ("KB금융", "105560", "금융", 65400, "+1.5%", "매수", 46, "금리 상승 수혜"),
        ("셀트리온", "068270", "바이오", 154000, "+2.8%", "매수", 40, "바이오시밀러 확산")
    ]
    
    # 테이블 형태로 표시
    df = pd.DataFrame(recommended_stocks, columns=[
        '종목명', '종목코드', '섹터', '현재가', '등락률', 'AI추천', 'RSI', '투자포인트'
    ])
    
    st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # 모멘텀 분석 예시 (삼성전자)
    st.markdown("### 📊 모멘텀 분석 예시: 삼성전자")
    
    # 가상 주가 데이터 생성
    dates = pd.date_range(start='2024-07-01', end='2024-10-15', freq='D')
    prices = 65000 + np.cumsum(np.random.randn(len(dates)) * 800)
    
    # RSI 계산 (간단 버전)
    rsi_values = []
    for i in range(len(prices)):
        if i < 14:
            rsi_values.append(50)
        else:
            gains = []
            losses = []
            for j in range(i-13, i+1):
                if j > 0:
                    change = prices[j] - prices[j-1]
                    if change > 0:
                        gains.append(change)
                        losses.append(0)
                    else:
                        gains.append(0)
                        losses.append(abs(change))
            
            avg_gain = np.mean(gains) if gains else 0
            avg_loss = np.mean(losses) if losses else 0
            
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            
            rsi_values.append(rsi)
    
    # 차트 생성
    fig = go.Figure()
    
    # 주가 차트
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name='주가',
        yaxis='y',
        line=dict(color='blue', width=2)
    ))
    
    # RSI 차트
    fig.add_trace(go.Scatter(
        x=dates,
        y=rsi_values,
        mode='lines',
        name='RSI',
        yaxis='y2',
        line=dict(color='red', width=2)
    ))
    
    # RSI 기준선
    fig.add_hline(y=70, line_dash="dash", line_color="red", yref='y2', annotation_text="과매수(70)")
    fig.add_hline(y=30, line_dash="dash", line_color="blue", yref='y2', annotation_text="과매도(30)")
    
    fig.update_layout(
        title="삼성전자 주가 및 RSI 분석",
        xaxis_title="날짜",
        yaxis=dict(title="주가 (원)", side="left"),
        yaxis2=dict(title="RSI", side="right", overlaying="y", range=[0, 100]),
        height=500,
        legend=dict(x=0, y=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 투자 신호 요약
    st.markdown("### 🚦 투자 신호 요약")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📈 모멘텀 분석**
        - 20일 이평선 상향 돌파
        - 거래량 증가 확인
        - **신호: 매수**
        """)
    
    with col2:
        st.markdown("""
        **⚖️ RSI 분석**
        - 현재 RSI: 45
        - 과매도 구간 탈출
        - **신호: 중립**
        """)
    
    with col3:
        st.markdown("""
        **🎯 종합 판단**
        - AI 점수: 85/100
        - 추천 비중: 5-7%
        - **신호: 매수**
        """)

# =============================================================================
# 메인 실행 부분
# =============================================================================

def main():
    """메인 함수"""
    
    # 진행 상황 표시 제거 - 깔끔한 UI
    
    st.markdown("---")
    
    # 각 단계별 실행
    if st.session_state.current_step == 0:
        step_ai_intro()
    elif st.session_state.current_step == 1:
        step_consultant()
    elif st.session_state.current_step == 2:
        step_market_analyst()
    elif st.session_state.current_step == 3:
        step_asset_allocator()
    elif st.session_state.current_step == 4:
        step_sector_researcher()
    elif st.session_state.current_step == 5:
        step_stock_analyzer()
    
    st.markdown("---")
    
    # 네비게이션 버튼
    show_navigation(st.session_state.current_step)

if __name__ == "__main__":
    main()