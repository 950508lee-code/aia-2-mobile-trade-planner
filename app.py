"""
AIA 2.0 — Dual-Team AI Investment Agency Dashboard
투자 에이전시 대시보드 메인 애플리케이션
"""

import streamlit as st
import pandas as pd
import numpy as np
# import altair as alt  # Python 3.14 호환성 문제로 임시 제거
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="AIA 2.0 — AI Investment Agency",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 유틸리티 함수들
def format_money(value):
    """숫자를 한국식 화폐 단위로 변환"""
    if value >= 1000000000000:  # 조
        return f"{value/1000000000000:.1f}조원"
    elif value >= 100000000:  # 억
        return f"{value/100000000:.1f}억원"
    elif value >= 10000:  # 만
        return f"{value/10000:.0f}만원"
    else:
        return f"{value:,.0f}원"

def format_percent(value):
    """소수를 퍼센트로 변환"""
    return f"{value*100:.1f}%" if value < 1 else f"{value:.1f}%"

def get_stock_info(종목코드):
    """종목 정보 조회 (더미 데이터)"""
    # 실제로는 API에서 가져올 데이터
    stock_data = {
        '005930': {'name': '삼성전자', 'sector': '반도체', 'price': 68000, 'PER': 12.5, 'RSI': 45.2, '밴드대비': -8.5},
        '000660': {'name': 'SK하이닉스', 'sector': '반도체', 'price': 89000, 'PER': 15.2, 'RSI': 38.7, '밴드대비': -12.3},
        '373220': {'name': 'LG에너지솔루션', 'sector': '배터리', 'price': 420000, 'PER': 22.1, 'RSI': 55.8, '밴드대비': 2.1},
        '207940': {'name': '삼성바이오로직스', 'sector': '바이오', 'price': 750000, 'PER': 28.5, 'RSI': 62.3, '밴드대비': 8.7},
        '035720': {'name': '카카오', 'sector': 'IT서비스', 'price': 42000, 'PER': 35.2, 'RSI': 41.2, '밴드대비': -15.2},
        '051910': {'name': 'LG화학', 'sector': '화학', 'price': 320000, 'PER': 18.7, 'RSI': 52.1, '밴드대비': -3.4},
        '006400': {'name': '삼성SDI', 'sector': '배터리', 'price': 380000, 'PER': 16.8, 'RSI': 48.9, '밴드대비': -6.7},
        '028260': {'name': '삼성물산', 'sector': '건설', 'price': 85000, 'PER': 8.9, 'RSI': 33.5, '밴드대비': -18.9},
        '323410': {'name': '카카오뱅크', 'sector': '금융', 'price': 18500, 'PER': 12.3, 'RSI': 44.1, '밴드대비': -9.8},
        '454740': {'name': 'L&K바이오메드', 'sector': '바이오', 'price': 24500, 'PER': 45.2, 'RSI': 67.8, '밴드대비': 12.4}
    }
    
    return stock_data.get(종목코드, {
        'name': f'종목{종목코드}',
        'sector': '기타',
        'price': 50000 + np.random.randint(-20000, 20000),
        'PER': 15 + np.random.randint(-10, 15),
        'RSI': 50 + np.random.randint(-30, 30),
        '밴드대비': np.random.randint(-20, 20)
    })

def init_session_state():
    """세션 상태 초기화"""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0
    
    if 'profile' not in st.session_state:
        st.session_state.profile = {}
    
    if 'choice_macro' not in st.session_state:
        st.session_state.choice_macro = None
    
    if 'choice_alloc' not in st.session_state:
        st.session_state.choice_alloc = None
    
    if 'choice_sector' not in st.session_state:
        st.session_state.choice_sector = None
    
    if 'picks' not in st.session_state:
        st.session_state.picks = []
    
    if 'decision' not in st.session_state:
        st.session_state.decision = None

