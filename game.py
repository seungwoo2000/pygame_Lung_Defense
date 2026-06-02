import pygame
import random
import os
import sys

# =====================================================================
# [경로] EXE 빌드 시 리소스 절대경로 보정 (PyInstaller 대응)
# =====================================================================
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# =====================================================================
# [상수] 화면 · 프레임 · SpO2 · 시간
# =====================================================================
BASE_WIDTH, BASE_HEIGHT = 700, 900
FPS = 60

SPO2_START         = 100   # 시작 시 초기 산소포화도(%)
SPO2_DECAY_PER_SEC = 5     # 초당 자동 감소량
SPO2_WIN_THRESHOLD = 90    # 생존 판정 최소 기준(%)
TIME_LIMIT         = 60    # 제한 시간(초)

# =====================================================================
# [상수] 이미지 스케일 배율
# =====================================================================
SCALE_ALVEOLUS, SCALE_BULLET  = 0.35, 0.3
SCALE_DUST, SCALE_FOOD         = 0.3, 0.6
SCALE_CIGARETTE, SCALE_BOSS    = 0.7, 1.0
SCALE_BROCCOLI, SCALE_WATER    = 0.45, 0.45
NEBULIZER_SCALE, NEBULIZER_EFFECT_SCALE = 0.15, 0.5

# =====================================================================
# [상수] 이동 속도
# =====================================================================
PLAYER_BASE_SPEED = 4
BULLET_SPEED      = 9
DUST_SPEED, FOOD_SPEED, CIGARETTE_SPEED = 2.0, 1.5, 1.0
BOSS_SPEED, BROCCOLI_SPEED, WATER_SPEED, NEBULIZER_SPEED = 1.2, 2.5, 2.5, 2.0

# =====================================================================
# [상수] 스폰 주기 · 조건
# =====================================================================
DUST_SPAWN_INTERVAL      = 0.15
FOOD_SPAWN_START         = 10;   FOOD_SPAWN_INTERVAL      = 1
CIGARETTE_SPAWN_START    = 15;   CIGARETTE_SPAWN_INTERVAL = 1.5
BROCCOLI_SPAWN_INTERVAL  = 1.5;  WATER_SPAWN_INTERVAL     = 2.1
NEBULIZER_SPAWN_TIMES    = [18, 28, 45]   # 필살기 강제 등장 시각(초)

BOSS_FIRST_DELAY = 20    # 보스 최초 등장 대기(초)
BOSS_INTERVAL    = 15    # 보스 재등장 간격(초)
BOSS_MAX_SPAWN   = 3     # 한 판 최대 보스 등장 횟수
BOSS_WARNING_SEC = 3     # 경고 연출 지속 시간(초)

# =====================================================================
# [상수] 적 체력 · 스케일링 · 보스
# =====================================================================
DUST_HP_BASE, FOOD_HP_BASE, CIGARETTE_HP_BASE = 1, 2, 4
ENEMY_HP_SCALE_PER_SEC = 0.15   # 초당 체력 증가량(난이도 자동 조절)
BOSS_HP_LIST = [100, 200, 300]  # 보스 등장 순번별 체력

# =====================================================================
# [상수] 처치 보상 · 아이템 효과 · 이펙트
# =====================================================================
SCORE_DUST, SCORE_FOOD, SCORE_CIGARETTE, SCORE_BOSS = 1, 6, 10, 100
SPO2_GAIN_DUST, SPO2_GAIN_FOOD, SPO2_GAIN_CIGARETTE, SPO2_GAIN_BOSS = 1, 3, 5, 10

BROCCOLI_MAX_STACK           = 30
ROW_CAPACITY                 = 10     # 한 줄 최대 병사 수
BROCCOLI_INSERT_OFFSET_RATIO = 0.33
WATER_SPEED_GAIN             = 0.25
PLAYER_BASE_DAMAGE           = 1
BROCCOLI_DAMAGE_GAIN         = 0      # 필요 시 숫자 UP

NEBULIZER_ALL_ENEMY_HP_DEC   = 50
NEBULIZER_EFFECT_DURATION_MS = 1000
POPUP_LIFETIME_MS    = 1000;  POPUP_RISE_PER_MS    = 0.06;  POPUP_ALPHA_DEC_PER_MS = 0.28
FLOAT_TEXT_LIFETIME_MS = 800; FLOAT_TEXT_RISE_SPEED = 0.05
MINI_HP_BAR_W, MINI_HP_BAR_H = 30, 6
BOSS_HP_BAR_W, BOSS_HP_BAR_H = 100, 15
ICON_SIZE = 32

# =====================================================================
# [경로] 리소스 폴더
# =====================================================================
IMG_PATH   = resource_path("image") + os.sep
SOUND_PATH = resource_path("sound") + os.sep
FONT_PATH  = resource_path("font")  + os.sep

