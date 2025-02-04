from itertools import filterfalse

import pygame
import random
class Fighter():
    #ham khoi tao khi bat dau
    def __init__(self,player,x,y,flip,data,sprite_sheet,animation_steps, sound):
        self.player= player
        self.size=data[0]
        self.image_scale=data[1]
        self.offset=data[2]
        self.flip=flip#Bien kiem tra su doi mat cua 2 player
        self.animation_list=self.load_images(sprite_sheet,animation_steps)
        self.action=0 #0: idle 1: run  2:jump 3: attack1 4: attack2 5: Hit 6: death
        self.frame_index=0
        self.image=self.animation_list[self.action][self.frame_index]
        self.update_time=pygame.time.get_ticks()
        self.running=False
        self.rect=pygame.Rect((x,y,80,100))
        self.vel_y=0
        self.jump= False
        self.attacking=False
        self.attack_type=0
        self.attack_cooldown=0 # hoi chieu
        self.attack_sound=sound
        self.hit=False
        self.health=100 #thanh mau'
        self.alive=True # su song
        self.ai_controlled = False
    #Xu ly hinh nhan vat chuyen dong.
    def load_images(self,sprite_sheet,animation_steps):
        #Nhap du lieu tu spireSheet
        animation_list=[]
        for y,animation in enumerate(animation_steps):
            temp_img_list=[]
            for x in range(animation):
                temp_img=sprite_sheet.subsurface(x*self.size,y*self.size,self.size,self.size)

                temp_img_list.append(pygame.transform.scale(temp_img,(self.size*self.image_scale,self.size*self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list


    def ai_move(self, target, round_over):
        if self.alive and not round_over:
            SPEED = 5
            GRAVITY = 2
            dx = 0
            dy = 0

            # Khoảng cách giữa AI và đối thủ
            distance_to_target = abs(target.rect.centerx - self.rect.centerx)

            # Logic di chuyển
            if distance_to_target > 150:  # Nếu khoảng cách lớn, tiến gần đối thủ
                if target.rect.centerx > self.rect.centerx:
                    dx = SPEED
                elif target.rect.centerx < self.rect.centerx:
                    dx = -SPEED
            elif distance_to_target < 50:  # Nếu quá gần, lùi lại
                if target.rect.centerx > self.rect.centerx:
                    dx = -SPEED
                elif target.rect.centerx < self.rect.centerx:
                    dx = SPEED

            # Tấn công khi ở khoảng cách phù hợp
            if 50 <= distance_to_target <= 150 and self.attack_cooldown == 0:
                self.attack(target)
                self.attack_type = random.choice([1, 2])  # Ngẫu nhiên chọn kiểu tấn công

            if self.jump == False:  # Chỉ nhảy khi không đang nhảy
                if self.health < 30 and target.attacking:  # Né khi máu thấp và đối thủ đang tấn công
                    self.vel_y = -30
                    self.jump = True
                elif distance_to_target < 70 and random.random() > 0.7:  # Hoặc nhảy khi đối thủ quá gần
                    self.vel_y = -30
                    self.jump = True

            # Áp dụng trọng lực
            self.vel_y += GRAVITY
            dy += self.vel_y

            # Đảm bảo AI không vượt ra ngoài màn hình
            if self.rect.bottom + dy > 500:  # Giới hạn mặt đất
                self.vel_y = 0
                dy = 500 - self.rect.bottom
                self.jump = False  # Đặt lại trạng thái nhảy khi AI chạm đất

            # Cập nhật vị trí
            self.rect.x += dx
            self.rect.y += dy

            # Đảm bảo AI luôn đối mặt với đối thủ
            self.flip = target.rect.centerx < self.rect.centerx

            # Giảm thời gian hồi chiêu
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 0.5

    def move(self, screen_width, screen_height, surface,target, round_over):
        #Toc do di chuyen
        SPEED=10
        GRAVITY=2
        dx=0
        dy=0
        self.running=False
        self.attack_type=0


        #Lay ban phim dieu khien
        key=pygame.key.get_pressed()
        #Chi thuc hien hanh dong khac neu dang khong tan cong
        if not self.ai_controlled and self.attacking == False and self.alive and not round_over:
            # kt nguoi choi 1 dieu khien
            if self.player==1:

                #thiet lap phim di chuyen ngang
                if key[pygame.K_a]:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_d]:
                    dx=SPEED
                    self.running=True
                # thiet lap phim di chuyen doc
                if key[pygame.K_w] and self.jump==False :
                    self.vel_y=-30
                    self.jump=True

                # tan cong
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # xac dinh loai tan cong duoc dung
                    if key[pygame.K_r]:
                        self.attack_type=1
                    if key[pygame.K_t]:
                        self.attack_type=2
            if self.player == 2:

                # thiet lap phim di chuyen ngang
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # thiet lap phim di chuyen doc
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # tan cong
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # xac dinh loai tan cong duoc dung
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2



        # ap dung trong luc
        self.vel_y+=GRAVITY
        dy+=self.vel_y


        # dam bao nguoi choi van con trong man hinh
        if self.rect.left+dx<0:
            dx=-self.rect.left
        if self.rect.right+dx>screen_width:
            dx=screen_width-self.rect.right
        if self.rect.bottom+dy> screen_height-110:
            self.vel_y=0
            self.jump=False
            dy=screen_height-110-self.rect.bottom


        #Dam bao nguoi choi luon doi mat voi nhau (tranh quay lung)
        if target.rect.centerx > self.rect.centerx:
            self.flip=False
        else:
            self.flip=True
        # ap dung tan cong hoi chieu
        if self.attack_cooldown>0:
            self.attack_cooldown-=1


        #Cap nhat vi tri nhan vat theo nut bam
        self.rect.x+=dx
        self.rect.y+=dy


    def update(self):
        # kt hanh dong gi cua nguoi choi dang duoc bieu dien
        if self.health<=0:
            self.health=0
            self.alive=False
            self.update_action(6)#6: death
        elif self.hit==True:
            self.update_action(5)#5: hit
        elif self.attacking==True:
            if self.attack_type==1:
                self.update_action(3)#3 attack 1
            elif self.attack_type==2:
                self.update_action(4)#4 attack 2
        elif self.jump== True:
            self.update_action(2)# nhay: co dau goi
        elif self.running==True:
            self.update_action(1)# 0: run
        else:
            self.update_action(0)#Neu running khong dung' thi se ve trang thai dung yen

        animation_cooldown=50
        #Cap nhat hinh anh nhan vat sau moi~ 0,5 giay
        animation_cooldown=50#Toc do chay cua nhan vat
        self.image=self.animation_list[self.action][self.frame_index]
        #Kiem tra neu thoi gian lan cuoi cap nhat qua dieu kien thi update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index+=1
            self.update_time=pygame.time.get_ticks()
        # kt neu hieu ung duoc hoan thanh
        if self.frame_index>= len(self.animation_list[self.action]):
            # kt neu nguoi choi chet thi ket thuc hieu ung
            if self.alive==False:
                self.frame_index= len(self.animation_list[self.action])-1
            else:
                self.frame_index=0
                # kt neu cuoc tan cong da duoc thuc hien
                if self.action==3 or self.action==4:
                    self.attacking=False
                    self.attack_cooldown=20
                # kt neu thiet hai xay ra
                if self.action== 5:
                    self.hit=False
                    # neu nguoi choi dang o giua cuoc tan cong sau do cuoc tan cong dung lai
                    self.attacking=False
                    self.attack_cooldown=20


    def attack (self,target):
        if self.attack_cooldown==0:
            # thuc hien hanh dong
            self.attacking=True
            self.attack_sound.play()
            # 2*self.rect.width la be rong chieu thuc.
            #(self.rect.centerx - (2*self.rect.width*self.flip) neu hai player quay lung voi nhau thi tru`, doi mat thi khong tru`
            attacking_rect =pygame.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y, 2*self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health-=10 #Moi lan tan cong trung' thi se mat 10hp
                target.hit=True
            self.attack_cooldown=20


    def update_action(self, new_action):
        # kt neu hanh dong moi khac hanh dong truoc do
        if new_action!= self.action:
            self.action= new_action
            # cap nhat hieu ung dang thiet lap
            self.frame_index =0
            self.update_time=pygame.time.get_ticks()



    def draw(self,surface):
        # ve hinh chu nhat co mau (color (255,0,0) la mau do) dai dien cho ng choi len man hinh
        img=pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img,(self.rect.x-(self.offset[0]*self.image_scale),self.rect.y-(self.offset[1]*self.image_scale)))

