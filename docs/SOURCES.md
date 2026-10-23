# 콘텐츠 근거와 에셋 출처

기준일: 2026-10-23. 사이트에 사용한 경력·프로젝트 설명과 에셋의 출처를 기록합니다.

## 경력과 공개 범위

- 경력·학력·교육·자격의 근거는 본인이 제공한 이력서이며 `assets/resume.pdf`로 제공합니다.
- 연락 이메일은 `yp0504@naver.com`입니다. PDF의 전화번호·주소 등은 웹 본문에 복제하지 않습니다.
- 재활용은 4인 팀 프로젝트, 나머지 전시 프로젝트는 본인 확인에 따른 개인 프로젝트입니다.
- 정확한 진행 기간은 확정되지 않아 생략했습니다. 재활용의 2026.09.16은 발표일입니다.

## 확인한 저장소 버전

| 저장소                                                                       | HEAD                                       |
| ---------------------------------------------------------------------------- | ------------------------------------------ |
| [Jetson Smart Fan](https://github.com/hckim-dev/jetson-smart-fan-controller) | `d7e1bbd5e8cbaf34c9f56e5f4ae124e06b194312` |
| [Smart Recycling](https://github.com/hckim-dev/smart-recycling-edge-ai)      | `c6114941bcd0616967b70e255e31b435098cf825` |
| [Smart Monitoring](https://github.com/hckim-dev/smart-monitoring-system)     | `778ce5d3c94f7af0c24ce3ef6cfd9fa797565722` |
| [FPGA Stopwatch](https://github.com/hckim-dev/fpga-stopwatch)                | `a6d862c870d2c8fdf5f61ed374e5b61ca8a7a46f` |
| [AVR RTC Calculator](https://github.com/hckim-dev/avr-rtc-calculator)        | `19954336d42c9912f279e186a570b241761f9de6` |
| [PokeDex](https://github.com/hckim-dev/PokeDex)                              | `4161b80765e1c03608f89984b506a7cf9ec3a53b` |

AVR의 이전 주소 `ATmega128a_rtc_calculator`가 `avr-rtc-calculator`로 이동하는 것을 확인해 사이트에 새 주소를 사용했습니다.

## 주요 확인 자료

- 선풍기: README, docs/architecture.md, development.md, review.md. `driver/smartfan.c`의 mutex 및 SET_AUTO 경계 대조. 테스트 수는 공개 기록이며 이번 작업에서 재실행한 수치가 아닙니다.
- 재활용: README 역할표, docs/protocol-spec.md, troubleshooting.md, 최종 발표 PDF. `edge_jetson/core/door_controller.py`의 miss_count/miss_tolerance 경로 대조. 발표자료의 MCU 팀원 역할을 포함해 개인 기여를 보수적으로 표현했습니다. 강한 신뢰성 주장과 환경이 불충분한 성능 수치는 옮기지 않았습니다.
- 모니터링: README, docs/07_troubleshooting_log.md, `stm32-firmware/timer.c`와 `option.h`의 96 MHz PWM 설정 대조. 가스 입력 모사 및 Qt에서 자동 차단을 판단하는 구조를 명시했습니다.
- FPGA: README, docs/verification.md. 타이밍 차트는 실제 VCD 재구성본, 보드 영상은 최종 버튼 수정 전 촬영이라는 조건을 반영했습니다.
- AVR: 최신 README의 I²C 계측 해석과 버전 대응 한계.
- PokeDex: README의 구조·캐시·테스트 설명과 실제 앱 화면.

## 에셋 대응표

| 사이트 에셋         | 원본 저장소 내 경로                                                |
| ------------------- | ------------------------------------------------------------------ |
| fan.webp            | jetson-smart-fan-controller / docs/assets/hardware-overview.jpg    |
| fan-demo.mp4        | jetson-smart-fan-controller / docs/assets/demo.mp4                 |
| recycling.webp      | smart-recycling-edge-ai / docs/assets/images/hardware_kiosk.jpg    |
| recycling-ui.webp   | smart-recycling-edge-ai / docs/assets/images/kiosk_detect_pass.png |
| monitoring.webp     | smart-monitoring-system / images/hardware_setup.png                |
| monitoring-ui.webp  | smart-monitoring-system / images/qt_normal.png                     |
| monitoring-demo.mp4 | smart-monitoring-system / images/demo.mp4 (H.264 720p 변환)        |
| fpga.webp           | fpga-stopwatch / docs/assets/timing_10ms.png                       |
| avr.webp            | avr-rtc-calculator / docs/assets/images/i2c_wave1.png              |
| pokedex.webp        | PokeDex / screenshots/list_screen.png                              |

이미지는 EXIF 방향 보정 후 최대 1500×1100 범위로 축소·WebP 변환했습니다. 내용 합성은 하지 않았습니다. HTML 구조 블록은 원본 아키텍처를 요약한 설명이며 직접 측정 자료가 아닙니다.

선풍기 README의 첨부 영상은 HTTP 404여서 저장소의 MP4를 로컬 에셋으로 제공했습니다. 모니터링 영상 원본은 HEVC이며 검증 Chromium에서 재생 준비가 완료되지 않아 H.264/AAC 720p, faststart 사본으로 변환했습니다. 재활용 영상은 재생 확인된 GitHub 첨부 링크입니다. 자동 재생은 하지 않습니다.
