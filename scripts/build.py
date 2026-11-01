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
    "tensorrps": (636, 476),
    "avr-car": (825, 1100),
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
                "AUTO 제어·센서 IPC·종료 경로의 회귀 검증을 수행하고, 결과를 저장소에 정리했습니다.",
            ),
        ],
        verified="C 테스트 11개, CLI 37개, 정리·DT 제안 6개를 통과했습니다. GCC analyzer와 ASan/UBSan·ThreadSanitizer로 정적 분석·메모리·동시성 검사를 수행했습니다. 모터·엔코더·센서·LCD의 통합 동작과 보호 정지 확인 기록을 함께 정리했습니다.",
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
        scope="전체 소프트웨어 아키텍처와 통신 프로토콜을 설계하고 통합을 담당했습니다. TensorRT 추론과 검출 누락 유예 FSM, Qt 바이너리 스트리밍, FastAPI·SQLite 기반 배출 이력·포인트 처리를 구현했습니다.",
        team="팀원 담당: AI 모델 벤치마크와 2-Stage 검사 모델(권민지), STM32 제어·초음파 센서 계측 및 서보 동작 튜닝(석민정), 키오스크 기구 설계·제작(현수근).",
        decisions=[
            (
                "통신 경계별 책임 분리",
                "장치 명령은 UART, 영상·검출 정보는 Binary TCP, 사용자 인증·정산은 REST API와 WebSocket으로 연결했습니다.",
            ),
            (
                "영상 검출과 도어 상태 집계를 분리",
                "Qt에서 도어 상태의 CLOSED → OPEN 전이마다 수량을 집계합니다. 프레임별 반복 검출과 도어 상태 변화를 분리해, 같은 개방 상태가 여러 번 집계되는 것을 방지했습니다.",
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
                "후보 유지·초기화 조건을 DoorController에 구현했습니다. 인식·분류·키오스크·정산을 연결한 통합 시연을 공개했습니다.",
            ),
        ],
        verified="재질 인식·분류 기구·Qt 키오스크·QR 사용자 연결·포인트 정산까지 5개 서브시스템을 통합했습니다. 전체 동작은 공개 시연과 2026.09.16 최종 발표 보고서에서 확인할 수 있습니다.",
    ),
    dict(
        slug="smart-monitoring",
        repo="smart-monitoring-system",
        title="Smart Monitoring System",
        label="03 / MCU TO REMOTE CONTROL",
        kind="개인 · 교육 프로젝트",
        image="monitoring",
        card_image="monitoring-ui",
        card_alt="현장 영상·입력값 차트·원격 제어를 통합한 Qt 관제 화면",
        alt="STM32 보드와 서보, 팬, 가변저항을 연결한 모니터링 프로토타입",
        message="MCU의 데이터가 원격 제어로 이어지도록",
        summary="STM32 베어메탈 펌웨어, Qt 관제 서버, Android 앱을 연결해 계측·자동 차단·원격 제어·현장 영상을 한 흐름으로 구성했습니다.",
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
        scope="STM32 레지스터 기반 펌웨어, Qt 관제 서버, Android 클라이언트를 직접 구현하고 UART·TCP로 연동했습니다. 가변저항으로 입력을 조절하고 서보·팬·LED를 연결해 자동 차단과 수동 복구 흐름을 구성했습니다.",
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
                "timer.c에 96 MHz 기준 PWM 설정을 반영했습니다. 자동 차단, 원격 명령, 현장 버튼과 Qt GUI를 통한 차단·복구 동작을 시연했습니다.",
            ),
        ],
        verified="입력값에 따른 자동 차단과 Android·현장 버튼·Qt GUI의 수동 제어를 연동했습니다. 스마트폰 카메라 영상, 센서 차트, CSV 기록을 하나의 관제 화면에 구성했으며, 전체 시연과 UART/TCP 규약·펌웨어·앱 문서를 공개했습니다.",
    ),
]


