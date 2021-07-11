import pygame
import random
import time
from datetime import datetime           # 게임을 위해 필요한 모듈들을 받아온다.

# 1. 게임 초기화를 위해 반드시 필요함
pygame.init()                           # 초기화한다. 게임 시작을 위해 반드시 해야 한다.

# 2.게임창 옵션  # 스크린 설정
size = [1400, 750]                      # 화면 크기= 1400, 750
screen = pygame.display.set_mode(size)  # 스크린을 만드는데, 위의 사이즈 리스트에서 크기를 받아온다.
title = "Avoid Game"                    # 창 제목 설정
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()             # 시간설정을 위해 필요하다.
pygame.mixer.init()                     # 음악설정을 위해 필요하다.

class obj:                              # obj라는 클래스를 만들어서 게임에 들어가는 여러 가지 객체를 만든다.
    def __init__(self):                 # 객체 시작할 때 부터 생기는 것들
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, address):         # 이미지 불러오는 함수, jpg, png 형식의 파일을 받아올 수 있다.
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()  # 이미지 불러오기, png에 사용
        else:
            self.img = pygame.image.load(address)   # 이미지 불러오기, jpg에 사용
            self.sx, self.sy = self.img.get_size()  # png와 jpg는 불러오는 방식이 다르기 때문에 두 가지를 따로 만들어야 한다.

    def change_size(self, sx, sy):                  # 이미지 크기를 조정할 수 있는 함수이다.
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))     # 스크린에 띄우기, 이것이 없으면 객체가 생겨도 화면에 나타나지 않는다.


# a.x-b.sx <=b.x <=a.x+a.sx
# a.y-b.sy<=b.y<=a.y+a.sy
def crash(a, b):                                    # 충돌 함수 정의. 캐릭터가 운석에 맞거나 아이템을 먹을 때 특정한 효과를 이끌어낼 수 있다.
    if (a.x - b.sx <= b.x-17) and (b.x <= a.x + a.sx-18):
        if (a.y - b.sy <= b.y-20) and (b.y <= a.y + a.sy-18): # 둘의 x좌표와 y좌표가 겹치면
            return True                                       # True를 반환한다
        else:
            return False
    else:
        return False



