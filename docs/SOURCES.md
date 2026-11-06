# 콘텐츠 근거와 에셋 출처

사이트 설명을 작성할 때 대조한 커밋·문서와 이미지·영상의 출처입니다. 아래 커밋은 작성 기준이며, 각 저장소의 현재 HEAD와 다를 수 있습니다.

## 표기 기준

- 경력·학력·교육·자격은 공개 [이력서](../assets/resume.pdf)를 근거로 합니다. 연락 이메일은 `yp0504@naver.com`이며, PDF의 전화번호·주소는 웹 본문에 복제하지 않습니다.
- 재활용은 4인 팀, FPGA SPI 센서 모니터링은 팀 프로젝트입니다. 나머지 전시 프로젝트는 개인 프로젝트입니다. 팀의 전체 결과와 본인 담당을 구분합니다.
- 프로젝트 기간은 웹 본문에서 생략했습니다. 재활용의 2026.09.16은 발표일입니다.
- 기능·설계 판단·본인 기여·구현 결과를 중심으로 소개하고, 입력 방식·집계 기준처럼 의미를 결정하는 조건을 명시합니다.
- 프로젝트의 시험 수치와 실물 확인 기록은 사이트 동작 검사와 구분합니다. 측정 조건이 없는 FPS·정확도·지연 수치는 사용하지 않습니다.

## 확인한 저장소 버전