def show_progress_bar():
    """현재까지의 선택 요약바 표시"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.profile:
            성향 = st.session_state.profile.get('성향', '미선택')
            st.info(f"💼 성향: {성향}")
        else:
            st.warning("💼 성향: 미선택")
    
    with col2:
        if st.session_state.profile:
            시장 = st.session_state.profile.get('시장', '미선택')
            st.info(f"🌍 시장: {시장}")
        else:
            st.warning("🌍 시장: 미선택")
    
    with col3:
        거시선택 = st.session_state.choice_macro or '미선택'
        if 거시선택 != '미선택':
            st.info(f"📊 거시: {거시선택}")
        else:
            st.warning("📊 거시: 미선택")
    
    with col4:
        현재단계 = ["인트로", "거시전략가", "자산배분가", "섹터리서처", "종목애널리스트", "CIO전략실"][st.session_state.current_tab]
        st.success(f"📍 현재: {현재단계}")
    
    st.divider()

def tab_intro():
    """① 인트로(온보딩) 탭"""
    st.title("🎯 AIA 2.0 — AI Investment Agency")
    st.markdown("### 당신만의 AI 투자 전략을 만들어보세요")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📝 투자 프로필 입력")
        
        # 가용자산 입력
        asset_amount = st.number_input(
            "가용 투자자산 (만원)",
            min_value=100,
            max_value=100000,
            value=2000,
            step=100,
            help="투자 가능한 총 자산을 만원 단위로 입력해주세요"
        )
        
        # 투자성향 선택
        risk_preference = st.radio(
            "투자 성향",
            ["안정형", "중립형", "공격형"],
            index=1,
            horizontal=True,
            help="• 안정형: 원금 보전 중시, 낮은 변동성 선호\n• 중립형: 적절한 수익과 위험의 균형\n• 공격형: 높은 수익 추구, 변동성 수용"
        )
        
        # 선호시장 선택
        market_preference = st.radio(
            "선호 시장",
            ["국내", "글로벌"],
            index=0,
            horizontal=True,
            help="• 국내: 한국 주식시장 중심\n• 글로벌: 해외 주식 및 자산 포함"
        )
        
        st.markdown("---")
        
        # 시작하기 버튼
        if st.button("🚀 투자 분석 시작하기", type="primary", width="stretch"):
            # 프로필 저장
            st.session_state.profile = {
                "asset": asset_amount,
                "성향": risk_preference,
                "시장": market_preference
            }
            st.session_state.current_tab = 1
            st.rerun()
    
    with col2:
        st.markdown("#### 💡 AIA 2.0 특징")
        st.info("""
        **🤖 AI 역할 기반 분석**
        • 거시전략가: 경제 환경 분석
        • 자산배분가: 최적 비중 제안
        • 섹터리서처: 유망 산업 발굴
        • 종목애널리스트: 개별 종목 분석
        • CIO전략실: 듀얼팀 포트폴리오 비교
        """)
        
        st.success("""
        **⚡ 3단계 선택 시스템**
        각 단계마다 보수형/중립형/공격형 
        3가지 옵션 중 선택 가능
        """)
        
        st.warning("""
        **🎯 맞춤형 추천**
        사용자 성향과 시장 환경을 종합하여
        A팀(안정형) vs B팀(공격형) 제안
        """)

def tab_macro():
    """② 거시전략가 탭"""
    st.title("📊 거시전략가 — 시장 환경 분석")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🌍 현재 거시경제 해석")
        
        # 3가지 해석 카드
        tab1, tab2, tab3 = st.tabs(["🛡️ 보수적 해석", "⚖️ 균형 해석", "🚀 공격적 해석"])
        
        with tab1:
            st.markdown("""
            #### 📉 신중한 접근 필요
            
            **주요 우려사항:**
            • 장단기 금리 역전 지속으로 경기침체 우려
            • 글로벌 유동성 위축 가능성
            • 지정학적 리스크 상존
            
            **투자 방향:**
            • 현금 및 단기채권 비중 확대
            • 방어주 중심 포트폴리오
            • 변동성 헤지 전략 고려
            """)
            
            if st.button("🛡️ 보수적 해석 선택", key="macro_conservative"):
                st.session_state.choice_macro = "보수형"
                st.success("보수적 해석이 선택되었습니다!")
        
        with tab2:
            st.markdown("""
            #### 📊 균형잡힌 관점
            
            **현황 분석:**
            • 금리 피크아웃 기대감으로 완만한 회복 전망
            • 기업 실적 개선 기대와 밸류에이션 부담 혼재
            • 섹터별 차별화 투자 기회 확대
            
            **투자 방향:**
            • 주식-채권 균형 배분 유지
            • 퀄리티 성장주 선별 투자
            • 섹터 로테이션 전략 활용
            """)
            
            if st.button("⚖️ 균형 해석 선택", key="macro_balanced"):
                st.session_state.choice_macro = "중립형"
                st.success("균형 해석이 선택되었습니다!")
        
        with tab3:
            st.markdown("""
            #### 📈 적극적 기회 포착
            
            **성장 동력:**
            • AI 혁신 사이클 가속화로 구조적 성장 기대
            • 글로벌 공급망 재편 수혜 가능성
            • 신재생에너지 전환 가속화
            
            **투자 방향:**
            • 성장주 중심 공격적 배분
            • 테마주 및 혁신 기업 집중 투자
            • 해외 성장 시장 진출 기업 선호
            """)
            
            if st.button("🚀 공격적 해석 선택", key="macro_aggressive"):
                st.session_state.choice_macro = "공격형"
                st.success("공격적 해석이 선택되었습니다!")
    
    with col2:
        st.markdown("### 📋 주요 거시지표")
        
        # 거시지표 데이터 (더미)
        macro_data = {
            "지표": ["환율(USD/KRW)", "한국 기준금리", "미국 기준금리", "10Y-2Y 스프레드", "코스피 PER", "원유 가격"],
            "현재값": ["1,370원", "3.50%", "5.25%", "-0.30%", "12.8배", "$87.5"],
            "상태": ["보합", "동결", "동결", "역전", "적정", "상승"]
        }
        
        df_macro = pd.DataFrame(macro_data)
        
        # 상태에 따른 컬러 매핑
        def color_status(val):
            if val == "상승":
                return 'background-color: #ffcccc'
            elif val == "역전":
                return 'background-color: #ffffcc'
            elif val == "적정":
                return 'background-color: #ccffcc'
            else:
                return 'background-color: #f0f0f0'
        
        styled_df = df_macro.style.map(color_status, subset=['상태'])
        st.dataframe(styled_df, width="stretch")
        
        st.markdown("### 📊 시장 심리 지수")
        
        # 간단한 게이지 차트
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 65,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "시장 신뢰도"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # 다음 단계 버튼
    st.markdown("---")
    if st.session_state.choice_macro:
        st.success(f"선택된 해석: {st.session_state.choice_macro}")
        if st.button("➡️ 다음 단계: 자산배분가", type="primary"):
            st.session_state.current_tab = 2
            st.rerun()
    else:
        st.warning("거시경제 해석을 선택해주세요.")

def tab_allocation():
    """③ 자산배분가 탭"""
    st.title("💰 자산배분가 — 포트폴리오 구성")
    
    st.markdown("### 🎯 3가지 자산배분 전략")
    
    # 자산배분 데이터 (더미)
    allocations = {
        "방어형": {"채권": 45, "주식": 35, "현금": 15, "금": 5},
        "균형형": {"채권": 30, "주식": 55, "현금": 10, "금": 5},
        "공격형": {"채권": 15, "주식": 75, "현금": 5, "금": 5}
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🛡️ 방어형 포트폴리오")
        
        # 파이차트 생성
        labels = list(allocations["방어형"].keys())
        values = list(allocations["방어형"].values())
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_traces(
            hoverinfo='label+percent',
            textinfo='value+percent',
            textfont_size=12,
            marker=dict(colors=colors, line=dict(color='#000000', width=2))
        )
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **안정성 우선 전략**
        • 예상 수익률: 연 5-7%
        • 예상 변동성: 8-12%
        • 적합한 투자자: 은퇴자, 보수적 성향
        """)
        
        if st.button("🛡️ 방어형 선택", key="alloc_defensive"):
            st.session_state.choice_alloc = "방어형"
            st.success("방어형 배분이 선택되었습니다!")
    
    with col2:
        st.markdown("#### ⚖️ 균형형 포트폴리오")
        
        labels = list(allocations["균형형"].keys())
        values = list(allocations["균형형"].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_traces(
            hoverinfo='label+percent',
            textinfo='value+percent',
            textfont_size=12,
            marker=dict(colors=colors, line=dict(color='#000000', width=2))
        )
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **균형잡힌 성장 전략**
        • 예상 수익률: 연 7-10%
        • 예상 변동성: 12-18%
        • 적합한 투자자: 일반 직장인, 중립적 성향
        """)
        
        if st.button("⚖️ 균형형 선택", key="alloc_balanced"):
            st.session_state.choice_alloc = "균형형"
            st.success("균형형 배분이 선택되었습니다!")
    
    with col3:
        st.markdown("#### 🚀 공격형 포트폴리오")
        
        labels = list(allocations["공격형"].keys())
        values = list(allocations["공격형"].values())
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_traces(
            hoverinfo='label+percent',
            textinfo='value+percent',
            textfont_size=12,
            marker=dict(colors=colors, line=dict(color='#000000', width=2))
        )
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **적극적 성장 전략**
        • 예상 수익률: 연 10-15%
        • 예상 변동성: 18-25%
        • 적합한 투자자: 젊은층, 공격적 성향
        """)
        
        if st.button("🚀 공격형 선택", key="alloc_aggressive"):
            st.session_state.choice_alloc = "공격형"
            st.success("공격형 배분이 선택되었습니다!")
    
    # 선택된 배분 요약
    if st.session_state.choice_alloc:
        st.markdown("---")
        st.markdown(f"### 📊 선택된 전략: {st.session_state.choice_alloc}")
        
        선택배분 = allocations[st.session_state.choice_alloc]
        사용자자산 = st.session_state.profile.get("asset", 2000) * 10000  # 만원을 원으로 변환
        
        배분금액 = {}
        for 자산, 비율 in 선택배분.items():
            배분금액[자산] = int(사용자자산 * 비율 / 100)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💼 자산별 배분 금액")
            for 자산, 금액 in 배분금액.items():
                st.metric(자산, format_money(금액), f"{선택배분[자산]}%")
        
        with col2:
            거시선택 = st.session_state.choice_macro
            if 거시선택 == "보수형":
                추천메시지 = "현재 거시환경이 불안정하여 방어적 자산 비중을 높게 유지하는 것이 적절합니다."
            elif 거시선택 == "공격형":
                추천메시지 = "성장 모멘텀이 강한 환경으로 주식 비중을 확대하여 수익 기회를 포착할 수 있습니다."
            else:
                추천메시지 = "균형잡힌 거시환경에서 리스크 대비 효율적인 자산배분을 추구합니다."
            
            st.success(f"**💡 전략 해설:** {추천메시지}")
    
    # 다음 단계 버튼
    st.markdown("---")
    if st.session_state.choice_alloc:
        if st.button("➡️ 다음 단계: 섹터리서처", type="primary"):
            st.session_state.current_tab = 3
            st.rerun()
    else:
        st.warning("자산배분 전략을 선택해주세요.")