s1 = obj()                                                     # 객체 생성(캐릭터)
s1.put_img("C:/Users/mgks2/OneDrive/바탕 화면/butterfly-1.png")  # 이미지를 불러온다.
s1.change_size(90, 90)                                         # 이미지를 불러올 때 주소에 있는 \와 /의 슬래시 방향에 유의해야 한다.
s1.x = round(size[0] / 2 - s1.sx / 2)                          # 초기 x좌표
s1.y = size[1] - s1.sy - 15                                    # 초기 y좌표
speed1 = 10
s1.move = speed1                                               # 초기 이동속도 설정. 10이지만 나중에 아이템에 따라 변할 수 있기에 숫자가 아닌 변수를 따로 하나 설정했다.
SB = 0                                                         # 게임 내에 만들어질 여러 화면을 구분하는 변수. 0=시작전 준비화면 1=게임화면 2=결과화면
SC = 0                                                         # 게임이 켜지고 꺼지는 것과 관련되어 있다. SC가 0이 아니게 되면 게임이 꺼진다.
count_list=[]                                                  # 점수가 저장되는 공간이다. 점수=버틴 시간 이다.
# 4.0 게임  시작 대기 화면
while SC==0:
    while SB == 0:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                      # 나가는 기능, SC가 0이 아니게 되면 프로그램이 멈춘다.
                pygame.quit()
            if event.type == pygame.KEYDOWN:                   # 스페이스를 누르면 게임 시작. SB가 1이 되면서 화면이 전환된다.
                if event.key == pygame.K_SPACE:                # 스페이스를 누르면 게임이 시작되면서 배경음악이 재생된다.
                    pygame.mixer.music.load('C:/Users/mgks2/OneDrive/바탕 화면/bgm') # 음악파일을 받아온다.
                    pygame.mixer.music.play(-1)                # play로 재생하는데, (-1)을 넣어두면 무한 반복된다.
                    SB = 1                                     # 게임 시작. 준비화면은 SB가 0일때만 나온다.

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 50)  # 폰트와 크기 설정. 해당 위치에서 폰트를 받아오고 크기가 정해진다.
        text = font.render("PRESS SPACE KEY TO START THE GAME", True, (255, 255, 0)) # 텍스트 설정. 어떤 텍스트를 적을지와 텍스트의 색 또한 고를 수 있다.
        screen.blit(text, (150, round(size[1] / 2 - 50)))      # 해당 텍스트를 스크린에 나타나게 한다. 앞서 정의했던 show 함수와 같은 원리이지만 텍스트는 obj가 아니기에 사용할 수 없다.
        pygame.display.flip()                                  # 전체 화면을 업데이트한다.

    # 4. 메인 이벤트 적용
    start_time = datetime.now()                                # 시간측정을 시작할 수 있게 한다.
    i_list = []                                                # 아이템이 저장되는 리스트
    i2_list = []                                               # 아이템과 충돌했을 때 효과를 처리하기 위해 만든 리스트
    i3_list = []                                               # 아이템이 화면 밖으로 나갔을 때 처리하기 위한 리스트
    m_list = []                                                # 운석이 저장되는 리스트
    m2_list = []                                               # 운석이 화면 밖으로 나갔을 때 처리하기 위한 리스트
    random_list = [0, 1, 2, 3, 4]                              # 이곳에서 랜덤한 요소를 받아 아이템을 생성한다.
    b_list = ["C:/Users/mgks2/OneDrive/바탕 화면/배경1.jpg",
              "C:/Users/mgks2/OneDrive/바탕 화면/배경2.jpg",
              "C:/Users/mgks2/OneDrive/바탕 화면/배경3.jpg",
              "C:/Users/mgks2/OneDrive/바탕 화면/배경4.jpg"]     # 배경 이미지 목록들.
    left_go = False
    right_go = False
    up_go = False
    down_go = False                                            # 이후 나올 캐릭터의 이동과 관련이 있다. 지금은 당연히 멈춰있는 상태.
    speed1 = 10                                                # 나비와 운석의 초기 속도이다.
    speed2 = 5
    t = 0                                                      # 이후 나올 아이템의 생성과 관련이 있다. 나중에 랜덤으로 바뀌니 지금은 무슨 숫자로 정의되든 상관없다.
    lose = 0                                                   # 지나간 운석들의 개수이다.
    life = 3                                                   # 목숨의 개수이다. 운석에 부딪힐 때마다 하나씩 깎이고, 아이템에 따라 달라질 수 있다.
    m_size = 80                                                # 운석의 크기이다.
    mn = 0                                                     # 운석의 크기인 m_size를 시간이 지남에 따라 더 크게 하기 위한 변수이다.
    time_divide = 0                                            # 아이템을 시간이 지남에 따라 생성하기 위한 변수이다. 일종의 차단기 역할을 한다.
    while SB == 1:                                             # 게임 코드. 이 while 문에 들어있는 코드들이 게임하는 동안 적용된다.
        # 4.1 FPS 설정
        clock.tick(60)                                         # 초당 프레임을 맞추기 위해 들어간다. 60프레임으로 설정되어있다.
        # 4.2 각종 입력 감지
        for event in pygame.event.get():                       # 여러 이벤트들. 여러 입력들을 감지해서 그것에 맞는 효과들을 낸다.
            if event.type == pygame.QUIT:                      # 나가는 기능, SB가 0이 아니게 되면 프로그램이 멈춘다.
                pygame.quit()
            if event.type == pygame.KEYDOWN:                   # KEYDOWN: 누를때, KEYUP: 뗄때
                if event.key == pygame.K_LEFT:                 # 왼쪽키가 눌린다면
                    left_go = True                             # 왼쪽으로 간다. left_go로 왼쪽으로 이동시키는 것은 나중에 나온다.
                elif event.key == pygame.K_RIGHT:              # 오른쪽키가 눌린다면. 이하 동일
                    right_go = True
            elif event.type == pygame.KEYUP:                   # 만약 KEYUP부분을 설정하지 않고 KEYDOWN 부분만 만들면 꾹 누르는 것이 인식되지 않고 누를 때마다 한칸씩만 움직인다.
                if event.key == pygame.K_LEFT:
                    left_go = False
                elif event.key == pygame.K_RIGHT:
                    right_go = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up_go = True
                elif event.key == pygame.K_DOWN:
                    down_go = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up_go = False
                elif event.key == pygame.K_DOWN:
                    down_go = False

            # print(event)
        # 4.3 입력,시간에 따른 변화    /움직임 정의
        now_time = datetime.now()                                           # 시간을 설정한다.
        delta_time = round((now_time - start_time).total_seconds())         # delta_time이 게임을 시작하고 경과된 시간이다.
        s1.move = speed1
        if left_go == True:                                                 # left_go가 True라면
            s1.x -= s1.move                                                 # s1(캐릭터)의 x좌표가 줄어든다. 왼쪽으로 이동한다.
            if s1.x <= 0:                                                   # 캐릭터가 왼쪽으로 더이상 이동할 수 없는 상황이면 x좌표가 0으로 고정되어 더이상 이동하지 않는다.
                s1.x = 0
        elif right_go == True:                                              # 다른 방향으로 이동하는 것도 위와 동일하다.
            s1.x += s1.move
            if s1.x >= size[0] - s1.sx:
                s1.x = size[0] - s1.sx
        if up_go == True:
            s1.y -= s1.move
            if s1.y <= 0:
                s1.y = 0
        elif down_go == True:
            s1.y += s1.move
            if s1.y >= size[1] - s1.sy:
                s1.y = size[1] - s1.sy
        if random.random() > 0.98:                                          # 약 2퍼센트의 확률이다.
            aa = obj()                                                      # aa라는 obj를 만든다.
            aa.put_img("C:/Users/mgks2/OneDrive/바탕 화면/methor-1.png")      # 이미지를 받아온다.
            aa.change_size(m_size, m_size)                                  # 크기를 설정한다. 가로와 세로가 m_size이고 시간이 지남에 따라 커진다.
            aa.x = random.randrange(0, size[0] - aa.sx - round(s1.sx / 2))  # x는 랜덤 운석의 크기만큼 제외 한 후 비행기 절반의 크기를 뺴준다.
            aa.y = 0                                                        # y값은 화면 맨 위로 설정한다.
            aa.move = speed2                                                # speed2 = 5, 아이템에 따라 변경될 수 있다.
            m_list.append(aa)                                               # 생성된 운석은 m_list에 저장된다.
        for ki in range(len(m_list)):                                       # m_list에 저장된 운석은 아래쪽으로 계속 떨어진다.
            na = m_list[ki]
            na.y += na.move
            if na.y >= size[1]:                                             # 화면에 나간 경우
                m2_list.append(ki)                                          # m2_list에 추가된다.
        for kd in m2_list:                                                  # 화면에서 나간 m2_list의 요소들은
            del m_list[kd]                                                  # m_list의 운석을 지운다.
            lose += 1                                                       # lose= 화면 밖을 나간 운석의 수
            m2_list.clear()                                                 # 이후 m2_list를 비워 오류가 나지 않게 한다.
        m2_list = []                                                        # (이대로 남겨두면 m_list의 운석은 사라졌는데 m2_list의 요소는 남아있어 인덱스 오류가 일어난다.)

        for ni in range(len(m_list)):                                       # m_list에 있는 운석들에 대해서
            ka = m_list[ni]
            if crash(ka, s1) == True:                                       # 캐릭터와 운석이 부딪히면
                pygame.mixer.music.load('C:/Users/mgks2/OneDrive/바탕 화면/explode.mp3')     # 충돌하는 효과음을 받아서
                pygame.mixer.music.play()                                                  # 재생한다.
                time.sleep(1)                                                              # 1초간 멈춘다.
                pygame.mixer.music.load('C:/Users/mgks2/OneDrive/바탕 화면/bgm')             # 그리고 다시 배경음악을 받아서
                pygame.mixer.music.play(-1)                                                # 처음부터 재생한다.
                life -= 1                                                                  # 목숨을 하나 깎는다.
                s1.x = round(size[0] / 2 - s1.sx / 2)
                s1.y = size[1] - s1.sy - 15                                 # s1(캐릭터)의 초기 x와 y좌표. 운석에 맞고 목숨이 깎인 채로 원점에서 시작한다.
                for c in m_list:                                            # 운석의 y좌표는
                    c.y=size[1]                                             # 화면의 맨 밑으로 간다. (=사라짐)
                if life == 0:                                               # 목숨이 0이 되었을 경우
                    count_list.append(delta_time)                           # 지금까지 버틴 시간을 count_list에 추가한다.
                    SB = 2                                                  # SB를 2로 만들어 게임에서 벗어나 결과창을 띄운다.
                    time.sleep(1)                                           # 결과창에 가기 전에 1초 정지한다.
                #ok_list.append(ni)
        i3_list = []                                                        # i3_list를 초기화한다. 운석을 처리하는 m2_list와 비슷한 원리이다.
        for i in range(len(i_list)):                                        # i_list는 아이템이 저장되는 곳이다.
            a = i_list[i]
            a.y += a.move                                                   # 아이템을 떨어지게 한다.
            if a.y >= size[1]:                                              # 아이템이 화면을 벗어나면
                i3_list.append(i)                                           # i3_list에 새로 추가한다.
        for d in i3_list:                                                   # i3_list에 있는 요소들(화면을 벗어난 아이템)에 대해서
            del i_list[d]                                                   # i_list에 있는 아이템을 삭제한다.
            if len(i3_list) + 2 <= len(m_list):
                del m_list[d]
            i3_list.clear()
        i2_list = []                                                        # i2_list를 초기화한다.
        for i in range(len(i_list)):                                        # 아이템들에 대해서
            a = i_list[i]
            if crash(a, s1) == True:                                        # 캐릭터와 충돌하면
                if t == 0:                                                  # 아이템의 랜덤한 효과를 발동한다.
                    if speed2 >= 20:                                        # 1. 운석의 속도를 줄인다.
                        speed2 -= 10                                        # 2. 운석의 속도를 늘린다.
                elif t == 1:                                                # 3. 나비의 속도를 늘린다.
                    speed2 += 5                                             # 4. 운석의 크기를 초기화한다.
                elif t == 2:                                                # 5. 목숨을 하나 늘린다.
                    speed1 += 5
                elif t == 3:
                    m_size = 80
                elif t == 4:
                    life += 1
                for c in i_list:                                            # 해당 아이템의 y좌표를
                    c.y = size[1]                                           # 화면 밖으로 보낸다.
                i2_list.append(i)                                           # 충돌한 아이템을 i2_list에 새로 추가한다.
        for c in i2_list:                                                   # i2_list에 있는 요소에 대해
            del i_list[c]                                                   # i_list에 있는 아이템을 삭제한다.
        for w in range(400):
            if lose == (30 * w):                                            # 화면을 벗어난 운석의 개수가 30의 배수가 될 때마다
                b = b_list * 100                                            # b_list는 배경 이미지이다.
                p = b[w]                                                    # b_list에서 가져오는 배경을 바꿔서
                pp = obj()
                pp.put_img(p)                                               # 새로 적용한다.
                pp.change_size(1400, 750)
        if delta_time % 5 == 3:                                             # 게임을 시작한 후 시간이 5의 배수+3초가 될때마다
            if time_divide == 0:                                            # time_divide가 0일때, 이렇게 해놓지 않으면 3.0초부터 3.99초까지 계속 코드가 돌아 아이템이 여럿 나온다.
                t = random.choice(random_list)                                   # e_list=[0,1,2,3,4], 다섯 개의 숫자 중 하나를 받아온다.
                bb = obj()                                                  # 그리고 그 숫자에 맞춰서 아이템을 하나 생성한다.
                bb.put_img("C:/Users/mgks2/OneDrive/바탕 화면/random.jpg")
                bb.change_size(80, 80)
                bb.x = random.randrange(0, size[0] - bb.sx - round(s1.sx / 2))
                bb.y = 0
                bb.move = 10                                                # 아이템을 만드는 과정은 운석과 매우 비슷하다. 다른 리스트에 저장되고 이름이 다를 뿐이다.
                i_list.append(bb)                                           # 그렇게 아이템을 하나 만들고 i_list에 저장한다.
                time_divide = 1                                             # 아이템을 만드는 코드는 time_divide가 0일때만 작동하므로 time_divide를 0이 아니게 하면 1번만 작동하고 더이상 아니게 할 수 있다.
        if delta_time % 5 == 4:                                             # 아이템이 나오는 시간이 아닐 때 time_divide를 다시 0으로 맞춰두면 다음 시간에 아이템이 또 나오게 할 수 있다.
            time_divide = 0
        if lose==(10 + mn):                                                 # 화면 밖을 나간 운석이 10의 배수가 될 때마다
            mn += 10
            m_size += 10                                                    # 운석의 크기를 더 크게 한다.
            speed2 += 1                                                     # 운석의 속도가 조금씩 늘어난다.

        # 4.4 그리기
        pp.show()                                                           # 아까 lose에 따라 바뀐 배경을 보이게 한다.
        s1.show()                                                           # 캐릭터를 보이게 한다.
        for a in m_list:                                                    # m_list에 있는 운석을 보이게 한다.
            a.show()                                                        # 운석이 충돌하거나 화면을 벗어날 때 쓰던 리스트들은 show를 쓰지 않았기에 k_list 외의 운석 요소들은 보이지 않는다.
        for a in i_list:                                                    # i_list에 있는 아이템을 보이게 한다.
            a.show()                                                        # 운석과 마찬가지로 화면에서 떨어지는 아이템만 보인다.

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)          # 지금까지 화면을 지나간 운석의 개수를 볼 수 있게 한다.
        text_lose = font.render("count : {}".format(lose), True, (0, 0, 0))
        screen.blit(text_lose, (10, 5))

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)          # 지금까지 지나간 시간을 볼 수 있게 한다.
        text_time = font.render("time : {}".format(delta_time), True, (0, 0, 0))
        screen.blit(text_time, (size[0] - 220, 5))

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)          # 현재의 목숨을 볼 수 있게 한다.
        text_life = font.render("life : {}".format(life), True, (0, 0, 0))
        screen.blit(text_life, (size[0] - 350, 5))

        # 4.5 업데이트
        pygame.display.flip()                                               # 전체 화면을 업데이트한다.
    # 게임 종료()
    size = [1400, 750]
    screen = pygame.display.set_mode(size)                                  # 게임 화면을 초기화한다. 하지 않으면 결과창과 죽는 당시의 게임창이 겹치게 된다.
    while SB == 2:                                                          # 결과 창이다.
        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 100)         # 'GAME OVER' 라는 글자를 띄운다.
        text = font.render("GAME OVER", True, (255, 255, 0))
        screen.blit(text, (350, round(size[1] / 2 - 50)))

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)
        text = font.render("PRESS SPACE TO RESTART", True, (255, 255, 0))
        screen.blit(text, (450, round(size[1] / 2 - 50)+150))

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)
        text = font.render("PRESS ESC TO EXIT", True, (255, 255, 0))
        screen.blit(text, (510, round(size[1] / 2 - 50)+200))

        font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)
        text = font.render("HIGH SCORE", True, (255, 0, 255))
        screen.blit(text, (1150, 5))
                                                                            # count_list는 죽었을 때 지금까지 버틴 시간들을 저장하는 리스트이다.
        count_list.sort()                                                   # count_list를 정렬하고,
        count_list.reverse()                                                # 뒤집어서 높은 것부터 가져올 수 있게 한다.
        if len(count_list)>10:                                              # 상위 10개의 기록만 볼 수 있게 10개가 넘어가면 가장 낮은 기록을 지운다.
            del count_list[-1]

        for i in range(len(count_list)):
            font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 30)      # 기록의 개수만큼 정렬된 기록을 텍스트로 만들어서 띄운다.
            text_count = font.render("{} : {}sec".format(i+1, count_list[i]), True, (255, 255, 255))
            screen.blit(text_count, (1200, 35+i*30))
            i+=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                   # 창닫기 버튼을 누르면 꺼질 수 있게 한다.
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                             # 결과 화면에서 스페이스 버튼을 누르면,
                    SB=1                                                    # SB=1이 되어 다시 게임화면으로 돌아간다. count_list에 있는 기록은 남아있다.
                    pygame.mixer.music.load('C:/Users/mgks2/OneDrive/바탕 화면/explode.mp3') # 다시 시작할 때에도 충돌 효과음을 넣었다.
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pygame.mixer.music.load('C:/Users/mgks2/OneDrive/바탕 화면/bgm')         # 다시 배경음악을 튼다.
                    pygame.mixer.music.play(-1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:                            # esc키를 눌러도 게임이 종료되게 설정했다.
                    pygame.quit()
        pygame.display.flip()                                               # 전체 화면을 업데이트한다.
pygame.quit()