# 콘텐츠 근거와 에셋 출처

사이트에 사용한 경력·프로젝트 설명과 에셋의 출처를 기록합니다. TensorRPS, STM32 두 작품, AVR 주행차·세탁기와 재활용의 정산 구현 범위는 2026-10-30, FPGA 전자레인지는 2026-10-29, 나머지 자료는 2026-10-23 기준으로 확인했습니다.

## 경력과 공개 범위

- 경력·학력·교육·자격의 근거는 본인이 제공한 이력서이며 `assets/resume.pdf`로 제공합니다.
- 연락 이메일은 `yp0504@naver.com`입니다. PDF의 전화번호·주소 등은 웹 본문에 복제하지 않습니다.
- 재활용은 4인 팀 프로젝트, 나머지 전시 프로젝트는 본인 확인에 따른 개인 프로젝트입니다.
- 사이트 본문에서는 프로젝트 기간을 생략했습니다. 재활용의 2026.09.16은 발표일입니다.

## 확인한 저장소 버전

| 저장소                                                                       | HEAD                                       |
| ---------------------------------------------------------------------------- | ------------------------------------------ |
| [Jetson Smart Fan](https://github.com/hckim-dev/jetson-smart-fan-controller) | `d7e1bbd5e8cbaf34c9f56e5f4ae124e06b194312` |
| [Smart Recycling](https://github.com/hckim-dev/smart-recycling-edge-ai)      | `9447df1675e309d977a419cd31950584a0d393e2` |
| [Smart Monitoring](https://github.com/hckim-dev/smart-monitoring-system)     | `778ce5d3c94f7af0c24ce3ef6cfd9fa797565722` |
| [FPGA Microwave Oven](https://github.com/hckim-dev/fpga-microwave-oven)      | `08e6835724b4ce0cb36112d1ddbe7e56efe928b2` |
| [TensorRPS](https://github.com/hckim-dev/jetson-orin-yolo11-rps)             | `8098d88d93216753565e747ee581e8933f480ec5` |
| [STM32 다중 출력 제어](https://github.com/hckim-dev/stm32-adc-pwm-spi-dma-ws2812b) | `76514eb7af979882508dcca4a7d0c18c0dfd995d` |
| [STM32 DC 모터 제어](https://github.com/hckim-dev/stm32-motor-project)      | `6e683a0b0c25046ddff63d9b67630b4757fd5120` |
| [AVR 장애물 회피 주행차](https://github.com/hckim-dev/avr-autonomous-car)   | `f5debb2025e933aad75c89c655c0aeb230361689` |
| [AVR 세탁기 제어](https://github.com/hckim-dev/avr-washing-machine)         | `fe93983c083c5e3dc4e5ebcc869949f51d92db7f` |
| [AVR RTC Calculator](https://github.com/hckim-dev/avr-rtc-calculator)        | `19954336d42c9912f279e186a570b241761f9de6` |
| [PokeDex](https://github.com/hckim-dev/PokeDex)                              | `4161b80765e1c03608f89984b506a7cf9ec3a53b` |

AVR의 이전 주소 `ATmega128a_rtc_calculator`가 `avr-rtc-calculator`로 이동하는 것을 확인해 사이트에 새 주소를 사용했습니다.

## 주요 확인 자료

- 선풍기: README, docs/architecture.md, development.md, review.md. `driver/smartfan.c`의 mutex 및 SET_AUTO 경계 대조. 테스트 수는 공개 기록이며 이번 작업에서 재실행한 수치가 아닙니다.
- 재활용: README 역할표, docs/architecture.md, protocol-spec.md, troubleshooting.md, 최종 발표 PDF. `edge_jetson/core/door_controller.py`의 miss_count/miss_tolerance 경로 대조. `server/app/services/kiosk_service.py`와 `repositories/user_repository.py`, `log_repository.py`에서 포인트·이력을 개별 commit하는 경로를 확인했습니다. 단일 SQL 포인트 갱신과 전체 정산의 단일 트랜잭션은 구분하며, 후자는 구현 성과로 주장하지 않습니다. 발표자료의 MCU 팀원 역할을 포함해 개인 기여를 보수적으로 표현했습니다. 강한 신뢰성 주장과 환경이 불충분한 성능 수치는 옮기지 않았습니다.
- 모니터링: README, docs/07_troubleshooting_log.md, `stm32-firmware/timer.c`와 `option.h`의 96 MHz PWM 설정 대조. 가스 입력 모사 및 Qt에서 자동 차단을 판단하는 구조를 명시했습니다.
- FPGA 전자레인지: README, docs/design.md, docs/verification.md, docs/troubleshooting.md 및 `control_lock.v`, `motor_controller.v`의 잠금·PWM 제어 대조. 테스트벤치 16개 PASS는 저장소의 검증 기록이며 포트폴리오 작업에서 재실행한 결과가 아닙니다. 가열 장치가 없는 제어 모형이고 도어 위치는 센서 없이 명령·시간으로 추정합니다. 내부 STA 통과를 외부 I/O 타이밍이나 실제 기구 안전성 검증으로 확대하지 않습니다.
- TensorRPS: README, docs/architecture.md, docs/setup.md, docs/validation.md 및 `core/trt_engine.py`, `core/detector.py`, `game/state_machine.py` 대조. 동일 커밋의 게임 로직 테스트 9개를 로컬에서 실행해 PASS를 확인했습니다. 공개 시연 영상은 전체 디코딩과 대표 장면을 확인했습니다. Jetson·GPU·카메라는 재실행하지 않았고 FPS·정확도·E2E 지연의 측정 성과를 주장하지 않습니다. CUDA 전송·추론 뒤 프레임마다 동기화하며, 여러 프레임을 겹쳐 처리하는 구조가 아닙니다. 모델 가중치·엔진은 제공되지 않아 전체 실행에 별도 준비가 필요합니다.
- STM32 다중 출력: README, docs/implementation.md, `main.c`, `ws2812b.c`, `exception.c`의 입력 매핑과 전송 경로. WS2812B는 TIM3 인터럽트 방식이며 DMA 전송으로 소개하지 않습니다. 흐름도는 코드의 데이터 흐름을 요약한 것으로 실제 배선도·실물 동작 증명이 아닙니다.
- STM32 모터: README, docs/design.md 및 `main.c`, `motor.c`, `key.c`의 명령·상태·출력 연결. 그림은 MCU 측 GPIO/PWM 출력과 논리 상태를 나타내며 외부 드라이버 회로나 물리적 회전·정지 완료를 의미하지 않습니다.
- AVR 주행차: README, docs/architecture.md, docs/hardware.md 및 `main.c`, `ultrasonic.c`의 거리 계측·회피 판단·수동 명령 처리. 실제 제작 사진을 사용하며, 센서 간섭 제거 효과·회피 성공률·응답 지연의 측정 성과를 주장하지 않습니다.
- AVR 세탁기: README, docs/architecture.md, docs/verification.md 및 `main.c`, `uart0.c`의 공정 상태·시간·수신 큐. 대표 이미지는 저장소에 보관된 기존 시연 영상의 추출 장면입니다. 최신 소스와 촬영 당시 바이너리의 동일성이나 모든 완료 경로의 정상 동작을 입증하는 자료로 사용하지 않습니다.
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
| fpga.webp           | fpga-microwave-oven / docs/assets/hardware_overview.jpg            |
| tensorrps.webp      | TensorRPS README의 [공개 시연 영상](https://github.com/user-attachments/assets/56a1ff8a-05af-4022-92a5-0b77f87816be) / 약 6초 장면 |
| stm32-adc.svg       | 본 사이트 제작 / stm32-adc-pwm-spi-dma-ws2812b의 main.c·ws2812b.c·exception.c 기반 흐름도 |
| stm32-motor.svg     | 본 사이트 제작 / stm32-motor-project의 main.c·motor.c·key.c 기반 MCU 출력 흐름도 |
| avr-car.webp        | avr-autonomous-car / docs/images/front.png                       |
| avr-washer.webp     | avr-washing-machine / docs/images/demo_preview.jpg               |
| avr.webp            | avr-rtc-calculator / docs/assets/images/i2c_wave1.png              |
| pokedex.webp        | PokeDex / screenshots/list_screen.png                              |

이미지는 EXIF 방향 보정 후 최대 1500×1100 범위로 축소·WebP 변환했습니다. 내용 합성은 하지 않았습니다. HTML 구조 블록은 원본 아키텍처를 요약한 설명이며 직접 측정 자료가 아닙니다.

선풍기 README의 첨부 영상은 HTTP 404여서 저장소의 MP4를 로컬 에셋으로 제공했습니다. 모니터링 영상 원본은 HEVC이며 검증 Chromium에서 재생 준비가 완료되지 않아 H.264/AAC 720p, faststart 사본으로 변환했습니다. 재활용 영상은 재생 확인된 GitHub 첨부 링크입니다. 자동 재생은 하지 않습니다.
