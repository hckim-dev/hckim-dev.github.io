"""Standard-library-only static HTML generation. Run from any directory."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GH = "https://github.com/hckim-dev/"
IMAGE_SIZES = {
    "fan": (825, 1100),
    "recycling": (825, 1100),
    "recycling-ui": (1500, 846),
    "monitoring": (825, 1100),
    "monitoring-ui": (717, 929),
    "fpga": (1383, 1100),
    "avr": (1320, 1100),
    "pokedex": (564, 1100),
}
PROJECTS = [
    dict(
        slug="smart-fan",
        repo="jetson-smart-fan-controller",
        title="Jetson Smart Fan Controller",
        label="01 / LINUX DEVICE CONTROL",
        kind="개인 · 교육 프로젝트",
        image="fan",
        alt="Jetson Orin Nano와 모터, 엔코더, LCD를 연결한 스마트 선풍기 실물",
        message="장치 제어부터 장애 시 정지까지",
        summary="Linux Kernel Driver와 사용자 프로그램의 역할을 분리하고, 센서 오류와 heartbeat 중단을 고려한 스마트 선풍기입니다.",
        role="Kernel Driver, 제어 앱, 센서 IPC 및 검증 구현",
        tags=["C11", "Linux", "ioctl", "Process / Thread"],
        result="정상 동작과 오류·종료 경로의 소프트웨어 회귀 검증 기록",
        demo="../../assets/fan-demo.mp4",
        doc="docs/architecture.md",
        review="docs/review.md",
        flow=[
            ("센서 → 사용자 공간", "BMP180 process → pipe → fanctl"),
            ("정책 → 커널", "fanctl → ioctl → smartfan.ko"),
            ("출력 · 표시", "GPIO/PWM → 모터 · LED / LCD worker"),
        ],
        scope="개인 프로젝트로 드라이버·사용자 제어 앱·센서 IPC를 구현했습니다. 드라이버는 기존 Linux GPIO/PWM provider를 재사용하며, 운전 정책은 사용자 공간에 둡니다.",
        decisions=[
            (
                "출력과 보호 정지의 소유권",
                "커널이 GPIO/PWM 출력과 lease·연속 구동 제한을 관리합니다. 앱의 제어 루프가 중단되는 경우를 고려해 정지 정책을 분리했습니다.",
            ),
            (
                "Blocking I/O를 제어 경로에서 분리",
                "BMP180 측정은 별도 process와 pipe, LCD·로그는 worker thread로 처리합니다. 제어 상태 변경은 main에 모으고 worker에는 snapshot을 전달합니다.",
            ),
            (
                "복구와 재기동을 구분",
                "센서 fault/stale 또는 보호 정지 후 정상 샘플만으로 다시 기동하지 않습니다. 사용자의 명시적인 ON을 요구합니다.",
            ),
        ],
        problem=[
            (
                "현상",
                "상태 조회 뒤 AUTO 출력을 갱신하기 전에 보호 정지가 개입하면, 오래된 상태를 근거로 재기동할 수 있었습니다.",
            ),
            ("원인 파악", "GET snapshot과 출력 변경 사이의 경쟁 경로를 확인했습니다."),
            (
                "수정",
                "SET_AUTO에서 차단 상태·샘플 freshness·rearm 조건을 출력 변경과 같은 kernel mutex 안에서 검증합니다.",
            ),
            (
                "확인 결과",
                "저장소에 AUTO·IPC·종료 경로 회귀 결과가 기록되어 있습니다. 최종 종료 경로 수정 후의 실물 재검증은 남아 있습니다.",
            ),
        ],
        verified="저장소 검증 문서: C 테스트 11개, CLI 37개, 정리·DT 제안 6개 통과. GCC analyzer, ASan/UBSan 및 ThreadSanitizer 검증 결과가 기록되어 있습니다. 기존 실물 통합 동작과 보호 정지 확인 보고가 있습니다.",
        limits="최종 종료 경로 수정 후 실물 재확인, LCD 대비, 전원 여유, RPM·발열·장기 반복 및 실제 suspend 측정은 남아 있습니다. 소프트웨어 테스트는 전기적 조건과 모든 동시 실행 순서를 보장하지 않습니다.",
    ),
    dict(
        slug="smart-recycling",
        repo="smart-recycling-edge-ai",
        title="Smart Recycling Edge AI",
        label="02 / SYSTEM INTEGRATION",
        kind="4인 팀 · 교육 프로젝트",
        image="recycling",
        alt="4구역 수거함과 분류 기구를 갖춘 재활용 키오스크 실물",
        message="인식·제어·서비스를 하나의 흐름으로",
        summary="재활용품 인식에서 분류 기구 제어, 키오스크 표시, 모바일 포인트 정산까지 연결한 Edge AI 시스템입니다.",
        role="전체 SW 아키텍처·통신 통합, 추론 파이프라인·Qt·정산 구현",
        tags=["Jetson", "TensorRT", "Qt / TCP", "FastAPI", "Android"],
        result="5개 서브시스템의 통합 시연과 최종 결과보고서 공개",
        demo="https://github.com/user-attachments/assets/a7b54b54-8b72-4728-b04c-dced2dc5ca10",
        doc="docs/protocol-spec.md",
        review="docs/presentation/smart_recycling_final_report.pdf",
        flow=[
            ("인식 → 제어", "Jetson ↔ UART ↔ STM32"),
            ("인식 → 화면", "Jetson → Binary TCP → Qt"),
            ("인증 → 정산", "Android ↔ REST / WebSocket ↔ FastAPI ↔ Qt"),
        ],
        scope="김호철: 전체 소프트웨어 아키텍처와 통신 프로토콜·통합 검증, TensorRT 비동기 파이프라인과 검출 누락 유예 FSM, Qt 바이너리 스트리밍 및 SQLite 정산 트랜잭션 구현. 팀 전체 결과와 개인 담당 범위를 구분합니다.",
        team="팀원 담당: AI 모델 벤치마크와 2-Stage 검사 모델(권민지), STM32 제어·초음파 센서 계측 및 서보 동작 튜닝(석민정), 키오스크 기구 설계·제작(현수근). 이 영역을 개인 단독 구현으로 소개하지 않습니다.",
        decisions=[
            (
                "통신 경계별 책임 분리",
                "장치 명령은 UART, 영상·검출 정보는 Binary TCP, 사용자 인증·정산은 REST API와 WebSocket으로 연결했습니다.",
            ),
            (
                "영상 검출과 도어 상태 집계를 분리",
                "화면의 반복 검출과 도어 상태 변화를 구분하고, 도어 개방의 rising edge를 카운팅에 사용해 반복 검출에 따른 중복 집계를 줄였습니다. 도어 개방 상태를 기준으로 한 집계이며 실제 물체의 낙하를 별도로 검증한 것은 아닙니다.",
            ),
            (
                "일시적 검출 누락을 상태로 처리",
                "검출이 한 프레임 사라졌다는 이유만으로 후보를 즉시 초기화하지 않고, 설정된 miss_tolerance를 넘었을 때 상태를 갱신합니다.",
            ),
        ],
        problem=[
            (
                "현상",
                "조명 변화나 블러로 검출이 잠시 끊기면 후보의 안정 감지 흐름이 초기화될 수 있었습니다.",
            ),
            (
                "원인 파악",
                "프레임 단위 검출 결과와 도어 제어 상태를 바로 연결한 경계를 확인했습니다.",
            ),
            (
                "수정",
                "DoorController에서 miss_count와 miss_tolerance로 누락을 유예하고, 같은 품목의 안정 감지 흐름을 유지하도록 구성했습니다.",
            ),
            (
                "확인 결과",
                "현재 소스에서 후보 유지·초기화 조건을 확인할 수 있고 통합 시연이 공개되어 있습니다. 개별 누락 시나리오의 정량 회귀 결과는 공개 자료에서 확인되지 않습니다.",
            ),
        ],
        verified="재질 인식·분류 기구·Qt 화면·QR 인증·포인트 정산을 연결한 팀 통합 시연과 2026.09.16 발표 보고서가 공개되어 있습니다. README 역할표와 보고서를 함께 확인했습니다.",
        limits="모델 성능은 팀의 데이터셋·시험 조건에 따른 결과입니다. 이 페이지는 별도의 FPS·지연 보장이나 상용 환경의 장기 신뢰성을 주장하지 않습니다. ",
    ),
    dict(
        slug="smart-monitoring",
        repo="smart-monitoring-system",
        title="Smart Monitoring System",
        label="03 / MCU TO REMOTE CONTROL",
        kind="개인 · 교육 프로젝트",
        image="monitoring",
        alt="STM32 보드와 서보, 팬, 가변저항을 연결한 모니터링 프로토타입",
        message="MCU의 데이터가 원격 제어로 이어지도록",
        summary="STM32 베어메탈 제어, Qt 중계, Android 원격 제어를 연결한 프로토타입입니다. 가스 입력은 가변저항으로 모사합니다.",
        role="STM32 펌웨어, Qt 관제 서버, Android 앱 구현·연동",
        tags=["STM32", "Bare-metal C", "UART / TCP", "Qt", "Kotlin"],
        result="자동 차단·모바일·현장 스위치·Qt 제어 통합 시연 공개",
        demo="../../assets/monitoring-demo.mp4",
        doc="docs/02_protocol_specification.md",
        review="docs/08_setup_and_operation_guide.md",
        flow=[
            ("계측 · 액추에이터", "가변저항 → ADC / STM32 → 서보·팬·LED"),
            ("중계 · 관제", "STM32 ↔ UART ↔ Qt"),
            ("원격 제어 · 영상", "Qt ↔ TCP ↔ Android / CameraX"),
        ],
        scope="개인 프로젝트로 STM32 레지스터 기반 펌웨어, Qt 관제 서버, Android 클라이언트와 통신 연동을 구현했습니다. 실제 가스 검지기가 아닌 가변저항 입력을 사용한 제어 프로토타입입니다.",
        decisions=[
            (
                "MCU·중계·모바일의 역할 분리",
                "STM32는 ADC와 액추에이터를 다루고, Qt는 UART/TCP 중계와 임계값 판단, Android는 영상 송신과 원격 명령을 담당합니다.",
            ),
            (
                "TCP의 메시지 경계를 명시",
                "JPEG 앞에 4바이트 Big-Endian 길이를 붙이고 수신 버퍼에 프레임이 완성될 때까지 기다립니다. UART의 계측값은 개행으로 구분합니다.",
            ),
            (
                "같은 제어 상태의 반복 적용 억제",
                "차단·복구 상태를 관리해 동일 명령으로 액추에이터를 반복 갱신하지 않도록 합니다. 현장 버튼과 원격 명령을 같은 상태 변경 경로에 연결합니다.",
            ),
        ],
        problem=[
            ("현상", "서보의 지시 각도와 실제 동작이 맞지 않는 문제가 있었습니다."),
            (
                "원인 파악",
                "APB1 버스 주파수와 TIM2 입력 클럭을 혼동해 PWM 분주 기준이 어긋난 경로를 확인했습니다.",
            ),
            (
                "수정",
                "타이머 입력 96 MHz에 맞춰 PSC=95, ARR=19999로 설정해 1 μs tick과 20 ms 주기를 구성했습니다.",
            ),
            (
                "확인 결과",
                "현재 timer.c 설정과 저장소 문제 해결 기록을 대조했습니다. 전체 차단·복구 시연이 공개되어 있으며 해당 설정의 최신 오실로스코프 계측 자료는 공개되어 있지 않습니다.",
            ),
        ],
        verified="저장소 시연은 가변저항 입력에 따른 자동 차단, Android 원격 명령, 물리 스위치, Qt GUI 제어를 다룹니다. UART/TCP 규약과 펌웨어·앱 기술 문서가 공개되어 있습니다.",
        limits="실제 가스 센서의 검출 정확도나 산업 안전 인증을 검증한 시스템은 아닙니다. 자동 차단 판단은 Qt에 있으며, 네트워크 단절 등 모든 장애 조건의 안전 동작을 보장하지 않습니다.",
    ),
]


def link(url, label, cls=""):
    return f'<a class="{cls}" href="{escape(url, quote=True)}">{label}</a>'


def photo(name, alt, prefix="", caption="", eager=False):
    src = f"{prefix}assets/{name}.webp"
    width, height = IMAGE_SIZES[name]
    return f'<figure class="detail-photo"><a class="zoom-link" href="{src}" aria-label="이미지 확대: {alt}"><img src="{src}" width="{width}" height="{height}" alt="{alt}" loading="{"eager" if eager else "lazy"}"></a><figcaption>{caption or "프로젝트 저장소의 실제 사진 · 클릭하여 확대"}</figcaption></figure>'


def shell(
    title,
    content,
    prefix="",
    description="장치 연동·통신 실무 경험을 바탕으로 MCU와 Linux 제어까지 확장하는 김호철의 포트폴리오.",
    canonical="",
):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 김호철</title><meta name="description" content="{description}"><meta name="theme-color" content="#f6f8fb"><meta property="og:title" content="{title} · 김호철"><meta property="og:description" content="{description}"><meta property="og:type" content="website"><link rel="canonical" href="https://hckim-dev.github.io/{canonical}"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"></head>
<body><a class="skip" href="#main">본문으로 건너뛰기</a><header class="header"><nav class="nav wrap" aria-label="주 메뉴"><a class="brand" href="{prefix}index.html"><span>HC.</span>김호철</a><button class="mobile-menu" aria-expanded="false" aria-controls="nav-links">메뉴</button><div class="nav-links" id="nav-links"><a href="{prefix}index.html#experience">실무 경험</a><a href="{prefix}index.html#projects">프로젝트</a><a href="{prefix}index.html#contact">연락처</a><a class="resume" href="{prefix}assets/resume.pdf">이력서 PDF ↗</a></div></nav></header>
{content}
<footer class="footer"><div class="wrap"><span>김호철 · Embedded &amp; Systems Software</span><span>자료 확인 2026.10.23 · {link(GH.rstrip("/"), "GitHub ↗")}</span></div></footer>
<dialog aria-label="프로젝트 이미지 확대"><div class="dialog-actions"><button type="button" class="zoom-toggle" aria-pressed="false">2배 확대</button><a class="original-image" target="_blank" rel="noopener">이미지 파일 열기 ↗</a><button type="button" class="dialog-close">닫기 ×</button></div><div class="image-viewport"><img alt=""></div><p></p></dialog></body></html>'''


def heading(number, en, title, text=""):
    return f'<div class="section-head"><div><div class="eyebrow">{number} / {en}</div><h2>{title}</h2></div><p>{text}</p></div>'


def home():
    content = """<main id="main" class="wrap"><section class="hero" aria-labelledby="hero-title"><div><div class="eyebrow">Embedded &amp; Systems Software</div><h1 id="hero-title">장치와 소프트웨어,<br><span>그 사이를 연결합니다.</span></h1><p class="lead">차량 진단과 센서 데이터 통신을 다룬 약 3년의 실무 경험.<br>MCU·Linux 제어 프로젝트로 장치에 대한 이해를 넓히고 있습니다.</p><p class="identity">김호철 <span>임베디드 · 시스템 SW 개발자</span></p><div class="actions"><a class="button" href="#projects">대표 프로젝트 보기 ↓</a><a class="button secondary" href="assets/resume.pdf">이력서 PDF ↗</a></div></div><figure class="hero-photo"><a class="zoom-link" href="assets/fan.webp" aria-label="스마트 선풍기 실물 이미지 확대"><img src="assets/fan.webp" width="825" height="1100" alt="Jetson과 모터·LCD·센서를 연결한 개인 스마트 선풍기 프로젝트 실물" fetchpriority="high"></a><figcaption><strong>직접 연결하고, 동작을 확인한 시스템</strong><span>Jetson Smart Fan</span></figcaption></figure></section>