def tab_sector():
    """④ 섹터 리서처 탭"""
    st.title("🔍 섹터리서처 — 유망 산업 발굴")
    
    # 섹터 상대강도 데이터 (더미)
    sector_data = {
        "섹터": ["AI/반도체", "로봇/자동화", "2차전지", "바이오/헬스", "게임/엔터", "화학/소재", "자동차", "에너지", "유틸리티", "필수소비재"],
        "상대강도": [24, 18, 15, 8, 5, -2, -3, -5, -8, -12]
    }
    
    df_sector = pd.DataFrame(sector_data)
    
    st.markdown("### 📊 섹터별 상대강도 분석")
    
    # 바차트 생성
    fig = px.bar(
        df_sector, 
        x="상대강도", 
        y="섹터", 
        orientation='h',
        color="상대강도",
        color_continuous_scale="RdYlGn",
        title="최근 3개월 대비 상대강도 (%)"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🎯 섹터 투자 테마 선택")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🚀 성장섹터")
        st.info("""
        **핵심 테마: AI 혁신**
        • AI/반도체 (+24%)
        • 로봇/자동화 (+18%)
        • 2차전지 (+15%)
        
        **투자 논리:**
        • 4차 산업혁명 가속화
        • 글로벌 공급망 재편 수혜
        • 탄소중립 정책 지원
        """)
        
        if st.button("🚀 성장섹터 선택", key="sector_growth"):
            st.session_state.choice_sector = ["AI/반도체", "로봇/자동화", "2차전지"]
            st.success("성장섹터가 선택되었습니다!")
    
    with col2:
        st.markdown("#### 💰 배당/가치섹터")
        st.info("""
        **핵심 테마: 밸류 투자**
        • 에너지 (-5%)
        • 유틸리티 (-8%)
        • 금융/보험 (0%)
        
        **투자 논리:**
        • 저평가 구간 진입
        • 안정적 배당 수익
        • 경기 회복 시 반등 기대
        """)
        
        if st.button("💰 배당/가치섹터 선택", key="sector_value"):
            st.session_state.choice_sector = ["에너지", "유틸리티", "금융/보험"]
            st.success("배당/가치섹터가 선택되었습니다!")
    
    with col3:
        st.markdown("#### 🛡️ 안정소비섹터")
        st.info("""
        **핵심 테마: 방어 투자**
        • 필수소비재 (-12%)
        • 바이오/헬스 (+8%)
        • 통신서비스 (-3%)
        
        **투자 논리:**
        • 경기 둔감 특성
        • 안정적 현금흐름
        • 고령화 수혜 가능성
        """)
        
        if st.button("🛡️ 안정소비섹터 선택", key="sector_defensive"):
            st.session_state.choice_sector = ["필수소비재", "바이오/헬스", "통신서비스"]
            st.success("안정소비섹터가 선택되었습니다!")
    
    # 선택된 섹터 표시
    if st.session_state.choice_sector:
        st.markdown("---")
        st.markdown("### ✅ 선택된 투자 섹터")
        
        선택된섹터 = st.session_state.choice_sector
        for i, 섹터 in enumerate(선택된섹터):
            상대강도 = df_sector[df_sector["섹터"] == 섹터]["상대강도"].iloc[0] if 섹터 in df_sector["섹터"].values else 0
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{i+1}. {섹터}**")
            with col2:
                st.metric("상대강도", f"{상대강도:+.0f}%")
            with col3:
                if 상대강도 > 10:
                    st.success("강세")
                elif 상대강도 > 0:
                    st.info("보합")
                else:
                    st.warning("약세")
    
    # 다음 단계 버튼
    st.markdown("---")
    if st.session_state.choice_sector:
        if st.button("➡️ 다음 단계: 종목애널리스트", type="primary"):
            st.session_state.current_tab = 4
            st.rerun()
    else:
        st.warning("투자 섹터를 선택해주세요.")

def tab_analyst():
    """⑤ 종목 애널리스트 탭"""
    st.title("📈 종목애널리스트 — 개별 종목 분석")
    
    # 분석 기준 선택
    st.markdown("### 🎛️ 분석 기준 설정")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        저평가_switch = st.checkbox("💰 저평가 위주", value=True)
    with col2:
        안정성_switch = st.checkbox("🛡️ 안정성 위주", value=True)
    with col3:
        성장성_switch = st.checkbox("🚀 성장성 위주", value=False)
    
    st.markdown("---")
    
    # 선택된 섹터 기반 종목 데이터 생성 (더미)
    선택섹터 = st.session_state.choice_sector or ["AI/반도체", "로봇/자동화"]
    
    stock_data = {
        "종목명": ["삼성전자", "네이버", "레인보우로보틱스", "LG에너지솔루션", "카카오", "셀트리온"],
        "섹터": ["AI/반도체", "AI/반도체", "로봇/자동화", "2차전지", "AI/반도체", "바이오/헬스"],
        "시총": [450, 45, 6.5, 85, 25, 35],
        "현재가": [78000, 198000, 337000, 485000, 55000, 185000],
        "PER": [20.5, 34.0, 82.1, 28.5, 45.2, 25.8],
        "PBR": [2.1, 4.2, 5.2, 3.8, 3.5, 2.9],
        "RSI": [58, 62, 64, 45, 55, 72],
        "밴드대비": [2.6, 8.8, 16.2, -5.2, 12.1, 22.5]
    }
    
    df_stocks = pd.DataFrame(stock_data)
    
    # 선택된 섹터의 종목만 필터링
    if 선택섹터:
        df_filtered = df_stocks[df_stocks["섹터"].isin(선택섹터)]
    else:
        df_filtered = df_stocks
    
    st.markdown("### 📊 종목 분석 결과")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 선택 가능한 테이블 생성
        if not df_filtered.empty:
            st.markdown("#### 💼 추천 종목 리스트")
            
            # 각 종목에 대한 카드 형태로 표시
            for idx, row in df_filtered.iterrows():
                with st.container():
                    stock_col1, stock_col2, stock_col3, stock_col4 = st.columns([2, 1, 1, 1])
                    
                    with stock_col1:
                        st.markdown(f"**{row['종목명']}** ({row['섹터']})")
                        st.caption(f"시총: {format_money(row['시총']*1000000000000)} | 현재가: {row['현재가']:,}원")
                    
                    with stock_col2:
                        st.metric("PER", f"{row['PER']:.1f}배")
                    
                    with stock_col3:
                        st.metric("RSI", f"{row['RSI']:.0f}")
                    
                    with stock_col4:
                        밴드상태 = "과열" if row['밴드대비'] > 15 else "적정" if row['밴드대비'] > -10 else "과매도"
                        if 밴드상태 == "과열":
                            st.error(f"밴드: {row['밴드대비']:+.1f}%")
                        elif 밴드상태 == "과매도":
                            st.success(f"밴드: {row['밴드대비']:+.1f}%")
                        else:
                            st.info(f"밴드: {row['밴드대비']:+.1f}%")
                    
                    # 종목 담기 버튼
                    if st.button(f"📝 {row['종목명']} 포트폴리오에 담기", key=f"pick_{idx}"):
                        if row['종목명'] not in st.session_state.picks:
                            st.session_state.picks.append(row['종목명'])
                            st.success(f"{row['종목명']}이(가) 포트폴리오에 추가되었습니다!")
                        else:
                            st.warning(f"{row['종목명']}은(는) 이미 포트폴리오에 있습니다.")
                    
                    st.divider()
        else:
            st.warning("선택된 섹터의 종목이 없습니다.")
    
    with col2:
        st.markdown("#### 🎯 선택된 종목")
        
        if st.session_state.picks:
            for i, 종목 in enumerate(st.session_state.picks):
                # 해당 종목의 정보 가져오기
                종목정보 = df_stocks[df_stocks["종목명"] == 종목].iloc[0] if 종목 in df_stocks["종목명"].values else None
                
                if 종목정보 is not None:
                    with st.container():
                        st.markdown(f"**{i+1}. {종목}**")
                        
                        # 점수 계산 (더미)
                        저평가점수 = max(0, min(100, 100 - 종목정보['PER'] * 2))
                        안정성점수 = max(0, min(100, 100 - abs(종목정보['RSI'] - 50)))
                        기술점수 = max(0, min(100, 50 + 종목정보['밴드대비']))
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("저평가", f"{저평가점수:.0f}점")
                            st.metric("안정성", f"{안정성점수:.0f}점")
                        with col_b:
                            st.metric("기술점수", f"{기술점수:.0f}점")
                            
                            # 코멘트
                            if 종목정보['밴드대비'] > 15:
                                코멘트 = "밴드 상단, 단기 과열 유의"
                            elif 종목정보['밴드대비'] < -10:
                                코멘트 = "밴드 하단, 매수 기회 검토"
                            else:
                                코멘트 = "밴드 중간, 추세 관찰 필요"
                        
                        st.caption(f"💡 {코멘트}")
                        
                        # 제거 버튼
                        if st.button(f"❌ 제거", key=f"remove_{i}"):
                            st.session_state.picks.remove(종목)
                            st.rerun()
                        
                        st.divider()
        else:
            st.info("아직 선택된 종목이 없습니다.\n\n왼쪽에서 관심 종목을 포트폴리오에 담아보세요.")
        
        # 포트폴리오 초기화 버튼
        if st.session_state.picks:
            if st.button("🗑️ 포트폴리오 초기화", key="clear_picks"):
                st.session_state.picks = []
                st.rerun()
    
    # 다음 단계 버튼
    st.markdown("---")
    if st.session_state.picks:
        st.success(f"선택된 종목: {len(st.session_state.picks)}개")
        if st.button("➡️ 다음 단계: CIO전략실", type="primary"):
            st.session_state.current_tab = 5
            st.rerun()
    else:
        st.warning("포트폴리오에 종목을 추가해주세요.")

