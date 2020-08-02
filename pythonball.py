import pgzrun#导入pgzrun模块
import math#导入math模块
import time#导入时间模块
import random#导入随机数
global Field#在Field列表，游戏中如果小球处于Field区域，则玩家可以用键盘直接控制小球运动
global Target#目标，小球落入Target则代表游戏胜利
global Walllist#墙列表，小球碰到墙会反弹
global BlackArea#黑洞区域，黑色小球落入黑洞会被传送
global WhiteArea#白洞区域，白色小球落入白洞会被传送
global TrapArea#势阱，小球在其周围收到向心力的作用
global ReplayDelay#replay键粘滞，防止一次按键导致多次反应
global ifDark#判断是否开启迷雾模式
global ifHaveDark#判断是否开启过迷雾模式
global DarkDelay#迷雾键粘滞，防止一次按键导致多次反应
global lifeDelay#生命保护，小球在一定时间内只会减掉一点生命，防止小球与墙壁相切生命减少过多
global Walllist#墙列表，包含直线墙壁和曲线墙壁
global exitDelay#退出键粘滞，防止一次按键导致多次反应
global Accelerate#加速区域列表，小球在该区域会受到一定力的加速作用，力的方向随时间变化
global Decelerate#减速带区域，小球在该区域会注意安全，谨慎慢行
global flag#标记1，系统维持一个flag1计数，有些操作需要在给定的flag时间点执行。防止在update()时多次执行同一操作
global flag2#标记2，用途同上
global Loading#加载模块，通过它实现正在加载的动画效果
global ifReplay#判断是否应当重玩本关
global ifBack#判断是否应当返回上一级界面
global ifReturn#判断是否应当回到开始界面
global Winlist#胜利列表，记录该玩家获胜的关卡。一旦玩家退出登录（包括退出游戏），列表自动清零
global Name#名字字符串，记录玩家的名字
global gotName#判断是否得到了名字，只有输入名字（或系统自动分配名字），也就是登录之后才能进行后续操作
global ifChoose#判断是否进入过选关界面，如果进入过选关界面，退回到开始界面时候会显示玩家头像
global ifwelcome#判断玩家是否打开了海报
global ifuppercase#判断当前名字输入是否是大写，因为keyboard不会判断是否大写
global ifmessage#判断是否有新的信件，如果有，会在开始界面显示相应图标
global ifsend#判断信件是否被打开
global WinTime#记录获胜时间
global memDrag#记录被软绳连续拉扯的时间，用于计算回复位移
global MemDark#记录玩家在迷雾模式下完成的关卡列表
global memDrag2#记录玩家被钢绳连续拉扯的时间
global ifwinall#判断玩家是否通关，通关的显示制作者名单和特别鸣谢
global memimage#记录此时玩家表情
memimage='player'#初始化表情
ifwinall=0#初始化为未通关
MemDark={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
WinTime={1:9999.0,2:9999.0,3:9999.0,4:9999.0,5:9999.0,6:9999.0,7:9999.0,
         8:9999.0,9:9999.0,10:9999.0,11:9999.0,12:9999.0,13:9999.0,14:9999.0}#初始化为胜利时间无穷大
ifHaveDark=1#初始化为不曾开启迷雾模式
ifsend=0#后面全部都是相关初始化
memDrag=0
memDrag2=0
ifmessage=0
ifuppercase=0
ifwelcome=0
ifChoose=0
colorlist=['black','white']#只有黑白色
MAX = int(1e05) ##假设垂直直线的斜率，普通墙壁的生命为1e05
gotName=0
Name=""
Winlist=[]
ifReturn =0
ifReplay=0
ifBack=0
Loading=0
flag=0
flag2=0
exitDelay=0
lifeDelay=0
DarkDelay=0
ReplayDelay=0
ifDark=1
Field=[]#可供用于运动的区域 Field=[(100,100,0),(1200,500,0)],位置和半径（调用FieldR）
FieldR=[250,100]#运动半径
Target=[]#靶点位置和半径[900,600,60]
Walllist=[]#墙的列表
BlackArea={}#BlackHoleR===100,例如：(100,100):(1000,600)
WhiteArea={}
HoleThreshHold=30
ForceThreshHold=10**7
TrapArea=[]#势阱，例如(400,600,1)
Tail=[]#小球尾巴，用于记录小球经过的位置
waitTail=[]#等待动画特效，做出运动圆环效果
WIDTH=1600#设置宽度
HEIGHT=900#设置高度
THRESHOLD=400#设置进入黑洞白洞的判断阈值，用于判断小球是否进入黑洞白洞
global angle#角度，每分钟变化60次
angle=0
global myBall#我的pythonball
class Wall1():#直线型墙类
    def __init__(self, x_0, y_0, k_0, l_0, color_0, v_0x = 0, v_0y = 0, rangex_1 = 0, rangex_2 = WIDTH, rangey_1 = 0, rangey_2 = HEIGHT, life = MAX):#给出墙的中心位置，长度，运动速度以及运动范围
        global Walllist#调用墙列表
        self.pic = Actor('wall1_k=' + str(k_0) + '_color=' + colorlist[color_0] + '_l=' + str(l_0))
        self.x0 = x_0#给出墙的中心位置
        self.y0 = y_0#给出墙的中心位置
        self.k = -1*k_0#给出墙的斜率
        self.b = y_0 - k_0 * x_0 ##不用输入参数b，直接计算
        self.color = color_0#给出墙的颜色
        self.v0x = v_0x#给出墙的速度
        self.v0y = v_0y#给出墙的速度
        self.l = l_0#给出墙的长度
        self.x1 = x_0 - l_0/(2*((1+k_0 ** 2) ** 0.5))#计算出墙的端点
        self.y1 = y_0 - l_0/(2*((1+k_0 ** 2) ** 0.5)) * k_0#计算出墙的端点
        self.x2 = 2 * x_0 - self.x1#计算出墙的端点
        self.y2 = 2 * y_0 - self.y1#计算出墙的端点
        self.rangex1 = rangex_1###设置Wall移动的范围，取一个矩形区域，以左上角和右下角坐标确定
        self.rangex2 = rangex_2###设置Wall移动的范围，取一个矩形区域，以左上角和右下角坐标确定
        self.rangey1 = rangey_1###设置Wall移动的范围，取一个矩形区域，以左上角和右下角坐标确定
        self.rangey2 = rangey_2###设置Wall移动的范围，取一个矩形区域，以左上角和右下角坐标确定
        self.life = life
    def inMap(self):###判断是否超出运动范围
        temp1 = self.x1 >= self.rangex1 and self.x2 >= self.rangex1 and self.x1 <= self.rangex2 and self.x2 <= self.rangex2
        temp2 = self.y1 >= self.rangey1 and self.y2 >= self.rangey1 and self.y1 <= self.rangey2 and self.y2 <= self.rangey2
        if temp1 and temp2: return True
        return False
    
    def updateWall(self): #不考虑旋转和加速，更新墙的位置
        global dt
        if self.inMap():
            self.x1 += dt * self.v0x
            self.x2 += dt * self.v0x
            self.x0 += dt * self.v0x
            self.y1 += dt * self.v0y
            self.y2 += dt * self.v0y
            self.y0 += dt * self.v0y
            self.b = self.y0 - self.k * self.x0
        else:
            self.v0x = -self.v0x ##让速度反向，来回运动
            self.v0y = -self.v0y
            self.x1 += dt * self.v0x
            self.x2 += dt * self.v0x
            self.x0 += dt * self.v0x
            self.y1 += dt * self.v0y
            self.y2 += dt * self.v0y
            self.y0 += dt * self.v0y
            self.b = self.y0 - self.k * self.x0    
        self.pic.pos = self.x0, self.y0
            
    def isPong(self, ball): ##判断是否接触碰撞
        if self.color==ball.color:
            return False
        dis = math.fabs(ball.y - self.k * ball.x - self.b) / (math.sqrt(1 + self.k ** 2)) ##点到直线距离
        if dis >= ball.R:
            return False
        if (self.x1-myBall.x)**2+(self.y1-myBall.y)**2<=myBall.R**2/4:
            if myBall.vx**2+myBall.vy**2<400:
                myBall.vx*=1.1
                myBall.vy*=1.1
            return True
        if (self.x2-myBall.x)**2+(self.y2-myBall.y)**2<=myBall.R**2/4:
            if myBall.vx**2+myBall.vy**2<400:
                myBall.vx*=1.1
                myBall.vy*=1.1
            return True

        if self.k==0:
            if ball.x <= min(self.x1,self.x2)-ball.R/1.5 or ball.x >= max(self.x1,self.x2)+ball.R/1.5 : return False
            return True
        k = -1 / self.k ##这是法向斜率
        b = ball.y - k * ball.x ##计算过圆心垂直墙面的直线方程
        x = - (self.b - b) / (self.k - k)  ##联立直线与墙壁方程，求得切点坐标
        y = k * x + b 
         ##验证切点范围，如果不在线段范围内视为不碰撞
        if y <= min(self.y1,self.y2) or y >= max(self.y1,self.y2) : return False
        if dis<ball.R:
            if ball.vy==0:ball.vy=1
            if ball.vx==0:ball.vx=1
            ball.vx+=ball.vx/math.fabs(ball.vx)*10*(self.k)/math.sqrt(self.k**2+1)
            ball.vy+=ball.vy/math.fabs(ball.vy)*10*(1)/math.sqrt(self.k**2+1)
            ball.x+=ball.vx/math.fabs(ball.vx)*10*math.fabs(self.k/math.sqrt(self.k**2+1))
            ball.y+=ball.vy/math.fabs(ball.vy)*10*math.fabs(1/math.sqrt(self.k**2+1))
        return True
        
    def getNormal(self, ball): ##获取法向斜率
        if self.isPong(ball):
            return -1/self.k
        else: pass
    
class Wall2():#圆形墙（曲线墙）
    #规定1，2，3，4对应第1，2，3，4象限
    def __init__(self, x_0, y_0, type_info, R_0, color_0, v_0x = 0, v_0y = 0, rangex_1 = 0, rangex_2 = WIDTH, rangey_1 = 0, rangey_2 = HEIGHT):
        self.pic = Actor('wall2_type=' + str(type_info) + '_color=' + colorlist[color_0] + '_r=' + str(R_0))
        self.k=123#因为需要调用墙列表的k值，因此也给Wall2一个斜率，但不实际用到
        self.x0 = x_0#位置
        self.y0 = y_0#位置
        self.type = type_info#判断是哪个方向的圆弧
        self.color = color_0#墙的颜色
        self.v0x = v_0x#速度
        self.v0y = v_0y#速度
        self.R = R_0#墙的曲率半径
        self.rangex1 = rangex_1#移动范围
        self.rangex2 = rangex_2#移动范围
        self.rangey1 = rangey_1#移动范围
        self.rangey2 = rangey_2#移动范围
        if self.type == 1: ##考虑圆心位置和半径与边界的关系。
            self.rangex2 -= R_0
            self.rangey1 += R_0
        elif self.type == 2:
            self.rangex1 += R_0
            self.rangey1 += R_0
        elif self.type == 3:
            self.rangex1 += R_0
            self.rangey2 -= R_0
        elif self.type == 4:
            self.rangex2 -= R_0
            self.rangey2 -= R_0
        
    def inMap(self): ##判断墙是否在规定范围内运动
        temp1 = self.x0 >= self.rangex1 and self.x0 <= self.rangex2 
        temp2 = self.y0 >= self.rangey1 and self.y0 <= self.rangey2
        if temp1 and temp2: return True
        return False
    
    def updateWall(self): #不考虑旋转和加速
        global dt
        self.pic.pos = self.x0, self.y0
        if self.inMap():
            self.x0 += dt * self.v0x
            self.y0 += dt * self.v0y
        else:
            self.v0x = -self.v0x
            self.v0y = -self.v0y
            self.x0 += dt * self.v0x
            self.y0 += dt * self.v0y
    
    def isPong(self, ball):#判断墙是否与球相碰
        if self.color==ball.color:
            return False
        dist = ((self.x0 - ball.x) ** 2 + (self.y0 - ball.y) ** 2) ** 0.5
        if dist < self.R - ball.R or dist > self.R + ball.R : return False ##圆弧与球的位置关系##modify
        dx = ball.x - self.x0
        dy = ball.y - self.y0
        if self.type == 1:
            return (dx > 0) and (dy < 0) ##球的半径为100，一定小于圆弧半径，否则碰撞会出现多个接触点
        elif self.type == 2:
            return (dy < 0) and (dx < 0)##modifydy反向
        elif self.type == 3:
            return (dy > 0) and (dx < 0)
        elif self.type == 4:
            return (dy > 0) and (dx > 0)
    
    def qieDian(self, ball):  ##计算切点位置，一般不作为对外接口，方便获取法向
        dx = ball.x - self.x0
        dy = ball.y - self.y0
        k = dy / dx
        y = k /((1+k**2)**0.5) * self.R + self.y0 ##利用向量共线的性质，切点、球心、弧的圆心三点共线
        x = 1 /((1+k**2)**0.5) * self.R + self.x0
        return x,y
    
    def getNormal(self,ball): ##获取碰撞点法向
        if self.isPong(ball):
            return (self.y0 - self.qieDian(ball)[1]) / (self.x0 - self.qieDian(ball)[0])
        else: pass
        
class Ball():#球类
    global game_status#调用游戏进程
    flagchange=0#是否需要变色的标记
    def __init__(self,x0,y0,vx0,vy0,color0,life0):#初始化位置，速度，颜色和生命值
        self.pic=Actor('blackball')
        self.x=x0#位置
        self.y=y0
        self.vx=vx0#速度
        self.vy=vy0
        self.color=color0#颜色
        self.life=life0#生命值
        self.R=50#半径
        self.Delay=0#变色粘滞，防止换过去又换回来
        self.Delay2=0#弹跳粘滞，防止被卡住
        self.flagchange=0
    def ShouldPong(self):#是否应当引发碰撞行为
        for iter in Walllist:
            if iter.isPong(myBall) and self.Delay2==0:
                if iter.k==123:
                    self.Pong(iter.getNormal(myBall))
                else:
                    if iter.k!=0:
                        self.Pong(-1.0/iter.k)
                    else:self.Pong(100000)
    def ShouldInHole(self):#是否落入黑洞白洞，如果是，进行相关转移操作
        if self.color==0:#确定颜色
            tmplist=BlackArea.keys()
        else:
            tmplist=WhiteArea.keys()
        for iter in tmplist:
            d2=(self.x-iter[0])**2+(self.y-iter[1])**2#计算与黑洞中心距离
            if d2<HoleThreshHold**2:
                 if self.color==0:
                    self.x=BlackArea[iter][0]
                    self.y=BlackArea[iter][1]
                 else:
                    self.x=WhiteArea[iter][0]
                    self.y=WhiteArea[iter][1]
                 self.vx/=10
                 self.vy/=10
                 self.flagchange=1#经过黑洞需要改变颜色
            else:
                Fx=ForceThreshHold*(self.x-iter[0])/d2/math.sqrt(d2)
                Fy=ForceThreshHold*(self.y-iter[1])/d2/math.sqrt(d2)#黑洞有吸引力
                self.Force(-Fx,-Fy) 
        if self.color==0:
            tmplist=WhiteArea.keys()
            tmp=WhiteArea
        else:
            tmplist=BlackArea.keys()
            tmp=BlackArea
        for iter in tmplist:
            tmpx=tmp[iter][0]
            tmpy=tmp[iter][1]
            d2=(self.x-tmpx)**2+(self.y-tmpy)**2
            if d2>100:
                Fx=ForceThreshHold*(self.x-tmpx)/d2/math.sqrt(d2)/100
                Fy=ForceThreshHold*(self.y-tmpy)/d2/math.sqrt(d2)/100
                self.Force(Fx,Fy)
        for iter in TrapArea:#势阱也有吸引力
            d2=(self.x-iter[0])**2+(self.y-iter[1])**2
            if int(math.sqrt(d2))<math.sqrt(iter[2])+60 and iter[2]!=1:
                fenmu=(self.x-iter[0])
                if fenmu==0:fenmu=1 
                myBall.Pong((self.y-iter[1])/fenmu)
                if self.vx>10:
                    self.vx*=0.9
                else:
                    self.vx+=10
                if self.vy<10:
                    self.vy*=0.9
                else:
                    self.vy+=10
                while(int(math.sqrt(d2))<math.sqrt(iter[2])+20):
                    self.x-=self.vx*dt
                    self.y-=self.vy*dt
                    d2=(self.x-iter[0])**2+(self.y-iter[1])**2
            elif int(math.sqrt(d2))<math.sqrt(iter[2])+250:
                d2=d2-iter[2]+10000
                Fx=3*ForceThreshHold*(self.x-iter[0])/d2/math.sqrt(d2)
                Fy=3*ForceThreshHold*(self.y-iter[1])/d2/math.sqrt(d2)
                self.Force(-Fx,-Fy)
    def updateBall(self):#更新位置
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        self.pic.pos=self.x,self.y
        self.ShouldPong()
        self.ShouldInHole()
    def change(self):#改变球的颜色
        if keyboard.space==True and self.Delay==0 or self.flagchange==1:
            sounds.clickinner.play()
            self.flagchange=0
            for iter in Walllist:
               if iter.isPong(myBall):
                    return
            if self.color==0:
                self.pic.image='whiteball'
            else:
                self.pic.image='blackball'
            self.color=not self.color
            self.Delay=10
    def Force(self,ax0,ay0):#球的受力
        self.vx+=ax0*dt
        self.vy+=ay0*dt
    def Pong(self,k):#法向
        if game_status==2:
            sounds.pong.play()
        global lifeDelay
        if self.Delay2>0:
            return
        tmp=-2.0*(1/k*self.vx+self.vy)/(k+1/k)#计算球的速度关于法向对称后的值
        self.vx=self.vx+tmp
        self.vy=self.vy+tmp*k
        if lifeDelay==0:
            self.life-=1
            lifeDelay=30
        if self.life==0:
            self.Lost()
        self.Delay2=5#弹跳粘滞，防止被卡住
   
        
    def Lost(self):#判断是否死亡
        if self.life==0:
            sounds.bgmplay.stop()
            sounds.gameover.play()
            return True
        return False
    def InField(self):#判断是否在Field内，如果是，小球可以用键盘控制
        for iter in Field:
            if (self.x-iter[0])**2+(self.y-iter[1])**2<FieldR[iter[2]]**2:
                return True
        return False
    def InTarget(self):#判断是否进入目标，是则获胜
         if (self.x-Target[0])**2+(self.y-Target[1])**2<Target[2]**2:
            return True
         return False
    def Move(self):#移动小球，在Field内。接受上下左右和wasd控制
        if self.InField():
            if keyboard.left==True or keyboard.a==True:
                self.Force(-THRESHOLD,0)
            if keyboard.right==True or keyboard.d==True:
                self.Force(THRESHOLD,0)
            if keyboard.up==True or keyboard.w==True:
                self.Force(0,-THRESHOLD)    
            if keyboard.down==True or keyboard.s==True:
                self.Force(0,THRESHOLD)

def setGame(setpos=[100,100,99],setField=[(100,100,0)],setTarget=[2000,1500,60],setWall=[],setBlackArea={},setWhiteArea={},setTrapArea=[],setAccelerate=[],setDecelerate=[]):#初始化游戏设置    
    global Target
    global Field
    global Walllist
    global BlackArea
    global WhiteArea
    global TrapArea
    global myBall
    global Accelerate
    global Decelerate
    Walllist=[Wall1(-10, 225, 100000, 450, 0, 0, 0),Wall1(-10, 675, 100000, 450, 0, 0, 0),Wall1(400, -10, 0, 800, 0, 0),Wall1(1200, -10, 0, 800, 0, 0, 0),
          Wall1(1610, 225, 100000, 450, 0, 0, 0),Wall1(1610, 675, 100000, 450, 0, 0, 0),Wall1(400, 910, 0, 800, 0, 0),Wall1(1200, 910, 0, 800, 0, 0, 0),
          Wall1(-10, 225, 100000, 450, 1, 0, 0),Wall1(-10, 675, 100000, 450, 1, 0, 0),Wall1(400, -10, 0, 800, 1, 0,0),Wall1(1200, -10, 0, 800, 1, 0, 0),
          Wall1(1610, 225, 100000, 450, 1, 0, 0),Wall1(1610, 675, 100000, 450, 1, 0, 0),Wall1(400, 910, 0, 800, 1, 0,0),Wall1(1200, 910, 0, 800, 1, 0, 0)]
    myBall=Ball(setpos[0],setpos[1],0,0,0,setpos[2])
    Field=setField
    Target=setTarget
    Walllist.extend(setWall)
    BlackArea=setBlackArea
    WhiteArea=setWhiteArea
    TrapArea=setTrapArea
    Accelerate=setAccelerate
    Decelerate=setDecelerate
setGame()
target=Actor('whitetarget')
target.pos=Target[0],Target[1]
dt=1/60

#按键
Exit = Actor('exit',topright=(1580,30))
back = Actor('back',topright=(1380,30))
returnstart = Actor ('back',topright=(1380,30))
replay = Actor('replay',topright=(1180,30))
mouse = (0,0)
game_status = 0
global n#当前关卡
n = 0

global timer#退出游戏计时器，防止玩家错误退出
timer=-300

def distance(a,b):#距离
    return ((b[0]-a[0])**2 + (b[1]-a[1])**2)**0.5

#1.开始界面    
def Start():
    global timer
    global Name
    global gotName
    global mouse
    global ifChoose
    global ifuppercase
    global Winlist
    global ifmessage
    global ifwinall
    timer+=1
    if timer==2:
        sounds.bgmstart.play()
    if timer>41:#41张图片组成动画
        timer-=1
    if timer<=0:
        screen.blit('welcome',(0,0))#张贴海报
        if keyboard.space:
            sounds.clickinner.play()#音效
            timer=1
    else:
        screen.blit(str(timer),(0,0))
        if ifwinall==1:#如果全胜，则奖励王冠
            tmp=Actor('king')
            tmp.pos=774,130
            tmp.draw()
        if timer==41 and gotName==0:#如果还没有输入名字，则需要输入名字
            screen.draw.text("Please enter your CODE ( ‘SPACE’ to continue):",(300,480),color='black',fontsize=40)
            screen.draw.text(Name,(950,480),color='black',fontsize=40)
            tmplen=len(Name)
            if keyboard.backspace and len(Name)!=0 or tmplen>=9:
                Name=Name[:-1]#名字不能超过8个字符
            flag=0#输入名字，支持数字，字母（含大小写）和下划线
            if keyboard.kp0 or keyboard.k_0:
                Name+='0'
            if keyboard.kp1 or keyboard.k_1:
                Name+='1'
            if keyboard.kp2 or keyboard.k_2:
                Name+='2'
            if keyboard.kp3 or keyboard.k_3:
                Name+='3'
            if keyboard.kp4 or keyboard.k_4:
                Name+='4'
            if keyboard.kp5 or keyboard.k_5:
                Name+='5'
            if keyboard.kp6 or keyboard.k_6:
                Name+='6'
            if keyboard.kp7 or keyboard.k_7:
                Name+='7'
            if keyboard.kp8 or keyboard.k_8:
                Name+='8'
            if keyboard.kp9 or keyboard.k_9:
                Name+='9'
            if keyboard.capslock:
                ifuppercase=(ifuppercase+1)%2
            if keyboard.a:
                if ifuppercase==0:
                    Name+='a'
                else:
                    Name+='A'
            if keyboard.b:
                if ifuppercase==0:
                    Name+='b'
                else:
                    Name+='B'
            if keyboard.c:
                if ifuppercase==0:
                    Name+='c'
                else:
                    Name+='C'
            if keyboard.d:
                if ifuppercase==0:
                    Name+='d'
                else:
                    Name+='D'
            if keyboard.e:
                if ifuppercase==0:
                    Name+='e'
                else:
                    Name+='E'
            if keyboard.f:
                if ifuppercase==0:
                    Name+='f'
                else:
                    Name+='F'
            if keyboard.g:
                if ifuppercase==0:
                    Name+='g'
                else:
                    Name+='G'
            if keyboard.h:
                if ifuppercase==0:
                    Name+='h'
                else:
                    Name+='H'
            if keyboard.i:
                if ifuppercase==0:
                    Name+='i'
                else:
                    Name+='I'
            if keyboard.j:
                if ifuppercase==0:
                    Name+='j'
                else:
                    Name+='J'
            if keyboard.k:
                if ifuppercase==0:
                    Name+='k'
                else:
                    Name+='K'
            if keyboard.l:
                if ifuppercase==0:
                    Name+='l'
                else:
                    Name+='L'
            if keyboard.m:
                if ifuppercase==0:
                    Name+='m'
                else:
                    Name+='M'
            if keyboard.n:
                if ifuppercase==0:
                    Name+='n'
                else:
                    Name+='N'
            if keyboard.o:
                if ifuppercase==0:
                    Name+='o'
                else:
                    Name+='O'
            if keyboard.p:
                if ifuppercase==0:
                    Name+='p'
                else:
                    Name+='P'
            if keyboard.q:
                if ifuppercase==0:
                    Name+='q'
                else:
                    Name+='Q'
            if keyboard.r:
                if ifuppercase==0:
                    Name+='r'
                else:
                    Name+='R'
            if keyboard.s:
                if ifuppercase==0:
                    Name+='s'
                else:
                    Name+='S'
            if keyboard.t:
                if ifuppercase==0:
                    Name+='t'
                else:
                    Name+='T'
            if keyboard.u:
                if ifuppercase==0:
                    Name+='u'
                else:
                    Name+='U'
            if keyboard.v:
                if ifuppercase==0:
                    Name+='v'
                else:
                    Name+='V'
            if keyboard.w:
                if ifuppercase==0:
                    Name+='w'
                else:
                    Name+='W'
            if keyboard.x:
                if ifuppercase==0:
                    Name+='x'
                else:
                    Name+='X'
            if keyboard.y:
                if ifuppercase==0:
                    Name+='y'
                else:
                    Name+='Y'
            if keyboard.z:
                if ifuppercase==0:
                    Name+='z'
                else:
                    Name+='Z'
            if keyboard.minus:
                Name+='_'
            if keyboard.SPACE :#按下空格代表名字输入结束
                sounds.clickinner.play()
                gotName=1
                sounds.game.play()
            if tmplen!=len(Name):#输入粘滞，防止一次读入多个字母
                sounds.click.play()
                time.sleep(0.2)
            mouse=(0,0)
        if timer==41 and gotName==1:
            if ifChoose==0:#开始游戏欢迎词
                if len(Name)==0:
                    Name="NOBODY"
                screen.draw.text("Hello "+Name+":",(670,450),color='black',fontsize=40)
                screen.draw.text("Let’s play a GAME!",(600,500),color='black',fontsize=60)
                screen.draw.text("LOG OFF",(100,800),color='white',fontsize=40)
            else:#如果是返回主菜单，则按如下输出，可以进入海报
                player=Actor('playersmile')#头像
                player.pos=200,780
                player.draw()
                screen.draw.text(Name,(130,880),color='white',fontsize=30)
                screen.draw.text("Click to see ACKNOWLEDGEMENTS",(430,500),color='white',fontsize=60)
                tmp1=1
                tmp2=1
                for i in range(1,8):
                    if not (i in Winlist):
                        tmp1=0
                    if not ((i+7) in Winlist):
                        tmp2=0
                if tmp1==1 or tmp2==1:##
                    screen.draw.text("Message",(200,150),color='black',fontsize=40)
                    tmp=Actor('message')
                    ifmessage=1
                    tmp.pos=250,100
                    tmp.draw()
def on_mouse_down(pos,button):
    global mouse
    global exitDelay
    mouse = pos
    if game_status == 0:
        if Exit.collidepoint(pos):
            exitDelay=180#退出粘滞，给用户返回机会
    if game_status == 1:
        ReturnStart()
        if Exit.collidepoint(pos):
            exitDelay=180#退出粘滞，给用户返回机会
    if game_status == 2:
        Back()
        Replay()
        if Exit.collidepoint(pos):
            exitDelay=180#退出粘滞，给用户返回机会

#3.返回开始界面
def ReturnStart():
    global game_status
    global flag
    global flag2
    global mouse
    global ifReturn
    flag=0
    flag2=0
    if returnstart.collidepoint(mouse) or ifReturn==1:#支持使用backspace，escape和鼠标操作
        sounds.click.play()
        sounds.welcome.play()
        game_status = 0
        if ifReturn==1:
            ifReturn=0
            mouse=(0,0)
#返回上级界面
def Back():
    global ifBack
    global game_status
    global mouse
    if back.collidepoint(mouse) or ifBack==1:#支持使用backspace，escape和鼠标操作
        sounds.frighted.stop()
        sounds.bgmplay.stop()
        sounds.click.play()
        sounds.bgmstart.play()
        game_status = 1
        if ifBack==1:
            ifBack=0
            mouse=(0,0)
            time.sleep(0.3)
#4.选关页面
def Level1():
    global n
    global mouse
    screen.clear()
    screen.blit("level1",(0,0))
    tmp=Actor('home')
    tmp.pos=180,800
    tmp.draw()
    if keyboard.down or keyboard.right:
        sounds.clickinner.play()
        n+=7
    c1 = [mouse,(740,410),(965,355),(1100,535),(1030,750),(800,800),(670,630),(890,575)]  #关卡数字位置
    setPrepare1()
    r = 80
    #根据位置判断玩家选择的关卡，支持键盘选关
    if keyboard.k_1==True or keyboard.kp1==True:
        sounds.clickinner.play()
        game_status = 2
        n = 1
        Play(1)
    elif keyboard.k_2==True or keyboard.kp2==True:
        sounds.clickinner.play()
        game_status = 2
        n = 2
        Play(2)
    elif keyboard.k_3==True or keyboard.kp3==True:
        sounds.clickinner.play()
        game_status = 2
        n = 3
        Play(3)
    elif keyboard.k_4==True or keyboard.kp4==True:
        sounds.clickinner.play()
        game_status = 2
        n = 4
        Play(4)
    elif keyboard.k_5==True or keyboard.kp5==True:
        sounds.clickinner.play()
        game_status = 2
        n = 5
        Play(5)
    elif keyboard.k_6==True or keyboard.kp6==True:
        sounds.clickinner.play()
        game_status = 2
        n = 6
        Play(6)
    elif keyboard.k_7==True or keyboard.kp7==True:
        sounds.clickinner.play()
        game_status = 2
        n = 7
        Play(7)
    else:
        for i in range(1,8):
            if distance(mouse,c1[i]) <= r:
                sounds.clickinner.play()
                game_status = 2
                n = i
                Play(i)
                mouse=(0,0)
#思路同level1
def Level2():
    global n
    global mouse
    screen.clear()
    screen.blit("level2",(0,0))
    tmp=Actor('home')
    tmp.pos=180,800
    tmp.draw()
    if keyboard.up or keyboard.left:
        sounds.clickinner.play()
        n-=7
    c2 = [mouse,(590,380),(840,450),(930,686),(775,890),(525,810),(440,590),(685,670)]  #关卡数字位置
    setPrepare2()
    r = 80
    if keyboard.k_1==True or keyboard.kp1==True:
        sounds.clickinner.play()
        game_status = 2
        n = 8
        Play(8)
    elif keyboard.k_2==True or keyboard.kp2==True:
        sounds.clickinner.play()
        game_status = 2
        n = 9
        Play(9)
    elif keyboard.k_3==True or keyboard.kp3==True:
        sounds.clickinner.play()
        game_status = 2
        n = 10
        Play(10)
    elif keyboard.k_4==True or keyboard.kp4==True:
        sounds.clickinner.play()
        game_status = 2
        n = 11
        Play(11)
    elif keyboard.k_5==True or keyboard.kp5==True:
        sounds.clickinner.play()
        game_status = 2
        n = 12
        Play(12)
    elif keyboard.k_6==True or keyboard.kp6==True:
        sounds.clickinner.play()
        game_status = 2
        n = 13
        Play(13)
    elif keyboard.k_7==True or keyboard.kp7==True:
        sounds.clickinner.play()
        game_status = 2
        n = 14
        Play(14)
    else:
        for i in range(1,8):
            if distance(mouse,c2[i]) <= r:
                sounds.clickinner.play()
                game_status = 2
                n = i+7
                Play(7+i)
                mouse=(0,0)

#9.重新开始
def Replay():
    global ifReplay
    global angle
    global ReplayDelay
    if replay.collidepoint(mouse) or (keyboard.r and ReplayDelay==0) or ifReplay==1:
        ifReplay=0
        sounds.frighted.stop()
        sounds.click.play()
        sounds.gameover.stop()
        sounds.gamewin.stop()
        sounds.bgmplay.play()
        angle=0
        ReplayDelay=30
        Play(n)

#5.游戏界面
def setPrepare1():
    global flag
    global myBall
    global TrapArea
    global Walllist
    flag+=1
    if flag<=1:
        Walllist=[Wall1(-10, 225, 100000, 450, 0, 0, 0),Wall1(-10, 675, 100000, 450, 0, 0, 0),Wall1(400, -10, 0, 800, 0, 0),Wall1(1200, -10, 0, 800, 0, 0, 0),
          Wall1(1610, 225, 100000, 450, 0, 0, 0),Wall1(1610, 675, 100000, 450, 0, 0, 0),Wall1(400, 910, 0, 800, 0, 0),Wall1(1200, 910, 0, 800, 0, 0, 0),
          Wall1(-10, 225, 100000, 450, 1, 0, 0),Wall1(-10, 675, 100000, 450, 1, 0, 0),Wall1(400, -10, 0, 800, 1, 0,0),Wall1(1200, -10, 0, 800, 1, 0, 0),
          Wall1(1610, 225, 100000, 450, 1, 0, 0),Wall1(1610, 675, 100000, 450, 1, 0, 0),Wall1(400, 910, 0, 800, 1, 0,0),Wall1(1200, 910, 0, 800, 1, 0, 0)]
        myBall=Ball(random.randint(100,1500),random.randint(100,800),random.randint(-800,800),random.randint(-800,800),0,999999)
        TrapArea=[]
    if myBall.Delay2!=0:
        myBall.Delay2-=1
    myBall.Force(0,500)
    myBall.pic.draw()
#选关界面前的小球特效制作
def setPrepare2():
    global flag2
    global myBall
    global TrapArea
    global Walllist
    flag2+=1
    if flag2<=1:
        Walllist=[Wall1(-10, 225, 100000, 450, 0, 0, 0),Wall1(-10, 675, 100000, 450, 0, 0, 0),Wall1(400, -10, 0, 800, 0, 0),Wall1(1200, -10, 0, 800, 0, 0, 0),
          Wall1(1610, 225, 100000, 450, 0, 0, 0),Wall1(1610, 675, 100000, 450, 0, 0, 0),Wall1(400, 910, 0, 800, 0, 0),Wall1(1200, 910, 0, 800, 0, 0, 0),
          Wall1(-10, 225, 100000, 450, 1, 0, 0),Wall1(-10, 675, 100000, 450, 1, 0, 0),Wall1(400, -10, 0, 800, 1, 0,0),Wall1(1200, -10, 0, 800, 1, 0, 0),
          Wall1(1610, 225, 100000, 450, 1, 0, 0),Wall1(1610, 675, 100000, 450, 1, 0, 0),Wall1(400, 910, 0, 800, 1, 0,0),Wall1(1200, 910, 0, 800, 1, 0, 0)]
        myBall=Ball(200,125,100,110,0,999999)
        TrapArea=[(400,225,1),(600,225,1),(800,225,1),(1000,225,1),(200,450,1),(400,450,1),(200,225,1),(1000,450,1),(1200,450,1),(1400,450,1)]
    if myBall.Delay2!=0:
        myBall.Delay2-=1
    myBall.pic.draw()
#开始游戏
def Play(n):
    global memimage
    memiage='player'
    sounds.bgmstart.stop()
    sounds.bgmplay.stop()
    sounds.ghost.stop()
    sounds.bgmplay.play(3)
    global angle
    angle=0
    global memDrag
    memDrag=0
    global ifHaveDark
    ifHaveDark=1
    global game_status
    game_status = 2
    if n==7:
        setGame([100,400,10],
                [(100,400,0)],
                [1500,450,60],
                [Wall1(500,450,MAX,450,0,0,200),Wall1(500,450,MAX,450,1,0,200),Wall1(700,450,MAX,450,0,0,-200),Wall1(700,450,MAX,450,1,0,-200),Wall1(900,450,MAX,450,0,0,300),Wall1(900,450,MAX,450,1,0,300),Wall1(1100,450,MAX,450,0,0,-300),Wall1(1100,450,MAX,450,1,0,-300)],
                {(1300,200):(200,200)},
                {(1300,600):(200,600)},
                [],
                [],
                [])
    elif n == 6:
        setGame([1400,750,20],
                [(1400,750,0)],
                [100,150,60],
                [Wall1(1400,200, -1, 300, 0,0,0,MAX),Wall1(300,700,0, 300, 0,0,0,MAX),Wall1(300,200, 1,400, 0,0,0,MAX)],
                {(800,650):(300,650)},
                {(1200,600):(350,300)},
                [(800,350,120)],
                [],
                [])
    elif n==3:
        setGame([100,100,20],
                [(100,100,0)],
                [1400,800,70],
                [Wall1(700, 200, -1, 400, 0),Wall1(700, 200, -1, 400, 1),Wall1(200, 600, 0, 400, 0),Wall1(200, 600, 0, 400, 1),Wall1(1400, 600, 0, 200, 0),Wall1(1400, 600, 0, 200, 1),Wall1(200, 300, 0, 200, 0),Wall1(200, 300, 0, 200, 1)],
                {(400,100):(300,700)},
                {(400,300):(1200,700)},
                [],
                [],
                [])
    elif n==4:
        setGame([50,450,20],
                [(100,450,0)],
                [1300,100,60],
                [Wall1(200,300,-1,300,0,0,0,0,MAX),Wall1(200,600,1,300,1,0,0,0,MAX),Wall1(800,700,1,400,1,0,0,0,MAX),Wall1(1400,300,0,400,0,0,0,MAX),Wall2(400,400,1,250,1,0,0,0),Wall2(400,400,4,250,0,0,0,0),Wall2(1300,500,4,200,1,0,0,0),Wall2(1300,700,2,200,0,0,0,0)],
                {(200,150):(1400,600)},
                {(200,750):(700,200)},
                [(1100,200,100)],
                [],
                [])
    elif n==13:
        setGame([100,400,20],
                [(100,400,0)],
                 [950,450,70],
                [Wall1(895, 450, MAX, 100, 0, -150, 0, 600, 896, 0, 600),Wall1(890, 450, MAX, 100, 1, -150, 0, 600, 896, 0, 600),Wall1(1010, 450, MAX, 100, 0, 150, 0, 1009, 1300, 399, 500),Wall1(1010, 450, MAX, 100, 1, 150, 0, 1009, 1300, 399, 500),Wall1(950, 390, 0, 100, 0, 0, -150, 900, 1000, 100, 390),Wall1(950, 390, 0, 100, 1, 0, -150, 900, 1000, 100, 390),Wall1(950, 510, 0, 100, 0, 0, 150, 900, 1000, 510, 800),Wall1(950, 510, 0, 100, 1, 0, 150, 900, 1000, 510, 800),Wall2(900,400,2,300,0),Wall2(900,400,2,300,1),Wall2(900,500,3,300,0),Wall2(900,500,3,300,1),Wall2(1000,400,1,300,0),Wall2(1000,400,1,300,1),Wall2(1000,500,4,300,0),Wall2(1000,500,4,300,1)],
                {},
                {},
                [],
                [],
                [])
    elif n==1:
        setGame([200,100,2],
                [(200,100,0)],
                [900,550,60],
                [Wall1(200, 600, -1, 400, 0),Wall1(200, 600, -1, 400, 1),Wall1(500, 350, 0, 400, 0),Wall1(500, 350, 0, 400, 1)],
                {},
                {},
                [],
                [],
                [])
    elif n==2:
        setGame([100,200,10],
                [(100,200,0)],
                [1350,800,60],
                [Wall1(200,550,0,400,0,25,0),Wall1(800,350,0,450,1,50,0),Wall2(1200,400,4,300,0,0,0,0),Wall2(300,350,3,200,1,0,0,0)],
                {(100,700):(1350,200)},
                {(100,700):(1350,200),(1200,700):(400,300)},
                [(800,100,150),(800,800,150),(800,500,1)],
                [],
                [])
    elif n==5:
        l1=100
        setGame(setpos=[150,750,8],
        setField=[(150,750,1)],
        setTarget=[825,600,60],
        setWall=[Wall1(125, 125, 1, l1, 0),Wall1(125, 125, 1, l1, 1),Wall1(1450, 125, -1, l1, 0),Wall1(1450, 125, -1, l1, 1),Wall1(1450, 775, 1, l1, 0),Wall1(1450, 775, 1,l1, 1),Wall1(550, 775, -1, l1, 0),Wall1(550, 775, -1, l1, 1),Wall1(550, 450, 1, l1, 0),Wall1(550, 450, 1,l1, 1),Wall1(1075, 450, -1, l1, 0),Wall1(1075, 450, -1, l1, 1),Wall1(1075, 650, 1, l1, 0),Wall1(1075, 650, 1,l1, 1)],
        setBlackArea={},
        setWhiteArea={},
        setTrapArea=[],
        setAccelerate=[],
        setDecelerate=[])
    elif n==9:
        R1=150
        R2=500
        R=(R1+R2)/3
        setGame(setpos=[150,150,15],
        setField=[(500,450,1)],
        setTarget=[800,450,60],
        setWall=[Wall2(800,450,1,R1,0),Wall2(800,450,2,R1,0),Wall2(800,450,3,R1,0),Wall2(800,450,4,R1,0),Wall2(800,450,1,R2,1),Wall2(800,450,2,R2,1),Wall2(800,450,3,R2,1),Wall2(800,450,4,R2,1),Wall2(800,450,1,R1,1),Wall2(800,450,2,R1,1),Wall2(800,450,3,R1,1),Wall2(800,450,4,R1,1)],
        setBlackArea={(800+R,450+R):(800,450)},
        setWhiteArea={(800+R,450+R):(800,450)},
        setTrapArea=[],
        setAccelerate=[(800-R,450-R),(800-R,450+R),(800+R,450-R)],
        setDecelerate=[])
    elif n==10:
        l1=500
        setGame(setpos=[150,150,50],
        setField=[(150,150,1)],
        setTarget=[1450,620,60],
        setWall=[Wall1(250, 250, 0, l1, 0),Wall1(750,250 , 0, l1, 0),Wall1(250, 250, 0, l1, 1),Wall1(750,250 , 0, l1, 1),Wall1(1250, 250, 0, l1, 0),Wall1(1250,250 , 0, l1, 1),Wall1(1250, 500, 0, l1, 0),Wall1(1250,500 , 0, l1, 1),Wall1(1250, 750, 0, l1, 0),Wall1(1250,750 , 0, l1, 1),
        Wall1(250, 750, 0, l1, 0),Wall1(750,750 , 0, l1, 0),Wall1(250, 750, 0, l1, 1),Wall1(750,750 , 0, l1, 1),
        Wall1(250, 500, 0, l1, 0),Wall1(250,500 , 0, l1, 1),Wall1(750, 500, 0, l1, 0),Wall1(750,500 , 0, l1, 1),
        Wall1(250,250 , 100000, l1, 0),Wall1(750, 500, 100000, l1, 1),Wall1(1250,250 , 100000, l1, 0)],
        setBlackArea={(1450,125):(150,375),(1450,375):(150,625)},
        setWhiteArea={},
        setTrapArea=[],
        setAccelerate=[(1000,125),(1000,375),(1000,625)],
        setDecelerate=[])
    elif n==11:
        R=300
        setGame(setpos=[425,150,10],
        setField=[(425,150,0)],
        setTarget=[1250,150,60],
        setWall=[Wall2(800,450,1,R,1),Wall2(800,450,1,R,0),Wall2(800,450,2,R,1),Wall2(800,450,2,R,0),Wall2(800-R,450,3,R,1),Wall2(800-R,450,3,R,0),Wall2(800-R,450,4,R,1),Wall2(800-R,450,4,R,0),Wall2(800+R,450,3,R,1),Wall2(800+R,450,3,R,0),Wall2(800+R,450,4,R,1),Wall2(800+R,450,4,R,0),Wall1(800+R, 250, 100000, 500, 0),Wall1(800+R, 250, 100000, 500, 1),Wall1(800+R*2, 250, 100000, 500, 0),Wall1(800+R*2, 250, 100000, 500, 1),Wall1(800, 250, 100000, 500, 1)],
        setBlackArea={},
        setWhiteArea={},
        setTrapArea=[],
        setAccelerate=[(800-R*0.5,450)],
        setDecelerate=[(800+R*1.5,450)])
    elif n==12:
        tmp=[]
        ttmp=[]
        tttmp=[]
        for i in range(1,13):
            tmp.append((i*100,50,1))
            tmp.append((i*100,450,1))
            tmp.append((i*100,850,1))
        for i in range(1,8):
            ttmp.append((i*400,250))
            ttmp.append((i*400-200,650))
            tttmp.append((i*400-200,250))
            tttmp.append((i*400,650))
        setGame(setpos=[150,150,50],
        setField=[(150,150,0)],
        setTarget=[1450,450,60],
        setWall=[],
        setBlackArea={},
        setWhiteArea={},
        setTrapArea=tmp,
        setAccelerate=ttmp,
        setDecelerate=tttmp)
    elif n==14:
        l1=500
        l2=100
        l3=200
        R1=150
        Y=300
        setGame(setpos=[150,150,10],
            setField=[(150,150,0)],
            setTarget=[800,650,60],
            setWall=[Wall1(800, 450, 0, l1, 0),Wall1(800, 450, 0, l1, 1),
            Wall1(750, 500, 1, l2, 0),Wall1(750, 500, 1, l2, 1),Wall1(850, 500, -1, l2, 0),Wall1(850, 500, -1, l2, 1),Wall1(800, 550, 0, l3, 0),Wall1(800, 550, 0, l3, 1),Wall1(700, 650, 100000, l3, 0),Wall1(700, 650, 100000, l3, 1),Wall1(900, 650, 100000, l3, 0),Wall1(900, 650, 100000, l3, 1),Wall1(800, 750, 0, l3, 0),Wall1(800, 750, 0, l3, 1),
            Wall2(550,Y,1,R1,1),
            Wall2(550,Y,2,R1,1),
            Wall2(550,Y,3,R1,1),
            Wall2(550,Y,4,R1,1),
            Wall2(1050,Y,1,R1,1),Wall2(1050,Y,1,R1,0),
            Wall2(1050,Y,2,R1,1),Wall2(1050,Y,2,R1,0),
            Wall2(1050,Y,3,R1,1),Wall2(1050,Y,3,R1,0),
            Wall2(1050,Y,4,R1,1),Wall2(1050,Y,4,R1,0)],
        setBlackArea={(1050,Y):(800,650),(550,Y):(1050,Y)},
        setWhiteArea={},
        setTrapArea=[],
        setAccelerate=[],
        setDecelerate=[])
    elif n==8:
        l1=500
        setGame(setpos=[150,450,1 ],
        setField=[],
        setTarget=[1450,480,60],
        setWall=[Wall1(400, 250, 100000, l1, 1),Wall1(400, 750, 100000, l1, 1),Wall1(800, 250, 100000, l1, 0),Wall1(800, 750, 100000, l1, 0),Wall1(1200, 250, 100000, l1, 1),Wall1(1200, 750, 100000, l1, 1)],
        setBlackArea={},
        setWhiteArea={},
        setTrapArea=[],
        setAccelerate=[],
        setDecelerate=[])
    else:
        setGame()
    target=Actor('whitetarget')
    target.pos=Target[0],Target[1]
    dt=1/60
    game_status = 2
#打印屏幕
def draw():
    global exitDelay
    global Loading
    global ifReplay
    global ifBack
    global ifReturn
    global Winlist
    global n
    global ifDark
    global angle
    global ifChoose
    global ifsend
    global ifmessage
    global ifwelcome
    global Name
    global MemDark
    global WinTime
    global memDrag
    global memDrag2
    global ifwinall
    global memimage
    if game_status == 0: #开始界面
        Start()
        Exit.draw()
        if ifwelcome>0:
            ifwelcome-=1
            screen.blit('welcome',(0,0))
            screen.draw.text("CLICK & press ‘SPACE’ to return",(600,870),color='black',fontsize=40)
            if keyboard.space:
                ifwelcome=0
                sounds.clickinner.play()
        elif ifsend>0:#如果打开了信件，显示信件内容
            if ifsend==99999990:
                sounds.bgmplay.stop()
                sounds.bgmstart.stop()
                sounds.ghost.stop()
                sounds.ghost.play()
                sounds.keyboard.play()
            ifsend-=1
            screen.draw.filled_circle((800,450),1500,(0,0,0))
            tmp1=1
            tmp2=1
            for i in range(1,8):#计算获胜关卡
                if not(i in Winlist):
                    tmp1=0
                if not ((i+7) in Winlist):
                    tmp2=0
            if tmp1==1 and tmp2==1:#如果全胜
                ifwinall=1
                if ifsend>99998800:
                    screen.draw.text("Hello "+Name+":\n\nWow!We met again!We're surprised that you have marched so far!\n\nYou have conquered Python Ball World!That's amazing.\n\nNow that's time to say good bye.We must say you are the smartest player since Python Ball World Formed.\n\nWe have documented you playing info below.Bye.\n\n      Best Wishes\n\n                               From 4L Team Lin Haowei,Li Haoyu,Lin yunying&Li Yuzhe.",(100,100),color='white',fontsize=40)
                    tmp1='       LEVEL 1:\n'
                    tmp2='       LEVEL 2:\n'
                    for i in range(1,8):
                        tmp1+='Mission '+str(i)+'    '+str(int(WinTime[i]))+'.'+str(int(WinTime[i]*100)%100//10)+'s'
                        tmp1+='\n'
                        tmp2+='Mission '+str(i)+'    '+str(int(WinTime[i+7]))+'.'+str((int(WinTime[i+7]*100)%100//10))+'s'
                        tmp2+='\n'
                    screen.draw.text(tmp1,(300,600),color='white',fontsize=40)
                    screen.draw.text(tmp2,(900,600),color='white',fontsize=40)
                    screen.draw.text("CLICK & press ‘SPACE’ to return",(600,870),color='white',fontsize=40)
                else:
                    ans="    AUTHOR(NAMES ARE IN RANDOM ORDER):\n\n                                   Lin Haowei\n\n                                     Li Haoyu\n\n                                  Lin Yunying\n\n                                      Li Yuzhe\n\n\n\n\n                                INSPIRATION:\n\n                                 ULTRAFLOW\n\n                                        DUET\n\n\n\n\n                                  SOFTWARE:\n\nMICROSOFT PAINT (3D)\n\nMICROSOFT POWERPOINT\n\nADOBE AFTEREFFECTS\n\nADOBE PRIMIER\n\nADOBE PHOTOSHOP\n\nTHONNY (import PYZERO)\n\n\n\n\nSOME PICTURES OR SOUNDS ARE FROM INTERNET:\n\nhttp://www.yisell.com/\n\nhttps://app.xunjiepdf.com/mp32wav/\n\nhttps://space.bilibili.com/275008758\n\n\n\n\n                     ACKNOWLEDGEMENT:\n\nChen Bin    Python Programming and Application\n\n\n\n\n                        Thank you for playing.\n\n"
                    screen.draw.text(ans,(100,ifsend-99998100+250),color='white',fontsize=80)
                    if 100<ifsend<99999999-15000:#特别鸣谢
                        ifsend=0
                        sounds.ghost.stop()
                        sounds.bgmstart.play()
                        sounds.clickinner.play()
                Exit.draw()
                if keyboard.space:
                    ifsend=0
                    sounds.ghost.stop()
                    sounds.bgmstart.play()
                    sounds.clickinner.play()
            elif tmp1==1 and tmp2==0:#第一封信
                screen.draw.text("Hello "+Name+":\n\nNice to meet you.We're satisfied for you have been familiar with Python Ball World.\n\nPython Ball is thought as a project rather than only a FIN homework.We do hope you can enjoy yourself here.\n\nLevel 2 is a built-in DLC version of Python Ball.\n\nIn level 2,more intersting and challenging devices are waiting for you.\n\nWe're looking forward to your coming,at destination of level 2.\n\n    Best Wishes\n\n                                  From 4L Team Lin Haowei,Li Haoyu,Lin yunying,Li Yuzhe.",(100,100),color='white',fontsize=40)
                Exit.draw()
                screen.draw.text("CLICK & press ‘SPACE’ to return",(600,870),color='white',fontsize=40)
                if keyboard.space:
                    ifsend=0
                    sounds.ghost.stop()
                    sounds.bgmstart.play()
                    sounds.clickinner.play()
            elif tmp1==0 and tmp2==1:#第二封信
                screen.draw.text("Hello "+Name+":\n\nNice to meet you.We're surprised that you started with level 2 and ultimately finished it.\n\nPython Ball is thought as a project rather than only a FIN homework.We do hope you can enjoy yourself here.\n\nLevel 1 is a primier version of Python Ball.\n\nIn level 1, which we designed more carefully.You'll find them fascinating as well.\n\nWe're looking forward to your coming,at destination of level 1.\n\n                                  From 4L Team Lin Haowei,Li Haoyu,Lin yunying,Li Yuzhe.",(100,100),color='white',fontsize=40)
                Exit.draw()
                screen.draw.text("CLICK & press ‘SPACE’ to return",(600,870),color='white',fontsize=40)
                if keyboard.space:
                    ifsend=0
                    sounds.ghost.stop()
                    sounds.bgmstart.play()
                    sounds.clickinner.play()
        else:
            if exitDelay>0:
                screen.blit('ifexit',(50,50))
                for i in range(10):
                    screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1),600+30*math.sin(angle/3+i*0.1)),int(exitDelay/60+i/20+1),(0,0,0))
                    screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1+15),600+30*math.sin(angle/3+i*0.1+15)),int(exitDelay/60+i/20+1),(255,255,255))
    elif game_status == 1: #选关界面
        ifChoose=1
        if keyboard.backspace or keyboard.escape or keyboard.left or keyboard.home:
            sounds.click.play()
            ifReturn=1
            ReturnStart()
        if 1 <= n <=7:
            Level1()
            for i in range(1,8):#获胜的关卡会有标记
                if i in Winlist:
                    screen.draw.filled_circle((50*i+300,50),30,(0,0,0))
                    screen.draw.text(str(i),(50*i+288,30),color='white',fontsize=60)
                    for j in range(30):
                        screen.draw.circle((50*i+(40)*math.cos(angle/10+j*0.1)+300,50+(40)*math.sin(angle/10+j*0.1)),2,(255,255,255))
        elif 8 <= n <=14:
            Level2()
            for i in range(1,8):#获胜的关卡会有标记
                if (i+7) in Winlist:
                    screen.draw.filled_circle((50*i+300,50),30,(255,255,255))
                    screen.draw.text(str(i),(50*i+288,30),color='black',fontsize=60)
                    for j in range(30):
                        screen.draw.circle((50*i+(40)*math.cos(angle/10+j*0.1)+300,50+(40)*math.sin(angle/10+j*0.1)),2,(0,0,0))
            for iter in TrapArea:#势阱显示抖动特效
                if myBall.color==0:
                    thiscolor=(255,255,255)
                else:
                    thiscolor=(0,0,0)
                Radium=int(math.sqrt(iter[2]))+random.randint(-2,2)
                if Radium<=0:
                    Radium=1
                for i in range(26,30):
                    screen.draw.circle((iter[0],iter[1]),Radium+i,thiscolor)
        returnstart.draw()
        Exit.draw()
        if exitDelay>0:
            screen.blit('ifexit',(50,50))
            for i in range(10):#退出界面环形动画
                screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1),600+30*math.sin(angle/3+i*0.1)),int(exitDelay/60+i/20+1),(0,0,0))
                screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1+15),600+30*math.sin(angle/3+i*0.1+15)),int(exitDelay/60+i/20+1),(255,255,255))
        player=Actor('player')
        player.pos=1450,780
        player.draw()
        screen.draw.text(Name,(1400,880),color='white',fontsize=30)
    elif game_status == 2: #游戏界面
        if keyboard.lshift:
            sounds.click.play()
            time.sleep(1)
        if myBall.Lost():
            screen.clear()
            screen.blit('lost',(0,0))#如果输了，显示失败界面
            if Loading==0:
                Loading=random.randint(120,300)
            if Loading==1:
                ifReplay=1
                Loading=0
                Replay()
                sounds.gameover.stop()
                sounds.gamewin.stop()
                sounds.bgmplay.play()
            if Loading>1:#显示哭脸表情
                for i in range(10):
                    screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1),800+30*math.sin(angle/3+i*0.1)),int(i/20+4),(0,0,0))
                    screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1+15),800+30*math.sin(angle/3+i*0.1+15)),int(i/20+4),(255,255,255))
            player=Actor('playercry')
            player.pos=1470,780
            player.draw()
            screen.draw.text(Name,(1400,880),color='white',fontsize=30)
        elif myBall.InTarget():#胜利
            screen.clear()
            screen.blit('win',(0,0))
            Winlist.append(n)
            if WinTime[n]>angle/60:
                WinTime[n]=angle/60
            if ifHaveDark==1:
                MemDark[n]=1#如果全程迷雾胜利会有记录
            if Loading==0:
                sounds.gamewin.play()
                Loading=random.randint(120,300)
            if Loading==1:
                ifBack=1
                Loading=0
                Back()
                sounds.bgmstart.play()
            if Loading>1:
                for i in range(10):
                    screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1),800+30*math.sin(angle/3+i*0.1)),int(i/20+4),(0,0,0))
                    screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1+15),800+30*math.sin(angle/3+i*0.1+15)),int(i/20+4),(255,255,255))
            player=Actor('player')
            player.pos=1450,780
            player.draw()
            screen.draw.text(Name,(1400,880),color='white',fontsize=30)
        else:
            player=Actor('player')
            screen.clear()
            player.pos=1480,780
            screen.blit('background',(0,0))
            for iter in Walllist:
                if iter.color!=myBall.color:
                    iter.pic.draw()
            if keyboard.backspace or keyboard.escape:
                sounds.click.play()
                ifBack=1
                Back()
            tmp=Actor('hook')
            tmp.pos=800,450
            tmp.draw()#钩子
            for iter in Accelerate:#加速带
                tmp=Actor('whiteaccelerate')
                if myBall.color==1:
                    tmp=Actor('blackaccelerate')
                tmp.pos=iter[0],iter[1]
                tmp.angle=angle
                tmp.draw()
                if (myBall.x-iter[0])**2+(myBall.y-iter[1])**2<10000:
                    myBall.vx+=300*math.cos(tmp.angle/360*2*math.pi)
                    myBall.vy+=-300*math.sin(tmp.angle/360*2*math.pi)#加速算法
            for iter in Decelerate:#减速带
                tmp=Actor('whitedecelerate')
                if myBall.color==1:
                    tmp=Actor('blackdecelerate')
                tmp.pos=iter[0],iter[1]
                tmp.draw()
                if (myBall.x-iter[0])**2+(myBall.y-iter[1])**2<10000:
                    myBall.vx/=1.1
                    myBall.vy/=1.1
            for iter in Field:#Field旋转特效
                x=random.randint(-2,2)
                for i in range(80):
                    screen.draw.filled_circle((iter[0]+x+FieldR[iter[2]]*math.cos(angle/20+i*0.01),iter[1]+x+FieldR[iter[2]]*math.sin(angle/20+i*0.01)),10,colorlist[myBall.color])
                    screen.draw.filled_circle((iter[0]+x+(FieldR[iter[2]]-23)*math.cos(angle/10+i*0.02),iter[1]+x+(FieldR[iter[2]]-23)*math.sin(angle/10+i*0.02)),8,colorlist[myBall.color])
                    screen.draw.filled_circle((iter[0]+x+(FieldR[iter[2]]-40)*math.cos(angle/5+i*0.02),iter[1]+x+(FieldR[iter[2]]-40)*math.sin(angle/5+i*0.02)),5,colorlist[myBall.color])  
                    screen.draw.filled_circle((iter[0]+x+(FieldR[iter[2]]-55)*math.cos(angle/4+i*0.02),iter[1]+x+(FieldR[iter[2]]-55)*math.sin(angle/4+i*0.02)),3,colorlist[myBall.color])
                for i in range(5):    
                    screen.draw.circle((iter[0],iter[1]),(3*angle)%(FieldR[iter[2]]-55)+1,colorlist[myBall.color])
                    screen.draw.circle((iter[0],iter[1]),(3*angle)%(FieldR[iter[2]]-55)+2,colorlist[myBall.color])
                    screen.draw.circle((iter[0],iter[1]),(3*angle)%(FieldR[iter[2]]-55)+3,colorlist[myBall.color])
                    screen.draw.circle((iter[0],iter[1]),(3*(angle+180))%(FieldR[iter[2]]-55)+3,colorlist[myBall.color])
                    screen.draw.circle((iter[0],iter[1]),(3*(angle+180))%(FieldR[iter[2]]-55)+3,colorlist[myBall.color])
            if keyboard.x:#使用钩子
                player.image='playerimpatient'
                if myBall.color==0:
                    screen.draw.line((myBall.x,myBall.y),(800,480),(255,255,255))
                    screen.draw.line((myBall.x,myBall.y-1),(800,480-1),(255,255,255))
                    screen.draw.line((myBall.x,myBall.y-2),(800,480-2),(255,255,255))
                else:
                    screen.draw.line((myBall.x,myBall.y),(800,480),(0,0,0))
                    screen.draw.line((myBall.x,myBall.y),(800,480-1),(0,0,0))
                    screen.draw.line((myBall.x,myBall.y),(800,480-2),(0,0,0))
                d2=(myBall.x-800)**2+(myBall.y-450)**2
                if keyboard.c and keyboard.v==False:#使用软绳
                    if memDrag==1:
                        sounds.normalrope.play()
                    myBall.x-=3*(myBall.x-800)/math.sqrt(d2)
                    myBall.y-=3*(myBall.y-480)/math.sqrt(d2)
                    memDrag+=1
                elif memDrag>0 and keyboard.v==False:#软绳弹回
                    memDrag-=1
                    myBall.x+=3*(myBall.x-800)/math.sqrt(d2)
                    myBall.y+=3*(myBall.y-480)/math.sqrt(d2)
                    sounds.normalrope.stop()
                x0=800
                y0=480
                x=myBall.x
                y=myBall.y
                vx=myBall.vx
                vy=myBall.vy
                tmp=-1.0*((x-x0)*vx+(y-y0)*vy)/((x-x0)**2+(y-y0)**2)
                if tmp>0:
                    tmp=0
                myBall.vx=vx+tmp*(x-x0)
                myBall.vy=vy+tmp*(y-y0)
                if keyboard.v:#使用弹绳
                    if memDrag2==1:
                        sounds.hardrope.play()
                    memDrag2+=1
                    myBall.Force(-1000*(myBall.x-800)/math.sqrt(d2),-1000*(myBall.y-480)/math.sqrt(d2))
                    for i in range(30):
                        x=800+i/30*(myBall.x-800)+random.randint(-2,2)
                        y=480+i/30*(myBall.y-480)+random.randint(-2,2)
                        screen.draw.circle((x,y),5,colorlist[not myBall.color])
            else:
                memDrag=0
                memDrag2=0
            if myBall.color==0:#绘制黑洞
                tmpArea=BlackArea.keys()
                tmpOut=WhiteArea.values()
                tmpInHole='whitehole'
                tmpOutHole='blackout'
            else:
                tmpArea=WhiteArea.keys()
                tmpOut=BlackArea.values()
                tmpInHole='blackhole'
                tmpOutHole='whiteout'
            for iter in tmpArea:#如果进入黑洞
                if (myBall.x-iter[0])**2+(myBall.y-iter[1])**2<90000:
                    player.image='playerfrighted'
                    if memimage!=player.image:
                        sounds.frighted.play()#恐惧表情
                else:
                    sounds.frighted.stop()
                tmp=Actor(tmpInHole)
                tmp.pos=iter[0],iter[1]
                tmp.angle=angle
                tmp.draw()
            for iter in tmpOut:#黑洞自带旋转特效
                tmp=Actor(tmpOutHole)
                tmp.pos=iter[0],iter[1]
                tmp.angle=-angle
                tmp.draw()
            for iter in TrapArea:#势阱
                if myBall.color==0:
                    thiscolor=(255,255,255)
                else:
                    thiscolor=(0,0,0)
                Radium=int(math.sqrt(iter[2]))+random.randint(-2,2)
                if Radium<=0:
                    Radium=1
                if Radium!=1 and iter[2]!=1:
                    screen.draw.filled_circle((iter[0],iter[1]),Radium,thiscolor)
                    screen.draw.circle((iter[0],iter[1]),Radium,thiscolor)
                    screen.draw.circle((iter[0],iter[1]),Radium,thiscolor)
                    screen.draw.circle((iter[0],iter[1]),Radium+10,thiscolor)
                    screen.draw.circle((iter[0],iter[1]),Radium+20,thiscolor)
                    screen.draw.circle((iter[0],iter[1]),Radium+25,thiscolor)
                    screen.draw.circle((iter[0],iter[1]),300-(5*angle)%300,thiscolor)
                for i in range(26,30):
                    screen.draw.circle((iter[0],iter[1]),Radium+i,thiscolor)
            if myBall.color==0:#秋的颜色不同，则目标颜色不同
                target.image='whitetarget'
            else:
                target.image='blacktarget'
            target.pos=Target[0],Target[1]
            target.angle=int(math.fabs(angle%360-180))
            target.draw()
            myBall.pic.draw()
            Tail.append((myBall.x,myBall.y))
            size=1
            for iter in Tail:
                screen.draw.circle(iter,int(size**2/(50))+1,colorlist[myBall.color])
                size+=1
            while len(Tail)>50:#小球尾巴
                Tail.pop(0)
            waitR=55
            if myBall.color==1:
                for i in range(30):
                    screen.draw.circle((myBall.x+waitR*math.cos(angle/10+i*0.1),myBall.y+waitR*math.sin(angle/10+i*0.1)),3,colorlist[myBall.color])
            else:
                for i in range(30):
                    screen.draw.circle((myBall.x+(waitR)*math.cos(angle/8+i*0.2),myBall.y+(waitR)*math.sin(angle/10+i*0.2)),3,colorlist[myBall.color]) 
            waitR=250
            for i in range(20):
                screen.draw.circle((myBall.x+waitR*math.cos(angle+i*0.3),myBall.y+waitR*math.sin(angle+i*0.3)),3,colorlist[myBall.color])
            waitsize=5
            R0=80
            waitTail.append((R0*math.cos(5*angle),R0*math.sin(5*angle)))
            for iter in waitTail:
                screen.draw.circle((Target[0]+iter[0],Target[1]+iter[1]),int(waitsize/(5)),colorlist[myBall.color])
                waitsize+=1
            while len(waitTail)>30:
                waitTail.pop(0)
            if myBall.life<10:
                screen.draw.text(str(myBall.life),(myBall.x-12,myBall.y-20),color=colorlist[not myBall.color],fontsize=60)
            else:
                screen.draw.text(str(myBall.life),(myBall.x-25,myBall.y-20),color=colorlist[not myBall.color],fontsize=60)
            if myBall.Delay!=0:
                myBall.Delay-=1
            if myBall.Delay2!=0:
                myBall.Delay2-=1
            if ifDark==1:
                screen.draw.filled_rect(Rect((0,0),(1600,myBall.y-500)),colorlist[myBall.color])
                screen.draw.filled_rect(Rect((0,myBall.y+500),(1600,900)),colorlist[myBall.color])
                screen.draw.filled_rect(Rect((0,0),(myBall.x-500,900)),colorlist[myBall.color])
                screen.draw.filled_rect(Rect((myBall.x+500,0),(1600,900)),colorlist[myBall.color])
                for i in range(-11,11):
                    for j in range(-11,11):
                        if (i*50+25)**2+(j*50)**2>200000:
                            screen.draw.filled_circle((i*50+25+myBall.x+random.randint(-5,5),j*50+myBall.y+random.randint(-5,5)),50,colorlist[myBall.color])
            screen.draw.text('Time(s):'+str(angle//60)+'.'+str(int(angle%60*100/60)//10),(600,30),color=colorlist[not myBall.color],fontsize=100)#输出时间
            if (myBall.x-Target[0])**2+(myBall.y-Target[1])**2<90000:
                player.image='playersmile'
            elif myBall.life==1:
                player.image='playerdesperate'
                if memimage!=player.image:
                    sounds.desperate.play()
            elif (myBall.vx**2+myBall.vy**2)<50000 and player.image=='player':
                player.image='playerimpatient'
            player.draw()
            if myBall.life!=1:
                sounds.desperate.stop()
            screen.draw.text(Name,(1400,880),color='white',fontsize=30)
            memimage=player.image
        Exit.draw()
        replay.draw()
        back.draw()
        if keyboard.r:#支持R键复位
            Replay()
        if ifDark==1:
            screen.draw.text('Press ''z'' to switch to the God’s perspective',(500,850),color=colorlist[not myBall.color],fontsize=40)
        else:
           screen.draw.text('Press ''z'' to switch to Explorer’s perspective',(500,850),color=colorlist[myBall.color],fontsize=40)
        tmp=Actor('blackchoose')
        tmp.pos=130,790
        tmp.draw()
        screen.draw.text(str((n-1)%7+1),(90,730),color='white',fontsize=200)
        if ifDark==0:
            for i in range(30):
                    screen.draw.filled_circle((130+(110)*math.cos(angle/10+i*0.1),790+(110)*math.sin(angle/10+i*0.1)),5,'black')
        else:
            for i in range(30):
                    screen.draw.filled_circle((130+(110)*math.cos(angle/10+i*0.1),790+(110)*math.sin(angle/10+i*0.1)),5,'white')
        if exitDelay>0:#退出
            screen.blit('ifexit',(50,50))
            for i in range(10):
                screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1),600+30*math.sin(angle/3+i*0.1)),int(exitDelay/60+i/20+1),(0,0,0))
                screen.draw.filled_circle((820+30*math.cos(angle/3+i*0.1+15),600+30*math.sin(angle/3+i*0.1+15)),int(exitDelay/60+i/20+1),(255,255,255))
