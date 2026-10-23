# 김호철 · 임베디드 / 시스템 SW 포트폴리오

장치 연동·통신 SW 실무 경험과 MCU·Linux·Edge AI 프로젝트를 소개하는 정적 사이트입니다.

**사이트:** https://hckim-dev.github.io/

## 구조와 실행

| 경로                                          | 역할                                                |
| --------------------------------------------- | --------------------------------------------------- |
| `scripts/build.py`                            | 콘텐츠와 HTML 생성기. Python 표준 라이브러리만 사용 |
| `index.html`, `projects/*/index.html`         | GitHub Pages에 제공할 생성된 HTML                   |
| `assets/`                                     | CSS·JavaScript·사진·영상·이력서                     |
| `scripts/verify.py`, `scripts/check_links.py` | 브라우저 및 외부 링크 검증                          |
| [docs/SOURCES.md](docs/SOURCES.md)            | 콘텐츠 근거, 에셋 출처와 확인 버전                  |

저장소 루트에서 실행합니다. 생성된 HTML이 있으므로 열람만 할 때는 빌드가 필요 없습니다.

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

<http://127.0.0.1:8000/>에서 열람합니다. 서버 종료는 `Ctrl+C`입니다. Python 임시 서버에서는 영상의 구간 이동이 제한될 수 있습니다.

## 콘텐츠 수정과 빌드

1. `scripts/build.py`에서 대표 프로젝트는 `PROJECTS`, 메인 소개·경력·보조 프로젝트는 `home()`을 수정합니다.
2. `python scripts/build.py`로 HTML을 재생성합니다.
3. 변경 내용을 확인하고 생성된 HTML도 함께 버전 관리합니다. HTML 직접 수정은 다음 생성 시 덮어써집니다.

CSS와 상호작용은 `assets/site.css`, `assets/site.js`에서 수정합니다. 별도 패키지 설치나 프런트엔드 빌드 도구는 필요 없습니다.

### 이력서 교체

`assets/resume.pdf`를 새 PDF로 교체합니다. 주소는 유지하고, 경력·역할·성과가 달라졌다면 웹 본문도 갱신합니다. 배포 후 같은 주소에서 새 파일이 열리는지 확인합니다.

### 프로젝트 추가·수정

- 대표 프로젝트는 `PROJECTS`의 기존 항목 형식을 따릅니다. `slug`는 상세 주소이므로 공개 후 변경하지 않습니다.
- 이미지 파일을 `assets/`에 넣고 실제 크기를 `IMAGE_SIZES`에 등록합니다. `demo`에는 상세 페이지 기준 상대 경로나 외부 영상 URL을 지정합니다.
- 보조 프로젝트는 `home()`의 `extras`에서 관리하며 저장소로 연결합니다.
- 새 근거·에셋 출처는 `docs/SOURCES.md`에 기록하고, 상세 경로를 추가하면 `scripts/verify.py`의 `ROUTES`도 갱신합니다.
- 실무·학습 경험, 개인·팀 기여, 소프트웨어 검증·실물 검증을 구분합니다.

## 검증

로컬 서버가 실행 중인 상태에서 아래 순서로 실행합니다. Playwright는 검증에만 필요합니다.

```powershell
python -m pip install playwright
python -m playwright install chromium
python scripts/verify.py
python scripts/check_links.py
```

`verify.py`는 4개 페이지를 320·390·768·1440px에서 검사하고, 이미지·확대·메뉴·내부 경로·PDF·뒤로가기·새로고침·JavaScript 없는 탐색을 확인합니다. `check_links.py`는 직전 브라우저 검사에서 수집한 외부 링크를 확인하므로 먼저 `verify.py`를 실행해야 합니다.

결과 JSON과 화면 캡처는 Git에서 제외된 `_handoff/qa/`에 저장됩니다. 영상·PDF를 직접 열고, 변경된 콘텐츠의 사실관계도 확인합니다. 이 검사는 프로젝트 하드웨어 검증이나 모든 브라우저의 접근성 인증을 대신하지 않습니다.

## GitHub Pages 배포

서버 처리나 SPA 라우팅 없이 저장소 루트의 정적 파일을 제공합니다. `.nojekyll`은 그대로 유지합니다. 저장소에는 별도 배포 workflow가 없으며, HTML 생성은 로컬에서 수행합니다.

배포할 때는 빌드·검증 후 생성된 HTML과 관련 에셋을 함께 커밋하고, 저장소의 **Settings → Pages**에서 지정된 배포 브랜치·폴더에 반영합니다. 관리 설정은 별도 확인 대상이며 이 문서가 설정 변경을 요구하지는 않습니다. 루트를 브랜치 배포 원본으로 사용할 수 있는 구조입니다.

고정 주소:

- `/` — 메인 및 인쇄 QR 목적지
- `/projects/smart-fan/`
- `/projects/smart-recycling/`
- `/projects/smart-monitoring/`
- `/assets/resume.pdf`

배포 후 위 주소의 직접 접속·새로고침, 이력서 및 영상 재생을 확인합니다. `_handoff/`에는 원본 자료·조사용 복사본·로컬 검증 기록이 있으므로 Git 추적과 배포 대상에서 제외합니다. 작업 폴더 전체를 업로드하지 않습니다.