def generate_final_portfolio():
    """사용자 선택을 기반으로 최종 포트폴리오 생성"""
    
    # 기본 정보 추출
    사용자성향 = st.session_state.profile.get('성향', '중립형')
    거시선택 = st.session_state.choice_macro
    자산배분선택 = st.session_state.choice_alloc
    선택섹터 = st.session_state.choice_sector or []
    선택종목 = st.session_state.picks or []
    사용자자산 = st.session_state.profile.get("asset", 2000) * 10000  # 만원을 원으로 변환
    
    # 자산배분 매핑
    배분매핑 = {
        "방어형": {"채권": 45, "주식": 35, "현금": 15, "금": 5},
        "균형형": {"채권": 30, "주식": 55, "현금": 10, "금": 5},
        "공격형": {"채권": 15, "주식": 75, "현금": 5, "금": 5}
    }
    
    # 기본 배분 선택
    기본배분 = 배분매핑.get(자산배분선택, 배분매핑["균형형"])
    최종배분 = 기본배분.copy()
    
    # 거시 환경에 따른 조정
    if 거시선택 == "보수형":
        최종배분["채권"] = min(60, 최종배분["채권"] + 10)
        최종배분["주식"] = max(20, 최종배분["주식"] - 8)
        최종배분["현금"] = min(25, 최종배분["현금"] + 8)
    elif 거시선택 == "공격형":
        최종배분["주식"] = min(80, 최종배분["주식"] + 10)
        최종배분["채권"] = max(10, 최종배분["채권"] - 8)
        최종배분["현금"] = max(5, 최종배분["현금"] - 2)
    
    # 사용자 성향에 따른 미세 조정
    if 사용자성향 == "안정형" and 거시선택 != "보수형":
        최종배분["채권"] = min(50, 최종배분["채권"] + 5)
        최종배분["주식"] = max(30, 최종배분["주식"] - 5)
    elif 사용자성향 == "공격형" and 거시선택 != "공격형":
        최종배분["주식"] = min(75, 최종배분["주식"] + 5)
        최종배분["채권"] = max(15, 최종배분["채권"] - 5)
    
    # 정규화 (합계 100%)
    총합 = sum(최종배분.values())
    for k in 최종배분:
        최종배분[k] = round(최종배분[k] / 총합 * 100, 1)
    
    # 종목 선정 (선택된 종목들 우선, 없으면 섹터 기반)
    if 선택종목:
        핵심종목 = 선택종목[:5]  # 최대 5개
    else:
        # 섹터 기반 기본 종목
        기본종목 = []
        if "AI/반도체" in 선택섹터:
            기본종목.extend(["삼성전자", "네이버"])
        if "로봇/자동화" in 선택섹터:
            기본종목.append("레인보우로보틱스")
        if "2차전지" in 선택섹터:
            기본종목.append("LG에너지솔루션")
        if "바이오/헬스" in 선택섹터:
            기본종목.append("셀트리온")
        
        if not 기본종목:  # 선택된 섹터가 없으면 기본 우량주
            기본종목 = ["삼성전자", "LG에너지솔루션", "셀트리온"]
        
        핵심종목 = 기본종목[:5]
    
    # 수익률/위험도 계산
    주식비중 = 최종배분["주식"] / 100
    
    # 성향과 선택에 따른 리스크 계수
    리스크계수 = 1.0
    if 사용자성향 == "공격형":
        리스크계수 += 0.2
    elif 사용자성향 == "안정형":
        리스크계수 -= 0.2
    
    if 거시선택 == "공격형":
        리스크계수 += 0.1
    elif 거시선택 == "보수형":
        리스크계수 -= 0.1
    
    기대수익률 = (주식비중 * 0.12 * 리스크계수 + (1-주식비중) * 0.04)
    변동성 = (주식비중 * 0.25 * 리스크계수 + (1-주식비중) * 0.05)
    샤프비율 = 기대수익률 / 변동성 if 변동성 > 0 else 0
    
    # 투자 금액 계산
    자산별금액 = {}
    for 자산, 비중 in 최종배분.items():
        자산별금액[자산] = int(사용자자산 * 비중 / 100)
    
    return {
        "배분": 최종배분,
        "종목": 핵심종목,
        "수익률": 기대수익률,
        "위험도": 변동성,
        "샤프": 샤프비율,
        "투자금액": 자산별금액,
        "총자산": 사용자자산
    }