def update():#更新
    global game_status
    global n
    global gotName
    global ifChoose
    global ifwelcome
    global ifmessage
    global ifsend
    global Winlist
    global Name
    global mouse
    if game_status == 0 and gotName==1 and ifwelcome==0:#如果再开始界面点到level
        if 1300 < mouse[0] < 1500 and 600 < mouse[1] < 650 or keyboard.up or keyboard.k_1 and timer==42 or keyboard.kp1 and timer==42:
            mouse=(0,0)
            game_status = 1
            n = 1
            sounds.clickinner.play()
            Level1()
        if 1300 < mouse[0] < 1500 and 700 < mouse[1] < 750 or keyboard.down or keyboard.k_2 and timer==42 or keyboard.kp2 and timer==42:
            mouse=(0,0)
            n = 8
            game_status = 1
            sounds.clickinner.play()
            Level2()
        if 100 < mouse[0] < 300 and 750 < mouse[1] < 900:
            mouse=(0,0)
            sounds.clickinner.play()
            gotName=0
            Name=''
            Winlist=[]
            ifChoose=0
            ifwinall=0
            ifmessage=0
        if 430 < mouse[0] < 1170 and 500 < mouse[1] < 550 and ifChoose==1:
            mouse=(0,0)
            sounds.clickinner.play()
            ifwelcome=100000000
        if (150 < mouse[0] < 300 and 80 < mouse[1] < 150 or keyboard.m==True )and ifmessage==1 :
            mouse=(0,0)
            sounds.clickinner.play()
            ifsend=100000000
    global lifeDelay
    global ifDark
    global angle
    global DarkDelay
    global ReplayDelay
    global exitDelay
    global Loading
    global ifHaveDark
    if Loading>1:
        Loading-=1
    if exitDelay>1:
        exitDelay-=1
        if keyboard.space:#取消退出进程
            sounds.clickinner.play()
            exitDelay=0
    if exitDelay==179:#退出音效
        sounds.click.play()
    if exitDelay==1:
        sounds.click.play()
        exit()
    angle+=1
    lifeDelay-=1
    if ReplayDelay>0:
        ReplayDelay-=1
    myBall.x=max(myBall.x,myBall.R-10)
    myBall.x=min(myBall.x,1600-myBall.R+10)
    myBall.y=max(myBall.y,myBall.R-10)
    myBall.y=min(myBall.y,900-myBall.R+10)
    if lifeDelay<0:
        lifeDelay=0
    for iter in Walllist:
        iter.updateWall()
    if not myBall.InTarget() and not myBall.Lost():#常规操作
        myBall.change()
        myBall.updateBall()
        myBall.Move()
        if keyboard.z==True and DarkDelay==0:#开启、关闭迷雾模式
            sounds.click.play()
            ifDark=not ifDark
            if ifDark==0:
                ifHaveDark=0#维护memDark
            DarkDelay=30
        if DarkDelay>0:
            DarkDelay-=1
pgzrun.go()