# =====================================================================
# [초기화] Pygame · 디스플레이
# =====================================================================
pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
# [계산] 모니터 해상도의 80% 크기로 창 비율 결정
scale_ratio = min(info.current_w / BASE_WIDTH, info.current_h / BASE_HEIGHT) * 0.8
display_w, display_h = int(BASE_WIDTH * scale_ratio), int(BASE_HEIGHT * scale_ratio)

screen     = pygame.display.set_mode((display_w, display_h))
background = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
clock      = pygame.time.Clock()
pygame.display.set_caption("강철폐포부대")

# [상태] 0=시작화면, 1=스토리, 2=준비, 3=본게임
STATE_START, STATE_INTRO, STATE_READY, STATE_GAME = 0, 1, 2, 3
game_state = STATE_START

# =====================================================================
# [함수] 리소스 로드 헬퍼
# =====================================================================
def load_img(path, scale=1.0):
    """이미지 로드 · 스케일 조정. 파일 없으면 더미 Surface 반환(방어)"""
    try:
        img = pygame.image.load(path)
        if scale != 1.0:
            img = pygame.transform.rotozoom(img, 0, scale)
        return img
    except Exception:
        return pygame.Surface((50, 50))

def load_sound(path):
    """사운드 로드. 파일 없으면 None 반환(방어)"""
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

