from collections import deque

direction = [(-1,0),(1,0),(0,-1),(0,1)]

n,m,K=map(int,input().split())
a=[[0]*m for _ in range(n)]
ans=0

# 출구 위치
def getExit(y,x,d):
    if d==0:
        return [y-1,x]
    elif d==1:
        return [y,x+1]
    elif d==2:
        return [y+1,x]
    else:
        return [y,x-1]

def inBoard(ny,nx):
    if 0<=ny<n and 0<=nx<m:
        return True
    return False

# 골렘이 어떤 좌표로 이동 가능한 상태인지 확인
def check(y,x):
    if not inBoard(y,x): # 좌표가 보드 밖에 위치하면
        if y<n and 0<=x<m: # 좌표가 위쪽이 뚫린 바구니 같은 공간에 있는지
            return True
    else: # 좌표가 보드 안에 위치하면
        if a[y][x]==0: # 다른 골렘이 없는지
            return True
    return False

# 골렘 이동
def move(r,d,no):
    global a

    y,x=-2,r # 골렘 내 중앙의 정령 위치. 보드 맨 위에서 두 칸 위인 y==-2 지점부터 내려온다.
    while True:
        # 골렘 수직 이동
        if check(y+2,x) and check(y+1,x-1) and check(y+1,x+1):
            y+=1
        # 골렘 왼쪽 이동
        elif check(y+1,x-1) and check(y-1,x-1) and check(y,x-2) and check(y+1,x-2) and check(y+2,x-1):
            y+=1
            x-=1
            d=(d-1)%4
        # 골렘 오른쪽 이동
        elif check(y+1,x+1) and check(y-1,x+1) and check(y,x+2) and check(y+1,x+2) and check(y+2,x+1):
            y+=1
            x+=1
            d=(d+1)%4
        else:
            break

    # 골렘 지도에 표시
    if not inBoard(y, x) or not inBoard(y + 1, x) or not inBoard(y-1,x) or not inBoard(y,x+1) or not inBoard(y,x-1):
        return [False, -1, -1]
    else:
        a[y][x]=a[y+1][x]=a[y-1][x]=a[y][x+1]=a[y][x-1]=no
        ey, ex = getExit(y, x, d)# 출구 위치
        a[ey][ex]=-no
        return [True,y,x]

# 정령 이동
def bfs(sy,sx,no):

    max_y = -2
    q=deque()
    q.append((sy,sx))
    visit=[[False]*m for _ in range(n)]
    visit[sy][sx]=True

    while q:
        y,x=q.popleft()
        max_y = max(max_y,y)
        for dy,dx in direction:
            ny,nx=y+dy,x+dx
            if not inBoard(ny,nx) or visit[ny][nx] or a[ny][nx]==0:
                continue
            # 절댓값이 같은 칸으로 움직이거나, 출구 칸에서 다른 칸으로 이동 가능
            if abs(a[y][x])==abs(a[ny][nx]) or (a[y][x]<0 and abs(a[ny][nx])!=abs(a[y][x])):
                q.append((ny,nx))
                visit[ny][nx]=True
                
    return max_y+1

for no in range(1,K+1):
    r,d=map(int,input().split())
    r-=1

    # 골렘 이동
    res=move(r,d,no)
    inBound,y,x=res

    # 골렘 몸 일부가 숲 벗어나있는지 확인
    if inBound:
        # 정령 이동
        ans+=bfs(y,x,no)
    else:
        # 숲 초기화
        a=[[0]*m for _ in range(n)]

print(ans)