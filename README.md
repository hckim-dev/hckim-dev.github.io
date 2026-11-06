# 김호철 · 임베디드 / 시스템 SW 포트폴리오

장치 연동·통신 SW 실무 경험과 MCU·Linux·Edge AI·FPGA 프로젝트를 소개하는 GitHub Pages 정적 사이트입니다.

[공개 사이트](https://hckim-dev.github.io/) · [콘텐츠 근거와 에셋 출처](docs/SOURCES.md)

## 로컬 미리보기

Python 3.10 이상을 사용합니다. 사이트 생성에는 표준 라이브러리만 필요하며, 브라우저 검증에는 Playwright와 Chromium을 사용합니다.

생성된 HTML이 저장소에 포함되어 있으므로 열람만 할 때는 빌드가 필요 없습니다. 저장소 루트에서 실행합니다.

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

<http://127.0.0.1:8000/>에서 열람하고 `Ctrl+C`로 종료합니다. Python 임시 서버에서는 영상의 구간 이동이 제한될 수 있습니다.

## 구조와 콘텐츠 수정

| 경로 | 역할 |
| --- | --- |
| `scripts/build.py` | 프로젝트 데이터·본문·공통 레이아웃과 HTML 생성 |
| `index.html`, `projects/*/index.html` | GitHub Pages에 제공하는 생성된 HTML |
| `assets/css/site.css`, `assets/js/site.js` | 스타일과 메뉴·이미지 확대 동작 |
| `assets/projects/<프로젝트>/` | 프로젝트별 이미지·시연 영상 |
| `assets/icons/favicon.svg`, `assets/resume.pdf` | 사이트 아이콘과 이력서 |
| `scripts/verify.py`, `scripts/check_links.py` | 브라우저 검증과 외부 링크 검사 |
| [docs/SOURCES.md](docs/SOURCES.md) | 설명의 근거·확인 커밋·자료 출처 |

대표 프로젝트는 `PROJECTS`, 메인 소개·경력·보조 프로젝트는 `home()`, 상세 공통 구성은 `detail()`에서 수정합니다. 본문을 바꾼 뒤 다음 명령으로 HTML을 다시 생성합니다.

```powershell
python scripts/build.py
```

생성된 HTML도 함께 버전 관리합니다. HTML을 직접 수정하면 다음 빌드에서 덮어써집니다. CSS·JavaScript만 수정했다면 HTML을 다시 생성할 필요는 없습니다.

### 이력서 교체

`assets/resume.pdf`를 새 PDF로 교체하고 경로는 유지합니다. 경력·역할·성과가 달라졌다면 웹 본문도 갱신합니다. 배포 후 고정 주소에서 새 PDF가 열리는지 확인합니다.

### 프로젝트 추가·수정

- 대표작은 `PROJECTS`의 기존 형식을 따릅니다. `slug`는 상세 주소이므로 공개 후 변경하지 않습니다. 검증 대상도 이 목록에서 자동으로 가져옵니다.
- 자료는 `assets/projects/<프로젝트>/`에 넣습니다. 에셋 이름은 소문자와 하이픈을 사용하고 `hardware.webp`, `ui.webp`, `demo.mp4`처럼 역할을 나타냅니다.
- `IMAGES`에는 이미지 키와 `(assets 기준 상대 경로, 실제 너비, 실제 높이)`를 등록합니다. 대표작의 `image`는 상세 대표 사진, `card_image`는 선택적인 메인 카드 이미지, `image_caption`은 상세 사진 캡션입니다. 추가 화면은 `detail()`에서 이미지 키로 연결합니다.
- `demo`에는 상세 페이지 기준 상대 경로(예: `../../assets/projects/smart-fan/demo.mp4`)나 외부 영상 URL을 지정합니다.
- 보조작은 `home()`의 `extras`에서 관리합니다. 첫 항목은 `IMAGES`의 이미지 키이며, 카드는 프로젝트 저장소로 연결됩니다.
- 이미지 대체 텍스트와 `docs/SOURCES.md`의 근거·출처도 함께 갱신합니다. 실무·교육 경험, 개인·팀 기여, 소프트웨어 시험·실물 확인을 구분해 작성합니다.

## 검증

미리보기 서버를 켜 둔 상태에서 **별도 터미널**을 열고 저장소 루트에서 실행합니다. Playwright 설치는 검증 환경을 처음 준비할 때 필요합니다.

```powershell
python -m pip install playwright
python -m playwright install chromium
python scripts/verify.py
python scripts/check_links.py
```

- `verify.py`: 생성기와 HTML의 일치, 현재 5개 페이지의 320·390·768·1440px 배치, 모든 이미지 확대·닫기·스크롤 잠금·포커스 복귀, 메뉴·내부 링크, 상세 새로고침·뒤로가기, PDF 응답·파일 일치, JavaScript 없는 탐색, 로컬 영상 재생을 확인합니다.
- `check_links.py`: 직전 브라우저 검사에서 수집한 외부 URL의 HTTP 응답을 확인합니다. 먼저 `verify.py`가 성공해야 합니다.

새 브라우저 검사를 시작하면 이전 보고서를 지우고, 전체 통과 후 새 보고서를 작성합니다. 결과 JSON과 화면 캡처는 Git에서 제외된 `_handoff/qa/`에 저장됩니다.

자동 검사와 별도로 변경된 화면·PDF·영상의 내용을 확인합니다. 외부 URL의 정상 응답은 해당 자료의 내용이나 영상 전체 재생을 검증한 결과가 아닙니다. 프로젝트 하드웨어 시험과 다른 브라우저·실제 기기 확인도 별도입니다.

## 배포와 고정 주소

저장소 루트의 정적 파일을 제공하며 `.nojekyll`을 유지합니다. 서버 처리·SPA 라우팅·별도 배포 workflow는 없고, HTML 생성은 로컬에서 수행합니다. Pages의 배포 브랜치·폴더는 저장소의 **Settings → Pages** 설정을 기준으로 합니다.

배포할 때는 빌드·검증 후 생성된 HTML과 새로 추가·이동·삭제한 에셋을 함께 반영합니다. `_handoff/`에는 원본·조사 자료와 검증 결과가 있으므로 작업 폴더 전체를 업로드하지 않습니다.

| 고정 경로 | 용도 |
| --- | --- |
| `/` | 메인과 인쇄 QR 목적지 |
| `/projects/smart-fan/` | Linux 스마트 선풍기 |
| `/projects/smart-recycling/` | 재활용 Edge AI 키오스크 |
| `/projects/smart-monitoring/` | STM32·Qt·Android 모니터링 |
| `/projects/fpga-spi-sensor-monitoring/` | FPGA SPI 센서 모니터링 |
| `/assets/resume.pdf` | 이력서 PDF |

배포 후 위 주소의 직접 접속·새로고침, 이력서 열람과 영상 재생을 확인합니다.
