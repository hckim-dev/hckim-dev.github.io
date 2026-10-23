# 김호철 · 임베디드 / 시스템 SW 포트폴리오

GitHub Pages용 정적 HTML/CSS/JavaScript 사이트입니다. 런타임 의존성, 외부 폰트, 백엔드, 로그인은 없습니다. 이 구현 작업에서는 원격 반영 및 Pages 설정 변경을 실행하지 않았으며, 공개 Pages 동작은 별도 확인이 필요합니다.

## 로컬 미리보기

저장소 루트에서 실행합니다.

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

<http://127.0.0.1:8000/>에서 확인합니다. 상세 주소는 `/projects/smart-fan/`, `/projects/smart-recycling/`, `/projects/smart-monitoring/`입니다. 각 주소에 실제 index.html을 두어 별도 라우팅 없이 직접 접속·새로고침할 수 있습니다.

## 수정 방법

- 본문: `scripts/build.py`의 `PROJECTS`와 `home()` 수정 후 `python scripts/build.py`. Python 표준 라이브러리만 필요하며 생성된 HTML도 함께 관리합니다.
- 디자인·기능: `assets/site.css`, `assets/site.js`.
- 이력서: `assets/resume.pdf`만 교체합니다. 경력 사실이 달라지면 웹 본문도 갱신합니다.
- 프로젝트 추가: `PROJECTS`에 항목과 이미지를 추가하고 생성합니다. 기존 상세 주소를 유지하고 확정한 대표작 순서를 임의로 바꾸지 않습니다.
- 이미지 출처와 확인 커밋: [docs/SOURCES.md](docs/SOURCES.md).

`_handoff/`는 Git에서 제외되는 로컬 전용 폴더입니다. 원본 문서, 조사용 clone, 스크린샷, 검증 JSON, 이어하기 문서가 있습니다. **배포 시 작업 폴더 전체가 아닌 Git 추적 파일 또는 선별한 사이트 파일만 사용합니다.** `.nojekyll`은 정적 파일을 그대로 제공하기 위한 파일입니다.

## 검증 재실행

미리보기 서버를 켠 상태에서:

```powershell
python -m pip install playwright
python -m playwright install chromium
python scripts/verify.py
python scripts/check_links.py
```

사이트 탐색·레이아웃·링크 검사이며 펌웨어·하드웨어 테스트가 아닙니다. 결과는 `_handoff/qa/`에 기록됩니다. [검증 결과](docs/VALIDATION.md)를 참고하세요.

다음 세션은 `_handoff/PROGRESS.md`부터 읽으면 이어갈 수 있습니다.
