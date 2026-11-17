import html
import json
import os
import random
import re
import sys
import uuid
import winsound
from datetime import datetime, date, timedelta
import calendar
import requests

from PyQt6.QtCore import (
    Qt, QTimer, QTime, QDate, QPoint, QRectF, QThread, pyqtSignal, QSize
)
from PyQt6.QtGui import (
    QColor, QFont, QPainter, QPainterPath, QPen, QBrush, QCursor, QAction,
    QTextCharFormat, QTextCursor
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QLineEdit, QTextEdit, QListWidget,
    QListWidgetItem, QStackedWidget, QComboBox, QCheckBox, QSpinBox,
    QFrame, QGridLayout, QScrollArea, QSizePolicy, QMessageBox,
    QGraphicsDropShadowEffect, QDateEdit
)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "widget_data.json")

KOREAN_DAYS = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
SHORT_WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]
SHORT_DAYS = ["일", "월", "화", "수", "목", "금", "토"]

CITIES = {
    "경남 창원": (35.2280, 128.6811),
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "인천": (37.4563, 126.7052),
    "대구": (35.8714, 128.6014),
    "대전": (36.3504, 127.3845),
    "광주": (35.1595, 126.8526),
    "수원": (37.2636, 127.0286),
    "성남": (37.4200, 127.1267),
    "울산": (35.5384, 129.3114),
    "제주": (33.4996, 126.5312),
}

WEATHER_CODES = {
    0: ("☀️", "맑음"),
    1: ("🌤️", "대체로 맑음"),
    2: ("⛅", "구름 조금"),
    3: ("☁️", "흐림"),
    45: ("🌫️", "안개"),
    48: ("🌫️", "짙은 안개"),
    51: ("🌦️", "약한 이슬비"),
    53: ("🌦️", "이슬비"),
    55: ("🌧️", "강한 이슬비"),
    61: ("🌧️", "약한 비"),
    63: ("🌧️", "비"),
    65: ("🌧️", "강한 비"),
    71: ("🌨️", "약한 눈"),
    73: ("❄️", "눈"),
    75: ("❄️", "강한 눈"),
    77: ("🌨️", "싸라기눈"),
    80: ("🌦️", "소나기"),
    81: ("🌧️", "강한 소나기"),
    82: ("⛈️", "폭우"),
    85: ("🌨️", "눈보라"),
    86: ("❄️", "강한 눈보라"),
    95: ("⛈️", "뇌우"),
    96: ("⛈️", "우박 동반 뇌우"),
    99: ("⛈️", "강한 뇌우"),
}

MEMO_COLORS = [
    {"name": "옐로우", "bg": "#2B2618", "border": "#F59E0B", "text": "#FEF3C7"},
    {"name": "민트", "bg": "#132A26", "border": "#10B981", "text": "#D1FAE5"},
    {"name": "블루", "bg": "#152238", "border": "#3B82F6", "text": "#DBEAFE"},
    {"name": "핑크", "bg": "#2D1625", "border": "#EC4899", "text": "#FCE7F3"},
    {"name": "퍼플", "bg": "#221736", "border": "#8B5CF6", "text": "#EDE9FE"},
]

OPIC_SENTENCES = [
    {
        "category": "💼 직장/업무",
        "en": "To be honest, I have a lot on my plate at work these days.",
        "ko": "솔직히 요즘 회사에서 처리해야 할 업무가 정말 많습니다."
    },
    {
        "category": "💼 직장/업무",
        "en": "My main responsibility is managing automated logistics projects.",
        "ko": "제 주요 담당 업무는 물류 자동화 프로젝트를 관리하는 것입니다."
    },
    {
        "category": "💼 직장/업무",
        "en": "Whenever a problem comes up, I try to figure it out right away.",
        "ko": "문제가 생길 때마다 저는 즉시 해결책을 찾으려고 노력합니다."
    },
    {
        "category": "💼 직장/업무",
        "en": "We had a tight deadline, so everyone worked overtime to finish it.",
        "ko": "마감 기한이 촉박해서 모두 야근하며 작업을 끝냈습니다."
    },
    {
        "category": "💼 직장/업무",
        "en": "I usually check my emails first thing in the morning at the office.",
        "ko": "저는 보통 출근하자마자 아침 제일 먼저 이메일을 확인합니다."
    },
    {
        "category": "💡 만능 표현 (IH/AL)",
        "en": "Speaking of my daily routine, it varies depending on my schedule.",
        "ko": "제 일상 루틴을 말씀드리자면, 일정에 따라 조금씩 달라집니다."
    },
    {
        "category": "💡 만능 표현 (IH/AL)",
        "en": "If my memory serves me right, it happened about two years ago.",
        "ko": "제 기억이 맞다면, 그 일은 약 2년 전에 있었던 일입니다."
    },
    {
        "category": "💡 만능 표현 (IH/AL)",
        "en": "Looking back, it was one of the most memorable experiences of my life.",
        "ko": "돌이켜보면, 제 인생에서 가장 기억에 남는 경험 중 하나였습니다."
    },
    {
        "category": "💡 만능 표현 (IH/AL)",
        "en": "To make a long story short, everything turned out great in the end.",
        "ko": "긴 이야기를 짧게 줄이자면, 결국 모든 것이 아주 잘 해결되었습니다."
    },
    {
        "category": "💡 만능 표현 (IH/AL)",
        "en": "What I like most about my job is working with talented coworkers.",
        "ko": "제 직업에서 가장 마음에 드는 점은 유능한 동료들과 함께 일하는 것입니다."
    },
    {
        "category": "🏖️ 여가/일상",
        "en": "On weekends, I prefer staying at home to recharge my batteries.",
        "ko": "주말에는 에너지를 재충전하기 위해 집에서 쉬는 것을 선호합니다."
    },
    {
        "category": "🏖️ 여가/일상",
        "en": "After a long day at work, nothing beats watching a movie on the couch.",
        "ko": "긴 하루 일과를 마친 후에는 소파에서 영화 보는 것만한 게 없습니다."
    },
    {
        "category": "🏖️ 여가/일상",
        "en": "Whenever I get stressed out, I go for a walk to clear my head.",
        "ko": "스트레스를 받을 때마다 머리를 식히러 산책을 나갑니다."
    },
    {
        "category": "🏃 건강/운동",
        "en": "I have been into working out lately to stay in good shape.",
        "ko": "최근에는 건강과 체력을 유지하기 위해 운동에 푹 빠져 있습니다."
    },
    {
        "category": "✈️ 여행/출장",
        "en": "I went on a business trip abroad last month, and it was quite hectic.",
        "ko": "지난달에 해외 출장을 다녀왔는데 일정이 꽤 바쁘고 정신없었습니다."
    },
    {
        "category": "✈️ 여행/출장",
        "en": "Before going on a trip, I always check the weather forecast in advance.",
        "ko": "여행을 떠나기 전에 저는 항상 일기예보를 미리 확인합니다."
    },
    {
        "category": "🎭 롤플레이",
        "en": "Could you let me know if there is any way to reschedule my appointment?",
        "ko": "예약 일정을 변경할 수 있는 방법이 있는지 알려주시겠어요?"
    },
    {
        "category": "🎭 롤플레이",
        "en": "I am really sorry, but something urgent just came up at work.",
        "ko": "정말 죄송하지만, 방금 회사에 급한 일이 생겼습니다."
    },
    {
        "category": "⚡ 돌발/문제해결",
        "en": "At first, I had no idea what to do, so I asked my coworker for help.",
        "ko": "처음에는 어떻게 해야 할지 몰라서 동료에게 도움을 요청했습니다."
    },
    {
        "category": "⚡ 돌발/기술",
        "en": "Thanks to smartphones, we can take care of almost everything on the go.",
        "ko": "스마트폰 덕분에 이동 중에도 거의 모든 일을 처리할 수 있습니다."
    },
]


class WeatherWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, city_name: str):
        super().__init__()
        self.city_name = city_name

    def run(self):
        lat, lon = CITIES.get(self.city_name, CITIES["경남 창원"])
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min"
            f"&timezone=Asia%2FSeoul&past_days=1&forecast_days=7"
        )
        try:
            resp = requests.get(url, timeout=6)
            resp.raise_for_status()
            data = resp.json()
            current = data.get("current", {})
            daily = data.get("daily", {})

            temp = current.get("temperature_2m", 0.0)
            humidity = current.get("relative_humidity_2m", 0)
            code = current.get("weather_code", 0)
            icon, desc = WEATHER_CODES.get(code, ("🌤️", "보통"))

            times = daily.get("time", [])
            d_codes = daily.get("weather_code", [])
            d_maxs = daily.get("temperature_2m_max", [])
            d_mins = daily.get("temperature_2m_min", [])

            daily_map = {}
            for idx, d_str in enumerate(times):
                c_val = d_codes[idx] if idx < len(d_codes) else 0
                d_icon, d_desc = WEATHER_CODES.get(c_val, ("🌤️", "보통"))
                hi = round(d_maxs[idx], 1) if idx < len(d_maxs) else round(temp, 1)
                lo = round(d_mins[idx], 1) if idx < len(d_mins) else round(temp, 1)
                daily_map[d_str] = {
                    "date": d_str,
                    "icon": d_icon,
                    "desc": d_desc,
                    "max": hi,
                    "min": lo,
                }

            today_dt = datetime.now().date()
            today_str = today_dt.strftime("%Y-%m-%d")
            today_info = daily_map.get(today_str, {"max": round(temp, 1), "min": round(temp, 1)})

            sat_dt = today_dt + timedelta(days=(5 - today_dt.weekday()))
            sun_dt = today_dt + timedelta(days=(6 - today_dt.weekday()))
            sat_info = daily_map.get(sat_dt.strftime("%Y-%m-%d"))
            sun_info = daily_map.get(sun_dt.strftime("%Y-%m-%d"))

            self.finished.emit({
                "ok": True,
                "city": self.city_name,
                "temp": round(temp, 1),
                "humidity": humidity,
                "icon": icon,
                "desc": desc,
                "max": today_info["max"],
                "min": today_info["min"],
                "sat": sat_info,
                "sun": sun_info,
                "daily_map": daily_map,
            })
        except Exception as e:
            self.finished.emit({
                "ok": False,
                "error": str(e),
            })


def parse_korean_time_from_line(line: str) -> str:
    # 1) 오전/오후 HH:MM
    m_colon = re.search(
        r"(오전|오후|아침|저녁|낮|밤|AM|PM|am|pm)?\s*(\d{1,2})\s*:\s*(\d{2})(?!\s*:\d{2})",
        line
    )
    if m_colon:
        ampm = (m_colon.group(1) or "").strip().lower()
        hh = int(m_colon.group(2))
        mm = int(m_colon.group(3))
        if 0 <= hh <= 23 and 0 <= mm <= 59:
            if ampm in ("오후", "저녁", "밤", "pm", "낮") and hh < 12:
                hh += 12
            elif ampm in ("오전", "아침", "am") and hh == 12:
                hh = 0
            elif not ampm and 1 <= hh <= 6:
                hh += 12
            return f"{hh:02d}:{mm:02d}"

    # 2) 오전/오후 H시 M분 / H시 반
    m_kr = re.search(
        r"(오전|오후|아침|저녁|낮|밤|AM|PM|am|pm)?\s*(\d{1,2})\s*시(?:\s*(\d{1,2})\s*분|\s*(반))?",
        line
    )
    if m_kr:
        ampm = (m_kr.group(1) or "").strip().lower()
        hh = int(m_kr.group(2))
        mm = 30 if m_kr.group(4) else (int(m_kr.group(3)) if m_kr.group(3) else 0)
        if 0 <= hh <= 24 and 0 <= mm <= 59:
            if hh == 24:
                hh = 0
            elif ampm in ("오후", "저녁", "밤", "pm", "낮") and hh < 12:
                hh += 12
            elif ampm in ("오전", "아침", "am") and hh == 12:
                hh = 0
            elif not ampm and 1 <= hh <= 6:
                hh += 12
            return f"{hh:02d}:{mm:02d}"

    return ""


def extract_schedules_from_email(
    subject: str,
    clean_lines: list,
    base_date: date = None,
    sender: str = ""
) -> list:
    if base_date is None:
        base_date = datetime.now().date()

    clean_subj = re.sub(
        r"^(\s*(\[[^\]]+\]|\([^)]+\)|RE|FW|FWD|답장|전달)\s*[:：]?\s*)+",
        "",
        subject or "",
        flags=re.IGNORECASE
    ).strip() or (subject or "메일 일정").strip()

    sched_kw_re = re.compile(
        r"(일정|일시|회의|미팅|간담회|세미나|교육|워크샵|워크숍|발표|보고|면접|리뷰|점검|"
        r"회식|모임|행사|시연|화상|줌|Zoom|Teams|팀즈|마감|기한|제출|회신|완료|오픈|"
        r"배포|출시|방문|출장|예약|참석|진행|장소|시간|날짜|까지|금일|내일|명일|모레|금주|차주|다음\s*주)",
        re.IGNORECASE
    )
    label_only_re = re.compile(
        r"^[-•*·\d.)\s]*(일시|일정|회의\s*일시|회의\s*일정|진행\s*일시|마감\s*기한|제출\s*기한|기한|마감|날짜|시간|When|Date)\s*[:：]?\s*$",
        re.IGNORECASE
    )

    merged_lines = []
    if subject:
        merged_lines.append(subject.strip())

    i = 0
    lines_slice = clean_lines[:35]
    while i < len(lines_slice):
        ln = lines_slice[i]
        if label_only_re.match(ln) and i + 1 < len(lines_slice):
            merged_lines.append(f"{ln} {lines_slice[i + 1]}")
            i += 2
        else:
            merged_lines.append(ln)
            i += 1

    subj_has_kw = bool(sched_kw_re.search(subject or ""))
    weekday_map = {"월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "일": 6}

    found = []
    seen_keys = set()

    for idx, ln in enumerate(merged_lines):
        line_has_kw = bool(sched_kw_re.search(ln))
        extracted_time = parse_korean_time_from_line(ln)
        has_dow_paren = bool(re.search(r"\([월화수목금토일](?:요일)?\)", ln))

        # Ignore lines without any schedule context unless they have explicit date + time/dow
        if not (line_has_kw or subj_has_kw or extracted_time or has_dow_paren):
            continue

        target_date = None

        # 1) YYYY년 M월 D일 or YYYY-MM-DD / YYYY.MM.DD / YYYY/MM/DD
        m_ymd = re.search(
            r"(20\d{2})\s*[-./년]\s*(\d{1,2})\s*[-./월]\s*(\d{1,2})\s*일?",
            ln
        )
        if m_ymd:
            try:
                target_date = date(int(m_ymd.group(1)), int(m_ymd.group(2)), int(m_ymd.group(3)))
            except ValueError:
                target_date = None

        # 2) M월 D일
        if target_date is None:
            m_md_kr = re.search(r"(?<!\d)(\d{1,2})\s*월\s*(\d{1,2})\s*일", ln)
            if m_md_kr:
                mm, dd = int(m_md_kr.group(1)), int(m_md_kr.group(2))
                yr = base_date.year
                if base_date.month == 12 and mm == 1:
                    yr += 1
                try:
                    target_date = date(yr, mm, dd)
                except ValueError:
                    target_date = None

        # 3) M/D or M.D (when accompanied by day-of-week, time, or schedule keyword)
        if target_date is None and (has_dow_paren or extracted_time or line_has_kw):
            m_slash = re.search(
                r"(?<![\d./-])(\d{1,2})\s*[/.]\s*(\d{1,2})(?:\s*\([월화수목금토일](?:요일)?\)|\s*(?:까지|마감|일정|회의|미팅|오전|오후|\d{1,2}\s*[:시]))",
                ln
            )
            if not m_slash and (has_dow_paren or re.search(r"(일시|일정|마감|기한)\s*[:：]", ln)):
                m_slash = re.search(r"(?<![\d./-])(\d{1,2})\s*[/.]\s*(\d{1,2})(?![\d./-])", ln)
            if m_slash:
                mm, dd = int(m_slash.group(1)), int(m_slash.group(2))
                if 1 <= mm <= 12 and 1 <= dd <= 31:
                    yr = base_date.year
                    if base_date.month == 12 and mm == 1:
                        yr += 1
                    try:
                        target_date = date(yr, mm, dd)
                    except ValueError:
                        target_date = None

        # 4) Relative dates (오늘/금일/내일/명일/모레/금주 X요일/다음주 X요일)
        if target_date is None and (line_has_kw or extracted_time):
            m_rel_dow = re.search(r"(이번\s*주|금주|다음\s*주|차주|내주)\s*([월화수목금토일])요일", ln)
            if m_rel_dow:
                prefix_w = m_rel_dow.group(1).replace(" ", "")
                target_wd = weekday_map[m_rel_dow.group(2)]
                days_ahead = target_wd - base_date.weekday()
                if prefix_w in ("다음주", "차주", "내주"):
                    days_ahead += 7
                elif days_ahead < 0:
                    days_ahead += 7
                target_date = base_date + timedelta(days=days_ahead)
            elif re.search(r"\b(모레|명후일)\b", ln) or "모레" in ln:
                target_date = base_date + timedelta(days=2)
            elif re.search(r"(내일|명일)", ln) and (extracted_time or re.search(r"(회의|미팅|일정|마감|기한|제출|발표|보고|진행|오전|오후|시)", ln)):
                target_date = base_date + timedelta(days=1)
            elif re.search(r"(오늘|금일|당일)", ln) and (extracted_time or re.search(r"(회의|미팅|일정|마감|기한|제출|발표|보고)", ln)):
                target_date = base_date

        if target_date is None:
            continue

        # Skip dates that are before the email's received date (e.g., past transaction/card logs)
        if target_date < base_date:
            continue
        # Skip dates older than 7 days before today
        if (datetime.now().date() - target_date).days > 7:
            continue

        time_label = extracted_time
        if not time_label:
            if re.search(r"(마감|기한|까지|제출)", ln):
                time_label = "마감"
            elif "오전" in ln:
                time_label = "오전"
            elif "오후" in ln:
                time_label = "오후"
            else:
                time_label = "종일"

        d_str = target_date.strftime("%Y-%m-%d")
        dow_kr = SHORT_WEEKDAYS[target_date.weekday()]
        short_date_str = f"{target_date.month:02d}/{target_date.day:02d}({dow_kr})"

        dedup_key = (d_str, time_label)
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)

        # Build concise title
        desc = re.sub(r"^[-•*·\d.)\s]*(일시|일정|회의\s*일시|시간|마감|기한|날짜)\s*[:：]\s*", "", ln).strip()
        if idx == 0 or len(desc) < 6 or desc == ln:
            sched_title = clean_subj
        else:
            # If the line has specific description alongside the subject
            sched_title = f"{clean_subj}"
        if sender and sender not in sched_title and len(sched_title) < 42:
            sched_title_with_sender = f"{sched_title} ({sender})"
        else:
            sched_title_with_sender = sched_title

        snippet = ln.lstrip("-•*· ").strip()
        if len(snippet) > 90:
            snippet = snippet[:87] + "..."

        found.append({
            "date": d_str,
            "short_date": short_date_str,
            "time": time_label,
            "title": sched_title_with_sender,
            "snippet": snippet,
        })
        if len(found) >= 3:
            break

    return found