| 프로젝트 | 확인 커밋 |
| --- | --- |
| [Jetson Smart Fan Controller](https://github.com/hckim-dev/jetson-smart-fan-controller) | `d7e1bbd5e8cbaf34c9f56e5f4ae124e06b194312` |
| [Smart Recycling Edge AI](https://github.com/hckim-dev/smart-recycling-edge-ai) | `9447df1675e309d977a419cd31950584a0d393e2` |
| [Smart Monitoring System](https://github.com/hckim-dev/smart-monitoring-system) | `778ce5d3c94f7af0c24ce3ef6cfd9fa797565722` |
| [FPGA SPI Sensor Monitoring](https://github.com/hckim-dev/fpga-spi-sensor-monitoring) | `b7debc23476ac3e07bbb7cb36a93eac9f37b9e9c` |
| [FPGA 전자레인지 제어 모형](https://github.com/hckim-dev/fpga-microwave-oven) | `08e6835724b4ce0cb36112d1ddbe7e56efe928b2` |
| [AVR RTC·계산기](https://github.com/hckim-dev/avr-rtc-calculator) | `19954336d42c9912f279e186a570b241761f9de6` |
| [AVR 장애물 회피 주행차](https://github.com/hckim-dev/avr-autonomous-car) | `f5debb2025e933aad75c89c655c0aeb230361689` |
| [Jetson 가위바위보](https://github.com/hckim-dev/jetson-orin-yolo11-rps) | `8098d88d93216753565e747ee581e8933f480ec5` |
| [PokeDex](https://github.com/hckim-dev/PokeDex) | `4161b80765e1c03608f89984b506a7cf9ec3a53b` |

## 내용별 근거

- **선풍기:** README와 설계·검증 문서, `driver/smartfan.c`의 mutex·`SET_AUTO` 경계를 대조했습니다. C·CLI·자원 정리·Device Tree 시험 수치는 저장소의 검증 기록입니다.
- **재활용:** README 역할표, 설계·통신·문제 해결 문서와 최종 발표 PDF를 근거로 합니다. `DoorController`의 검출 누락 유예와 Qt의 도어 상태 전이 집계를 구분합니다. 포인트·배출 이력은 별도 commit 경로이므로 전체 정산을 하나의 트랜잭션으로 처리한다고 설명하지 않습니다.
- **모니터링:** README, 문제 해결 문서와 `stm32-firmware/timer.c`·`option.h`의 96 MHz PWM 설정을 대조했습니다. 가변저항 입력 모사와 Qt의 자동 차단 판단을 본문에 명시합니다.
- **FPGA SPI 센서 모니터링:** README, `docs/implementation.md`, `docs/interface.md`, `desktop/README.md`, Master `sensor_reader.v`·`uart_reporter.v`와 Qt 수신·CSV 코드를 대조했습니다. 본인은 Master·인터페이스·Qt, 팀원은 센서 Driver·Slave 담당입니다. 시험 수치·내부 타이밍 결과는 저장소 기록이며, 외부 SPI I/O Timing Closure나 센서 정확도 측정으로 확대하지 않습니다. OLED 수정에서는 특정 초기화 값을 단독 원인으로 확정하지 않습니다.
- **FPGA 전자레인지:** README, 설계·검증·문제 해결 문서와 `control_lock.v`·`motor_controller.v`를 대조했습니다. 테스트벤치 16개 PASS는 저장소 기록입니다. 가열 장치가 없는 제어 모형이며, 도어 위치는 명령·시간으로 추정합니다. 내부 타이밍 결과와 외부 I/O·기구 검증을 구분합니다.
- **AVR RTC·계산기:** README의 RTC·재귀 하향 파서 구현, I²C 계측 해석과 자료별 버전 대응을 근거로 합니다.
- **AVR 주행차:** README, 설계·하드웨어 문서와 `main.c`·`ultrasonic.c`의 거리 계측·회피 판단·수동 명령을 대조했습니다. 센서 간섭 제거 효과·회피 성공률·응답 지연의 측정 성과는 주장하지 않습니다.
- **Jetson 가위바위보:** README, 구조·실행·검증 문서와 TensorRT 추론·게임 상태 코드를 대조했습니다. 작성 시 동일 커밋의 게임 로직 테스트 9개를 별도 로컬 실행해 통과했습니다. CUDA 전송·추론 후 프레임마다 동기화하며, 여러 프레임을 겹쳐 처리하는 구조는 아닙니다. Jetson 실행에는 별도 모델·엔진 준비가 필요합니다.
- **PokeDex:** README의 구조·캐시·시험 설명과 실제 앱 화면을 근거로 합니다. 이름 검색·타입 필터는 Room에 저장된 데이터를 대상으로 합니다.

## 에셋 출처

사이트 파일은 `assets/projects/` 기준이며 각 링크에서 열 수 있습니다. 원본 경로는 위 표의 해당 프로젝트 저장소를 기준으로 합니다.

| 프로젝트 | 사이트 파일 | 원본 경로·자료 |
| --- | --- | --- |
| 선풍기 | [hardware.webp](../assets/projects/smart-fan/hardware.webp) | `docs/assets/hardware-overview.jpg` |
| 선풍기 | [demo.mp4](../assets/projects/smart-fan/demo.mp4) | `docs/assets/demo.mp4` |
| 재활용 | [hardware.webp](../assets/projects/smart-recycling/hardware.webp) | `docs/assets/images/hardware_kiosk.jpg` |
| 재활용 | [ui.webp](../assets/projects/smart-recycling/ui.webp) | `docs/assets/images/kiosk_detect_pass.png` |
| 모니터링 | [hardware.webp](../assets/projects/smart-monitoring/hardware.webp) | `images/hardware_setup.png` |
| 모니터링 | [ui.webp](../assets/projects/smart-monitoring/ui.webp) | `images/qt_normal.png` |
| 모니터링 | [demo.mp4](../assets/projects/smart-monitoring/demo.mp4) | `images/demo.mp4` |
| FPGA SPI | [hardware.webp](../assets/projects/fpga-spi-sensor-monitoring/hardware.webp) | `docs/assets/hardware/system_setup.png` |
| FPGA SPI | [ui.webp](../assets/projects/fpga-spi-sensor-monitoring/ui.webp) | `docs/assets/desktop/monitoring.png` |
| FPGA SPI | [demo.mp4](../assets/projects/fpga-spi-sensor-monitoring/demo.mp4) | `docs/assets/video/sensor_monitoring_demo.mp4` |
| FPGA 전자레인지 | [hardware.webp](../assets/projects/fpga-microwave-oven/hardware.webp) | `docs/assets/hardware_overview.jpg` |
| AVR RTC·계산기 | [i2c-waveform.webp](../assets/projects/avr-rtc-calculator/i2c-waveform.webp) | `docs/assets/images/i2c_wave1.png` |
| AVR 주행차 | [hardware.webp](../assets/projects/avr-autonomous-car/hardware.webp) | `docs/images/front.png` |
| Jetson 가위바위보 | [demo-frame.webp](../assets/projects/jetson-orin-yolo11-rps/demo-frame.webp) | [공개 시연 영상](https://github.com/user-attachments/assets/56a1ff8a-05af-4022-92a5-0b77f87816be)의 약 6초 장면 |
| PokeDex | [list-screen.webp](../assets/projects/pokedex/list-screen.webp) | `screenshots/list_screen.png` |

## 변환과 재생

- 이미지는 EXIF 방향 보정 후 최대 1500×1100 범위로 축소·WebP 변환했습니다. 내용 합성은 하지 않았습니다. HTML의 시스템 구조 블록은 원본 설계를 요약한 설명입니다.
- 선풍기·FPGA SPI 영상은 H.264 MP4에 재인코딩 없이 faststart 처리를 적용했습니다. 처리 전후 압축 스트림 SHA-256이 같고 화질·해상도·프레임·재생 시간은 유지됩니다.
- 모니터링의 HEVC 원본은 H.264/AAC 720p·faststart 사본으로 변환했습니다. 재활용 시연은 공개 GitHub 첨부 링크로 연결하며, 영상은 자동 재생하지 않습니다.
- Jetson 가위바위보와 FPGA SPI 시연은 전체 디코딩과 대표 장면을 확인했습니다. 이 확인과 프로젝트 하드웨어·GPU 실행 시험은 구분합니다.
- CSS·JavaScript와 HC 파비콘은 이 사이트용으로 작성했으며, 별도 웹폰트·아이콘 라이브러리는 사용하지 않습니다.