def tab_cio():
    """⑥ CIO 전략실 탭"""
    st.title("🏆 CIO전략실 — 맞춤형 최종 포트폴리오")
    
    st.markdown("### 🎯 당신만의 투자 포트폴리오가 완성되었습니다!")
    
    # 사용자 선택 요약
    with st.expander("📋 당신의 투자 여정 요약", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"**👤 투자자 프로필**\n• 자산: {st.session_state.profile.get('asset', 0)}만원\n• 성향: {st.session_state.profile.get('성향', '미선택')}\n• 시장: {st.session_state.profile.get('시장', '미선택')}")
        with col2:
            st.info(f"**📊 거시 분석**\n• 선택한 관점: {st.session_state.choice_macro or '미선택'}")
        with col3:
            st.info(f"**💰 자산 배분**\n• 선택한 전략: {st.session_state.choice_alloc or '미선택'}")
        with col4:
            섹터 = ', '.join(st.session_state.choice_sector[:2]) + ('...' if len(st.session_state.choice_sector) > 2 else '') if st.session_state.choice_sector else '미선택'
            종목수 = len(st.session_state.picks) if st.session_state.picks else 0
            st.info(f"**🎯 투자 대상**\n• 섹터: {섹터}\n• 선택 종목: {종목수}개")
    
    # 최종 포트폴리오 생성
    final_portfolio = generate_final_portfolio()
    
    st.markdown("---")
    
    # 메인 포트폴리오 카드
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💼 당신의 최종 투자 포트폴리오")
        
        # 포트폴리오 특성
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("예상 수익률", format_percent(final_portfolio['수익률']), help="연간 기대수익률")
        with col_b:
            st.metric("예상 변동성", format_percent(final_portfolio['위험도']), help="연간 변동성 (위험도)")
        with col_c:
            st.metric("샤프 비율", f"{final_portfolio['샤프']:.2f}", help="위험 대비 수익 효율성")
        
        st.markdown("---")
        
        # 자산 배분
        st.markdown("#### 📊 자산 배분 및 투자 금액")
        
        배분데이터 = []
        for 자산, 비중 in final_portfolio['배분'].items():
            금액 = final_portfolio['투자금액'][자산]
            배분데이터.append({
                "자산": 자산,
                "비중(%)": f"{비중}%",
                "투자금액": format_money(금액)
            })
        
        df_배분 = pd.DataFrame(배분데이터)
        st.dataframe(df_배분, width="stretch", hide_index=True)
        
        # 파이차트
        fig = go.Figure(data=[go.Pie(
            labels=list(final_portfolio['배분'].keys()),
            values=list(final_portfolio['배분'].values()),
            hole=0.4,
            textinfo='label+percent',
            textfont_size=12
        )])
        fig.update_layout(height=300, showlegend=True, title="자산 배분 비율")
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.markdown("### 🎯 핵심 종목 구성")
        
        if final_portfolio['종목']:
            for i, 종목 in enumerate(final_portfolio['종목'], 1):
                with st.container():
                    st.markdown(f"**{i}. {종목}**")
                    
                    # 종목별 간단한 정보 (더미)
                    if 종목 == "삼성전자":
                        st.caption("🏭 반도체 | 시총 1위 | 배당주")
                    elif 종목 == "네이버":
                        st.caption("💻 IT | 플랫폼 | 성장주")
                    elif 종목 == "레인보우로보틱스":
                        st.caption("🤖 로봇 | 혁신기업 | 테마주")
                    elif 종목 == "LG에너지솔루션":
                        st.caption("🔋 배터리 | 글로벌 | ESG")
                    elif 종목 == "셀트리온":
                        st.caption("💊 바이오 | 신약개발 | 성장")
                    else:
                        st.caption("📈 우량주")
                    
                    st.divider()
        else:
            st.info("선택된 종목이 없습니다.\n이전 단계에서 관심 종목을 선택해보세요.")
        
        st.markdown("### 🔥 투자 근거")
        
        # 동적 투자 근거 생성
        근거텍스트 = f"""
        **🎯 맞춤형 설계**
        • {st.session_state.profile.get('성향', '중립형')} 성향 반영
        • {st.session_state.choice_macro or '균형적'} 거시 관점 적용
        • {st.session_state.choice_alloc or '균형형'} 배분 전략 기반
        
        **📈 기대 효과**
        • 연간 {format_percent(final_portfolio['수익률'])} 수익 목표
        • {format_percent(final_portfolio['위험도'])} 변동성으로 리스크 관리
        • 샤프비율 {final_portfolio['샤프']:.2f}로 효율적 투자
        """
        
        if st.session_state.choice_sector:
            근거텍스트 += f"\n\n**🚀 선택 테마**\n• {', '.join(st.session_state.choice_sector)} 중심 구성"
        
        st.success(근거텍스트)
    
    
    # 최종 결정 및 요약
    st.markdown("---")
    st.markdown("### 🎊 포트폴리오 확정하기")
    
    사용자자산 = st.session_state.profile.get("asset", 2000)
    
    if st.button("✅ 이 포트폴리오로 확정하기", type="primary", width="stretch"):
        st.session_state.decision = "최종포트폴리오확정"
        
        # 최종 요약서
        with st.expander("📋 최종 투자 포트폴리오 확정서", expanded=True):
            st.markdown(f"""
            ## 🎯 {st.session_state.profile.get('성향', '중립형')} 투자자 맞춤 포트폴리오 확정
            
            **👤 투자자 정보**
            • 투자 가능 자산: {format_money(사용자자산 * 10000)}
            • 투자 성향: {st.session_state.profile.get('성향', '중립형')}
            • 선호 시장: {st.session_state.profile.get('시장', '국내')}
            
            **📊 최종 포트폴리오 성과 지표**
            • 예상 수익률: {format_percent(final_portfolio['수익률'])}
            • 예상 변동성: {format_percent(final_portfolio['위험도'])}
            • 샤프 비율: {final_portfolio['샤프']:.2f}
            
            **🎪 당신의 투자 여정**
            • 1단계 거시 관점: {st.session_state.choice_macro or '미선택'}
            • 2단계 자산배분: {st.session_state.choice_alloc or '미선택'}
            • 3단계 섹터 선택: {', '.join(st.session_state.choice_sector) if st.session_state.choice_sector else '미선택'}
            • 4단계 종목 선택: {len(st.session_state.picks)}개 종목 선정
            
            **� 최종 자산배분 및 투자금액**
            """)
            
            # 자산배분 표시
            for 자산, 비중 in final_portfolio['배분'].items():
                투자금액 = final_portfolio['투자금액'][자산]
                st.write(f"• **{자산} {비중}%**: {format_money(투자금액)}")
            
            st.markdown(f"""
            **🎯 핵심 투자 종목**
            """)
            
            # 종목 표시
            for i, 종목 in enumerate(final_portfolio['종목'], 1):
                st.write(f"{i}. {종목}")
            
            # 맞춤형 한줄 요약
            한줄요약 = f"당신의 {st.session_state.profile.get('성향', '중립형')} 성향과 {st.session_state.choice_alloc or '균형형'} 전략을 바탕으로 한 개인 맞춤형 포트폴리오"
            
            st.success(f"**💡 포트폴리오 요약**: {한줄요약}")
            
            st.balloons()  # 축하 효과
            st.success("🎉 포트폴리오가 성공적으로 확정되었습니다!")
    
    # 처음부터 다시 시작 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 새로운 포트폴리오 만들기"):
            # 모든 선택사항 초기화
            for key in list(st.session_state.keys()):
                if key.startswith(('choice_', 'profile', 'picks', 'decision')):
                    del st.session_state[key]
            st.session_state.current_tab = 0
            st.rerun()
    
    with col2:
        if st.button("� 포트폴리오 수정하기"):
            st.session_state.current_tab = 1  # 거시전략가부터 다시 시작
            st.rerun()

def main():
    """메인 애플리케이션"""
    
    # 세션 상태 초기화
    init_session_state()
    
    # 상단 제목
    st.title("🏦 AIA 2.0 — Dual-Team AI Investment Agency")
    st.markdown("**AI 역할 기반 투자 의사결정 플랫폼**")
    
    # 진행상황 표시바
    show_progress_bar()
    
    # 탭 네비게이션
    tab_names = ["🎯 인트로", "📊 거시전략가", "💰 자산배분가", "🔍 섹터리서처", "📈 종목애널리스트", "🏆 CIO전략실", "⚡ Trade Planner"]
    
    # 현재 탭에 따라 페이지 표시
    current_tab = st.session_state.current_tab
    
    # 상단 탭 네비게이션 (시각적 표시용)
    tab_cols = st.columns(7)
    for i, tab_name in enumerate(tab_names):
        with tab_cols[i]:
            if i == current_tab:
                st.success(f"**{tab_name}**")
            elif i < current_tab:
                st.info(tab_name)
            else:
                st.secondary_column if hasattr(st, 'secondary_column') else st.write(tab_name)
    
    st.markdown("---")
    
    # 탭별 컨텐츠 표시
    if current_tab == 0:
        tab_intro()
    elif current_tab == 1:
        tab_macro()
    elif current_tab == 2:
        tab_allocation()
    elif current_tab == 3:
        tab_sector()
    elif current_tab == 4:
        tab_analyst()
    elif current_tab == 5:
        tab_cio()
    elif current_tab == 6:
        tab_trade_planner()
    
    # 하단 네비게이션
    st.markdown("---")
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if current_tab > 0:
            if st.button("⬅️ 이전 단계", key="nav_prev"):
                st.session_state.current_tab = max(0, current_tab - 1)
                st.rerun()
    
    with nav_col2:
        progress = (current_tab + 1) / 7
        st.progress(progress, text=f"진행률: {progress*100:.0f}% ({current_tab + 1}/7 단계)")
    
    with nav_col3:
        if current_tab < 6:
            if st.button("다음 단계 ➡️", key="nav_next"):
                st.session_state.current_tab = min(6, current_tab + 1)
                st.rerun()

if __name__ == "__main__":
    main()