def summarize_email_body(raw_body: str, subject: str = "", base_date: date = None, sender: str = "") -> dict:
    if not raw_body and not subject:
        return {
            "one_line": "본문 내용이 없습니다.",
            "bullets": ["본문 내용이 없는 메일입니다."],
            "preview": "",
            "schedules": []
        }

    text = (raw_body or "").replace("\r\n", "\n").replace("\r", "\n")

    cutoff_patterns = [
        r"(?m)^-{3,}\s*(Original Message|원본 메시지)\s*-{3,}",
        r"(?m)^_{8,}",
        r"(?m)^(From|보낸 사람|발신)\s*:\s*.+",
        r"(?m)^\d{4}[-./년]\s*\d{1,2}[-./월]\s*\d{1,2}일?.*작성:",
    ]
    for pat in cutoff_patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m and m.start() > 15:
            text = text[:m.start()]

    text = re.sub(r"<https?://[^>]+>", "", text)
    text = re.sub(r"https?://\S+", "[링크]", text)
    text = re.sub(r"<[^>]+>", " ", text)

    raw_lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.split("\n")]

    greeting_re = re.compile(
        r"^(안녕하세요|안녕하십니까|반갑습니다|수고하십니다|수고 많으십니다|좋은 하루|Dear\b|Hi\b|Hello\b)",
        re.IGNORECASE
    )
    closing_re = re.compile(
        r"^(감사합니다|고맙습니다|수고하세요|좋은 하루 되세요|좋은 하루 보내세요|"
        r".*드림\.?$|.*올림\.?$|.*배상\.?$|Best regards|Regards|Thank you|Thanks)",
        re.IGNORECASE
    )
    noise_re = re.compile(
        r"(본 메일은 발신전용|보안메일|무단\s*전재|confidential|unsubscribe)",
        re.IGNORECASE
    )
    key_terms = (
        "요청", "확인", "공유", "일정", "마감", "기한", "회의", "검토", "전달",
        "안내", "회신", "첨부", "변경", "완료", "필수", "보고", "승인", "결재",
        "문의", "긴급", "중요", "제출", "참석", "진행", "결과", "금일", "내일", "금주"
    )

    clean_lines = []
    candidate_lines = []

    for ln in raw_lines:
        if not ln or len(ln) < 2:
            continue
        if re.match(r"^[-=*_•·\s]+$", ln):
            continue
        if ln.startswith(">"):
            continue
        if noise_re.search(ln):
            continue

        clean_lines.append(ln)

        stripped_ln = re.sub(
            r"^(안녕하세요[,.\s!]*|안녕하십니까[,.\s!]*|[가-힣A-Za-z0-9\s]{1,15}(님|팀장님|매니저님|대리님|과장님|차장님|부장님|담당자님)[,.\s!]*)+",
            "",
            ln
        ).strip()

        if closing_re.match(ln) and len(ln) < 35:
            continue
        if greeting_re.match(ln) and len(stripped_ln) < 6:
            continue

        target = stripped_ln if len(stripped_ln) >= 6 else ln
        candidate_lines.append(target)

    schedules = extract_schedules_from_email(subject, clean_lines, base_date=base_date, sender=sender)

    if not candidate_lines:
        candidate_lines = clean_lines

    if not candidate_lines:
        return {
            "one_line": "본문 요약 정보가 없습니다.",
            "bullets": ["표시할 본문 텍스트가 없습니다."],
            "preview": "",
            "schedules": schedules,
        }

    scored = []
    for idx, ln in enumerate(candidate_lines):
        score = 0
        for kw in key_terms:
            if kw in ln:
                score += 2
        if re.search(r"(\d{1,2}월|\d{1,2}일|\d{1,2}:\d{2}|\d+시)", ln):
            score += 2
        if 10 <= len(ln) <= 95:
            score += 1
        if idx < 3:
            score += 1
        scored.append((score, idx, ln))

    top_scored = sorted(scored, key=lambda x: (-x[0], x[1]))[:3]
    top_ordered = [item[2] for item in sorted(top_scored, key=lambda x: x[1])]

    bullets = []
    for b in top_ordered:
        b_clean = b.lstrip("-•*· ").strip()
        if len(b_clean) > 150:
            b_clean = b_clean[:147] + "..."
        bullets.append(b_clean)

    one_line = bullets[0]
    if len(one_line) > 120:
        one_line = one_line[:117] + "..."

    preview_text = "\n".join(clean_lines[:14])
    if len(preview_text) > 700:
        preview_text = preview_text[:697] + "..."

    return {
        "one_line": one_line,
        "bullets": bullets,
        "preview": preview_text,
        "schedules": schedules,
    }


class OutlookWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, max_items: int = 25):
        super().__init__()
        self.max_items = max_items

    def run(self):
        pythoncom = None
        try:
            import pythoncom as _pythoncom
            import win32com.client
            pythoncom = _pythoncom
            pythoncom.CoInitialize()

            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)  # 6 == olFolderInbox

            unread_total = int(getattr(inbox, "UnReadItemCount", 0))
            items = inbox.Items
            items.Sort("[ReceivedTime]", True)

            emails = []
            today_date = datetime.now().date()
            msg = items.GetFirst()
            scanned = 0

            while msg is not None and len(emails) < self.max_items and scanned < 80:
                scanned += 1
                try:
                    msg_class = getattr(msg, "Class", 0)
                    if msg_class in (43, 53, 54, 55, 56, 26):
                        entry_id = str(getattr(msg, "EntryID", ""))
                        subject = str(getattr(msg, "Subject", "") or "(제목 없음)").strip()
                        sender = str(getattr(msg, "SenderName", "") or "알 수 없음").strip()
                        unread = bool(getattr(msg, "UnRead", False))
                        recv_dt = getattr(msg, "ReceivedTime", None)

                        raw_body = ""
                        try:
                            raw_body = str(getattr(msg, "Body", "") or "")
                        except Exception:
                            raw_body = ""

                        r_date = today_date
                        if recv_dt is not None:
                            try:
                                r_date = date(recv_dt.year, recv_dt.month, recv_dt.day)
                                if r_date == today_date:
                                    time_str = f"오늘 {recv_dt.hour:02d}:{recv_dt.minute:02d}"
                                elif r_date.year == today_date.year:
                                    time_str = f"{recv_dt.month:02d}/{recv_dt.day:02d} {recv_dt.hour:02d}:{recv_dt.minute:02d}"
                                else:
                                    time_str = f"{recv_dt.year}.{recv_dt.month:02d}.{recv_dt.day:02d}"
                            except Exception:
                                time_str = str(recv_dt)[:16]
                        else:
                            time_str = ""

                        summary_info = summarize_email_body(
                            raw_body,
                            subject,
                            base_date=r_date,
                            sender=sender
                        )

                        emails.append({
                            "entry_id": entry_id,
                            "subject": subject,
                            "sender": sender,
                            "unread": unread,
                            "time": time_str,
                            "one_line": summary_info["one_line"],
                            "bullets": summary_info["bullets"],
                            "preview": summary_info["preview"],
                            "schedules": summary_info.get("schedules", []),
                        })
                except Exception:
                    pass
                msg = items.GetNext()

            self.finished.emit({
                "ok": True,
                "unread_count": unread_total,
                "emails": emails,
                "updated_at": datetime.now().strftime("%H:%M:%S")
            })
        except Exception as e:
            self.finished.emit({
                "ok": False,
                "error": str(e)
            })
        finally:
            if pythoncom is not None:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass


class DataManager:
    def __init__(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")
        self.data = {
            "opacity": 92,
            "always_on_top": True,
            "city": "경남 창원",
            "topbar_pos": None,
            "todos": [
                {
                    "id": str(uuid.uuid4()),
                    "text": "데스크톱 상단 바 위젯 기능 둘러보기",
                    "done": False,
                    "priority": "중요",
                    "created": today_str
                }
            ],
            "schedules": {
                today_str: [
                    {"id": str(uuid.uuid4()), "time": "14:00", "title": "오후 집중 업무 시간"}
                ]
            },
            "memos": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "아이디어 노트",
                    "content": "여기에 자유롭게 메모를 작성하세요.\n입력한 내용은 날짜별로 자동 저장되며 검색할 수 있습니다! ✨",
                    "color_idx": 0,
                    "date": today_str,
                    "updated_at": now_time
                }
            ],
            "pomodoro_count": 0
        }
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
                today_str = datetime.now().strftime("%Y-%m-%d")
                changed = False
                if not self.data.get("changwon_default_migrated"):
                    self.data["city"] = "경남 창원"
                    self.data["changwon_default_migrated"] = True
                    changed = True
                for m in self.data.get("memos", []):
                    if not m.get("id"):
                        m["id"] = str(uuid.uuid4())
                        changed = True
                    if not m.get("date"):
                        m["date"] = today_str
                        changed = True
                    if "updated_at" not in m:
                        m["updated_at"] = ""
                        changed = True
                if changed:
                    self.save()
            except Exception:
                pass

    def save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


class MemoCardWidget(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, memo_id: str, parent=None):
        super().__init__(parent)
        self.memo_id = memo_id
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.memo_id)
            event.accept()
        else:
            super().mousePressEvent(event)


class CircularTimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 160)
        self.progress = 1.0
        self.time_text = "25:00"
        self.mode_text = "집중 시간"
        self.accent_color = QColor("#6366F1")

    def set_state(self, progress: float, time_text: str, mode_text: str, color_hex: str):
        self.progress = max(0.0, min(1.0, progress))
        self.time_text = time_text
        self.mode_text = mode_text
        self.accent_color = QColor(color_hex)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        size = min(w, h) - 14
        x = (w - size) / 2
        y = (h - size) / 2
        rect = QRectF(x, y, size, size)

        track_pen = QPen(QColor(255, 255, 255, 25), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, 0, 360 * 16)

        if self.progress > 0:
            prog_pen = QPen(self.accent_color, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(prog_pen)
            span_angle = int(-self.progress * 360 * 16)
            painter.drawArc(rect, 90 * 16, span_angle)

        painter.setPen(QColor("#F8FAFC"))
        font = QFont("Malgun Gothic", 20, QFont.Weight.Bold)
        painter.setFont(font)
        time_rect = QRectF(x, y + size * 0.25, size, size * 0.35)
        painter.drawText(time_rect, Qt.AlignmentFlag.AlignCenter, self.time_text)

        painter.setPen(QColor("#94A3B8"))
        sub_font = QFont("Malgun Gothic", 9, QFont.Weight.Medium)
        painter.setFont(sub_font)
        sub_rect = QRectF(x, y + size * 0.58, size, size * 0.2)
        painter.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, self.mode_text)