def link(url, label, cls="", aria_label=""):
    aria = f' aria-label="{escape(aria_label, quote=True)}"' if aria_label else ""
    return f'<a class="{cls}" href="{escape(url, quote=True)}"{aria}>{label}</a>'


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
<footer class="footer"><div class="wrap"><span>김호철 · Embedded &amp; Systems Software</span><span>{link(GH + "hckim-dev.github.io/blob/master/docs/SOURCES.md", "콘텐츠 근거 ↗")} · {link(GH.rstrip("/"), "GitHub ↗")}</span></div></footer>
<dialog aria-label="프로젝트 이미지 확대"><div class="dialog-actions"><button type="button" class="zoom-toggle" aria-pressed="false">2배 확대</button><a class="original-image" target="_blank" rel="noopener">이미지 파일 열기 ↗</a><button type="button" class="dialog-close">닫기 ×</button></div><div class="image-viewport"><img alt=""></div><p></p></dialog></body></html>'''


def heading(number, en, title, text=""):
    return f'<div class="section-head"><div><div class="eyebrow">{number} / {en}</div><h2>{title}</h2></div><p>{text}</p></div>'


def home():
    content = """<main id="main" class="wrap"><section class="hero" aria-labelledby="hero-title"><div><div class="eyebrow">Embedded &amp; Systems Software</div><h1 id="hero-title">장치와 소프트웨어,<br><span>그 사이를 연결합니다.</span></h1><p class="lead">차량 진단과 센서 데이터 통신을 다룬 약 3년의 실무 경험.<br>MCU·Linux 제어 프로젝트로 장치에 대한 이해를 넓히고 있습니다.</p><p class="identity">김호철 <span>임베디드 · 시스템 SW 개발자</span></p><div class="actions"><a class="button" href="#projects">대표 프로젝트 보기 ↓</a><a class="button secondary" href="assets/resume.pdf">이력서 PDF ↗</a></div></div><figure class="hero-photo"><a class="zoom-link" href="assets/fan.webp" aria-label="스마트 선풍기 실물 이미지 확대"><img src="assets/fan.webp" width="825" height="1100" alt="Jetson과 모터·LCD·센서를 연결한 개인 스마트 선풍기 프로젝트 실물" fetchpriority="high"></a><figcaption><strong>직접 연결하고, 동작을 확인한 시스템</strong><span>Jetson Smart Fan</span></figcaption></figure></section>
<div class="summary-strip"><div><span>PROFESSIONAL EXPERIENCE</span><strong>3년 3개월 · 장치 연동 SW</strong></div><div><span>FROM DEVICE TO SERVICE</span><strong>통신 · 데이터 처리 · 제어</strong></div><div><span>ENGINEERING APPROACH</span><strong>문제 분석과 구현</strong></div></div>
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
        "MCU·Linux·Edge AI로 확장한 프로젝트입니다. 핵심 기능과 설계 판단, 직접 담당한 구현을 소개합니다.",
    )
    for p in PROJECTS:
        card_image = p.get("card_image", p["image"])
        card_alt = p.get("card_alt", p["alt"])
        content += f'''<article class="project"><div class="project-media"><img src="assets/{card_image}.webp" width="{IMAGE_SIZES[card_image][0]}" height="{IMAGE_SIZES[card_image][1]}" alt="{card_alt}" loading="lazy"></div><div class="project-body"><div class="project-kicker">{p["label"]} · {p["kind"]}</div><h3>{p["message"]}</h3><p>{p["title"]}</p><p class="role-line"><strong>본인 역할</strong> · {p["role"]}</p><div class="tags">{"".join(f"<span>{t}</span>" for t in p["tags"])}</div><p>{p["result"]}</p><a class="text-link" href="projects/{p["slug"]}/">{p["title"]} 상세 보기 →</a></div></article>'''
    content += (
        '</section><section class="section" id="more-projects">'
        + heading("03", "More projects", "장치 제어에서 추론·앱까지", "FPGA 제어 논리, AVR 장치 제어, Jetson 영상 추론과 Android 앱으로 구현 경험을 확장했습니다.")
        + '<div class="cards">'
    )
    extras = [
        (
            "fpga.webp",
            "FPGA 기반 전자레인지 제어 모형",
            "fpga-microwave-oven",
            "Verilog · FSM · PWM · 테스트벤치",
            "Basys3에서 시간 설정·도어 서보·모터 PWM·조작 잠금을 통합했습니다. 단일 클럭의 FSM과 동시 입력 우선순위를 설계하고, 16개 테스트벤치로 상태 전환·출력 경계 조건을 검증했습니다.",
            "Basys3에 버튼·로터리 인코더·서보·DC 모터를 연결한 전자레인지 제어 모형",
        ),
        (
            "avr.webp",
            "AVR 기반 RTC·계산기",
            "avr-rtc-calculator",
            "C · I²C · 오실로스코프",
            "DS1307 RTC·LCD·키패드를 연결해 시계와 정수 계산기를 통합했습니다. I²C 레지스터 제어와 재귀 하향 수식 파서를 구현하고, 오실로스코프로 SDA·SCL의 주소·데이터·ACK/NACK을 분석했습니다.",
            "I2C START와 장치 주소를 분석한 실제 오실로스코프 계측",
        ),
        (
            "avr-car.webp",
            "AVR 기반 장애물 회피 주행차",
            "avr-autonomous-car",
            "C · 초음파 · Interrupt · PWM · Bluetooth",
            "초음파 센서 3개의 거리로 회피 방향을 판단하고 Bluetooth로 수동 조종합니다. 센서 순차 구동·Echo 인터럽트 계측·모터 PWM을 연결하고, 두 FND에 주행 방향과 통계를 표시했습니다.",
            "전방과 좌우에 초음파 센서 3개를 장착한 AVR 장애물 회피 주행차 실물",
        ),
        (
            "tensorrps.webp",
            "Jetson 기반 가위바위보",
            "jetson-orin-yolo11-rps",
            "Python · TensorRT · CUDA · OpenCV",
            "YOLO11·TensorRT로 손 제스처를 인식해 2인·PC 대전을 구성했습니다. 추론 버퍼를 사전 할당·재사용하고, 10프레임 판정과 게임 FSM을 연결해 라운드·점수를 관리합니다.",
            "TensorRPS 시연 영상의 손 제스처 탐지 박스와 카운트다운·점수 화면",
        ),
        (
            "pokedex.webp",
            "PokeDex",
            "PokeDex",
            "Kotlin · MVI · Room",
            "Room·Paging 3·RemoteMediator로 로컬 캐시를 구성했습니다. MVI·Flow로 화면 상태를 관리하고, 저장된 데이터의 이름 검색·타입 필터·즐겨찾기를 구현했습니다.",
            "PokeDex 앱의 포켓몬 목록 화면",
        ),
    ]
    for im, title, repo, tech, body, alt in extras:
        width, height = IMAGE_SIZES[Path(im).stem]
        content += f'<article class="small-card"><a class="zoom-link" href="assets/{im}" aria-label="{title} 이미지 확대"><img src="assets/{im}" width="{width}" height="{height}" alt="{alt}" loading="lazy"></a><div class="project-kicker">개인 · 학습 프로젝트</div><h3>{title}</h3><p><strong>{tech}</strong></p><p>{body}</p>{link(GH + repo, "저장소 · 설계와 검증 ↗", "text-link", title + " 저장소 · 설계와 검증 ↗")}</article>'
    content += (
        '</div></section><section class="section" id="skills">'
        + heading("04", "Skills & Learning", "경험에 연결된 기술")
        + """<div class="skills"><div><div class="skill-row"><strong>장치 통신 · 데이터 처리</strong><p>Java · Kotlin · Linux · CAN · Ethernet · Bluetooth<br>지아이티 차량 진단 / 브이유텍 센서·중계기 실무</p></div><div class="skill-row"><strong>MCU · Linux 제어</strong><p>C · C++ · STM32 · AVR · ioctl · IPC<br>스마트 선풍기 / 모니터링 / AVR RTC·계산기·주행차</p></div><div class="skill-row"><strong>시스템 통합 · 사용자 화면</strong><p>Qt · Python · TensorRT · FastAPI · Android<br>재활용 키오스크 / 모니터링 / 가위바위보 / PokeDex</p></div><div class="skill-row"><strong>디지털 논리 · 검증</strong><p>Verilog · FSM · 테스트벤치 · Vivado<br>FPGA 기반 전자레인지 제어 모형</p></div></div><div class="education"><div class="eyebrow">Education · Qualifications</div><h3>AI 시스템반도체 SW 개발자 과정 2기</h3><p>대한상공회의소 서울인력개발원<br>2026.05.27 — 2026.12.16 · 교육 중</p><p>MCU·통신, Linux 시스템·드라이버, Qt, Edge AI, FPGA·Verilog 실습</p><hr><p><strong>장안대학교 인터넷정보통신과 · 3년제</strong><br>2015.03 — 2021.02 · 졸업<br>학점 3.95 / 4.5</p><p><strong>자격 · 어학</strong><br>정보처리산업기사 · 네트워크관리사 2급 · JLPT N1</p></div></div></section><section class="contact" id="contact"><div class="eyebrow">05 / Contact</div><h2>함께 연결할 다음 시스템을 기다립니다.</h2><a class="email" href="mailto:yp0504@naver.com">yp0504@naver.com ↗</a><div class="actions"><a class="button" href="assets/resume.pdf">이력서 PDF 열기 ↗</a><a class="button secondary" href="https://github.com/hckim-dev?tab=repositories">GitHub 전체 저장소 ↗</a></div></section></main>"""
    )
    return shell("임베디드 · 시스템 SW 포트폴리오", content)


def detail(p):
    prefix = "../../"
    content = f"""<main id="main" class="wrap"><header class="detail-head"><div class="breadcrumb"><a href="../../index.html#projects">포트폴리오</a> / {p["title"]}</div><div class="eyebrow">{p["label"]}</div><h1>{p["title"]}</h1><p class="lead">{p["summary"]}</p><div class="meta"><div><strong>프로젝트 구분</strong>{p["kind"]}</div><div><strong>본인 역할</strong>{p["role"]}</div></div><div class="actions">{link(p["demo"], "시연 영상 열기 ↗", "button")}{link(GH + p["repo"], "소스 코드 ↗", "button secondary")}</div></header><div class="detail-layout"><nav class="side-nav" aria-label="프로젝트 목차"><a href="#overview">01 프로젝트 · 역할</a><a href="#architecture">02 시스템 구조</a><a href="#design">03 설계 판단</a><a href="#problem">04 문제 해결</a><a href="#verification">05 구현 결과</a><a href="#resources">06 관련 자료</a></nav><div><section id="overview" class="detail-section"><h2>01. 프로젝트와 본인 역할</h2><p>{p["scope"]}</p>"""
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
    content += f'<section id="verification" class="detail-section"><h2>05. 구현 결과</h2><p>{p["verified"]}</p></section>'
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
