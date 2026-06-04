<!--
████████████████████████████████████████████████████████████████████
  seungwoo2000 · pygame_Lung_Defense — K-디지털 트레이닝 포트폴리오 README
████████████████████████████████████████████████████████████████████
-->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7f1d1d,50:dc2626,100:f97316&height=220&section=header&text=🫁%20강철폐포부대&fontSize=52&fontColor=ffffff&fontAlignY=40&desc=폐%20건강%20교육용%20슈팅게임&descAlignY=62&descColor=fed7aa&animation=fadeIn" alt="header" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-게임엔진-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey?style=for-the-badge)
![Type](https://img.shields.io/badge/Type-교육용%20게임-ff4444?style=for-the-badge)

<br/>

> **게임을 하며 자연스럽게 폐 건강 지식을 익힌다**  
> 에듀테인먼트(Edutainment) — 교육(Education) + 오락(Entertainment)

</div>

---

## 📋 훈련 과정 정보

| 항목 | 내용 |
|:---|:---|
| 🏫 **훈련기관** | 아시아경제 교육센터 |
| 📚 **훈련과정명** | 융합\_데이터 기반 차세대 디지털 헬스케어 AI 솔루션 5회차 |
| 🏷️ **훈련유형** | K-디지털 트레이닝 |
| 📅 **훈련기간** | 2026-02-03 ~ 2026-07-30 (6개월) |
| 💡 **프로젝트 분류** | 디지털 헬스케어 × Python 게임 개발 · 교육용 에듀테인먼트 |

---

## 🫁 이 게임은 무엇인가요?

```
"딱딱한 건강 정보는 그만, 직접 싸우며 배운다!"

세균과 바이러스가 폐를 침범합니다.
당신은 좌우로 움직이며 이들을 물리치는 수호자입니다.
적을 처치할수록 폐 건강 상식이 쌓입니다.
```

**강철폐포부대**는 폐 건강 정보를 게임으로 풀어낸 **교육용 슈팅 게임**입니다.  
재미있게 플레이하는 동안 자연스럽게 폐와 폐포의 역할,  
그리고 우리 몸을 위협하는 세균·바이러스에 대해 익힐 수 있습니다.

| 🎮 키워드 | 설명 |
|:---|:---|
| **에듀테인먼트** | 교육(Education) + 오락(Entertainment) — 게임으로 배우는 폐 건강 |
| **폐 건강 테마** | 폐포·세균·바이러스 등 실제 의학 개념을 게임 캐릭터·스토리로 구현 |
| **횡스크롤 슈팅** | 좌우로 이동하며 밀려오는 적을 물리치는 직관적인 액션 |

> 💡 **폐포(alveoli)란?**  
> 폐 속 작은 공기주머니로, 산소와 이산화탄소를 교환하는 핵심 기관입니다.  
> 이 소중한 폐포를 침입자로부터 지키는 것이 이 게임의 미션입니다!

---

## 🕹️ 바로 플레이하기

> Python 설치 없이 **.exe 파일**만 실행하면 바로 플레이할 수 있습니다!

| 플랫폼 | 다운로드 |
|:---:|:---:|
| 🪟 **Windows** | [📥 강철폐포부대.exe 다운로드](#) |


---

## 🛠️ 기술 스택

> 비전공자도 이해할 수 있도록, 각 기술이 **어떤 역할**을 하는지 함께 설명합니다.

| 기술 | 한 줄 설명 | 핵심 키워드 |
|:---:|:---|:---|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | 게임 전체 로직을 짜는 프로그래밍 언어 | `게임 루프` `객체지향` `이벤트 처리` |
| ![Pygame](https://img.shields.io/badge/Pygame-3776AB?logo=python&logoColor=white) | Python으로 2D 게임을 만들 수 있게 해주는 라이브러리 | `스프라이트` `충돌감지` `렌더링` `사운드` |

---

## 📁 파일 구조

```
pygame_Lung_Defense/
│
├── 📂 font/          # 게임 UI에 사용된 폰트 파일
├── 📂 image/         # 캐릭터, 배경, 적, UI 등 스프라이트 이미지
├── 📂 sound/         # 배경음악(BGM) 및 효과음(SFX)
│
├── game.py           # 🎮 메인 실행 파일 (전체 게임 로직)
├── .gitignore        # Git 버전관리 제외 파일 목록
└── README.md         # 프로젝트 설명 문서
```

> `font/` · `image/` · `sound/` 세 폴더로 에셋을 분류해  
> 코드(game.py)와 리소스를 깔끔하게 분리한 구조입니다.

---

## ✨ 주요 기능

```
⬅️➡️ 좌우 이동 조작    →  키보드(← →)로 플레이어를 좌우로 움직여 적 대응
🔫  슈팅 액션          →  발사체를 쏘아 세균 · 바이러스 적 캐릭터 처치
👾  헬스케어 테마 적    →  폐를 위협하는 세균 · 바이러스 · 유해물질 등장
💥  충돌 감지          →  총알과 적 간의 pygame 스프라이트 충돌 판정
🔊  사운드 시스템      →  BGM 재생 + 발사 · 피격 효과음
🖼️  이미지 렌더링      →  커스텀 스프라이트 · 배경 이미지 로드 및 표시
✍️  커스텀 폰트        →  점수 · 체력 등 게임 UI에 전용 폰트 적용
```

---

## 📈 배운 점 · 성장 포인트

| 분야 | 배운 것 | 이걸 배워서 뭘 할 수 있게 됐나? |
|:---|:---|:---|
| 🎮 **게임 루프** | `while True` 기반 pygame 루프 구조 | 프레임마다 화면을 업데이트하는 실시간 렌더링 이해 |
| 🖼️ **스프라이트** | 이미지 로드 · 좌표 이동 · 화면 그리기 | 캐릭터와 배경을 픽셀 단위로 제어 |
| 💥 **충돌 감지** | `pygame.Rect` 충돌 처리 | 총알이 적(바이러스·세균)에 맞는 순간을 코드로 판단 |
| 🔫 **발사 시스템** | 키 입력 → 총알 객체 생성 → 이동 | 플레이어 입력을 게임 오브젝트로 연결하는 흐름 구현 |
| 🔊 **사운드** | `pygame.mixer` BGM · 효과음 재생 | 게임에 몰입감을 주는 사운드 시스템 구현 |
| ✍️ **폰트 렌더링** | `pygame.font` 커스텀 폰트 적용 | 점수, 체력 등 게임 UI 텍스트 표시 |
| 🗂️ **에셋 관리** | font / image / sound 폴더 분리 | 코드와 리소스를 분리하는 프로젝트 구조화 |
| 🏥 **헬스케어 연계** | 폐 건강 개념을 게임 콘텐츠로 기획 | 의학 지식을 창의적인 에듀테인먼트로 표현하는 경험 |

---

## ⚙️ 실행 방법

**1️⃣ 저장소 클론**
```bash
git clone https://github.com/seungwoo2000/pygame_Lung_Defense.git
cd pygame_Lung_Defense
```

**2️⃣ pygame 설치**
```bash
pip install pygame
```

**3️⃣ 게임 실행**
```bash
python game.py
```

> ✅ Python 3.8 이상 권장

---

<div align="center">

<br/>

*"게임으로 배우는 폐 건강 — 쏘고, 막고, 지킨다!"* 🫁🔫

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:f97316,50:dc2626,100:7f1d1d&height=130&section=footer&text=K-디지털%20트레이닝%20|%20아시아경제%20교육센터&fontSize=15&fontColor=ffffff&fontAlignY=65" width="100%"/>

**📅 2026.02 ~ 2026.07** &nbsp;|&nbsp; Made with 🎮 during K-Digital Training

</div>