class DesktopWidget(QMainWindow):
    BAR_HEIGHT = 48
    EXPANDED_HEIGHT = 450
    OPIC_BANNER_HEIGHT = 104

    def __init__(self):
        super().__init__()
        self.dm = DataManager()
        self.drag_pos = None
        self.bg_alpha = int(self.dm.data.get("opacity", 92) * 2.55)
        self.always_on_top = self.dm.data.get("always_on_top", True)

        self.is_expanded = False
        self.active_tab = 0
        self.opic_active = False
        self.current_opic = None
        self.last_opic_idx = -1
        self.opic_completing = False
        self.opic_close_timer = QTimer(self)
        self.opic_close_timer.setSingleShot(True)
        self.opic_close_timer.timeout.connect(self.hide_opic_challenge)

        # Timer state
        self.timer_total_sec = 25 * 60
        self.timer_remain_sec = 25 * 60
        self.timer_running = False
        self.timer_mode_label = "집중 타이머 (25분)"
        self.timer_color = "#6366F1"

        self.todo_filter = "전체"
        self.mail_filter = "전체"
        self.cached_emails = []
        self.expanded_mail_ids = set()
        self.unread_mail_count = 0
        self.mail_worker = None
        self.ticker_idx = 0

        self.selected_date = date.today()
        self.cal_year = self.selected_date.year
        self.cal_month = self.selected_date.month
        self.current_memo_id = None
        self.memo_date_filter = "전체"
        self.memo_search_query = ""
        self.memo_card_refs = {}

        self.init_window()
        self.init_ui()
        self.init_timers()
        self.refresh_weather()
        self.refresh_outlook_mails()

    def init_window(self):
        self.setWindowTitle("Desktop Top Bar Widget")
        screen = QApplication.primaryScreen().availableGeometry()
        self.bar_width = min(1520, max(1100, screen.width() - 60))
        self.setFixedSize(self.bar_width, self.BAR_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.update_window_flags()

        pos = self.dm.data.get("topbar_pos")
        if pos and isinstance(pos, list) and len(pos) == 2:
            x = max(0, min(pos[0], screen.width() - self.bar_width))
            y = max(0, min(pos[1], screen.height() - self.BAR_HEIGHT))
            self.move(x, y)
        else:
            x = screen.x() + (screen.width() - self.bar_width) // 2
            y = screen.y() + 6
            self.move(x, y)

    def update_window_flags(self):
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(2, 2, self.width() - 4, self.height() - 4)
        path = QPainterPath()
        path.addRoundedRect(rect, 14, 14)

        bg_color = QColor(15, 23, 42, max(85, min(255, self.bg_alpha)))
        painter.fillPath(path, QBrush(bg_color))

        pen = QPen(QColor(255, 255, 255, 42), 1.0)
        painter.setPen(pen)
        painter.drawPath(path)

    def make_v_divider(self):
        div = QFrame()
        div.setFixedSize(1, 20)
        div.setStyleSheet("background: rgba(255, 255, 255, 0.12); border: none;")
        return div

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(12, 6, 12, 6)
        root_layout.setSpacing(6)

        # =========================================================
        # 1. SLIM HORIZONTAL TOP BAR (Always visible, 36px inner)
        # =========================================================
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(2, 0, 2, 0)
        top_bar.setSpacing(8)

        # Grip + Clock & Date
        grip_lbl = QLabel("✦")
        grip_lbl.setStyleSheet("color: #6366F1; font-size: 12px; font-weight: bold;")
        grip_lbl.setToolTip("드래그하여 위치 이동")
        top_bar.addWidget(grip_lbl)

        self.time_lbl = QLabel("00:00:00")
        self.time_lbl.setStyleSheet("color: #F8FAFC; font-size: 14px; font-weight: 800; background: transparent;")
        top_bar.addWidget(self.time_lbl)

        self.date_lbl = QLabel("11.16(월)")
        self.date_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 600; background: transparent;")
        top_bar.addWidget(self.date_lbl)

        top_bar.addWidget(self.make_v_divider())

        # Compact Weather
        self.city_combo = QComboBox()
        self.city_combo.addItems(list(CITIES.keys()))
        saved_city = self.dm.data.get("city", "경남 창원")
        if saved_city not in CITIES:
            saved_city = "경남 창원"
        self.city_combo.setCurrentText(saved_city)
        self.city_combo.setFixedHeight(24)
        self.city_combo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.city_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255,255,255,0.07); color: #E2E8F0;
                border: 1px solid rgba(255,255,255,0.12); border-radius: 5px;
                padding: 0 5px; font-size: 10px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1E293B; color: #F8FAFC; selection-background-color: #6366F1;
            }
        """)
        self.city_combo.currentTextChanged.connect(self.on_city_changed)
        top_bar.addWidget(self.city_combo)

        self.weather_main_lbl = QLabel("🌤️ --°C")
        self.weather_main_lbl.setStyleSheet("color: #F8FAFC; font-size: 11px; font-weight: bold;")
        top_bar.addWidget(self.weather_main_lbl)

        self.weather_weekend_lbl = QLabel("주말 토-- · 일--")
        self.weather_weekend_lbl.setStyleSheet("""
            background: rgba(99, 102, 241, 0.16);
            color: #C7D2FE;
            border: 1px solid rgba(99, 102, 241, 0.30);
            border-radius: 5px;
            padding: 1px 6px;
            font-size: 10px;
            font-weight: bold;
        """)
        self.weather_weekend_lbl.setToolTip("이번 주말(토·일) 날씨 예보 불러오는 중...")
        top_bar.addWidget(self.weather_weekend_lbl)

        refresh_w_btn = QPushButton("↻")
        refresh_w_btn.setFixedSize(20, 20)
        refresh_w_btn.setToolTip("날씨 새로고침")
        refresh_w_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_w_btn.setStyleSheet(self.icon_btn_style())
        refresh_w_btn.clicked.connect(self.refresh_weather)
        top_bar.addWidget(refresh_w_btn)

        top_bar.addWidget(self.make_v_divider())

        # Thin & Long Mail Summary Ticker Strip (Middle Stretch Area)
        ticker_frame = QFrame()
        ticker_frame.setFixedHeight(30)
        ticker_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.70);
                border: 1px solid rgba(99, 102, 241, 0.25);
                border-radius: 8px;
            }
            QFrame:hover {
                border: 1px solid rgba(99, 102, 241, 0.55);
                background: rgba(30, 41, 59, 0.90);
            }
        """)
        ticker_layout = QHBoxLayout(ticker_frame)
        ticker_layout.setContentsMargins(8, 0, 6, 0)
        ticker_layout.setSpacing(6)

        self.ticker_badge = QLabel("📧 메일요약")
        self.ticker_badge.setStyleSheet("""
            background: rgba(59, 130, 246, 0.22); color: #93C5FD;
            border-radius: 4px; padding: 1px 5px; font-size: 10px; font-weight: bold; border: none;
        """)
        ticker_layout.addWidget(self.ticker_badge)

        self.ticker_btn = QPushButton("Outlook 메일 요약을 불러오는 중입니다...")
        self.ticker_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ticker_btn.setToolTip("클릭하면 메일 요약 상세 패널이 열립니다")
        self.ticker_btn.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.ticker_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #E2E8F0; border: none;
                font-size: 11px; text-align: left; padding: 0 2px;
            }
            QPushButton:hover { color: #FFFFFF; }
        """)
        self.ticker_btn.clicked.connect(self.on_ticker_clicked)
        ticker_layout.addWidget(self.ticker_btn, 1)

        prev_mail_btn = QPushButton("◀")
        prev_mail_btn.setFixedSize(18, 18)
        prev_mail_btn.setToolTip("이전 메일 요약")
        prev_mail_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        prev_mail_btn.setStyleSheet("QPushButton { background: transparent; color: #94A3B8; border: none; font-size: 9px; } QPushButton:hover { color: white; }")
        prev_mail_btn.clicked.connect(self.prev_ticker_mail)
        ticker_layout.addWidget(prev_mail_btn)

        next_mail_btn = QPushButton("▶")
        next_mail_btn.setFixedSize(18, 18)
        next_mail_btn.setToolTip("다음 메일 요약")
        next_mail_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        next_mail_btn.setStyleSheet("QPushButton { background: transparent; color: #94A3B8; border: none; font-size: 9px; } QPushButton:hover { color: white; }")
        next_mail_btn.clicked.connect(self.next_ticker_mail)
        ticker_layout.addWidget(next_mail_btn)

        top_bar.addWidget(ticker_frame, 1)

        top_bar.addWidget(self.make_v_divider())

        # Segmented Navigation Tabs (Click to expand/switch, click active tab to collapse)
        self.nav_btns = []
        tabs = [
            ("✅ 할일", 0),
            ("📧 메일", 1),
            ("📅 일정", 2),
            ("📝 메모", 3),
            ("⏱️ 타이머", 4),
        ]
        for label, idx in tabs:
            btn = QPushButton(label)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setFixedHeight(26)
            btn.setToolTip("클릭하여 패널 펼치기/접기")
            btn.clicked.connect(lambda checked, i=idx: self.on_tab_clicked(i))
            top_bar.addWidget(btn)
            self.nav_btns.append(btn)

        self.fold_btn = QPushButton("▼")
        self.fold_btn.setFixedSize(22, 24)
        self.fold_btn.setToolTip("패널 펼치기 / 접기")
        self.fold_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.fold_btn.setStyleSheet(self.icon_btn_style())
        self.fold_btn.clicked.connect(self.toggle_expand)
        top_bar.addWidget(self.fold_btn)

        self.opic_top_btn = QPushButton("🗣️ 오픽")
        self.opic_top_btn.setFixedHeight(26)
        self.opic_top_btn.setToolTip("오픽 한문장 따라치기 열기/닫기 (1시간마다 자동 표시)")
        self.opic_top_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.opic_top_btn.setStyleSheet("""
            QPushButton {
                background: rgba(16, 185, 129, 0.18);
                color: #6EE7B7;
                border: 1px solid rgba(16, 185, 129, 0.40);
                border-radius: 6px;
                padding: 0 8px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #10B981;
                color: #0F172A;
            }
        """)
        self.opic_top_btn.clicked.connect(self.toggle_opic_challenge)
        top_bar.addWidget(self.opic_top_btn)

        top_bar.addWidget(self.make_v_divider())

        # Opacity & Window Controls
        op_lbl = QLabel("🔆")
        op_lbl.setToolTip("배경 투명도 조절")
        op_lbl.setStyleSheet("font-size: 10px;")
        top_bar.addWidget(op_lbl)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(35, 100)
        self.opacity_slider.setValue(self.dm.data.get("opacity", 92))
        self.opacity_slider.setFixedWidth(46)
        self.opacity_slider.setToolTip(f"투명도: {self.opacity_slider.value()}%")
        self.opacity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px; background: rgba(255,255,255,0.18); border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #6366F1; border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #F8FAFC; width: 10px; height: 10px; margin: -3px 0; border-radius: 5px;
            }
        """)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        top_bar.addWidget(self.opacity_slider)

        self.pin_btn = QPushButton("📌")
        self.pin_btn.setFixedSize(22, 22)
        self.pin_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin_btn.clicked.connect(self.toggle_always_on_top)
        self.update_pin_style()
        top_bar.addWidget(self.pin_btn)

        min_btn = QPushButton("─")
        min_btn.setFixedSize(22, 22)
        min_btn.setToolTip("최소화")
        min_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        min_btn.setStyleSheet(self.icon_btn_style())
        min_btn.clicked.connect(self.showMinimized)
        top_bar.addWidget(min_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(22, 22)
        close_btn.setToolTip("종료")
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06); color: #CBD5E1;
                border-radius: 6px; font-size: 10px; border: none;
            }
            QPushButton:hover {
                background: #EF4444; color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        top_bar.addWidget(close_btn)

        root_layout.addLayout(top_bar)

        # =========================================================
        # 1.5. HOURLY OPIC SENTENCE TYPING BANNER (Auto-appears every 1h)
        # =========================================================
        self.opic_frame = QFrame()
        self.opic_frame.setObjectName("OpicBanner")
        self.opic_frame.setFixedHeight(self.OPIC_BANNER_HEIGHT - 6)
        self.opic_frame.setStyleSheet("""
            QFrame#OpicBanner {
                background: rgba(16, 185, 129, 0.10);
                border: 1px solid rgba(16, 185, 129, 0.45);
                border-left: 4px solid #10B981;
                border-radius: 9px;
            }
        """)
        opic_vbox = QVBoxLayout(self.opic_frame)
        opic_vbox.setContentsMargins(12, 6, 12, 6)
        opic_vbox.setSpacing(4)

        opic_top_row = QHBoxLayout()
        opic_top_row.setSpacing(8)

        opic_badge = QLabel("🗣️ 오픽 1시간 한문장 훈련")
        opic_badge.setStyleSheet("""
            background: rgba(16, 185, 129, 0.25); color: #6EE7B7;
            border-radius: 4px; padding: 1px 6px; font-size: 10px; font-weight: bold; border: none;
        """)
        opic_top_row.addWidget(opic_badge)

        self.opic_cat_lbl = QLabel("💼 직장/업무")
        self.opic_cat_lbl.setStyleSheet("color: #A5B4FC; font-size: 10px; font-weight: bold; border: none; background: transparent;")
        opic_top_row.addWidget(self.opic_cat_lbl)

        self.opic_ko_lbl = QLabel("")
        self.opic_ko_lbl.setStyleSheet("color: #CBD5E1; font-size: 11px; border: none; background: transparent;")
        opic_top_row.addWidget(self.opic_ko_lbl, 1)

        self.opic_streak_lbl = QLabel(f"🔥 누적 {self.dm.data.get('opic_count', 0)}회 완료")
        self.opic_streak_lbl.setStyleSheet("color: #FBBF24; font-size: 10px; font-weight: bold; border: none; background: transparent;")
        opic_top_row.addWidget(self.opic_streak_lbl)

        hint_opic_btn = QPushButton("💡 뜻 보기")
        hint_opic_btn.setFixedHeight(20)
        hint_opic_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        hint_opic_btn.setStyleSheet("""
            QPushButton {
                background: rgba(245, 158, 11, 0.18); color: #FDE68A;
                border-radius: 4px; padding: 0 7px; font-size: 10px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: rgba(245, 158, 11, 0.35); color: white; }
        """)
        hint_opic_btn.clicked.connect(self.show_opic_korean_hint)
        opic_top_row.addWidget(hint_opic_btn)

        next_opic_btn = QPushButton("🔄 다른 문장")
        next_opic_btn.setFixedHeight(20)
        next_opic_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        next_opic_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.08); color: #E2E8F0;
                border-radius: 4px; padding: 0 7px; font-size: 10px; border: none;
            }
            QPushButton:hover { background: rgba(255,255,255,0.18); color: white; }
        """)
        next_opic_btn.clicked.connect(self.pick_and_render_opic_sentence)
        opic_top_row.addWidget(next_opic_btn)

        skip_opic_btn = QPushButton("닫기 ✕")
        skip_opic_btn.setFixedHeight(20)
        skip_opic_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        skip_opic_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.06); color: #94A3B8;
                border-radius: 4px; padding: 0 6px; font-size: 10px; border: none;
            }
            QPushButton:hover { background: rgba(239,68,68,0.25); color: #F87171; }
        """)
        skip_opic_btn.clicked.connect(self.hide_opic_challenge)
        opic_top_row.addWidget(skip_opic_btn)

        opic_vbox.addLayout(opic_top_row)

        self.opic_en_lbl = QLabel("")
        self.opic_en_lbl.setTextFormat(Qt.TextFormat.RichText)
        self.opic_en_lbl.setStyleSheet("font-size: 13px; font-weight: bold; border: none; background: transparent;")
        opic_vbox.addWidget(self.opic_en_lbl)

        self.opic_input = QLineEdit()
        self.opic_input.setPlaceholderText("✍️ 위 영어 문장을 그대로 따라 치면 창이 자동으로 사라집니다...")
        self.opic_input.setFixedHeight(26)
        self.opic_input.setStyleSheet("""
            QLineEdit {
                background: rgba(15, 23, 42, 0.75);
                color: #F8FAFC;
                border: 1px solid rgba(16, 185, 129, 0.40);
                border-radius: 6px;
                padding: 0 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 1px solid #10B981;
                background: rgba(15, 23, 42, 0.92);
            }
        """)
        self.opic_input.textChanged.connect(self.on_opic_input_changed)
        opic_vbox.addWidget(self.opic_input)

        root_layout.addWidget(self.opic_frame)
        self.opic_frame.setVisible(False)

        # =========================================================
        # 2. COLLAPSIBLE DROPDOWN CONTENT PANEL
        # =========================================================
        self.panel_frame = QFrame()
        self.panel_frame.setStyleSheet("""
            QFrame#DropdownPanel {
                border-top: 1px solid rgba(255, 255, 255, 0.10);
                background: transparent;
            }
        """)
        self.panel_frame.setObjectName("DropdownPanel")
        panel_layout = QVBoxLayout(self.panel_frame)
        panel_layout.setContentsMargins(2, 6, 2, 2)
        panel_layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.build_todo_page())
        self.stack.addWidget(self.build_mail_page())
        self.stack.addWidget(self.build_calendar_page())
        self.stack.addWidget(self.build_memo_page())
        self.stack.addWidget(self.build_timer_page())
        panel_layout.addWidget(self.stack, 1)

        root_layout.addWidget(self.panel_frame, 1)

        # Start in slim collapsed bar state
        self.panel_frame.setVisible(False)
        self.update_nav_styles()
        self.update_clock()

    def on_tab_clicked(self, index: int):
        if self.is_expanded and self.active_tab == index:
            self.set_expanded(False)
        else:
            self.active_tab = index
            self.stack.setCurrentIndex(index)
            self.set_expanded(True)

    def toggle_expand(self):
        self.set_expanded(not self.is_expanded)

    def set_expanded(self, expanded: bool):
        self.is_expanded = expanded
        self.panel_frame.setVisible(expanded)
        self.fold_btn.setText("▲" if expanded else "▼")
        self.update_nav_styles()
        self.update_window_height()

    def update_window_height(self):
        base_h = self.EXPANDED_HEIGHT if self.is_expanded else self.BAR_HEIGHT
        extra_h = self.OPIC_BANNER_HEIGHT if self.opic_active else 0
        self.setFixedSize(self.bar_width, base_h + extra_h)
        self.update()

    # ---------------------------------------------------------
    # Hourly OPIc Sentence Typing Challenge
    # ---------------------------------------------------------
    def toggle_opic_challenge(self):
        if self.opic_active:
            self.hide_opic_challenge()
        else:
            self.show_opic_challenge()

    def show_opic_challenge(self):
        self.opic_close_timer.stop()
        self.opic_active = True
        self.opic_completing = False
        self.opic_frame.setVisible(True)
        self.pick_and_render_opic_sentence()
        self.update_window_height()
        self.activateWindow()
        self.opic_input.setFocus()

    def hide_opic_challenge(self):
        self.opic_close_timer.stop()
        self.opic_active = False
        self.opic_completing = False
        self.opic_frame.setVisible(False)
        self.opic_input.blockSignals(True)
        self.opic_input.clear()
        self.opic_input.blockSignals(False)
        self.update_window_height()

    def show_opic_korean_hint(self):
        if self.current_opic:
            self.opic_ko_lbl.setText(f"🇰🇷 {self.current_opic['ko']}")
            self.opic_ko_lbl.setStyleSheet("color: #FDE68A; font-size: 11px; font-weight: bold; border: none; background: transparent;")
            self.opic_input.setFocus()

    def pick_and_render_opic_sentence(self):
        if not OPIC_SENTENCES:
            return
        self.opic_close_timer.stop()
        candidates = [i for i in range(len(OPIC_SENTENCES)) if i != self.last_opic_idx]
        idx = random.choice(candidates) if candidates else 0
        self.last_opic_idx = idx
        self.current_opic = OPIC_SENTENCES[idx]
        self.opic_completing = False

        self.opic_cat_lbl.setText(f"[{self.current_opic['category']}]")
        self.opic_ko_lbl.setText("✍️ 영문 타이핑을 완료하면 한국어 뜻이 마지막에 표시됩니다")
        self.opic_ko_lbl.setStyleSheet("color: #94A3B8; font-size: 10px; border: none; background: transparent;")
        self.opic_streak_lbl.setText(f"🔥 누적 {self.dm.data.get('opic_count', 0)}회 완료")

        self.opic_input.blockSignals(True)
        self.opic_input.setReadOnly(False)
        self.opic_input.clear()
        self.opic_input.setStyleSheet("""
            QLineEdit {
                background: rgba(15, 23, 42, 0.75);
                color: #F8FAFC;
                border: 1px solid rgba(16, 185, 129, 0.40);
                border-radius: 6px;
                padding: 0 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 1px solid #10B981;
                background: rgba(15, 23, 42, 0.92);
            }
        """)
        self.opic_input.blockSignals(False)
        self.render_opic_progress_html("")
        self.opic_input.setFocus()

    def render_opic_progress_html(self, typed_str: str):
        if not self.current_opic:
            return
        target = self.current_opic["en"]
        parts = []
        for i, ch in enumerate(target):
            esc_ch = html.escape(ch)
            if i < len(typed_str):
                if typed_str[i].lower() == ch.lower():
                    parts.append(f"<span style='color:#34D399;'>{esc_ch}</span>")
                else:
                    parts.append(f"<span style='color:#F87171; text-decoration:underline;'>{esc_ch}</span>")
            else:
                parts.append(f"<span style='color:#F8FAFC;'>{esc_ch}</span>")
        self.opic_en_lbl.setText("".join(parts))

    def on_opic_input_changed(self, text: str):
        if not self.current_opic or self.opic_completing:
            return
        self.render_opic_progress_html(text)

        target_raw = self.current_opic["en"].strip()
        ko_text = self.current_opic["ko"].strip()
        typed_norm = re.sub(r"\s+", " ", text.strip()).lower()
        target_norm = re.sub(r"\s+", " ", target_raw).lower()
        target_no_punct = target_norm.rstrip(".?!")

        if typed_norm and (typed_norm == target_norm or typed_norm == target_no_punct):
            self.opic_completing = True
            self.dm.data["opic_count"] = self.dm.data.get("opic_count", 0) + 1
            self.dm.save()
            self.opic_streak_lbl.setText(f"🔥 누적 {self.dm.data['opic_count']}회 완료")
            self.opic_ko_lbl.setText("🎉 타이핑 완료! 아래 한국어 뜻을 확인하세요 (잠시 후 자동으로 사라집니다)")
            self.opic_ko_lbl.setStyleSheet("color: #34D399; font-size: 11px; font-weight: bold; border: none; background: transparent;")
            self.opic_en_lbl.setText(
                f"<span style='color:#34D399;'>✅ {html.escape(target_raw)}</span>"
            )
            self.opic_input.blockSignals(True)
            self.opic_input.setReadOnly(True)
            self.opic_input.setText(f"🇰🇷 뜻: {ko_text}")
            self.opic_input.setStyleSheet("""
                QLineEdit {
                    background: rgba(245, 158, 11, 0.20);
                    color: #FDE68A;
                    border: 1px solid #F59E0B;
                    border-radius: 6px;
                    padding: 0 10px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            self.opic_input.blockSignals(False)
            try:
                winsound.Beep(987, 120)
                winsound.Beep(1318, 180)
            except Exception:
                pass
            self.opic_close_timer.start(2600)

    def update_nav_styles(self):
        for i, btn in enumerate(self.nav_btns):
            if self.is_expanded and i == self.active_tab:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #6366F1; color: #FFFFFF;
                        border-radius: 6px; padding: 0 8px;
                        font-size: 11px; font-weight: bold; border: none;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255, 255, 255, 0.05); color: #CBD5E1;
                        border-radius: 6px; padding: 0 8px;
                        font-size: 11px; font-weight: 600; border: none;
                    }
                    QPushButton:hover {
                        background: rgba(255, 255, 255, 0.14); color: #FFFFFF;
                    }
                """)

    # ---------------------------------------------------------
    # Top Bar Mail Summary Ticker Controls
    # ---------------------------------------------------------
    def update_ticker_display(self):
        if not self.cached_emails:
            self.ticker_btn.setText("표시할 최신 메일이 없습니다.")
            return

        self.ticker_idx = self.ticker_idx % len(self.cached_emails)
        mail = self.cached_emails[self.ticker_idx]
        sender = mail.get("sender", "")
        subject = mail.get("subject", "")
        one_line = mail.get("one_line", "")
        scheds = mail.get("schedules", [])
        prefix = "● " if mail.get("unread") else ""

        sched_tag = ""
        sched_tip = ""
        if scheds:
            s0 = scheds[0]
            sched_tag = f"📅[{s0.get('short_date', '')} {s0.get('time', '')}] "
            sched_lines = "\n".join(
                f"  • {s.get('date')} ({s.get('time')}) : {s.get('snippet', '')}"
                for s in scheds
            )
            sched_tip = f"\n📅 감지된 일정:\n{sched_lines}\n"

        text = f"{prefix}{sched_tag}[{sender}] {subject}  —  💬 {one_line}"
        self.ticker_btn.setText(text)
        self.ticker_btn.setToolTip(
            f"보낸사람: {sender} ({mail.get('time', '')})\n"
            f"제목: {subject}\n"
            f"요약: {one_line}"
            f"{sched_tip}\n"
            "클릭하면 메일 탭에서 상세 요약 및 일정을 펼칩니다."
        )

    def next_ticker_mail(self):
        if self.cached_emails:
            self.ticker_idx = (self.ticker_idx + 1) % len(self.cached_emails)
            self.update_ticker_display()

    def prev_ticker_mail(self):
        if self.cached_emails:
            self.ticker_idx = (self.ticker_idx - 1) % len(self.cached_emails)
            self.update_ticker_display()

    def on_ticker_clicked(self):
        if self.cached_emails:
            mail = self.cached_emails[self.ticker_idx % len(self.cached_emails)]
            eid = mail.get("entry_id", "")
            if eid:
                self.expanded_mail_ids.add(eid)
                self.render_mail_list()
        self.active_tab = 1
        self.stack.setCurrentIndex(1)
        self.set_expanded(True)

    # ---------------------------------------------------------
    # Page 1: To-Do List (Wide Horizontal Layout)
    # ---------------------------------------------------------
    def build_todo_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Single top control + input bar
        top_row = QHBoxLayout()
        top_row.setSpacing(6)

        self.todo_stat_lbl = QLabel("완료 0 / 0")
        self.todo_stat_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: bold;")
        top_row.addWidget(self.todo_stat_lbl)

        self.filter_btns = {}
        for f_name in ["전체", "진행중", "완료"]:
            b = QPushButton(f_name)
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.setFixedHeight(24)
            b.clicked.connect(lambda checked, fn=f_name: self.set_todo_filter(fn))
            top_row.addWidget(b)
            self.filter_btns[f_name] = b

        top_row.addSpacing(8)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["일반", "중요", "긴급"])
        self.priority_combo.setFixedWidth(58)
        self.priority_combo.setFixedHeight(26)
        self.priority_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255,255,255,0.08); color: #F8FAFC;
                border: 1px solid rgba(255,255,255,0.12); border-radius: 6px;
                padding-left: 6px; font-size: 11px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1E293B; color: #F8FAFC; selection-background-color: #6366F1;
            }
        """)
        top_row.addWidget(self.priority_combo)

        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("새로운 할 일 입력 후 Enter...")
        self.todo_input.setFixedHeight(26)
        self.todo_input.setStyleSheet(self.input_style())
        self.todo_input.returnPressed.connect(self.add_todo)
        top_row.addWidget(self.todo_input, 1)

        add_btn = QPushButton("+ 할일 추가")
        add_btn.setFixedHeight(26)
        add_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        add_btn.setStyleSheet(self.primary_btn_style())
        add_btn.clicked.connect(self.add_todo)
        top_row.addWidget(add_btn)

        clear_done_btn = QPushButton("🗑️ 완료 정리")
        clear_done_btn.setFixedHeight(26)
        clear_done_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        clear_done_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.05); color: #94A3B8;
                border-radius: 6px; font-size: 10px; border: none; padding: 0 8px;
            }
            QPushButton:hover { background: rgba(239,68,68,0.18); color: #F87171; }
        """)
        clear_done_btn.clicked.connect(self.clear_completed_todos)
        top_row.addWidget(clear_done_btn)

        layout.addLayout(top_row)

        self.todo_scroll = QScrollArea()
        self.todo_scroll.setWidgetResizable(True)
        self.todo_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.todo_container = QWidget()
        self.todo_container.setStyleSheet("background: transparent;")
        self.todo_list_layout = QVBoxLayout(self.todo_container)
        self.todo_list_layout.setContentsMargins(0, 0, 2, 0)
        self.todo_list_layout.setSpacing(4)
        self.todo_list_layout.addStretch()
        self.todo_scroll.setWidget(self.todo_container)
        layout.addWidget(self.todo_scroll, 1)

        self.update_todo_filter_styles()
        self.refresh_todo_list()
        return page

    def set_todo_filter(self, f_name: str):
        self.todo_filter = f_name
        self.update_todo_filter_styles()
        self.refresh_todo_list()

    def update_todo_filter_styles(self):
        for name, btn in self.filter_btns.items():
            if name == self.todo_filter:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #6366F1; color: white; border-radius: 5px;
                        padding: 0 8px; font-size: 10px; font-weight: bold; border: none;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255,255,255,0.06); color: #94A3B8; border-radius: 5px;
                        padding: 0 8px; font-size: 10px; border: none;
                    }
                    QPushButton:hover { background: rgba(255,255,255,0.12); color: #E2E8F0; }
                """)

    def add_todo(self):
        text = self.todo_input.text().strip()
        if not text:
            return
        self.dm.data["todos"].insert(0, {
            "id": str(uuid.uuid4()),
            "text": text,
            "done": False,
            "priority": self.priority_combo.currentText(),
            "created": datetime.now().strftime("%Y-%m-%d")
        })
        self.todo_input.clear()
        self.dm.save()
        self.refresh_todo_list()

    def toggle_todo(self, todo_id: str, checked: bool):
        for item in self.dm.data["todos"]:
            if item["id"] == todo_id:
                item["done"] = checked
                break
        self.dm.save()
        self.refresh_todo_list()

    def delete_todo(self, todo_id: str):
        self.dm.data["todos"] = [t for t in self.dm.data["todos"] if t["id"] != todo_id]
        self.dm.save()
        self.refresh_todo_list()

    def clear_completed_todos(self):
        self.dm.data["todos"] = [t for t in self.dm.data["todos"] if not t.get("done")]
        self.dm.save()
        self.refresh_todo_list()

    def refresh_todo_list(self):
        while self.todo_list_layout.count() > 1:
            child = self.todo_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        todos = self.dm.data.get("todos", [])
        done_cnt = sum(1 for t in todos if t.get("done"))
        self.todo_stat_lbl.setText(f"완료 {done_cnt} / {len(todos)}")

        filtered = []
        for t in todos:
            if self.todo_filter == "진행중" and t.get("done"):
                continue
            if self.todo_filter == "완료" and not t.get("done"):
                continue
            filtered.append(t)

        if not filtered:
            empty_lbl = QLabel("등록된 할 일이 없습니다 ✨")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("color: #64748B; font-size: 11px; padding: 20px;")
            self.todo_list_layout.insertWidget(0, empty_lbl)
            return

        badge_colors = {
            "긴급": ("#EF4444", "rgba(239, 68, 68, 0.18)"),
            "중요": ("#F59E0B", "rgba(245, 158, 11, 0.18)"),
            "일반": ("#60A5FA", "rgba(96, 165, 250, 0.15)"),
        }

        for idx, item in enumerate(filtered):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.07);
                    border-radius: 7px;
                }
                QFrame:hover {
                    background: rgba(255, 255, 255, 0.08);
                }
            """)
            row = QHBoxLayout(card)
            row.setContentsMargins(10, 5, 10, 5)
            row.setSpacing(8)

            cb = QCheckBox()
            cb.setChecked(item.get("done", False))
            cb.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            cb.setStyleSheet("""
                QCheckBox::indicator {
                    width: 15px; height: 15px; border-radius: 4px;
                    border: 2px solid #64748B; background: transparent;
                }
                QCheckBox::indicator:checked {
                    background: #10B981; border-color: #10B981;
                }
            """)
            tid = item["id"]
            cb.toggled.connect(lambda checked, i=tid: self.toggle_todo(i, checked))
            row.addWidget(cb)

            prio = item.get("priority", "일반")
            fg, bg = badge_colors.get(prio, badge_colors["일반"])
            badge = QLabel(prio)
            badge.setFixedWidth(34)
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setStyleSheet(f"""
                background: {bg}; color: {fg}; border-radius: 4px;
                font-size: 9px; font-weight: bold; padding: 1px 3px; border: none;
            """)
            row.addWidget(badge)

            txt_lbl = QLabel(item.get("text", ""))
            txt_lbl.setWordWrap(True)
            if item.get("done"):
                txt_lbl.setStyleSheet("color: #64748B; font-size: 11px; text-decoration: line-through; border: none; background: transparent;")
            else:
                txt_lbl.setStyleSheet("color: #F1F5F9; font-size: 11px; border: none; background: transparent;")
            row.addWidget(txt_lbl, 1)

            del_btn = QPushButton("✕")
            del_btn.setFixedSize(18, 18)
            del_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            del_btn.setStyleSheet("""
                QPushButton {
                    background: transparent; color: #64748B; border: none; font-size: 10px; border-radius: 4px;
                }
                QPushButton:hover { background: rgba(239,68,68,0.2); color: #F87171; }
            """)
            del_btn.clicked.connect(lambda checked, i=tid: self.delete_todo(i))
            row.addWidget(del_btn)

            self.todo_list_layout.insertWidget(idx, card)

    # ---------------------------------------------------------
    # Page 2: Outlook Mail & Summary List
    # ---------------------------------------------------------
    def build_mail_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        top_row = QHBoxLayout()
        top_row.setSpacing(6)

        self.mail_unread_badge = QLabel("안 읽은 메일 0통")
        self.mail_unread_badge.setStyleSheet("""
            background: rgba(59, 130, 246, 0.18);
            color: #60A5FA;
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-radius: 6px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: bold;
        """)
        top_row.addWidget(self.mail_unread_badge)

        self.mail_sched_badge = QLabel("📅 일정 메일 0통")
        self.mail_sched_badge.setStyleSheet("""
            background: rgba(245, 158, 11, 0.18);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: 6px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: bold;
        """)
        top_row.addWidget(self.mail_sched_badge)

        self.mail_filter_btns = {}
        for f_name, f_label in [("전체", "전체"), ("안읽음", "안읽음"), ("일정포함", "📅 일정포함")]:
            b = QPushButton(f_label)
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.setFixedHeight(22)
            b.clicked.connect(lambda checked, fn=f_name: self.set_mail_filter(fn))
            top_row.addWidget(b)
            self.mail_filter_btns[f_name] = b

        self.mail_status_lbl = QLabel("Outlook 연결 대기 중...")
        self.mail_status_lbl.setStyleSheet("color: #64748B; font-size: 10px; margin-left: 6px;")
        top_row.addWidget(self.mail_status_lbl)

        top_row.addStretch()

        hint_lbl = QLabel("💡 메일 내 일정 감지 시 [📅 날짜] 뱃지 표시 및 캘린더 자동 연동")
        hint_lbl.setStyleSheet("color: #64748B; font-size: 10px;")
        top_row.addWidget(hint_lbl)

        refresh_m_btn = QPushButton("↻ 새로고침")
        refresh_m_btn.setFixedHeight(22)
        refresh_m_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_m_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.08); color: #E2E8F0;
                border-radius: 5px; padding: 0 8px; font-size: 10px; border: none;
            }
            QPushButton:hover { background: rgba(255,255,255,0.16); color: white; }
        """)
        refresh_m_btn.clicked.connect(self.refresh_outlook_mails)
        top_row.addWidget(refresh_m_btn)

        layout.addLayout(top_row)

        self.mail_scroll = QScrollArea()
        self.mail_scroll.setWidgetResizable(True)
        self.mail_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.mail_container = QWidget()
        self.mail_container.setStyleSheet("background: transparent;")
        self.mail_list_layout = QVBoxLayout(self.mail_container)
        self.mail_list_layout.setContentsMargins(0, 0, 2, 0)
        self.mail_list_layout.setSpacing(4)
        self.mail_list_layout.addStretch()
        self.mail_scroll.setWidget(self.mail_container)
        layout.addWidget(self.mail_scroll, 1)

        self.update_mail_filter_styles()
        return page

    def set_mail_filter(self, f_name: str):
        self.mail_filter = f_name
        self.update_mail_filter_styles()
        self.render_mail_list()

    def update_mail_filter_styles(self):
        for name, btn in self.mail_filter_btns.items():
            if name == self.mail_filter:
                btn.setStyleSheet("""
                    QPushButton {
                        background: #6366F1; color: white; border-radius: 5px;
                        padding: 0 8px; font-size: 10px; font-weight: bold; border: none;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255,255,255,0.06); color: #94A3B8; border-radius: 5px;
                        padding: 0 8px; font-size: 10px; border: none;
                    }
                    QPushButton:hover { background: rgba(255,255,255,0.12); color: #E2E8F0; }
                """)

    def sync_mail_schedules(self, emails: list) -> int:
        schedules_map = self.dm.data.setdefault("schedules", {})
        dismissed = set(self.dm.data.setdefault("dismissed_mail_schedules", []))

        existing_keys = set()
        for d_key, day_list in schedules_map.items():
            for item in day_list:
                mk = item.get("mail_key")
                if mk:
                    existing_keys.add(mk)

        added_count = 0
        for mail in emails:
            eid = mail.get("entry_id", "")
            sender = mail.get("sender", "")
            for s in mail.get("schedules", []):
                d_str = s.get("date", "")
                t_str = s.get("time", "종일")
                title = s.get("title", "")
                snippet = s.get("snippet", "")
                if not d_str or not title:
                    continue
                mail_key = f"{eid[:24]}_{d_str}_{t_str}_{title[:20]}"
                if mail_key in dismissed or mail_key in existing_keys:
                    continue

                day_list = schedules_map.setdefault(d_str, [])
                # Also avoid duplicating identical title+time on the same day
                if any(x.get("title") == title and x.get("time") == t_str for x in day_list):
                    existing_keys.add(mail_key)
                    continue

                day_list.append({
                    "id": str(uuid.uuid4()),
                    "time": t_str,
                    "title": title,
                    "from_mail": True,
                    "entry_id": eid,
                    "sender": sender,
                    "snippet": snippet,
                    "mail_key": mail_key,
                })
                day_list.sort(key=lambda x: x.get("time", ""))
                existing_keys.add(mail_key)
                added_count += 1

        if added_count > 0:
            self.dm.save()
        return added_count

    def jump_to_calendar_date(self, date_str: str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            self.selected_date = dt
            self.cal_year = dt.year
            self.cal_month = dt.month
            self.render_calendar()
            self.refresh_schedule_list()
            self.active_tab = 2
            self.stack.setCurrentIndex(2)
            self.set_expanded(True)
        except Exception:
            pass

    def refresh_outlook_mails(self):
        if self.mail_worker is not None and self.mail_worker.isRunning():
            return
        self.mail_status_lbl.setText("받은편지함 및 메일 일정 분석 중...")
        self.mail_worker = OutlookWorker(max_items=40)
        self.mail_worker.finished.connect(self.on_outlook_loaded)
        self.mail_worker.start()

    def on_outlook_loaded(self, res: dict):
        if res.get("ok"):
            self.unread_mail_count = res.get("unread_count", 0)
            self.cached_emails = res.get("emails", [])
            self.mail_unread_badge.setText(f"안 읽은 메일 {self.unread_mail_count}통")

            sched_mail_cnt = sum(1 for m in self.cached_emails if m.get("schedules"))
            total_sched_cnt = sum(len(m.get("schedules", [])) for m in self.cached_emails)
            self.mail_sched_badge.setText(f"📅 감지된 일정 {total_sched_cnt}건")
            if "일정포함" in self.mail_filter_btns:
                self.mail_filter_btns["일정포함"].setText(f"📅 일정포함 ({sched_mail_cnt})")

            self.sync_mail_schedules(self.cached_emails)
            if hasattr(self, "days_grid"):
                self.render_calendar()
                self.refresh_schedule_list()

            if self.unread_mail_count > 0:
                self.nav_btns[1].setText(f"📧 메일({self.unread_mail_count})")
                self.ticker_badge.setText(f"📧 안읽음 {self.unread_mail_count}")
            else:
                self.nav_btns[1].setText("📧 메일")
                self.ticker_badge.setText("📧 메일요약")
            self.mail_status_lbl.setText(f"동기화: {res.get('updated_at', '')}")
            self.update_ticker_display()
            self.render_mail_list()
        else:
            self.mail_status_lbl.setText("Outlook 연결 실패")
            self.ticker_btn.setText("클래식 Outlook 앱을 실행하면 최신 메일 한줄 요약이 여기에 표시됩니다.")
            self.render_mail_error(res.get("error", ""))

    def render_mail_error(self, err_msg: str):
        while self.mail_list_layout.count() > 1:
            child = self.mail_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        lbl = QLabel(
            "📬 클래식 Outlook 앱에 연결할 수 없습니다. "
            "PC에 설치된 Office Outlook 실행 여부를 확인한 뒤 [↻ 새로고침]을 눌러주세요."
        )
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("color: #94A3B8; font-size: 11px; padding: 20px;")
        self.mail_list_layout.insertWidget(0, lbl)

    def render_mail_list(self):
        while self.mail_list_layout.count() > 1:
            child = self.mail_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        filtered = []
        for m in self.cached_emails:
            if self.mail_filter == "안읽음" and not m.get("unread"):
                continue
            if self.mail_filter == "일정포함" and not m.get("schedules"):
                continue
            filtered.append(m)

        if not filtered:
            if self.mail_filter == "안읽음":
                empty_txt = "안 읽은 메일이 없습니다 🎉"
            elif self.mail_filter == "일정포함":
                empty_txt = "일정이 감지된 메일이 없습니다 📅"
            else:
                empty_txt = "표시할 메일이 없습니다."
            empty_lbl = QLabel(empty_txt)
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("color: #64748B; font-size: 11px; padding: 20px;")
            self.mail_list_layout.insertWidget(0, empty_lbl)
            return

        for idx, mail in enumerate(filtered):
            is_unread = mail.get("unread", False)
            scheds = mail.get("schedules", [])
            has_sched = bool(scheds)

            card = QFrame()
            if has_sched:
                card.setStyleSheet("""
                    QFrame {
                        background: rgba(245, 158, 11, 0.09);
                        border: 1px solid rgba(245, 158, 11, 0.32);
                        border-left: 3px solid #F59E0B;
                        border-radius: 7px;
                    }
                    QFrame:hover { background: rgba(245, 158, 11, 0.15); }
                """)
            elif is_unread:
                card.setStyleSheet("""
                    QFrame {
                        background: rgba(59, 130, 246, 0.10);
                        border: 1px solid rgba(59, 130, 246, 0.30);
                        border-left: 3px solid #3B82F6;
                        border-radius: 7px;
                    }
                    QFrame:hover { background: rgba(59, 130, 246, 0.16); }
                """)
            else:
                card.setStyleSheet("""
                    QFrame {
                        background: rgba(255, 255, 255, 0.04);
                        border: 1px solid rgba(255, 255, 255, 0.07);
                        border-radius: 7px;
                    }
                    QFrame:hover { background: rgba(255, 255, 255, 0.08); }
                """)

            vbox = QVBoxLayout(card)
            vbox.setContentsMargins(10, 5, 10, 5)
            vbox.setSpacing(4)

            # Single wide horizontal row: Dot + Sender + Subject + Schedule Badge + 1-line summary + [요약] + [열기]
            row = QHBoxLayout()
            row.setSpacing(8)

            if is_unread:
                dot_lbl = QLabel("●")
                dot_lbl.setStyleSheet("color: #3B82F6; font-size: 9px; border: none; background: transparent;")
                row.addWidget(dot_lbl)

            sender_lbl = QLabel(mail.get("sender", ""))
            sender_lbl.setFixedWidth(115)
            sender_lbl.setStyleSheet(
                f"color: {'#93C5FD' if is_unread else '#94A3B8'}; "
                f"font-size: 11px; font-weight: {'bold' if is_unread else 'normal'}; "
                "border: none; background: transparent;"
            )
            row.addWidget(sender_lbl)

            subj_lbl = QLabel(mail.get("subject", ""))
            subj_lbl.setFixedWidth(340)
            subj_lbl.setStyleSheet(
                f"color: {'#F8FAFC' if is_unread else '#CBD5E1'}; "
                f"font-size: 11px; font-weight: {'bold' if is_unread else 'normal'}; "
                "border: none; background: transparent;"
            )
            row.addWidget(subj_lbl)

            if has_sched:
                s0 = scheds[0]
                extra_cnt = f" 외 {len(scheds) - 1}" if len(scheds) > 1 else ""
                sched_btn_txt = f"📅 {s0.get('short_date', '')} {s0.get('time', '')}{extra_cnt}"
                sched_pill = QPushButton(sched_btn_txt)
                sched_pill.setFixedHeight(20)
                sched_pill.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                sched_pill.setToolTip(
                    f"감지된 일정: {s0.get('date')} {s0.get('time')}\n"
                    f"내용: {s0.get('snippet', '')}\n"
                    "클릭하면 [📅 일정] 탭의 해당 날짜로 이동합니다."
                )
                sched_pill.setStyleSheet("""
                    QPushButton {
                        background: rgba(245, 158, 11, 0.22);
                        color: #FDE68A;
                        border: 1px solid rgba(245, 158, 11, 0.45);
                        border-radius: 4px;
                        padding: 0 6px;
                        font-size: 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: #F59E0B;
                        color: #0F172A;
                    }
                """)
                target_d = s0.get("date", "")
                sched_pill.clicked.connect(lambda checked, d_str=target_d: self.jump_to_calendar_date(d_str))
                row.addWidget(sched_pill)

            one_line = mail.get("one_line", "")
            one_lbl = QLabel(f"💬 {one_line}" if one_line else "")
            one_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; border: none; background: transparent;")
            row.addWidget(one_lbl, 1)

            time_lbl = QLabel(mail.get("time", ""))
            time_lbl.setStyleSheet("color: #64748B; font-size: 10px; border: none; background: transparent;")
            row.addWidget(time_lbl)

            entry_id = mail.get("entry_id", "")
            is_expanded = entry_id in self.expanded_mail_ids

            sum_btn = QPushButton("요약 ▴" if is_expanded else "요약 ▾")
            sum_btn.setFixedHeight(20)
            sum_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            sum_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {'#6366F1' if is_expanded else 'rgba(99, 102, 241, 0.18)'};
                    color: {'#FFFFFF' if is_expanded else '#A5B4FC'};
                    border-radius: 4px; padding: 0 7px; font-size: 10px; font-weight: bold; border: none;
                }}
                QPushButton:hover {{ background: #6366F1; color: white; }}
            """)
            sum_btn.clicked.connect(lambda checked, eid=entry_id: self.toggle_mail_summary(eid))
            row.addWidget(sum_btn)

            open_btn = QPushButton("열기 ↗")
            open_btn.setFixedHeight(20)
            open_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            open_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,0.08); color: #CBD5E1;
                    border-radius: 4px; padding: 0 7px; font-size: 10px; border: none;
                }
                QPushButton:hover { background: #3B82F6; color: white; }
            """)
            open_btn.clicked.connect(lambda checked, eid=entry_id: self.open_outlook_mail(eid))
            row.addWidget(open_btn)

            vbox.addLayout(row)

            if is_expanded:
                sum_box = QFrame()
                sum_box.setStyleSheet("""
                    QFrame {
                        background: rgba(15, 23, 42, 0.65);
                        border: 1px solid rgba(99, 102, 241, 0.30);
                        border-radius: 6px;
                    }
                """)
                sb_layout = QVBoxLayout(sum_box)
                sb_layout.setContentsMargins(10, 6, 10, 6)
                sb_layout.setSpacing(4)

                if has_sched:
                    s_hdr = QLabel("📅 메일에서 감지된 일정 (캘린더 자동 표시됨)")
                    s_hdr.setStyleSheet("color: #FBBF24; font-size: 10px; font-weight: bold; border: none; background: transparent;")
                    sb_layout.addWidget(s_hdr)

                    for s_item in scheds:
                        s_row = QHBoxLayout()
                        s_row.setSpacing(6)
                        s_info = QLabel(
                            f"• [{s_item.get('date')} ({s_item.get('short_date', '')[-2:-1]}) {s_item.get('time')}] "
                            f"{s_item.get('snippet', '')}"
                        )
                        s_info.setWordWrap(True)
                        s_info.setStyleSheet("color: #FDE68A; font-size: 11px; border: none; background: transparent;")
                        s_row.addWidget(s_info, 1)

                        go_cal_btn = QPushButton("📅 달력에서 보기")
                        go_cal_btn.setFixedHeight(20)
                        go_cal_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                        go_cal_btn.setStyleSheet("""
                            QPushButton {
                                background: rgba(245, 158, 11, 0.22); color: #FDE68A;
                                border-radius: 4px; padding: 0 7px; font-size: 10px; font-weight: bold; border: none;
                            }
                            QPushButton:hover { background: #F59E0B; color: #0F172A; }
                        """)
                        s_d = s_item.get("date", "")
                        go_cal_btn.clicked.connect(lambda checked, d_str=s_d: self.jump_to_calendar_date(d_str))
                        s_row.addWidget(go_cal_btn)
                        sb_layout.addLayout(s_row)

                bullets = mail.get("bullets", [])
                if bullets:
                    b_title = QLabel("📌 핵심 내용 요약")
                    b_title.setStyleSheet("color: #A5B4FC; font-size: 10px; font-weight: bold; border: none; background: transparent;")
                    sb_layout.addWidget(b_title)

                    bullet_txt = "\n".join(f"• {b}" for b in bullets)
                    b_lbl = QLabel(bullet_txt)
                    b_lbl.setWordWrap(True)
                    b_lbl.setStyleSheet("color: #E2E8F0; font-size: 11px; border: none; background: transparent;")
                    sb_layout.addWidget(b_lbl)

                preview = mail.get("preview", "")
                if preview:
                    p_title = QLabel("📄 본문 발췌")
                    p_title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: bold; margin-top: 2px; border: none; background: transparent;")
                    sb_layout.addWidget(p_title)

                    p_lbl = QLabel(preview)
                    p_lbl.setWordWrap(True)
                    p_lbl.setStyleSheet("color: #94A3B8; font-size: 10px; border: none; background: transparent;")
                    sb_layout.addWidget(p_lbl)

                vbox.addWidget(sum_box)

            self.mail_list_layout.insertWidget(idx, card)

    def toggle_mail_summary(self, entry_id: str):
        if not entry_id:
            return
        if entry_id in self.expanded_mail_ids:
            self.expanded_mail_ids.remove(entry_id)
        else:
            self.expanded_mail_ids.add(entry_id)
        self.render_mail_list()

    def open_outlook_mail(self, entry_id: str):
        if not entry_id:
            return
        try:
            import win32com.client
            outlook = win32com.client.Dispatch("Outlook.Application")
            ns = outlook.GetNamespace("MAPI")
            item = ns.GetItemFromID(entry_id)
            item.Display()
            QTimer.singleShot(1500, self.refresh_outlook_mails)
        except Exception as e:
            self.mail_status_lbl.setText(f"메일 열기 실패: {e}")

    # ---------------------------------------------------------
    # Page 3: Calendar & Schedule (2-Column Horizontal Split)
    # ---------------------------------------------------------
    def build_calendar_page(self):
        page = QWidget()
        h_layout = QHBoxLayout(page)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(12)

        # Left Column: Compact Calendar
        cal_card = QFrame()
        cal_card.setFixedWidth(320)
        cal_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 10px;
            }
        """)
        cal_vbox = QVBoxLayout(cal_card)
        cal_vbox.setContentsMargins(8, 6, 8, 6)
        cal_vbox.setSpacing(4)

        nav_row = QHBoxLayout()
        prev_btn = QPushButton("◀")
        prev_btn.setFixedSize(22, 22)
        prev_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        prev_btn.setStyleSheet(self.icon_btn_style())
        prev_btn.clicked.connect(self.prev_month)
        nav_row.addWidget(prev_btn)

        self.cal_header_lbl = QLabel()
        self.cal_header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cal_header_lbl.setStyleSheet("color: #F8FAFC; font-size: 12px; font-weight: bold; border: none;")
        nav_row.addWidget(self.cal_header_lbl, 1)

        today_btn = QPushButton("오늘")
        today_btn.setFixedHeight(20)
        today_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        today_btn.setStyleSheet("""
            QPushButton {
                background: rgba(99, 102, 241, 0.2); color: #A5B4FC;
                border-radius: 4px; padding: 0 6px; font-size: 10px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: rgba(99, 102, 241, 0.35); color: white; }
        """)
        today_btn.clicked.connect(self.go_today)
        nav_row.addWidget(today_btn)

        next_btn = QPushButton("▶")
        next_btn.setFixedSize(22, 22)
        next_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        next_btn.setStyleSheet(self.icon_btn_style())
        next_btn.clicked.connect(self.next_month)
        nav_row.addWidget(next_btn)
        cal_vbox.addLayout(nav_row)

        dow_grid = QGridLayout()
        for col, d_str in enumerate(SHORT_DAYS):
            lbl = QLabel(d_str)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            color = "#F87171" if col == 0 else ("#60A5FA" if col == 6 else "#94A3B8")
            lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold; border: none; background: transparent;")
            dow_grid.addWidget(lbl, 0, col)
        cal_vbox.addLayout(dow_grid)

        self.days_grid = QGridLayout()
        self.days_grid.setSpacing(2)
        cal_vbox.addLayout(self.days_grid, 1)

        self.cal_weekend_lbl = QLabel("🌤️ 주말 예보 불러오는 중...")
        self.cal_weekend_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cal_weekend_lbl.setStyleSheet("""
            background: rgba(99, 102, 241, 0.12);
            color: #C7D2FE;
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 6px;
            padding: 3px 6px;
            font-size: 10px;
            font-weight: bold;
        """)
        cal_vbox.addWidget(self.cal_weekend_lbl)

        h_layout.addWidget(cal_card)

        # Right Column: Selected Date Schedule List
        right_col = QVBoxLayout()
        right_col.setSpacing(6)

        s_in_row = QHBoxLayout()
        s_in_row.setSpacing(6)

        self.sched_date_lbl = QLabel()
        self.sched_date_lbl.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: bold;")
        s_in_row.addWidget(self.sched_date_lbl)

        s_in_row.addSpacing(8)

        self.sched_time_input = QLineEdit("09:00")
        self.sched_time_input.setFixedWidth(52)
        self.sched_time_input.setFixedHeight(26)
        self.sched_time_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sched_time_input.setStyleSheet(self.input_style())
        s_in_row.addWidget(self.sched_time_input)

        self.sched_title_input = QLineEdit()
        self.sched_title_input.setPlaceholderText("선택한 날짜의 새 일정 입력 후 Enter...")
        self.sched_title_input.setFixedHeight(26)
        self.sched_title_input.setStyleSheet(self.input_style())
        self.sched_title_input.returnPressed.connect(self.add_schedule)
        s_in_row.addWidget(self.sched_title_input, 1)

        s_add_btn = QPushButton("+ 일정 등록")
        s_add_btn.setFixedHeight(26)
        s_add_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        s_add_btn.setStyleSheet(self.primary_btn_style())
        s_add_btn.clicked.connect(self.add_schedule)
        s_in_row.addWidget(s_add_btn)

        right_col.addLayout(s_in_row)

        sched_scroll = QScrollArea()
        sched_scroll.setWidgetResizable(True)
        sched_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        sched_container = QWidget()
        sched_container.setStyleSheet("background: transparent;")
        self.sched_list_layout = QVBoxLayout(sched_container)
        self.sched_list_layout.setContentsMargins(0, 0, 2, 0)
        self.sched_list_layout.setSpacing(4)
        self.sched_list_layout.addStretch()
        sched_scroll.setWidget(sched_container)
        right_col.addWidget(sched_scroll, 1)

        h_layout.addLayout(right_col, 1)

        self.render_calendar()
        self.refresh_schedule_list()
        return page

    def prev_month(self):
        if self.cal_month == 1:
            self.cal_month = 12
            self.cal_year -= 1
        else:
            self.cal_month -= 1
        self.render_calendar()

    def next_month(self):
        if self.cal_month == 12:
            self.cal_month = 1
            self.cal_year += 1
        else:
            self.cal_month += 1
        self.render_calendar()

    def go_today(self):
        self.selected_date = date.today()
        self.cal_year = self.selected_date.year
        self.cal_month = self.selected_date.month
        self.render_calendar()
        self.refresh_schedule_list()

    def select_date(self, d: date):
        self.selected_date = d
        self.render_calendar()
        self.refresh_schedule_list()

    def render_calendar(self):
        self.cal_header_lbl.setText(f"{self.cal_year}년 {self.cal_month}월")

        while self.days_grid.count():
            item = self.days_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdatescalendar(self.cal_year, self.cal_month)
        schedules = self.dm.data.get("schedules", {})
        today = date.today()

        for r_idx, week in enumerate(month_days):
            for c_idx, d in enumerate(week):
                d_str = d.strftime("%Y-%m-%d")
                day_events = schedules.get(d_str, [])
                has_events = bool(day_events)
                has_mail_event = any(ev.get("from_mail") for ev in day_events)
                is_current_month = (d.month == self.cal_month)
                is_selected = (d == self.selected_date)
                is_today = (d == today)

                btn_text = f"{d.day}•" if has_events else f"{d.day}"
                btn = QPushButton(btn_text)
                btn.setFixedHeight(24)
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                if has_events:
                    btn.setToolTip(
                        f"{d_str} 일정 {len(day_events)}건"
                        + (" (📧 메일 일정 포함)" if has_mail_event else "")
                    )

                if is_selected:
                    bg = "#6366F1"
                    fg = "#FFFFFF"
                    border = "1px solid #F59E0B" if has_mail_event else "none"
                elif is_today:
                    bg = "rgba(99, 102, 241, 0.2)"
                    fg = "#A5B4FC"
                    border = "1px solid #6366F1"
                elif has_mail_event:
                    bg = "rgba(245, 158, 11, 0.14)"
                    fg = "#FDE68A" if is_current_month else "#94A3B8"
                    border = "1px solid rgba(245, 158, 11, 0.35)"
                else:
                    bg = "transparent"
                    border = "none"
                    if not is_current_month:
                        fg = "#475569"
                    elif c_idx == 0:
                        fg = "#F87171"
                    elif c_idx == 6:
                        fg = "#60A5FA"
                    else:
                        fg = "#E2E8F0"

                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {bg}; color: {fg}; border: {border};
                        border-radius: 5px; font-size: 10px; font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background: {'#4F46E5' if is_selected else 'rgba(255,255,255,0.1)'};
                    }}
                """)
                btn.clicked.connect(lambda checked, dt=d: self.select_date(dt))
                self.days_grid.addWidget(btn, r_idx, c_idx)

    def add_schedule(self):
        title = self.sched_title_input.text().strip()
        time_str = self.sched_time_input.text().strip() or "종일"
        if not title:
            return
        d_key = self.selected_date.strftime("%Y-%m-%d")
        schedules = self.dm.data.setdefault("schedules", {})
        day_list = schedules.setdefault(d_key, [])
        day_list.append({
            "id": str(uuid.uuid4()),
            "time": time_str,
            "title": title
        })
        day_list.sort(key=lambda x: x.get("time", ""))
        self.sched_title_input.clear()
        self.dm.save()
        self.render_calendar()
        self.refresh_schedule_list()

    def delete_schedule(self, d_key: str, sched_id: str):
        schedules = self.dm.data.get("schedules", {})
        if d_key in schedules:
            for s in schedules[d_key]:
                if s["id"] == sched_id and s.get("mail_key"):
                    dismissed = self.dm.data.setdefault("dismissed_mail_schedules", [])
                    if s["mail_key"] not in dismissed:
                        dismissed.append(s["mail_key"])
            schedules[d_key] = [s for s in schedules[d_key] if s["id"] != sched_id]
            if not schedules[d_key]:
                del schedules[d_key]
        self.dm.save()
        self.render_calendar()
        self.refresh_schedule_list()

    def refresh_schedule_list(self):
        d_key = self.selected_date.strftime("%Y-%m-%d")
        dow = KOREAN_DAYS[self.selected_date.weekday()]
        self.sched_date_lbl.setText(f"📌 {self.selected_date.month}월 {self.selected_date.day}일 ({dow})")

        while self.sched_list_layout.count() > 1:
            child = self.sched_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        day_list = self.dm.data.get("schedules", {}).get(d_key, [])
        if not day_list:
            empty = QLabel("이 날짜에 등록된 일정이 없습니다.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color: #64748B; font-size: 11px; padding: 20px;")
            self.sched_list_layout.insertWidget(0, empty)
            return

        for idx, item in enumerate(day_list):
            is_mail = bool(item.get("from_mail"))
            card = QFrame()
            if is_mail:
                card.setStyleSheet("""
                    QFrame {
                        background: rgba(245, 158, 11, 0.09);
                        border: 1px solid rgba(245, 158, 11, 0.25);
                        border-left: 3px solid #F59E0B;
                        border-radius: 5px;
                    }
                """)
            else:
                card.setStyleSheet("""
                    QFrame {
                        background: rgba(255, 255, 255, 0.05);
                        border-left: 3px solid #6366F1;
                        border-radius: 5px;
                    }
                """)
            row = QHBoxLayout(card)
            row.setContentsMargins(10, 5, 8, 5)
            row.setSpacing(6)

            t_lbl = QLabel(item.get("time", ""))
            t_lbl.setFixedWidth(48)
            t_lbl.setStyleSheet(
                f"color: {'#FDE68A' if is_mail else '#A5B4FC'}; "
                "font-size: 11px; font-weight: bold; border: none; background: transparent;"
            )
            row.addWidget(t_lbl)

            if is_mail:
                m_badge = QLabel("📧 메일")
                m_badge.setStyleSheet("""
                    background: rgba(245, 158, 11, 0.22); color: #FBBF24;
                    border-radius: 4px; padding: 1px 5px; font-size: 9px; font-weight: bold; border: none;
                """)
                row.addWidget(m_badge)

            title_lbl = QLabel(item.get("title", ""))
            title_lbl.setWordWrap(True)
            title_lbl.setStyleSheet("color: #F1F5F9; font-size: 11px; border: none; background: transparent;")
            if item.get("snippet"):
                title_lbl.setToolTip(f"원문 발췌: {item['snippet']}")
            row.addWidget(title_lbl, 1)

            if is_mail and item.get("entry_id"):
                eid = item["entry_id"]
                open_m_btn = QPushButton("메일 ↗")
                open_m_btn.setFixedHeight(18)
                open_m_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                open_m_btn.setToolTip("이 일정이 포함된 Outlook 메일 원문 열기")
                open_m_btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255,255,255,0.08); color: #CBD5E1;
                        border-radius: 4px; padding: 0 6px; font-size: 9px; border: none;
                    }
                    QPushButton:hover { background: #3B82F6; color: white; }
                """)
                open_m_btn.clicked.connect(lambda checked, e=eid: self.open_outlook_mail(e))
                row.addWidget(open_m_btn)

            sid = item["id"]
            del_btn = QPushButton("✕")
            del_btn.setFixedSize(18, 18)
            del_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            del_btn.setStyleSheet("""
                QPushButton { background: transparent; color: #64748B; border: none; font-size: 10px; }
                QPushButton:hover { color: #F87171; }
            """)
            del_btn.clicked.connect(lambda checked, dk=d_key, i=sid: self.delete_schedule(dk, i))
            row.addWidget(del_btn)

            self.sched_list_layout.insertWidget(idx, card)

    # ---------------------------------------------------------
    # Page 4: Sticky Memo Pad (Date-grouped & Searchable)
    # ---------------------------------------------------------
    def build_memo_page(self):
        page = QWidget()
        h_layout = QHBoxLayout(page)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(10)

        # Left Column: Search + Date Filter + Date-grouped Memo List
        left_card = QFrame()
        left_card.setFixedWidth(340)
        left_card.setStyleSheet("""
            QFrame#MemoLeftPanel {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
            }
        """)
        left_card.setObjectName("MemoLeftPanel")
        left_vbox = QVBoxLayout(left_card)
        left_vbox.setContentsMargins(8, 7, 8, 7)
        left_vbox.setSpacing(6)

        # 1) Search Row
        search_row = QHBoxLayout()
        search_row.setSpacing(4)

        self.memo_search_input = QLineEdit()
        self.memo_search_input.setPlaceholderText("🔍 메모 검색 (제목 · 내용 · 날짜)...")
        self.memo_search_input.setFixedHeight(26)
        self.memo_search_input.setStyleSheet(self.input_style())
        self.memo_search_input.textChanged.connect(self.on_memo_search_changed)
        search_row.addWidget(self.memo_search_input, 1)

        self.memo_search_clear_btn = QPushButton("✕")
        self.memo_search_clear_btn.setFixedSize(24, 26)
        self.memo_search_clear_btn.setToolTip("검색어 지우기")
        self.memo_search_clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.memo_search_clear_btn.setStyleSheet(self.icon_btn_style())
        self.memo_search_clear_btn.clicked.connect(self.clear_memo_search)
        self.memo_search_clear_btn.setVisible(False)
        search_row.addWidget(self.memo_search_clear_btn)

        left_vbox.addLayout(search_row)

        # 2) Date Filter Row
        filter_row = QHBoxLayout()
        filter_row.setSpacing(4)

        self.memo_date_filter_combo = QComboBox()
        self.memo_date_filter_combo.setFixedHeight(24)
        self.memo_date_filter_combo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.memo_date_filter_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255,255,255,0.08); color: #F8FAFC;
                border: 1px solid rgba(255,255,255,0.12); border-radius: 5px;
                padding: 0 6px; font-size: 10px; font-weight: bold;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1E293B; color: #F8FAFC; selection-background-color: #6366F1;
            }
        """)
        self.memo_date_filter_combo.currentIndexChanged.connect(self.on_memo_date_filter_changed)
        filter_row.addWidget(self.memo_date_filter_combo, 1)

        self.memo_all_btn = QPushButton("전체")
        self.memo_all_btn.setFixedHeight(24)
        self.memo_all_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.memo_all_btn.setToolTip("모든 날짜의 메모 보기")
        self.memo_all_btn.clicked.connect(lambda: self.set_memo_date_filter("전체"))
        filter_row.addWidget(self.memo_all_btn)

        self.memo_today_btn = QPushButton("오늘")
        self.memo_today_btn.setFixedHeight(24)
        self.memo_today_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.memo_today_btn.setToolTip("오늘 날짜 메모만 보기")
        self.memo_today_btn.clicked.connect(
            lambda: self.set_memo_date_filter(datetime.now().strftime("%Y-%m-%d"))
        )
        filter_row.addWidget(self.memo_today_btn)

        self.memo_count_lbl = QLabel("0건")
        self.memo_count_lbl.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: bold; padding-left: 2px;")
        filter_row.addWidget(self.memo_count_lbl)

        left_vbox.addLayout(filter_row)

        # 3) Date-grouped Memo List Scroll Area
        self.memo_list_scroll = QScrollArea()
        self.memo_list_scroll.setWidgetResizable(True)
        self.memo_list_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.memo_list_container = QWidget()
        self.memo_list_container.setStyleSheet("background: transparent;")
        self.memo_list_layout = QVBoxLayout(self.memo_list_container)
        self.memo_list_layout.setContentsMargins(0, 0, 2, 0)
        self.memo_list_layout.setSpacing(4)
        self.memo_list_layout.addStretch()
        self.memo_list_scroll.setWidget(self.memo_list_container)
        left_vbox.addWidget(self.memo_list_scroll, 1)

        h_layout.addWidget(left_card)

        # Right Column: Memo Editor (Date Picker + Title + Color + Content)
        right_col = QVBoxLayout()
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.setSpacing(6)

        top_row = QHBoxLayout()
        top_row.setSpacing(6)

        date_tag_lbl = QLabel("📅 날짜")
        date_tag_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: bold;")
        top_row.addWidget(date_tag_lbl)

        self.memo_date_edit = QDateEdit()
        self.memo_date_edit.setCalendarPopup(True)
        self.memo_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.memo_date_edit.setDate(QDate.currentDate())
        self.memo_date_edit.setFixedWidth(104)
        self.memo_date_edit.setFixedHeight(26)
        self.memo_date_edit.setToolTip("메모 저장 날짜 선택 (클릭하여 달력 열기)")
        self.memo_date_edit.setStyleSheet("""
            QDateEdit {
                background: rgba(99, 102, 241, 0.16);
                color: #E0E7FF;
                border: 1px solid rgba(99, 102, 241, 0.4);
                border-radius: 6px;
                padding: 0 6px;
                font-size: 11px;
                font-weight: bold;
            }
            QDateEdit::drop-down {
                border: none;
                width: 16px;
            }
        """)
        self.memo_date_edit.dateChanged.connect(self.on_memo_date_edited)
        top_row.addWidget(self.memo_date_edit)

        self.memo_title_edit = QLineEdit()
        self.memo_title_edit.setPlaceholderText("메모 제목을 입력하세요...")
        self.memo_title_edit.setFixedHeight(26)
        self.memo_title_edit.setStyleSheet(self.input_style())
        self.memo_title_edit.textEdited.connect(self.on_memo_title_edited)
        top_row.addWidget(self.memo_title_edit, 1)

        for c_idx, c_info in enumerate(MEMO_COLORS):
            c_btn = QPushButton()
            c_btn.setFixedSize(16, 16)
            c_btn.setToolTip(c_info["name"])
            c_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            c_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {c_info['border']}; border-radius: 8px;
                    border: 2px solid rgba(255,255,255,0.3);
                }}
                QPushButton:hover {{ border-color: white; }}
            """)
            c_btn.clicked.connect(lambda checked, ci=c_idx: self.set_memo_color(ci))
            top_row.addWidget(c_btn)

        new_memo_btn = QPushButton("+ 새 메모")
        new_memo_btn.setFixedHeight(26)
        new_memo_btn.setToolTip("선택한 날짜(또는 오늘)로 새 메모 추가")
        new_memo_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        new_memo_btn.setStyleSheet(self.primary_btn_style())
        new_memo_btn.clicked.connect(self.create_new_memo)
        top_row.addWidget(new_memo_btn)

        del_memo_btn = QPushButton("🗑️")
        del_memo_btn.setFixedSize(26, 26)
        del_memo_btn.setToolTip("현재 메모 삭제")
        del_memo_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        del_memo_btn.setStyleSheet(self.icon_btn_style())
        del_memo_btn.clicked.connect(self.delete_current_memo)
        top_row.addWidget(del_memo_btn)

        right_col.addLayout(top_row)

        self.memo_editor = QTextEdit()
        self.memo_editor.setPlaceholderText("여기에 자유롭게 메모를 입력하세요 (날짜별 자동 저장 · 좌측에서 검색 가능)...")
        self.memo_editor.textChanged.connect(self.on_memo_content_changed)
        right_col.addWidget(self.memo_editor, 1)

        h_layout.addLayout(right_col, 1)

        self.refresh_memo_ui()
        return page

    def ensure_memos_valid(self):
        memos = self.dm.data.setdefault("memos", [])
        today_str = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")
        if not memos:
            memos.append({
                "id": str(uuid.uuid4()),
                "title": "기본 메모",
                "content": "",
                "color_idx": 0,
                "date": today_str,
                "updated_at": now_time
            })
            self.dm.save()
        for m in memos:
            if not m.get("id"):
                m["id"] = str(uuid.uuid4())
            if not m.get("date"):
                m["date"] = today_str
            if "updated_at" not in m:
                m["updated_at"] = now_time
        return memos

    def get_current_memo(self):
        memos = self.ensure_memos_valid()
        if self.current_memo_id:
            for m in memos:
                if m["id"] == self.current_memo_id:
                    return m
        # Default to most recent memo by date
        sorted_memos = sorted(
            memos,
            key=lambda x: (x.get("date", ""), x.get("updated_at", "")),
            reverse=True
        )
        cur = sorted_memos[0]
        self.current_memo_id = cur["id"]
        return cur

    def format_memo_date_label(self, d_str: str) -> str:
        try:
            dt = datetime.strptime(d_str, "%Y-%m-%d").date()
            dow = SHORT_WEEKDAYS[dt.weekday()]
            today = date.today()
            if dt == today:
                return f"{d_str} ({dow}·오늘)"
            return f"{d_str} ({dow})"
        except Exception:
            return d_str

    def update_memo_date_filter_combo(self):
        memos = self.ensure_memos_valid()
        date_counts = {}
        for m in memos:
            d = m.get("date", datetime.now().strftime("%Y-%m-%d"))
            date_counts[d] = date_counts.get(d, 0) + 1

        today_str = datetime.now().strftime("%Y-%m-%d")
        all_dates = sorted(set(list(date_counts.keys()) + [today_str]), reverse=True)

        self.memo_date_filter_combo.blockSignals(True)
        self.memo_date_filter_combo.clear()
        self.memo_date_filter_combo.addItem(f"📅 전체 날짜 ({len(memos)}건)", "전체")

        selected_idx = 0
        for idx, d_str in enumerate(all_dates, start=1):
            cnt = date_counts.get(d_str, 0)
            lbl = f"📅 {self.format_memo_date_label(d_str)} · {cnt}건"
            self.memo_date_filter_combo.addItem(lbl, d_str)
            if self.memo_date_filter == d_str:
                selected_idx = idx

        if self.memo_date_filter != "전체" and selected_idx == 0:
            self.memo_date_filter = "전체"

        self.memo_date_filter_combo.setCurrentIndex(selected_idx)
        self.memo_date_filter_combo.blockSignals(False)

        # Update quick filter button styles
        is_all = (self.memo_date_filter == "전체")
        is_today = (self.memo_date_filter == today_str)
        active_style = """
            QPushButton {
                background: #6366F1; color: white; border-radius: 5px;
                padding: 0 7px; font-size: 10px; font-weight: bold; border: none;
            }
        """
        idle_style = """
            QPushButton {
                background: rgba(255,255,255,0.06); color: #94A3B8; border-radius: 5px;
                padding: 0 7px; font-size: 10px; border: none;
            }
            QPushButton:hover { background: rgba(255,255,255,0.14); color: #F8FAFC; }
        """
        self.memo_all_btn.setStyleSheet(active_style if is_all else idle_style)
        self.memo_today_btn.setStyleSheet(active_style if is_today else idle_style)

    def make_memo_preview_text(self, content: str, query: str) -> str:
        clean = re.sub(r"\s+", " ", (content or "").strip())
        if not clean:
            return "(내용 없음)"
        if query:
            idx = clean.lower().find(query.lower())
            if idx != -1:
                start = max(0, idx - 12)
                end = min(len(clean), idx + len(query) + 26)
                prefix = "..." if start > 0 else ""
                suffix = "..." if end < len(clean) else ""
                return f"🔎 {prefix}{clean[start:end]}{suffix}"
        return clean[:42] + ("..." if len(clean) > 42 else "")

    def render_memo_list(self):
        while self.memo_list_layout.count() > 1:
            child = self.memo_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.memo_card_refs.clear()

        memos = self.ensure_memos_valid()
        q = self.memo_search_query.strip().lower()

        filtered = []
        for m in memos:
            m_date = m.get("date", "")
            m_title = m.get("title", "") or "제목 없음"
            m_content = m.get("content", "")

            if self.memo_date_filter != "전체" and m_date != self.memo_date_filter:
                continue

            if q:
                haystack = f"{m_title} {m_content} {m_date}".lower()
                if q not in haystack:
                    continue

            filtered.append(m)

        filtered.sort(
            key=lambda x: (x.get("date", ""), x.get("updated_at", "")),
            reverse=True
        )

        if q:
            self.memo_count_lbl.setText(f"검색 {len(filtered)}건")
        else:
            self.memo_count_lbl.setText(f"총 {len(filtered)}건")

        if not filtered:
            msg = (
                f"'{self.memo_search_query}' 검색 결과가 없습니다 🔍"
                if q else "해당 날짜에 저장된 메모가 없습니다.\n우측 [+ 새 메모]를 눌러 작성해보세요 ✨"
            )
            empty_lbl = QLabel(msg)
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setWordWrap(True)
            empty_lbl.setStyleSheet("color: #64748B; font-size: 11px; padding: 24px 8px;")
            self.memo_list_layout.insertWidget(0, empty_lbl)
            return

        insert_pos = 0
        last_date = None

        for m in filtered:
            m_date = m.get("date", "")
            if m_date != last_date:
                last_date = m_date
                hdr = QLabel(f"📅 {self.format_memo_date_label(m_date)}")
                hdr.setStyleSheet("""
                    color: #A5B4FC; font-size: 10px; font-weight: bold;
                    padding: 3px 4px 1px 4px; background: transparent; border: none;
                """)
                self.memo_list_layout.insertWidget(insert_pos, hdr)
                insert_pos += 1

            mid = m["id"]
            c_idx = m.get("color_idx", 0)
            c_info = MEMO_COLORS[c_idx % len(MEMO_COLORS)]
            is_sel = (mid == self.current_memo_id)

            card = MemoCardWidget(mid)
            self.apply_memo_card_style(card, c_info["border"], is_sel)
            card.clicked.connect(self.select_memo_by_id)

            c_vbox = QVBoxLayout(card)
            c_vbox.setContentsMargins(8, 5, 8, 5)
            c_vbox.setSpacing(2)

            top_line = QHBoxLayout()
            top_line.setSpacing(6)

            t_text = m.get("title") or "제목 없음"
            title_lbl = QLabel(t_text)
            title_lbl.setStyleSheet(
                f"color: {'#FFFFFF' if is_sel else '#F1F5F9'}; "
                "font-size: 11px; font-weight: bold; border: none; background: transparent;"
            )
            top_line.addWidget(title_lbl, 1)

            upd = m.get("updated_at", "")
            meta_lbl = QLabel(upd)
            meta_lbl.setStyleSheet("color: #64748B; font-size: 9px; border: none; background: transparent;")
            top_line.addWidget(meta_lbl)

            c_vbox.addLayout(top_line)

            prev_str = self.make_memo_preview_text(m.get("content", ""), self.memo_search_query.strip())
            preview_lbl = QLabel(prev_str)
            preview_lbl.setStyleSheet(
                f"color: {'#FDE68A' if q and q in (m.get('content', '').lower()) else '#94A3B8'}; "
                "font-size: 10px; border: none; background: transparent;"
            )
            c_vbox.addWidget(preview_lbl)

            self.memo_list_layout.insertWidget(insert_pos, card)
            insert_pos += 1

            self.memo_card_refs[mid] = {
                "card": card,
                "title_lbl": title_lbl,
                "preview_lbl": preview_lbl,
                "meta_lbl": meta_lbl,
                "border_color": c_info["border"],
            }

    def apply_memo_card_style(self, card: QFrame, border_color: str, is_selected: bool):
        if is_selected:
            card.setStyleSheet(f"""
                MemoCardWidget {{
                    background: rgba(99, 102, 241, 0.20);
                    border: 1px solid #6366F1;
                    border-left: 4px solid {border_color};
                    border-radius: 6px;
                }}
            """)
        else:
            card.setStyleSheet(f"""
                MemoCardWidget {{
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid rgba(255, 255, 255, 0.07);
                    border-left: 3px solid {border_color};
                    border-radius: 6px;
                }}
                MemoCardWidget:hover {{
                    background: rgba(255, 255, 255, 0.09);
                }}
            """)

    def refresh_memo_ui(self):
        cur = self.get_current_memo()
        self.update_memo_date_filter_combo()
        self.render_memo_list()
        self.load_memo_into_editor(cur)

    def load_memo_into_editor(self, memo: dict):
        self.memo_date_edit.blockSignals(True)
        try:
            dt = datetime.strptime(memo.get("date", ""), "%Y-%m-%d").date()
            self.memo_date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        except Exception:
            self.memo_date_edit.setDate(QDate.currentDate())
        self.memo_date_edit.blockSignals(False)

        self.memo_title_edit.blockSignals(True)
        self.memo_title_edit.setText(memo.get("title", ""))
        self.memo_title_edit.blockSignals(False)

        self.memo_editor.blockSignals(True)
        self.memo_editor.setPlainText(memo.get("content", ""))
        self.memo_editor.blockSignals(False)

        self.apply_memo_theme(memo.get("color_idx", 0))
        self.highlight_memo_search_in_editor()

    def highlight_memo_search_in_editor(self):
        selections = []
        q = self.memo_search_query.strip()
        if q:
            doc = self.memo_editor.document()
            cursor = QTextCursor(doc)
            fmt = QTextCharFormat()
            fmt.setBackground(QColor("#F59E0B"))
            fmt.setForeground(QColor("#0F172A"))
            while True:
                cursor = doc.find(q, cursor)
                if cursor.isNull():
                    break
                sel = QTextEdit.ExtraSelection()
                sel.cursor = cursor
                sel.format = fmt
                selections.append(sel)
        self.memo_editor.setExtraSelections(selections)

    def apply_memo_theme(self, color_idx: int):
        c = MEMO_COLORS[color_idx % len(MEMO_COLORS)]
        self.memo_editor.setStyleSheet(f"""
            QTextEdit {{
                background: {c['bg']};
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }}
        """)

    def select_memo_by_id(self, memo_id: str):
        if not memo_id:
            return
        self.current_memo_id = memo_id
        cur = self.get_current_memo()
        for mid, ref in self.memo_card_refs.items():
            is_sel = (mid == self.current_memo_id)
            self.apply_memo_card_style(ref["card"], ref["border_color"], is_sel)
            ref["title_lbl"].setStyleSheet(
                f"color: {'#FFFFFF' if is_sel else '#F1F5F9'}; "
                "font-size: 11px; font-weight: bold; border: none; background: transparent;"
            )
        self.load_memo_into_editor(cur)

    def on_memo_search_changed(self, text: str):
        self.memo_search_query = text
        self.memo_search_clear_btn.setVisible(bool(text.strip()))
        self.render_memo_list()
        self.highlight_memo_search_in_editor()

    def clear_memo_search(self):
        self.memo_search_input.clear()

    def set_memo_date_filter(self, d_filter: str):
        self.memo_date_filter = d_filter
        self.update_memo_date_filter_combo()
        self.render_memo_list()

    def on_memo_date_filter_changed(self, idx: int):
        if idx < 0:
            return
        val = self.memo_date_filter_combo.itemData(idx)
        if val:
            self.memo_date_filter = val
            self.update_memo_date_filter_combo()
            self.render_memo_list()

    def on_memo_date_edited(self, qdate: QDate):
        cur = self.get_current_memo()
        new_date_str = qdate.toString("yyyy-MM-dd")
        if cur.get("date") != new_date_str:
            cur["date"] = new_date_str
            cur["updated_at"] = datetime.now().strftime("%H:%M")
            if self.memo_date_filter != "전체" and self.memo_date_filter != new_date_str:
                self.memo_date_filter = new_date_str
            self.dm.save()
            self.update_memo_date_filter_combo()
            self.render_memo_list()

    def on_memo_title_edited(self, new_title: str):
        cur = self.get_current_memo()
        cur["title"] = new_title
        cur["updated_at"] = datetime.now().strftime("%H:%M")
        self.dm.save()
        if self.memo_search_query.strip():
            self.render_memo_list()
        elif cur["id"] in self.memo_card_refs:
            ref = self.memo_card_refs[cur["id"]]
            ref["title_lbl"].setText(new_title or "제목 없음")
            ref["meta_lbl"].setText(cur["updated_at"])

    def on_memo_content_changed(self):
        cur = self.get_current_memo()
        cur["content"] = self.memo_editor.toPlainText()
        cur["updated_at"] = datetime.now().strftime("%H:%M")
        self.dm.save()
        if self.memo_search_query.strip():
            self.render_memo_list()
            self.highlight_memo_search_in_editor()
        elif cur["id"] in self.memo_card_refs:
            ref = self.memo_card_refs[cur["id"]]
            ref["preview_lbl"].setText(self.make_memo_preview_text(cur["content"], ""))
            ref["meta_lbl"].setText(cur["updated_at"])

    def set_memo_color(self, color_idx: int):
        cur = self.get_current_memo()
        cur["color_idx"] = color_idx
        self.apply_memo_theme(color_idx)
        self.dm.save()
        if cur["id"] in self.memo_card_refs:
            c_info = MEMO_COLORS[color_idx % len(MEMO_COLORS)]
            ref = self.memo_card_refs[cur["id"]]
            ref["border_color"] = c_info["border"]
            self.apply_memo_card_style(ref["card"], c_info["border"], True)

    def create_new_memo(self):
        memos = self.ensure_memos_valid()
        target_date = (
            self.memo_date_filter
            if self.memo_date_filter != "전체"
            else datetime.now().strftime("%Y-%m-%d")
        )
        same_day_cnt = sum(1 for m in memos if m.get("date") == target_date)
        new_memo = {
            "id": str(uuid.uuid4()),
            "title": f"{target_date[5:]} 메모 {same_day_cnt + 1}",
            "content": "",
            "color_idx": len(memos) % len(MEMO_COLORS),
            "date": target_date,
            "updated_at": datetime.now().strftime("%H:%M")
        }
        memos.append(new_memo)
        self.current_memo_id = new_memo["id"]
        if self.memo_search_query.strip():
            self.memo_search_input.clear()
        self.dm.save()
        self.refresh_memo_ui()
        self.memo_title_edit.setFocus()
        self.memo_title_edit.selectAll()

    def delete_current_memo(self):
        memos = self.ensure_memos_valid()
        if len(memos) <= 1:
            memos[0]["content"] = ""
            memos[0]["title"] = "기본 메모"
            memos[0]["date"] = datetime.now().strftime("%Y-%m-%d")
            memos[0]["updated_at"] = datetime.now().strftime("%H:%M")
            self.current_memo_id = memos[0]["id"]
        else:
            memos[:] = [m for m in memos if m["id"] != self.current_memo_id]
            self.current_memo_id = memos[-1]["id"]
        self.dm.save()
        self.refresh_memo_ui()

    # ---------------------------------------------------------
    # Page 5: Pomodoro & Custom Timer (Horizontal Layout)
    # ---------------------------------------------------------
    def build_timer_page(self):
        page = QWidget()
        h_layout = QHBoxLayout(page)
        h_layout.setContentsMargins(20, 8, 20, 8)
        h_layout.setSpacing(24)

        h_layout.addStretch()

        self.circle_timer = CircularTimerWidget()
        h_layout.addWidget(self.circle_timer)

        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        right_col.setSpacing(12)

        preset_row = QHBoxLayout()
        preset_row.setSpacing(8)
        presets = [
            ("🍅 집중 25분", 25, "집중 타이머 (25분)", "#6366F1"),
            ("☕ 짧은 휴식 5분", 5, "짧은 휴식 (5분)", "#10B981"),
            ("🛋️ 긴 휴식 15분", 15, "긴 휴식 (15분)", "#3B82F6"),
        ]
        for label, mins, mode_str, color in presets:
            b = QPushButton(label)
            b.setFixedHeight(30)
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255,255,255,0.07); color: #E2E8F0;
                    border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;
                    padding: 0 12px; font-size: 11px; font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {color}; color: white; border-color: {color};
                }}
            """)
            b.clicked.connect(lambda checked, m=mins, ms=mode_str, c=color: self.set_timer_preset(m, ms, c))
            preset_row.addWidget(b)
        right_col.addLayout(preset_row)

        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(10)

        self.timer_start_btn = QPushButton("▶ 시작")
        self.timer_start_btn.setFixedSize(110, 32)
        self.timer_start_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timer_start_btn.setStyleSheet("""
            QPushButton {
                background: #6366F1; color: white; border-radius: 8px;
                font-size: 12px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #4F46E5; }
        """)
        self.timer_start_btn.clicked.connect(self.toggle_timer)
        ctrl_row.addWidget(self.timer_start_btn)

        reset_btn = QPushButton("↺ 초기화")
        reset_btn.setFixedSize(90, 32)
        reset_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        reset_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.08); color: #CBD5E1; border-radius: 8px;
                font-size: 12px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: rgba(255,255,255,0.16); color: white; }
        """)
        reset_btn.clicked.connect(self.reset_timer)
        ctrl_row.addWidget(reset_btn)

        ctrl_row.addSpacing(12)

        lbl_custom = QLabel("직접 설정(분):")
        lbl_custom.setStyleSheet("color: #94A3B8; font-size: 11px;")
        ctrl_row.addWidget(lbl_custom)

        self.custom_min_spin = QSpinBox()
        self.custom_min_spin.setRange(1, 180)
        self.custom_min_spin.setValue(30)
        self.custom_min_spin.setFixedSize(54, 28)
        self.custom_min_spin.setStyleSheet("""
            QSpinBox {
                background: rgba(255,255,255,0.08); color: white;
                border: 1px solid rgba(255,255,255,0.15); border-radius: 5px; padding-left: 6px; font-size: 11px;
            }
        """)
        ctrl_row.addWidget(self.custom_min_spin)

        apply_custom_btn = QPushButton("적용")
        apply_custom_btn.setFixedSize(46, 28)
        apply_custom_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        apply_custom_btn.setStyleSheet(self.primary_btn_style())
        apply_custom_btn.clicked.connect(
            lambda: self.set_timer_preset(
                self.custom_min_spin.value(),
                f"커스텀 ({self.custom_min_spin.value()}분)",
                "#F59E0B"
            )
        )
        ctrl_row.addWidget(apply_custom_btn)

        ctrl_row.addSpacing(10)

        self.pomo_count_lbl = QLabel(f"🔥 누적 완료: {self.dm.data.get('pomodoro_count', 0)}회")
        self.pomo_count_lbl.setStyleSheet("color: #FBBF24; font-size: 12px; font-weight: bold;")
        ctrl_row.addWidget(self.pomo_count_lbl)

        ctrl_row.addStretch()
        right_col.addLayout(ctrl_row)

        h_layout.addLayout(right_col)
        h_layout.addStretch()

        self.update_timer_display()
        return page

    def set_timer_preset(self, minutes: int, label: str, color: str):
        self.timer_running = False
        self.timer_total_sec = minutes * 60
        self.timer_remain_sec = self.timer_total_sec
        self.timer_mode_label = label
        self.timer_color = color
        self.timer_start_btn.setText("▶ 시작")
        self.update_timer_display()

    def toggle_timer(self):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.timer_start_btn.setText("⏸ 일시정지")
        else:
            self.timer_start_btn.setText("▶ 계속")

    def reset_timer(self):
        self.timer_running = False
        self.timer_remain_sec = self.timer_total_sec
        self.timer_start_btn.setText("▶ 시작")
        self.update_timer_display()

    def tick_timer(self):
        if not self.timer_running:
            return
        if self.timer_remain_sec > 0:
            self.timer_remain_sec -= 1
            self.update_timer_display()
        if self.timer_remain_sec == 0:
            self.timer_running = False
            self.timer_start_btn.setText("▶ 시작")
            self.dm.data["pomodoro_count"] = self.dm.data.get("pomodoro_count", 0) + 1
            self.dm.save()
            self.pomo_count_lbl.setText(f"🔥 누적 완료: {self.dm.data['pomodoro_count']}회")
            try:
                winsound.Beep(880, 300)
                winsound.Beep(1174, 400)
            except Exception:
                pass
            self.timer_remain_sec = self.timer_total_sec
            self.update_timer_display()

    def update_timer_display(self):
        mins, secs = divmod(self.timer_remain_sec, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        prog = self.timer_remain_sec / self.timer_total_sec if self.timer_total_sec > 0 else 0
        self.circle_timer.set_state(prog, time_str, self.timer_mode_label, self.timer_color)

    # ---------------------------------------------------------
    # Shared Helpers, Clock, Weather & Window Dragging
    # ---------------------------------------------------------
    def init_timers(self):
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.on_second_tick)
        self.clock_timer.start(1000)

        self.ticker_timer = QTimer(self)
        self.ticker_timer.timeout.connect(self.next_ticker_mail)
        self.ticker_timer.start(6000)

        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.refresh_weather)
        self.weather_timer.start(30 * 60 * 1000)

        self.mail_timer = QTimer(self)
        self.mail_timer.timeout.connect(self.refresh_outlook_mails)
        self.mail_timer.start(2 * 60 * 1000)

        self.opic_timer = QTimer(self)
        self.opic_timer.timeout.connect(self.show_opic_challenge)
        self.opic_timer.start(60 * 60 * 1000)  # 1시간(3,600,000ms)마다 오픽 문장 표시
        QTimer.singleShot(1500, self.show_opic_challenge)

    def on_second_tick(self):
        self.update_clock()
        self.tick_timer()

    def update_clock(self):
        now = datetime.now()
        self.time_lbl.setText(now.strftime("%H:%M:%S"))
        dow = SHORT_WEEKDAYS[now.weekday()]
        self.date_lbl.setText(f"{now.month:02d}.{now.day:02d}({dow})")

    def on_city_changed(self, city_name: str):
        self.dm.data["city"] = city_name
        self.dm.save()
        self.refresh_weather()

    def refresh_weather(self):
        city = self.city_combo.currentText()
        self.weather_worker = WeatherWorker(city)
        self.weather_worker.finished.connect(self.on_weather_loaded)
        self.weather_worker.start()

    def on_weather_loaded(self, res: dict):
        if res.get("ok"):
            city_name = res.get("city", "경남 창원")
            self.weather_main_lbl.setText(f"{res['icon']} {res['temp']}°C ({res['desc']})")

            sat = res.get("sat")
            sun = res.get("sun")
            if sat and sun:
                sat_short = f"토{sat['icon']}{int(round(sat['min']))}~{int(round(sat['max']))}°"
                sun_short = f"일{sun['icon']}{int(round(sun['min']))}~{int(round(sun['max']))}°"
                self.weather_weekend_lbl.setText(f"주말 {sat_short} · {sun_short}")

                sat_md = sat["date"][5:].replace("-", "/")
                sun_md = sun["date"][5:].replace("-", "/")
                wk_tip = (
                    f"[{city_name} 현재 날씨]\n"
                    f"• 현재: {res['icon']} {res['temp']}°C ({res['desc']})\n"
                    f"• 오늘 최고 {res['max']}°C / 최저 {res['min']}°C · 습도 {res['humidity']}%\n\n"
                    f"[{city_name} 이번 주말 날씨]\n"
                    f"• 토요일({sat_md}): {sat['icon']} {sat['desc']} (최저 {sat['min']}°C / 최고 {sat['max']}°C)\n"
                    f"• 일요일({sun_md}): {sun['icon']} {sun['desc']} (최저 {sun['min']}°C / 최고 {sun['max']}°C)"
                )
                self.weather_main_lbl.setToolTip(wk_tip)
                self.weather_weekend_lbl.setToolTip(wk_tip)

                if hasattr(self, "cal_weekend_lbl"):
                    self.cal_weekend_lbl.setText(
                        f"🌤️ 주말({city_name})  토({sat_md}) {sat['icon']} {sat['min']}°/{sat['max']}° ({sat['desc']})  ·  "
                        f"일({sun_md}) {sun['icon']} {sun['min']}°/{sun['max']}° ({sun['desc']})"
                    )
                    self.cal_weekend_lbl.setToolTip(wk_tip)
            else:
                self.weather_main_lbl.setToolTip(f"최고 {res['max']}°C / 최저 {res['min']}°C · 습도 {res['humidity']}%")
                self.weather_weekend_lbl.setText("주말 예보 없음")
        else:
            self.weather_main_lbl.setText("🌤️ --°C")
            self.weather_weekend_lbl.setText("주말 --")

    def on_opacity_changed(self, value: int):
        self.bg_alpha = int(value * 2.55)
        self.opacity_slider.setToolTip(f"투명도: {value}%")
        self.dm.data["opacity"] = value
        self.dm.save()
        self.update()

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.dm.data["always_on_top"] = self.always_on_top
        self.dm.save()
        self.update_pin_style()
        self.update_window_flags()

    def update_pin_style(self):
        if self.always_on_top:
            self.pin_btn.setToolTip("항상 위 고정 켜짐 (클릭하여 해제)")
            self.pin_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(99, 102, 241, 0.35); color: white;
                    border: 1px solid #6366F1; border-radius: 6px; font-size: 10px;
                }
            """)
        else:
            self.pin_btn.setToolTip("항상 위 고정 꺼짐 (클릭하여 고정)")
            self.pin_btn.setStyleSheet(self.icon_btn_style())

    def icon_btn_style(self):
        return """
            QPushButton {
                background: rgba(255,255,255,0.06); color: #CBD5E1;
                border-radius: 6px; font-size: 10px; border: none;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.15); color: white;
            }
        """

    def input_style(self):
        return """
            QLineEdit {
                background: rgba(255, 255, 255, 0.07);
                color: #F8FAFC;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                padding: 0 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
                background: rgba(255, 255, 255, 0.1);
            }
        """

    def primary_btn_style(self):
        return """
            QPushButton {
                background: #6366F1; color: white;
                border-radius: 6px; padding: 0 10px;
                font-size: 11px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #4F46E5; }
        """

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.drag_pos is not None:
            self.drag_pos = None
            pos = self.pos()
            self.dm.data["topbar_pos"] = [pos.x(), pos.y()]
            self.dm.save()

    def closeEvent(self, event):
        pos = self.pos()
        self.dm.data["topbar_pos"] = [pos.x(), pos.y()]
        self.dm.save()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Malgun Gothic", 10))
    widget = DesktopWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