def tab_trade_planner():
    """Trade Planner - 모멘텀+RSI 기반 매수·매도 타이밍 및 전략 설정"""
    st.header("⚡ Trade Planner")
    st.markdown("**모멘텀 + RSI 지표 기반 단순하고 실용적인 매매 전략을 제시합니다**")
    
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
    
    # CIO에서 확정된 포트폴리오가 있는지 확인
    if 'final_portfolio' not in st.session_state or st.session_state.final_portfolio is None:
        st.warning("⚠️ 먼저 CIO전략실에서 포트폴리오를 확정해주세요.")
        return
    
    final_portfolio = st.session_state.final_portfolio
    
    # 포트폴리오 요약 카드
    with st.container():
        st.markdown("### 📊 확정된 포트폴리오 요약")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 투자금액", format_money(sum(final_portfolio['투자금액'].values())))
        with col2:
            st.metric("예상 수익률", format_percent(final_portfolio['수익률']))
        with col3:
            st.metric("예상 변동성", format_percent(final_portfolio['위험도']))
        with col4:
            st.metric("샤프 비율", f"{final_portfolio['샤프']:.2f}")
    
    st.markdown("---")
    
    # 전체 투자 전략 설정
    st.markdown("### 🎯 전체 투자 실행 전략")
    
    col1, col2 = st.columns(2)
    
    with col1:
        투자방식 = st.selectbox(
            "투자 실행 방식",
            ["일시불 투자", "분할 매수 (DCA)", "하락시 점진 매수", "기술적 타이밍"],
            help="포트폴리오 전체를 어떤 방식으로 구축할지 선택하세요"
        )
        
        실행기간 = st.selectbox(
            "투자 실행 기간",
            ["즉시 실행", "1주일 내", "1개월 내", "3개월 내", "6개월 내"],
            help="전체 포트폴리오 구축을 완료할 기간을 설정하세요"
        )
    
    with col2:
        리밸런싱주기 = st.selectbox(
            "리밸런싱 주기",
            ["분기별 (3개월)", "반기별 (6개월)", "연간 (12개월)", "편차 20% 도달시", "시장 상황 변화시"],
            help="포트폴리오 비중을 재조정할 주기를 설정하세요"
        )
        
        위험관리방식 = st.selectbox(
            "위험 관리 방식",
            ["스톱로스 -20%", "스톱로스 -15%", "시장상황 모니터링", "장기 보유", "변동성 기준 조정"],
            help="손실 제한 및 위험 관리 방식을 선택하세요"
        )
    
    st.markdown("---")
    
    # 자산별 상세 트레이드 플랜
    st.markdown("### 📈 자산별 트레이드 플랜")
    
    for 자산, 비중 in final_portfolio['배분'].items():
        if 비중 > 0:
            투자금액 = final_portfolio['투자금액'][자산]
            
            with st.expander(f"💰 {자산} ({비중}% | {format_money(투자금액)})", expanded=True):
                
                # 자산별 특성에 따른 전략 제안
                if "주식" in 자산 or "ETF" in 자산:
                    매수전략 = generate_stock_trade_plan(자산, 투자금액, 투자방식)
                elif "채권" in 자산:
                    매수전략 = generate_bond_trade_plan(자산, 투자금액, 투자방식)
                elif "현금" in 자산:
                    매수전략 = generate_cash_trade_plan(자산, 투자금액)
                else:
                    매수전략 = generate_default_trade_plan(자산, 투자금액, 투자방식)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 매수 전략**")
                    for step in 매수전략['매수단계']:
                        st.write(f"• {step}")
                    
                    st.markdown("**⏰ 타이밍 신호**")
                    for signal in 매수전략['타이밍신호']:
                        st.write(f"• {signal}")
                
                with col2:
                    st.markdown("**💡 매도 조건**")
                    for condition in 매수전략['매도조건']:
                        st.write(f"• {condition}")
                    
                    st.markdown("**⚠️ 위험 신호**")
                    for risk in 매수전략['위험신호']:
                        st.write(f"• {risk}")
                
                # 분할매수 스케줄이 있는 경우
                if '분할스케줄' in 매수전략:
                    st.markdown("**📅 분할 매수 스케줄**")
                    스케줄_df = pd.DataFrame(매수전략['분할스케줄'])
                    st.dataframe(스케줄_df, width="stretch")
    
    st.markdown("---")
    
    # 종목별 상세 트레이드 플랜 (사용자가 선택한 종목들)
    if hasattr(st.session_state, 'picks') and st.session_state.picks:
        st.markdown("### 🎯 선별 종목별 상세 전략")
        
        for 종목코드 in st.session_state.picks:
            종목정보 = get_stock_info(종목코드)
            
            with st.expander(f"📈 {종목정보['name']} ({종목코드})", expanded=False):
                
                # 현재 기술적 분석 상태
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    현재가 = 종목정보.get('price', 50000 + np.random.randint(-10000, 10000))
                    st.metric("현재가", format_money(현재가))
                    
                    RSI = 종목정보.get('RSI', 50 + np.random.randint(-30, 30))
                    if RSI > 70:
                        rsi_status = "🔴 과매수"
                    elif RSI < 30:
                        rsi_status = "🟢 과매도"
                    else:
                        rsi_status = "� 중립"
                    st.metric("RSI 지표", f"{RSI:.1f}", help=rsi_status)
                
                with col2:
                    # 단순 모멘텀 계산 (20일 이동평균 기준)
                    이동평균20 = 현재가 * (0.95 + np.random.random() * 0.1)
                    ma20_momentum = ((현재가 - 이동평균20) / 이동평균20) * 100
                    
                    momentum_color = "🟢" if ma20_momentum > 0 else "🔴"
                    st.metric("20일선 모멘텀", f"{ma20_momentum:+.1f}%", help=f"{momentum_color} {'상승' if ma20_momentum > 0 else '하락'} 추세")
                    
                    # 모멘텀 강도
                    if abs(ma20_momentum) > 10:
                        momentum_strength = "강함"
                    elif abs(ma20_momentum) > 5:
                        momentum_strength = "보통"
                    else:
                        momentum_strength = "약함"
                    st.metric("모멘텀 강도", momentum_strength)
                
                with col3:
                    # 60일 장기 모멘텀
                    이동평균60 = 현재가 * (0.90 + np.random.random() * 0.2)
                    ma60_momentum = ((현재가 - 이동평균60) / 이동평균60) * 100
                    
                    long_momentum_color = "🟢" if ma60_momentum > 0 else "🔴"
                    st.metric("60일선 모멘텀", f"{ma60_momentum:+.1f}%", help=f"{long_momentum_color} 장기 추세")
                    
                    # 전체 신호 계산
                    signal_score = calculate_momentum_rsi_signal(RSI, ma20_momentum, ma60_momentum)
                    if signal_score >= 70:
                        signal_status = "🟢 강한 매수"
                    elif signal_score >= 40:
                        signal_status = "🟡 보통 매수"
                    else:
                        signal_status = "🔴 대기/매도"
                    st.metric("종합 신호", signal_status)
                
                # 매수/매도 시그널 및 전략
                매수신호점수 = calculate_momentum_rsi_signal(RSI, ma20_momentum, ma60_momentum)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 모멘텀+RSI 매수 전략**")
                    
                    if 매수신호점수 >= 70:
                        st.success("🟢 **강한 매수 신호**")
                        st.write("• RSI 과매도 + 모멘텀 상승 확인")
                        st.write("• 즉시 50% 물량 매수")
                        st.write("• 추가 하락시 30% 물량 추가")
                        st.write("• 모멘텀 전환 확인시 20% 마지막 매수")
                    elif 매수신호점수 >= 40:
                        st.info("🟡 **보통 매수 신호**")
                        st.write("• RSI 중립 + 약한 모멘텀 상승")
                        st.write("• 30% 물량 우선 매수")
                        st.write("• RSI 30 이하 진입시 40% 추가")
                        st.write("• 모멘텀 강화시 30% 추가 매수")
                    else:
                        st.warning("🔴 **매수 대기**")
                        st.write("• RSI 과매수 or 모멘텀 하락")
                        st.write("• 현재는 매수 관망 필요")
                        st.write("• RSI 30 이하 + 모멘텀 전환 대기")
                        st.write("• 기술적 반등 신호 확인 후 진입")
                
                with col2:
                    st.markdown("**💡 모멘텀 기반 매도 전략**")
                    
                    # 목표 수익률을 모멘텀 강도에 따라 조정
                    if ma20_momentum > 10:
                        목표수익률 = 25  # 강한 상승 모멘텀
                    elif ma20_momentum > 5:
                        목표수익률 = 20  # 보통 상승 모멘텀
                    elif ma20_momentum > 0:
                        목표수익률 = 15  # 약한 상승 모멘텀
                    else:
                        목표수익률 = 10  # 하락 모멘텀
                    
                    손절가 = 현재가 * 0.85
                    목표가 = 현재가 * (1 + 목표수익률/100)
                    
                    st.write(f"• **목표가**: {format_money(목표가)} (+{목표수익률}%)")
                    st.write(f"• **손절가**: {format_money(손절가)} (-15%)")
                    st.write("• RSI 70 이상 + 모멘텀 둔화시 50% 매도")
                    st.write("• RSI 80 이상시 추가 30% 매도")
                    st.write("• 모멘텀 하락 전환시 전량 매도 검토")
                
                # 주간/월간 모니터링 포인트
                st.markdown("**📅 모멘텀+RSI 모니터링 일정**")
                
                모니터링_df = pd.DataFrame({
                    '주기': ['매일 장마감 후', '매주 월요일', '매월 첫째주', '분기별'],
                    '체크포인트': [
                        'RSI 지표 + 20일선 모멘텀 확인',
                        '60일선 장기 모멘텀 추세 점검',
                        '모멘텀 전환점 및 매매 타이밍 재조정',
                        '전체 포지션 리뷰 및 전략 수정'
                    ],
                    '매수 조건': [
                        'RSI < 40 + 모멘텀 상승 전환',
                        'RSI < 30 + 20일선 골든크로스',  
                        '장기 하락 후 모멘텀 반등 신호',
                        '시장 사이클 변화에 따른 재진입'
                    ],
                    '매도 조건': [
                        'RSI > 70 + 모멘텀 둔화',
                        'RSI > 80 or 20일선 데드크로스',
                        '목표 수익률 달성 + 모멘텀 피크',
                        '장기 모멘텀 하락 전환 확인'
                    ]
                })
                
                st.dataframe(모니터링_df, width="stretch")
    
    st.markdown("---")
    
    # 전체 포트폴리오 실행 캘린더
    st.markdown("### 📅 투자 실행 캘린더")
    
    if 투자방식 == "분할 매수 (DCA)":
        generate_dca_calendar(final_portfolio, 실행기간)
    elif 투자방식 == "하락시 점진 매수":
        generate_dip_buying_calendar(final_portfolio)
    elif 투자방식 == "기술적 타이밍":
        generate_technical_calendar(final_portfolio)
    else:
        generate_lump_sum_calendar(final_portfolio)
    
    st.markdown("---")
    
    # 트레이딩 체크리스트
    st.markdown("### ✅ 트레이딩 실행 체크리스트")
    
    체크리스트 = [
        "증권계좌 투자금 입금 완료",
        "각 자산별 매수 주문 가격 설정",
        "손절/목표가 주문 등록",
        "분할매수 일정 캘린더 등록",
        "포트폴리오 모니터링 알림 설정",
        "리밸런싱 주기 알림 설정",
        "시장 뉴스 모니터링 채널 구독",
        "비상시 연락처 및 대응방안 준비"
    ]
    
    for i, 항목 in enumerate(체크리스트):
        st.checkbox(항목, key=f"checklist_{i}")
    
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