<div class="summary-strip"><div><span>PROFESSIONAL EXPERIENCE</span><strong>3년 3개월 · 장치 연동 SW</strong></div><div><span>FROM DEVICE TO SERVICE</span><strong>통신 · 데이터 처리 · 제어</strong></div><div><span>ENGINEERING APPROACH</span><strong>설계 근거와 검증 범위</strong></div></div>
<section id="experience" class="section">"""
    content += heading(
        "01",
        "Experience",
        "현장에서 쌓은 연결의 경험",
        "Linux 응용 SW와 Android에서 장치의 데이터를 사용자 기능으로 연결했습니다.",
    )
    content += """<article class="experience"><div><h3>지아이티 <small>GIT</small></h3><p class="role">SW개발1팀 · 연구원</p><p class="date">2022.01 — 2024.02</p></div><div><h4>차량 진단 애플리케이션 · 장비 통신</h4><ul><li>Java/Kotlin 기반 Android 차량 진단 기능과 CAN·Ethernet 통신 모듈, 보안 제어기 데이터 위변조 검증 기능 개발</li><li>외부 센서·알고리즘을 연동한 소음 기반 진단 기능과 점검 결과 전송 기능 구현</li><li>국내·북미·유럽·중국 출시 및 브랜드별 빌드 대응. Hilt·Jetpack Compose 사내 세미나 진행</li></ul></div></article><article class="experience"><div><h3>브이유텍</h3><p class="role">영상보안개발팀 · 사원</p><p class="date">2020.08 — 2021.08</p></div><div><h4>Linux 센서·중계기 데몬 · 모니터링 SW</h4><ul><li>Raspberry Pi·Banana Pi·Jetson TX2에서 동작하는 Java 센서·중계기 프로그램 개발</li><li>Netty·Pi4J·BlueZ·TinyB를 활용해 센서 데이터 선별·파싱·서버 전송 구현. 변전소 2곳 시범사업 적용</li><li>Socket/XML·RTSP·FCM 기반 Android 화재안전 모니터링과 Bluetooth 리더기 연동 앱 개발</li></ul></div></article></section><section id="projects" class="section">"""
    content += heading(
        "02",
        "Selected projects",
        "설계에서 동작까지",
        "실무 이후의 교육·프로젝트 경험입니다. 개인 구현과 팀 기여, 검증 결과와 남은 조건을 함께 정리했습니다.",
    )
    for p in PROJECTS:
        content += f'''<article class="project"><div class="project-media"><img src="assets/{p["image"]}.webp" width="{IMAGE_SIZES[p["image"]][0]}" height="{IMAGE_SIZES[p["image"]][1]}" alt="{p["alt"]}" loading="lazy"></div><div class="project-body"><div class="project-kicker">{p["label"]} · {p["kind"]}</div><h3>{p["message"]}</h3><p>{p["title"]}</p><p class="role-line"><strong>본인 역할</strong> · {p["role"]}</p><div class="tags">{"".join(f"<span>{t}</span>" for t in p["tags"])}</div><p>{p["result"]}</p><a class="text-link" href="projects/{p["slug"]}/">{p["title"]} 상세 보기 →</a></div></article>'''
    content += (
        '</section><section class="section" id="more-projects">'
        + heading("03", "More projects", "기초를 넓힌 구현들")
        + '<div class="cards">'
    )
    extras = [
        (
            "fpga",
            "FPGA Microwave Oven",
            "fpga-microwave-oven",
            "Verilog · FSM · PWM · 테스트벤치",
            "시간 제어·도어 서보·모터 PWM·조작 잠금을 통합한 전자레인지 제어 모형. 동시 입력과 상태 전환의 경계 조건을 검증했습니다. 테스트벤치 16개 PASS 기록이 있으며, 가열 장치 없이 도어 위치는 명령·시간으로 추정합니다.",
            "Basys3에 버튼·로터리 인코더·서보·DC 모터를 연결한 전자레인지 제어 모형",
        ),
        (
            "avr",
            "AVR RTC · 계산기",
            "avr-rtc-calculator",
            "C · I²C · 오실로스코프",
            "DS1307 통신과 재귀 하향 수식 파서. SDA·SCL 계측에서 주소와 ACK/NACK을 해석했습니다. 파형과 현재 펌웨어의 버전 대응은 재확인이 필요합니다.",
            "I2C START와 장치 주소를 분석한 실제 오실로스코프 계측",
        ),
        (
            "pokedex",
            "PokeDex",
            "PokeDex",
            "Kotlin · MVI · Room",
            "Paging3와 Room을 연결한 로컬 캐시, 단방향 상태 관리, 계층별 테스트를 구성한 Android 앱입니다.",
            "PokeDex 앱의 포켓몬 목록 화면",
        ),
    ]
    for im, title, repo, tech, body, alt in extras:
        content += f'<article class="small-card"><img src="assets/{im}.webp" width="{IMAGE_SIZES[im][0]}" height="{IMAGE_SIZES[im][1]}" alt="{alt}" loading="lazy"><div class="project-kicker">개인 · 학습 프로젝트</div><h3>{title}</h3><p><strong>{tech}</strong></p><p>{body}</p>{link(GH + repo, "저장소 · 설계와 검증 ↗", "text-link")}</article>'
    content += (
        '</div></section><section class="section" id="skills">'
        + heading("04", "Skills & Learning", "경험에 연결된 기술")
        + """<div class="skills"><div><div class="skill-row"><strong>장치 통신 · 데이터 처리</strong><p>Java · Kotlin · Linux · CAN · Ethernet · Bluetooth<br>지아이티 차량 진단 / 브이유텍 센서·중계기 실무</p></div><div class="skill-row"><strong>MCU · Linux 제어</strong><p>C · C++ · STM32 · AVR · ioctl · IPC<br>스마트 선풍기 / 모니터링 / RTC·계산기 프로젝트</p></div><div class="skill-row"><strong>시스템 통합 · 사용자 화면</strong><p>Qt · Python · TensorRT · FastAPI · Android<br>재활용 키오스크 / 모니터링 / PokeDex 프로젝트</p></div><div class="skill-row"><strong>디지털 논리 · 검증</strong><p>Verilog · FSM · 테스트벤치 · Vivado<br>FPGA Microwave Oven 학습 프로젝트</p></div></div><div class="education"><div class="eyebrow">Education · Qualifications</div><h3>AI 시스템반도체 SW 개발자 과정 2기</h3><p>대한상공회의소 서울인력개발원<br>2026.05.27 — 2026.12.16 · 교육 중</p><p>MCU·통신, Linux 시스템·드라이버, Qt, Edge AI, FPGA·Verilog 실습</p><hr><p><strong>장안대학교 인터넷정보통신과 · 3년제</strong><br>2015.03 — 2021.02 · 졸업<br>학점 3.95 / 4.5</p><p><strong>자격 · 어학</strong><br>정보처리산업기사 · 네트워크관리사 2급 · JLPT N1</p></div></div></section><section class="contact" id="contact"><div class="eyebrow">05 / Contact</div><h2>함께 연결할 다음 시스템을 기다립니다.</h2><a class="email" href="mailto:yp0504@naver.com">yp0504@naver.com ↗</a><div class="actions"><a class="button" href="assets/resume.pdf">이력서 PDF 열기 ↗</a><a class="button secondary" href="https://github.com/hckim-dev?tab=repositories">GitHub 전체 저장소 ↗</a></div></section></main>"""
    )
    return shell("임베디드 · 시스템 SW 포트폴리오", content)


def detail(p):
    prefix = "../../"
    content = f"""<main id="main" class="wrap"><header class="detail-head"><div class="breadcrumb"><a href="../../index.html#projects">포트폴리오</a> / {p["title"]}</div><div class="eyebrow">{p["label"]}</div><h1>{p["title"]}</h1><p class="lead">{p["summary"]}</p><div class="meta"><div><strong>프로젝트 구분</strong>{p["kind"]}</div><div><strong>본인 역할</strong>{p["role"]}</div></div><div class="actions">{link(p["demo"], "시연 영상 열기 ↗", "button")}{link(GH + p["repo"], "소스 코드 ↗", "button secondary")}</div></header><div class="detail-layout"><nav class="side-nav" aria-label="프로젝트 목차"><a href="#overview">01 프로젝트 · 역할</a><a href="#architecture">02 시스템 구조</a><a href="#design">03 설계 판단</a><a href="#problem">04 문제 해결</a><a href="#verification">05 검증과 한계</a><a href="#resources">06 관련 자료</a></nav><div><section id="overview" class="detail-section"><h2>01. 프로젝트와 본인 역할</h2><p>{p["scope"]}</p>"""
    if p.get("team"):
        content += f'<div class="note">{p["team"]}</div>'
    content += (
        '<div style="margin-top:24px">'
        + photo(p["image"], p["alt"], prefix, eager=True)
        + "</div></section>"
    )
    if p["slug"] in ["smart-recycling", "smart-monitoring"]:
        ui = "recycling-ui" if p["slug"] == "smart-recycling" else "monitoring-ui"
        content += photo(
            ui,
            "재활용 키오스크 실제 검출 화면"
            if p["slug"] == "smart-recycling"
            else "Qt 관제 서버 실제 화면",
            prefix,
            "프로젝트 저장소의 실제 UI 화면 · 클릭하여 확대",
        )
    content += (
        '<section id="architecture" class="detail-section"><h2>02. 시스템 구조</h2><div class="flow">'
        + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in p["flow"])
        + '</div><p class="source-note">저장소의 시스템 구조를 요약한 설명입니다. 각 블록은 데이터·제어 경로를 나타냅니다.</p></section>'
    )
    content += (
        '<section id="design" class="detail-section"><h2>03. 핵심 설계 판단</h2>'
        + "".join(f"<h3>{a}</h3><p>{b}</p>" for a, b in p["decisions"])
        + "</section>"
    )
    content += (
        '<section id="problem" class="detail-section"><h2>04. 문제 해결 사례</h2><ol class="steps">'
        + "".join(f"<li><strong>{a}</strong><p>{b}</p></li>" for a, b in p["problem"])
        + "</ol></section>"
    )
    content += f'<section id="verification" class="detail-section"><h2>05. 검증 결과와 한계</h2><h3>공개 자료에서 확인한 결과</h3><p>{p["verified"]}</p><div class="note"><strong>확인 범위</strong><br>{p["limits"]}</div></section>'
    content += (
        '<section id="resources" class="detail-section"><h2>06. 관련 자료</h2><div class="resources">'
        + link(GH + p["repo"], "저장소 ↗", "button secondary")
        + link(
            GH + p["repo"] + "/blob/HEAD/" + p["doc"],
            "설계 · 통신 문서 ↗",
            "button secondary",
        )
        + link(
            GH + p["repo"] + "/blob/HEAD/" + p["review"],
            "결과보고서 ↗" if p["slug"] == "smart-recycling" else "검증 · 실행 문서 ↗",
            "button secondary",
        )
        + '</div><p class="source-note">사진·시연·기술 근거: 프로젝트 공개 저장소. 사진은 웹 열람을 위해 크기와 형식을 조정했습니다. 외부 영상은 링크에서 직접 재생할 수 있습니다.</p></section><div class="detail-contact"><h2>경력과 다른 프로젝트도 확인해 보세요.</h2><div class="actions"><a class="button" href="../../assets/resume.pdf">이력서 PDF 열기 ↗</a><a class="button secondary" href="mailto:yp0504@naver.com">이메일로 연락하기 ↗</a></div><a class="text-link" href="../../index.html#projects">← 대표 프로젝트 목록으로</a></div></div></div></main>'
    )
    return shell(
        p["title"], content, prefix, p["summary"], "projects/" + p["slug"] + "/"
    )


if __name__ == "__main__":
    (ROOT / "index.html").write_text(home(), encoding="utf-8")
    for p in PROJECTS:
        folder = ROOT / "projects" / p["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(detail(p), encoding="utf-8")
    print("Generated 4 static HTML pages.")