# =====================================================================
# [로드] UI · 배경 이미지
# =====================================================================
img_start_bg     = pygame.transform.scale(load_img(IMG_PATH+"game_start.png"), (BASE_WIDTH, BASE_HEIGHT))
img_name         = load_img(IMG_PATH+"game_name.png", 0.85)
img_btn_start    = load_img(IMG_PATH+"start_button.png", 0.35)
rect_name        = img_name.get_rect(center=(BASE_WIDTH//2, int(BASE_HEIGHT*0.22)+50))
rect_btn_start   = img_btn_start.get_rect(center=(BASE_WIDTH//2, int(BASE_HEIGHT*0.85)))

img_ready_start  = load_img(IMG_PATH+"버튼_START.png", 0.85)
rect_ready_start = img_ready_start.get_rect(center=(BASE_WIDTH/2, int(BASE_HEIGHT*0.85)))

img_success_bg    = pygame.transform.scale(load_img(IMG_PATH+"success.png"), (BASE_WIDTH, BASE_HEIGHT))
img_title_success = load_img(IMG_PATH+"button_success.png", 0.8)
img_fail_bg       = pygame.transform.scale(load_img(IMG_PATH+"fail.png"),    (BASE_WIDTH, BASE_HEIGHT))
img_title_gameover = load_img(IMG_PATH+"button_fail.png", 0.8)

img_btn_retry  = load_img(IMG_PATH+"버튼_RETRY.png", 0.85); rect_btn_retry = img_btn_retry.get_rect()
img_btn_quit   = load_img(IMG_PATH+"버튼_QUIT.png",  0.85); rect_btn_quit  = img_btn_quit.get_rect()

img_warning_boss     = load_img(IMG_PATH+"warning_boss.png", 0.7)
img_nebulizer_effect = load_img(IMG_PATH+"effect_nebulizer.png", NEBULIZER_EFFECT_SCALE)

img_bg        = pygame.transform.scale(load_img(IMG_PATH+"background.png"), (BASE_WIDTH, BASE_HEIGHT))
img_icon_star = pygame.transform.scale(load_img(IMG_PATH+"star.png"),  (ICON_SIZE, ICON_SIZE))
img_icon_time = pygame.transform.scale(load_img(IMG_PATH+"time.png"),  (ICON_SIZE, ICON_SIZE))
img_icon_spo2 = pygame.transform.scale(load_img(IMG_PATH+"o2.png"),    (45, 45))

# =====================================================================
# [로드] 인게임 오브젝트 이미지
# =====================================================================
img_player    = load_img(IMG_PATH+"alveolus.png",  SCALE_ALVEOLUS)
img_bullet    = load_img(IMG_PATH+"bullet.png",    SCALE_BULLET)
img_dust      = load_img(IMG_PATH+"dust.png",      SCALE_DUST)
img_food      = load_img(IMG_PATH+"food.png",      SCALE_FOOD)
img_cigarette = load_img(IMG_PATH+"cigarette.png", SCALE_CIGARETTE)
img_broccoli  = load_img(IMG_PATH+"broccoli.png",  SCALE_BROCCOLI)
img_water     = load_img(IMG_PATH+"water.png",     SCALE_WATER)
img_nebulizer = load_img(IMG_PATH+"nebulizer.png", NEBULIZER_SCALE)
img_bosses    = [load_img(IMG_PATH+f"boss{i}.png", SCALE_BOSS) for i in (1,2,3)]

# [방어] 네불라이저 이미지가 화면 절반 초과 시 강제 축소
if img_nebulizer.get_width() > BASE_WIDTH//2 - 20:
    img_nebulizer = pygame.transform.rotozoom(img_nebulizer, 0, (BASE_WIDTH//2-20)/img_nebulizer.get_width())

# [캐싱] 충돌 판정용 이미지 크기
w_p,h_p = img_player.get_size();    w_b,h_b = img_bullet.get_size()
w_d,h_d = img_dust.get_size();      w_f,h_f = img_food.get_size()
w_c,h_c = img_cigarette.get_size(); w_boss,h_boss = img_bosses[0].get_size()
w_broc,h_broc = img_broccoli.get_size()
w_w,h_w = img_water.get_size();     w_n,h_n = img_nebulizer.get_size()

intro_images = [pygame.transform.scale(load_img(IMG_PATH+f"story{i}.png"),(BASE_WIDTH,BASE_HEIGHT)) for i in range(1,8)]

# =====================================================================
# [로드] 사운드 · BGM
# =====================================================================
sfx_item         = load_sound(SOUND_PATH+"아이템획득.mp3")
sfx_start        = load_sound(SOUND_PATH+"게임시작.mp3")
sfx_fail         = load_sound(SOUND_PATH+"게임실패.mp3")
sfx_success      = load_sound(SOUND_PATH+"게임성공.mp3")
sfx_boss_warning = load_sound(SOUND_PATH+"경고음.mp3")
sfx_nebulizer    = load_sound(SOUND_PATH+"네불라이저효과음.mp3")
sfx_die          = load_sound(SOUND_PATH+"sound_hit.mp3")
sfx_button       = load_sound(SOUND_PATH+"버튼클릭음.mp3")
sfx_shoot        = load_sound(SOUND_PATH+"발사소리.mp3")
if sfx_shoot: sfx_shoot.set_volume(0.5)

pygame.mixer.music.load(SOUND_PATH+"배경음1.mp3")
pygame.mixer.music.play(-1)

# =====================================================================
# [로드] 폰트 (커스텀 TTF → 실패 시 시스템 Arial 폴백)
# =====================================================================
try:
    font_sm = pygame.font.Font(os.path.join(FONT_PATH,"Bazzi.ttf"), 28)
    font_bg = pygame.font.Font(os.path.join(FONT_PATH,"Bazzi.ttf"), 50)
    font_ui = pygame.font.Font(os.path.join(FONT_PATH,"Bazzi.ttf"), 34)
except Exception:
    print("커스텀 폰트를 찾을 수 없습니다. 기본 폰트로 실행합니다.")
    font_sm = pygame.font.SysFont("arial", 28, bold=True)
    font_bg = pygame.font.SysFont("arial", 50, bold=True)
    font_ui = pygame.font.SysFont("arial", 34, bold=True)
font_title = pygame.font.SysFont("impact", 90, bold=True)

# =====================================================================
# [함수] 유틸리티
# =====================================================================
def get_non_overlap_x(existing_list, width, start_x=0, end_x=None, min_gap=10):
    """겹치지 않는 랜덤 X 좌표 반환 (최대 100회 탐색, 실패 시 무작위 반환)"""
    if end_x is None: end_x = BASE_WIDTH//2 - width
    if start_x >= end_x: end_x = start_x + 1
    for _ in range(100):
        x = random.randrange(start_x, end_x)
        if not any(abs(x - obj[0]) < width + min_gap for obj in existing_list):
            return x
    return random.randrange(start_x, end_x)

def draw_txt(surf, txt, font, c_txt, c_out, x, y):
    """8방향 외곽선 텍스트 렌더링 (가독성 향상)"""
    for dx, dy in [(-2,-2),(-2,2),(2,-2),(2,2),(0,-2),(-2,0),(2,0),(0,2)]:
        surf.blit(font.render(txt, True, c_out), (x+dx, y+dy))
    surf.blit(font.render(txt, True, c_txt), (x, y))

def draw_bar(surf, x, y, w, h, ratio, c_fill, c_bg=(40,40,40)):
    """둥근 게이지 바 렌더링 (ratio: 0.0~1.0)"""
    pygame.draw.rect(surf, c_bg,    (x, y, w, h), border_radius=h//2)
    fw = int(w * max(0.0, min(1.0, ratio)))
    if fw > 0: pygame.draw.rect(surf, c_fill, (x, y, fw, h), border_radius=h//2)
    pygame.draw.rect(surf, (0,0,0), (x, y, w, h), width=2, border_radius=h//2)

def draw_hp(surf, x, y, hp, max_hp, is_boss=False):
    """적 머리 위 소형 체력바 렌더링"""
    if hp <= 0: return
    w, h = (BOSS_HP_BAR_W, BOSS_HP_BAR_H) if is_boss else (MINI_HP_BAR_W, MINI_HP_BAR_H)
    pygame.draw.rect(surf, (80,0,0),    (x, y, w, h))
    pygame.draw.rect(surf, (255,50,50), (x, y, int(w*(hp/max_hp)), h))
    pygame.draw.rect(surf, (0,0,0),     (x, y, w, h), width=1)

# =====================================================================
# [함수] 게임 초기화
# =====================================================================
def reset_game():
    """재시작 시 모든 게임 데이터를 초기 상태로 되돌림"""
    global p_list, bullet_list, to_x, move_speed, spo2, bullet_damage
    global e_list, boss_data, itm_list, f_txts, neb_data, dmg_pops
    global is_over, is_success, score, t_start, sec, t_spawn, sound_end

    p_list        = [[BASE_WIDTH/2 - w_p/2, BASE_HEIGHT - h_p - 20]]
    to_x          = 0
    move_speed    = PLAYER_BASE_SPEED
    spo2          = SPO2_START
    bullet_list   = []
    bullet_damage = PLAYER_BASE_DAMAGE

    e_list = {'dust':[], 'food':[], 'cig':[]}   # 각 요소: [x, y, 현재체력, 최대체력]

    initial_boss_hp = BOSS_HP_LIST[0] if BOSS_HP_LIST else 100
    boss_data = {
        'hp': initial_boss_hp, 'max_hp': initial_boss_hp,
        'alive': False, 'x': 0, 'y': 0,
        'warn': False, 't_warn': 0, 't_last': 0,
        'imgs': img_bosses.copy(), 'cnt': 0, 'cur': img_bosses[0],
    }

    itm_list  = {'broc':[], 'water':[]}
    f_txts    = [];  dmg_pops = []
    neb_data  = {'list':[], 'times':set(), 'on':False, 't_on':0}

    is_over, is_success, score = False, False, 0
    t_start, sec = pygame.time.get_ticks(), 0
    # [스폰 타이머] 음수 초기값 → 시작 직후 즉각 스폰 방지
    t_spawn   = {'dust':-1, 'food':-3, 'cig':-6, 'broc':-5, 'water':-7}
    sound_end = False

reset_game()

# =====================================================================
# [메인 루프]
# =====================================================================
play, is_run, intro_idx = True, False, 0

while play:
    clock.tick(FPS)
    sh_x, sh_y = 0, 0   # [흔들림] 화면 shake 오프셋 — 매 프레임 초기화

    # ------------------------------------------------------------------
    # [이벤트] 키보드 · 마우스 입력
    # ------------------------------------------------------------------
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: play = False

        if game_state == STATE_START and ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = ev.pos[0]/scale_ratio, ev.pos[1]/scale_ratio
            if rect_btn_start.collidepoint(mx, my):
                if sfx_button: sfx_button.play()
                intro_idx, game_state = 0, STATE_INTRO

        elif game_state == STATE_INTRO and ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
            if sfx_button: sfx_button.play()
            intro_idx += 1
            if intro_idx >= len(intro_images): game_state = STATE_READY

        elif game_state == STATE_READY and ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = ev.pos[0]/scale_ratio, ev.pos[1]/scale_ratio
            if rect_ready_start.collidepoint(mx, my):
                if sfx_button: sfx_button.play()
                if sfx_start:  sfx_start.play()
                is_run, t_start = True, pygame.time.get_ticks()
                pygame.mixer.music.load(SOUND_PATH+"배경음2.mp3"); pygame.mixer.music.play(-1)
                game_state = STATE_GAME

        elif game_state == STATE_GAME:
            if (is_over or is_success) and ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos[0]/scale_ratio, ev.pos[1]/scale_ratio
                if rect_btn_retry.collidepoint(mx, my):
                    if sfx_button: sfx_button.play()
                    reset_game(); is_run, t_start = True, pygame.time.get_ticks()
                    pygame.mixer.music.load(SOUND_PATH+"배경음2.mp3"); pygame.mixer.music.play(-1)
                if rect_btn_quit.collidepoint(mx, my):
                    if sfx_button: sfx_button.play()
                    play = False   # [종료] sfx 유무와 관계없이 항상 실행

            elif is_run and not is_over and not is_success:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RIGHT:  to_x = move_speed
                    elif ev.key == pygame.K_LEFT: to_x = -move_speed
                    elif ev.key == pygame.K_SPACE:
                        if sfx_shoot: sfx_shoot.play()
                        for p in p_list: bullet_list.append([p[0]+w_p/2-w_b/2, p[1]])
                elif ev.type == pygame.KEYUP and ev.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    to_x = 0

    # ------------------------------------------------------------------
    # [렌더링] 화면 상태별 배경
    # ------------------------------------------------------------------
    if game_state == STATE_START:
        background.blit(img_start_bg,(0,0)); background.blit(img_name,rect_name); background.blit(img_btn_start,rect_btn_start)
    elif game_state == STATE_INTRO:
        if intro_idx < len(intro_images): background.blit(intro_images[intro_idx],(0,0))
    elif game_state == STATE_READY:
        background.blit(img_start_bg,(0,0)); background.blit(img_ready_start,rect_ready_start)

    # ------------------------------------------------------------------
    # [본 게임] 메인 로직
    # ------------------------------------------------------------------
    elif game_state == STATE_GAME:
        background.blit(img_bg,(0,0))

        if is_run and not is_over and not is_success:
            sec    = (pygame.time.get_ticks() - t_start) / 1000
            t_left = max(0, int(TIME_LIMIT - sec))
            spo2  -= SPO2_DECAY_PER_SEC * (clock.get_time() / 1000)

            # [판정] 게임 오버 · 클리어
            if spo2 <= 0: spo2, is_over = 0, True
            if sec >= TIME_LIMIT:
                if spo2 >= SPO2_WIN_THRESHOLD: is_success = True
                else: is_over = True

            # --- 스폰 ---
            all_e = e_list['dust'] + e_list['cig'] + e_list['food']
            # [스케일링] 경과 시간에 비례해 적 체력 자동 증가
            s_dust = DUST_HP_BASE      + int(sec * ENEMY_HP_SCALE_PER_SEC)
            s_food = FOOD_HP_BASE      + int(sec * ENEMY_HP_SCALE_PER_SEC)
            s_cig  = CIGARETTE_HP_BASE + int(sec * ENEMY_HP_SCALE_PER_SEC)

            if sec - t_spawn['dust'] >= DUST_SPAWN_INTERVAL:
                t_spawn['dust'] = sec
                e_list['dust'].append([get_non_overlap_x(all_e,w_d), 0, s_dust, s_dust])

            if sec >= FOOD_SPAWN_START and int(sec) - t_spawn['food'] >= FOOD_SPAWN_INTERVAL:
                t_spawn['food'] = int(sec)
                e_list['food'].append([get_non_overlap_x(all_e,w_f), 0, s_food, s_food])

            if sec >= CIGARETTE_SPAWN_START and int(sec) - t_spawn['cig'] >= CIGARETTE_SPAWN_INTERVAL:
                t_spawn['cig'] = int(sec)
                e_list['cig'].append([get_non_overlap_x(all_e,w_c), 0, s_cig, s_cig])

            # [보스 스폰] 조건: 생존 보스 없음 + 대기 중 + 횟수 여유 + 시간 충족
            if (not boss_data['alive'] and boss_data['imgs'] and boss_data['cnt'] < BOSS_MAX_SPAWN
                    and int(sec)-boss_data['t_last'] >= BOSS_INTERVAL and sec >= BOSS_FIRST_DELAY):
                if sfx_boss_warning: sfx_boss_warning.play()
                cnt = boss_data['cnt']
                hp  = BOSS_HP_LIST[cnt] if cnt < len(BOSS_HP_LIST) else BOSS_HP_LIST[-1]
                boss_data.update({'alive':True,'warn':True,'t_warn':pygame.time.get_ticks(),
                                  't_last':int(sec),'x':random.randrange(0,max(1,BASE_WIDTH//2-w_boss)),
                                  'y':0,'hp':hp,'max_hp':hp})
                boss_data['cur'] = random.choice(boss_data['imgs']); boss_data['imgs'].remove(boss_data['cur'])
                boss_data['cnt'] += 1

            # [아이템 스폰] 화면 오른쪽 절반에서 등장
            if int(sec) - t_spawn['broc'] >= BROCCOLI_SPAWN_INTERVAL:
                t_spawn['broc'] = int(sec)
                all_i = itm_list['broc'] + itm_list['water']
                itm_list['broc'].append([get_non_overlap_x(all_i,w_broc,BASE_WIDTH//2,BASE_WIDTH-w_broc,80), 0])

            if int(sec) - t_spawn['water'] >= WATER_SPAWN_INTERVAL:
                t_spawn['water'] = int(sec)
                all_i = itm_list['broc'] + itm_list['water']
                itm_list['water'].append([get_non_overlap_x(all_i,w_w,BASE_WIDTH//2,BASE_WIDTH-w_w,80), 0])

            # [네불라이저 스폰] 지정 시각에 1회씩만 등장
            for t in NEBULIZER_SPAWN_TIMES:
                if sec >= t and t not in neb_data['times']:
                    neb_data['times'].add(t)
                    mx = BASE_WIDTH//2; my = BASE_WIDTH-w_n
                    neb_data['list'].append([mx if my<=mx else random.randrange(mx,my), 0])

            # --- 플레이어 이동 · 화면 이탈 방지 ---
            for p in p_list: p[0] += to_x
            if p_list:
                lx = min(p[0] for p in p_list)
                if lx < 0:
                    for p in p_list: p[0] -= lx
                rx = max(p[0] for p in p_list)
                if rx > BASE_WIDTH - w_p:
                    for p in p_list: p[0] -= (rx - (BASE_WIDTH - w_p))

            # --- 적 처리 (먼지 · 고지방 · 담배) ---
            # [구조] 튜플 리스트로 3종 적에 동일 로직 재사용
            e_info = [('dust',img_dust,     w_d,h_d,DUST_SPEED,     SCORE_DUST,     SPO2_GAIN_DUST),
                      ('food',img_food,     w_f,h_f,FOOD_SPEED,     SCORE_FOOD,     SPO2_GAIN_FOOD),
                      ('cig', img_cigarette,w_c,h_c,CIGARETTE_SPEED,SCORE_CIGARETTE,SPO2_GAIN_CIGARETTE)]

            for key,img,w,h,spd,sc,sgn in e_info:
                for e in e_list[key][:]:   # [사본 순회] 안전한 삭제를 위해 복사본으로 반복
                    e[1] += spd; background.blit(img,(e[0],e[1]))
                    draw_hp(background, e[0]+w/2-MINI_HP_BAR_W/2, e[1]-12, e[2], e[3])
                    hit = False; rect = pygame.Rect(e[0],e[1],w,h)
                    for p in p_list[:]:
                        if rect.colliderect(pygame.Rect(p[0],p[1],w_p,h_p)):
                            p_list.remove(p); hit=True
                            if sfx_die: sfx_die.play()
                            if e in e_list[key]: e_list[key].remove(e)
                            break
                    if hit:
                        if not p_list: is_over = True
                        continue
                    if e[1] >= BASE_HEIGHT - h: is_over = True

            # --- 보스 처리 ---
            if boss_data['alive']:
                boss_data['y'] += BOSS_SPEED; background.blit(boss_data['cur'],(boss_data['x'],boss_data['y']))
                draw_hp(background, boss_data['x']+w_boss/2-BOSS_HP_BAR_W/2, boss_data['y']-25,
                        boss_data['hp'], boss_data['max_hp'], is_boss=True)
                rect = pygame.Rect(boss_data['x'],boss_data['y'],w_boss,h_boss)
                for p in p_list[:]:
                    if rect.colliderect(pygame.Rect(p[0],p[1],w_p,h_p)):
                        p_list.remove(p)
                        if sfx_die: sfx_die.play()
                        boss_data['hp'] -= 5
                        if boss_data['hp'] <= 0:
                            boss_data['alive']=False; score+=SCORE_BOSS; spo2=min(100,spo2+SPO2_GAIN_BOSS)
                        break
                if not p_list or boss_data['y'] >= BASE_HEIGHT - h_boss: is_over = True

            # --- 아이템 처리 (브로콜리 · 물) ---
            i_info = [('broc',img_broccoli,w_broc,h_broc,BROCCOLI_SPEED),
                      ('water',img_water,  w_w,   h_w,   WATER_SPEED)]
            for key,img,w,h,spd in i_info:
                for i in itm_list[key][:]:
                    i[1] += spd; background.blit(img,(i[0],i[1]))
                    if i[1] >= BASE_HEIGHT - h: itm_list[key].remove(i); continue
                    for p in p_list:
                        if pygame.Rect(i[0],i[1],w,h).colliderect(pygame.Rect(p[0],p[1],w_p,h_p)):
                            if sfx_item: sfx_item.play()
                            itm_list[key].remove(i)
                            if key == 'broc':
                                f_txts.append([p[0],p[1],"Squad +1",(0,255,50),pygame.time.get_ticks()])
                                bullet_damage += BROCCOLI_DAMAGE_GAIN
                                if len(p_list) < BROCCOLI_MAX_STACK:
                                    ox, oy = w_p*BROCCOLI_INSERT_OFFSET_RATIO, h_p*0.6
                                    if len(p_list) % ROW_CAPACITY == 0:
                                        p_list.insert(0,[max(pl[0] for pl in p_list), min(pl[1] for pl in p_list)-oy])
                                    else:
                                        p_list.insert(0,[p_list[0][0]-ox, p_list[0][1]])
                            elif key == 'water':
                                f_txts.append([p[0],p[1],"Speed UP!",(0,200,255),pygame.time.get_ticks()])
                                move_speed += WATER_SPEED_GAIN
                            break

            # --- 필살기 네불라이저 처리 ---
            for neb in neb_data['list'][:]:
                neb[1] += NEBULIZER_SPEED; background.blit(img_nebulizer,(neb[0],neb[1]))
                if neb[1] >= BASE_HEIGHT - h_n: neb_data['list'].remove(neb); continue
                rect = pygame.Rect(neb[0],neb[1],w_n,h_n)
                if any(rect.colliderect(pygame.Rect(p[0],p[1],w_p,h_p)) for p in p_list):
                    if sfx_nebulizer: sfx_nebulizer.play()
                    f_txts.append([p_list[0][0],p_list[0][1],f"DAMAGE ALL -{NEBULIZER_ALL_ENEMY_HP_DEC}",(0,220,255),pygame.time.get_ticks()])
                    neb_data['list'].remove(neb); neb_data.update({'on':True,'t_on':pygame.time.get_ticks()})
                    for k,_,w,_,_,sc,sgn in e_info:
                        for e in e_list[k][:]:
                            e[2] -= NEBULIZER_ALL_ENEMY_HP_DEC
                            dmg_pops.append((e[0]+w//2,e[1],pygame.time.get_ticks()))
                            if e[2] <= 0: e_list[k].remove(e); score+=sc; spo2=min(100,spo2+sgn)
                    if boss_data['alive']:
                        boss_data['hp'] -= NEBULIZER_ALL_ENEMY_HP_DEC
                        dmg_pops.append((boss_data['x']+w_boss//2,boss_data['y'],pygame.time.get_ticks()))
                        if boss_data['hp'] <= 0: boss_data['alive']=False; score+=SCORE_BOSS; spo2=min(100,spo2+SPO2_GAIN_BOSS)

            # --- 총알 처리 ---
            for b in bullet_list[:]:
                b[1] -= BULLET_SPEED; background.blit(img_bullet,(b[0],b[1]))
                if b[1] <= 0: bullet_list.remove(b); continue
                hit = False
                for k,_,w,h,_,sc,sgn in e_info:
                    for e in e_list[k][:]:
                        if e[0]<b[0]<e[0]+w and e[1]<b[1]<e[1]+h:
                            e[2]-=bullet_damage; bullet_list.remove(b); hit=True
                            if e[2]<=0: e_list[k].remove(e); score+=sc; spo2=min(100,spo2+sgn)
                            break
                    if hit: break
                if hit: continue
                bx,by = boss_data['x'],boss_data['y']
                if boss_data['alive'] and bx<b[0]<bx+w_boss and by<b[1]<by+h_boss:
                    boss_data['hp']-=bullet_damage; bullet_list.remove(b)
                    if boss_data['hp']<=0: boss_data['alive']=False; score+=SCORE_BOSS; spo2=min(100,spo2+SPO2_GAIN_BOSS)

        # ------------------------------------------------------------------
        # [렌더링] UI · 이펙트
        # ------------------------------------------------------------------

        # [병사] Y 기준 정렬 → 뒤 병사가 먼저 그려져 자연스럽게 겹침
        for p in sorted(p_list, key=lambda v: v[1]): background.blit(img_player,(p[0],p[1]))

        # [HUD] 점수 · 시간 · SpO2
        background.blit(img_icon_star,(20,20))
        draw_txt(background,f"{score}",font_ui,(255,215,0),(80,50,0),20+ICON_SIZE+10,20)
        background.blit(img_icon_time,(BASE_WIDTH//2-50,20))
        draw_txt(background,f"{t_left if 't_left' in locals() else TIME_LIMIT}",font_ui,(255,255,255),(50,50,50),BASE_WIDTH//2-50+ICON_SIZE+10,20)
        c_sp = (0,200,100) if spo2>=SPO2_WIN_THRESHOLD else (255,80,80)
        draw_bar(background,BASE_WIDTH//2-200,65,400,24,spo2/100.0,c_sp)
        background.blit(img_icon_spo2,(BASE_WIDTH//2-200-5,65-ICON_SIZE-10))
        draw_txt(background,f"{int(spo2)}%",font_ui,c_sp,(0,0,0),BASE_WIDTH//2-200+ICON_SIZE+10,65-ICON_SIZE-5)

        ct = pygame.time.get_ticks()

        # [이펙트] 플로팅 텍스트 — 상승하며 서서히 투명해짐
        for f in f_txts[:]:
            dt = ct - f[4]
            if dt > FLOAT_TEXT_LIFETIME_MS: f_txts.remove(f); continue
            f[1] -= FLOAT_TEXT_RISE_SPEED * clock.get_time()
            ts = font_ui.render(f[2],True,f[3]); a = pygame.Surface(ts.get_size(),pygame.SRCALPHA)
            a.blit(ts,(0,0)); a.set_alpha(max(0,255-int((dt/FLOAT_TEXT_LIFETIME_MS)*255)))
            background.blit(a,(f[0]+w_p/2-ts.get_width()/2,f[1]-40))

        # [이펙트] 보스 경고 — 붉은 플래시 + 경고 이미지 흔들림
        if boss_data['warn']:
            el = (ct - boss_data['t_warn']) / 1000
            if el > BOSS_WARNING_SEC: boss_data['warn'] = False
            else:
                sh_x,sh_y = random.randint(-2,2),random.randint(-2,2)
                if int(el*6)%2 == 0:
                    fl=pygame.Surface((BASE_WIDTH,BASE_HEIGHT)); fl.set_alpha(100); fl.fill((255,0,0)); background.blit(fl,(0,0))
                if img_warning_boss: background.blit(img_warning_boss,img_warning_boss.get_rect(center=(BASE_WIDTH/2,BASE_HEIGHT/2-200)))
                else: txt=font_bg.render("BOSS WARNING !!!",True,(255,255,0)); background.blit(txt,(BASE_WIDTH/2-txt.get_width()/2,BASE_HEIGHT/2-200))

        # [이펙트] 네불라이저 발동 — 푸른 화면 플래시
        if neb_data['on']:
            if ct - neb_data['t_on'] > NEBULIZER_EFFECT_DURATION_MS: neb_data['on'] = False
            else:
                fl=pygame.Surface((BASE_WIDTH,BASE_HEIGHT)); fl.set_alpha(90); fl.fill((0,220,255)); background.blit(fl,(0,0))
                if img_nebulizer_effect: background.blit(img_nebulizer_effect,img_nebulizer_effect.get_rect(center=(BASE_WIDTH/2,400)))

        # [이펙트] 네불라이저 데미지 팝업 숫자
        for d in dmg_pops[:]:
            dt = ct - d[2]
            if dt > POPUP_LIFETIME_MS: dmg_pops.remove(d); continue
            ts=font_sm.render(f"-{NEBULIZER_ALL_ENEMY_HP_DEC}",True,(0,220,255)); ts.set_alpha(max(0,255-int(dt*POPUP_ALPHA_DEC_PER_MS)))
            background.blit(ts,(d[0]-ts.get_width()/2,(d[1]-30)-dt*POPUP_RISE_PER_MS))

        # ------------------------------------------------------------------
        # [결과 화면] 성공 / 게임 오버
        # ------------------------------------------------------------------
        if is_over or is_success:
            if not sound_end:
                pygame.mixer.music.stop()
                (sfx_success.play() if is_success and sfx_success else sfx_fail.play() if sfx_fail else None)
                sound_end = True

            background.blit(img_success_bg if is_success else img_fail_bg,(0,0))

            bw,bh=600,460; bx,by=BASE_WIDTH//2-bw//2,BASE_HEIGHT//2-280
            bs=pygame.Surface((bw,bh),pygame.SRCALPHA); bs.fill((0,0,0,180))
            pygame.draw.rect(bs,(255,255,255,100),(0,0,bw,bh),width=4,border_radius=20); background.blit(bs,(bx,by))

            tit = img_title_success if is_success else img_title_gameover
            if tit: background.blit(tit,tit.get_rect(center=(BASE_WIDTH//2,by+80)))
            else:
                lbl="SUCCESS!" if is_success else "GAME OVER"; c=(100,255,100) if is_success else (255,80,80)
                draw_txt(background,lbl,font_title,c,(0,0,0),BASE_WIDTH//2-font_title.size(lbl)[0]//2,by+20)

            sl=f"FINAL SCORE :  {score}"
            draw_txt(background,sl,font_bg,(255,215,0),(0,0,0),BASE_WIDTH//2-font_bg.size(sl)[0]//2,by+250)

            c_sp=(0,200,100) if spo2>=SPO2_WIN_THRESHOLD else (255,80,80)
            sp_txt=f"SpO2 Normal ({int(spo2)}%)" if spo2>=SPO2_WIN_THRESHOLD else f"SpO2 Danger! ({int(spo2)}%)"
            sx=BASE_WIDTH//2-(ICON_SIZE+10+font_ui.size(sp_txt)[0])//2
            background.blit(img_icon_spo2,(sx-10,by+325)); draw_txt(background,sp_txt,font_ui,c_sp,(0,0,0),sx+ICON_SIZE+10,by+330)
            draw_bar(background,BASE_WIDTH//2-150,by+380,300,24,spo2/100.0,c_sp)

            rect_btn_retry.center,rect_btn_quit.center=(BASE_WIDTH/2-140,by+bh+90),(BASE_WIDTH/2+140,by+bh+90)
            background.blit(img_btn_retry,rect_btn_retry); background.blit(img_btn_quit,rect_btn_quit)

    # [출력] background → screen 스케일 변환 후 최종 출력 (shake 오프셋 반영)
    scaled = pygame.transform.scale(background,(display_w,display_h))
    screen.fill((0,0,0)); screen.blit(scaled,(sh_x,sh_y)); pygame.display.update()

pygame.quit()