def generate_stock_trade_plan(자산명, 투자금액, 투자방식):
    """주식/ETF 모멘텀+RSI 기반 매매 전략 생성"""
    if 투자방식 == "분할 매수 (DCA)":
        return {
            '매수단계': [
                "1차: RSI 50 이하 + 모멘텀 중립시 40% 매수",
                "2차: RSI 40 이하 + 모멘텀 상승시 30% 추가", 
                "3차: RSI 30 이하 + 모멘텀 강화시 20% 추가",
                "4차: RSI 20 이하 극과매도시 10% 마지막 매수"
            ],
            '타이밍신호': [
                "RSI 30-40 구간 + 20일선 모멘텀 상승",
                "RSI 과매도 + 60일선 지지 확인",
                "단기 모멘텀 반등 + 장기 추세 유지",
                "거래량 증가와 함께 RSI 상승"
            ],
            '매도조건': [
                "RSI 70 이상 + 모멘텀 둔화시 50% 매도",
                "RSI 80 이상시 30% 추가 매도",
                "모멘텀 하락 전환 + RSI 피크시 매도 고려",
                "장기 모멘텀 하락시 전량 매도"
            ],
            '위험신호': [
                "RSI 과매수 + 모멘텀 급격한 둔화",
                "20일선 데드크로스 + RSI 하락",
                "거래량 급증과 함께 RSI 급락",
                "장기 모멘텀 하락 전환 신호"
            ],
            '분할스케줄': [
                {'주차': '1주차', '비중': '40%', '금액': format_money(투자금액 * 0.4), '조건': 'RSI 50↓ + 모멘텀 중립'},
                {'주차': '2주차', '비중': '30%', '금액': format_money(투자금액 * 0.3), '조건': 'RSI 40↓ + 모멘텀 상승'},
                {'주차': '3-4주차', '비중': '20%', '금액': format_money(투자금액 * 0.2), '조건': 'RSI 30↓ + 모멘텀 강화'},
                {'주차': '5-8주차', '비중': '10%', '금액': format_money(투자금액 * 0.1), '조건': 'RSI 20↓ 극과매도'}
            ]
        }
    else:
        return {
            '매수단계': [
                "RSI + 모멘텀 복합신호 확인 후 일시불 매수",
                "매수 즉시 RSI 80 손절라인 설정",
                "모멘텀 지속성 확인하여 포지션 유지"
            ],
            '타이밍신호': [
                "RSI 30-40 구간 + 모멘텀 상승 전환",
                "20일선 골든크로스 + RSI 상승",
                "거래량 폭증 + RSI 과매도 탈출",
                "장기 모멘텀 지지 + 단기 반등"
            ],
            '매도조건': [
                "RSI 70 이상 + 모멘텀 피크 확인",
                "20일선 데드크로스 + RSI 하락",
                "목표 수익률 달성 + 모멘텀 둔화",
                "RSI 80 이상 강제 손절"
            ],
            '위험신호': [
                "RSI 급락 + 모멘텀 급속 하락",
                "거래량 폭증과 함께 RSI 과매수",
                "장기 모멘텀 하락 전환",
                "시장 전체 RSI 과열 신호"
            ]
        }

def generate_bond_trade_plan(자산명, 투자금액, 투자방식):
    """채권 매매 전략 생성"""
    return {
        '매수단계': [
            "금리 상승 국면에서 단계별 매수",
            "듀레이션 리스크 고려한 분산 매수",
            "만기별 래더링 전략 적용"
        ],
        '타이밍신호': [
            "중앙은행 통화정책 변화",
            "국채 금리 상승 추세",
            "신용 스프레드 확대",
            "인플레이션 지표 안정화"
        ],
        '매도조건': [
            "금리 하락 국면 진입",
            "만기 1년 이내 도달",
            "신용 등급 하향",
            "더 좋은 대안 발생"
        ],
        '위험신호': [
            "급격한 금리 변동",
            "발행기관 신용도 악화",
            "유동성 부족 현상",
            "통화정책 불확실성 증가"
        ]
    }

def generate_cash_trade_plan(자산명, 투자금액):
    """현금성 자산 관리 전략"""
    return {
        '매수단계': [
            "고금리 예적금 우선 배치",
            "CMA/MMF 등 유동성 자산 활용",
            "단기 채권형 펀드 고려"
        ],
        '타이밍신호': [
            "시장 불확실성 증가",
            "투자 기회 대기",
            "금리 상승 국면",
            "포트폴리오 리밸런싱 필요"
        ],
        '매도조건': [
            "매력적인 투자 기회 발생",
            "금리 하락 전환점",
            "자산 재배분 필요",
            "긴급 자금 필요"
        ],
        '위험신호': [
            "인플레이션 급상승",
            "금리 급락",
            "통화 가치 하락",
            "기회비용 증가"
        ]
    }

def generate_default_trade_plan(자산명, 투자금액, 투자방식):
    """기본 매매 전략 생성"""
    return {
        '매수단계': [
            "시장 상황 분석 후 매수",
            "리스크 관리 하에 진입",
            "분산 투자 원칙 적용"
        ],
        '타이밍신호': [
            "기술적 지표 호전",
            "펀더멘털 개선",
            "시장 심리 회복",
            "거시 환경 안정"
        ],
        '매도조건': [
            "목표 수익률 달성",
            "투자 논리 변화",
            "리스크 증가",
            "더 나은 기회 발생"
        ],
        '위험신호': [
            "예상치 못한 변수",
            "시장 구조 변화",
            "유동성 위기",
            "시스템 리스크"
        ]
    }

def calculate_momentum_rsi_signal(rsi, ma20_momentum, ma60_momentum):
    """단순 모멘텀 + RSI 기반 매매 신호 계산"""
    score = 0
    
    # RSI 신호 (50% 가중치)
    if rsi < 30:
        score += 50  # 강한 매수
    elif rsi < 40:
        score += 30  # 보통 매수  
    elif rsi < 50:
        score += 10  # 약한 매수
    elif rsi > 70:
        score -= 30  # 매도 신호
    elif rsi > 80:
        score -= 50  # 강한 매도
    
    # 단기 모멘텀 신호 (30% 가중치)
    if ma20_momentum > 5:
        score += 30
    elif ma20_momentum > 0:
        score += 15
    elif ma20_momentum < -5:
        score -= 20
    elif ma20_momentum < -10:
        score -= 30
    
    # 장기 모멘텀 신호 (20% 가중치)
    if ma60_momentum > 10:
        score += 20
    elif ma60_momentum > 0:
        score += 10
    elif ma60_momentum < -10:
        score -= 15
    elif ma60_momentum < -20:
        score -= 25
    
    return max(0, min(100, score))

def calculate_buy_signal_score(rsi, bollinger_position, ma20_diff, ma60_diff):
    """단순 모멘텀 + RSI 기반 매수 신호 점수 계산 (0-100)"""
    score = 50  # 기본 점수
    
    # RSI 기반 점수 (가중치 40%)
    if rsi < 30:
        rsi_score = 40  # 강한 매수 신호
    elif rsi < 40:
        rsi_score = 25  # 보통 매수 신호
    elif rsi < 50:
        rsi_score = 10  # 약한 매수 신호
    elif rsi > 70:
        rsi_score = -30  # 매도 신호
    elif rsi > 80:
        rsi_score = -50  # 강한 매도 신호
    else:
        rsi_score = 0  # 중립
    
    # 모멘텀 기반 점수 (가중치 60%)
    momentum_score = 0
    
    # 20일선 모멘텀 (30% 가중치)
    if ma20_diff > 5:
        momentum_score += 20
    elif ma20_diff > 0:
        momentum_score += 10
    elif ma20_diff < -5:
        momentum_score -= 15
    elif ma20_diff < -10:
        momentum_score -= 25
    
    # 60일선 모멘텀 (30% 가중치)  
    if ma60_diff > 10:
        momentum_score += 20
    elif ma60_diff > 0:
        momentum_score += 10
    elif ma60_diff < -10:
        momentum_score -= 15
    elif ma60_diff < -20:
        momentum_score -= 25
    
    # 최종 점수 계산
    final_score = score + rsi_score + momentum_score
    
    return max(0, min(100, final_score))

def generate_dca_calendar(portfolio, 실행기간):
    """DCA 실행 캘린더 생성"""
    st.markdown("**분할 매수 일정표**")
    
    if 실행기간 == "1주일 내":
        periods = 7
        interval = "일"
    elif 실행기간 == "1개월 내":
        periods = 4
        interval = "주"
    elif 실행기간 == "3개월 내":
        periods = 12
        interval = "주"
    else:
        periods = 6
        interval = "월"
    
    # 분할 매수 스케줄 생성
    today = pd.Timestamp.now()
    dates = pd.date_range(start=today, periods=periods+1, freq='W' if interval == "주" else 'D' if interval == "일" else 'M')[1:]
    
    총투자금 = sum(portfolio['투자금액'].values())
    회차별금액 = 총투자금 / periods
    
    calendar_data = []
    for i, date in enumerate(dates):
        calendar_data.append({
            '일정': date.strftime('%Y-%m-%d (%a)'),
            f'{interval}차': f"{i+1}/{periods}",
            '투자금액': format_money(회차별금액),
            '누적금액': format_money(회차별금액 * (i+1)),
            '비고': f"전체 포트폴리오 {100/periods:.1f}% 매수"
        })
    
    calendar_df = pd.DataFrame(calendar_data)
    st.dataframe(calendar_df, width="stretch")

def generate_dip_buying_calendar(portfolio):
    """하락매수 조건표 생성"""
    st.markdown("**하락매수 조건표**")
    
    조건_data = [
        {'하락폭': '-5%', '매수비중': '30%', '대상': '안정적 대형주/ETF', '조건': 'RSI 40 이하'},
        {'하락폭': '-10%', '매수비중': '40%', '대상': '전체 포트폴리오', '조건': '볼린저밴드 하단'},
        {'하락폭': '-15%', '매수비중': '20%', '대상': '성장주 위주', '조건': 'RSI 30 이하'},
        {'하락폭': '-20%', '매수비중': '10%', '대상': '전략적 기회', '조건': '공포지수 최고점'}
    ]
    
    조건_df = pd.DataFrame(조건_data)
    st.dataframe(조건_df, width="stretch")

def generate_technical_calendar(portfolio):
    """모멘텀+RSI 기반 기술적 분석 체크포인트"""
    st.markdown("**모멘텀+RSI 기술적 분석 체크포인트**")
    
    체크포인트_data = [
        {
            '주기': '매일 장마감 후', 
            '체크항목': 'RSI 지표 + 20일선 모멘텀', 
            '매수 조건': 'RSI < 40 + 모멘텀 상승',
            '매도 조건': 'RSI > 70 + 모멘텀 둔화',
            '액션': '단기 매매 신호 확인'
        },
        {
            '주기': '매주 월요일', 
            '체크항목': '60일선 장기 모멘텀 + RSI 추세', 
            '매수 조건': 'RSI < 30 + 장기 모멘텀 지지',
            '매도 조건': 'RSI > 80 + 장기 모멘텀 하락',
            '액션': '주간 트렌드 방향성 확인'
        },
        {
            '주기': '매월 첫째주', 
            '체크항목': '월간 모멘텀 사이클 + RSI 패턴', 
            '매수 조건': '월간 RSI 바닥권 + 모멘텀 전환',
            '매도 조건': '월간 RSI 고점 + 모멘텀 피크',
            '액션': '중기 포지션 재조정'
        },
        {
            '주기': '분기별', 
            '체크항목': '장기 모멘텀 사이클 + RSI 매크로', 
            '매수 조건': '분기 RSI 저점 + 모멘텀 사이클 전환',
            '매도 조건': '분기 RSI 고점 + 모멘텀 사이클 피크',
            '액션': '전체 포트폴리오 리밸런싱'
        }
    ]
    
    체크포인트_df = pd.DataFrame(체크포인트_data)
    st.dataframe(체크포인트_df, width="stretch")

def generate_lump_sum_calendar(portfolio):
    """일시불 투자 체크리스트"""
    st.markdown("**일시불 투자 실행 체크리스트**")
    
    체크리스트_data = [
        {'순서': '1단계', '항목': '시장 상황 최종 점검', '완료': False},
        {'순서': '2단계', '항목': '포트폴리오 배분 확인', '완료': False},
        {'순서': '3단계', '항목': '매수 주문 일괄 실행', '완료': False},
        {'순서': '4단계', '항목': '손절/목표가 설정', '완료': False},
        {'순서': '5단계', '항목': '모니터링 알림 설정', '완료': False}
    ]
    
    체크리스트_df = pd.DataFrame(체크리스트_data)
    st.dataframe(체크리스트_df, width="stretch")