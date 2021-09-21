#导入flask
from flask import Flask,render_template,request,escape,url_for,jsonify
import cmath

import time
from copy import deepcopy

aaa=[]

#各结点的数据结构，保存了状态，双亲等信息
class Node:
    def __init__(self, state,cost_g,cost_h,parent,search,path):
        self.state = state
        self.cost_g = cost_g
        self.cost_h = cost_h 
        self.parent = parent
        self.search = search
        self.path=path
#exam_solve函数通过计算目标状态与初始结点的逆序对数判断问题是否可解  
def exam_solve(initial_state,goal_state):
    initial_count = 0
    temp=[]
    for i in range(3) :
        for j in range(3) :
            if(initial_state[i][j]!=0):
                temp.append(initial_state[i][j])
    for i in range(8) : 
        j=i+1
        while(j<8):
            if(temp[i]>temp[j]):
                initial_count +=1
            j+=1

    goal_count = 0
    temp=[]
    for i in range(3) :
        for j in range(3) :
            if(goal_state[i][j]!=0):
                temp.append(goal_state[i][j])
    for i in range(8) : 
        j=i+1
        while(j<8):
            if(temp[i]>temp[j]):
                goal_count +=1
            j+=1

    if(initial_count%2==goal_count%2):
        return True
    else:
        return False
#启发函数excu_h_0计算不在位结点数
def excu_h_0(state,goal_state):
    total=0
    for i in range(3):
        for j in range(3):
            if(goal_state[i][j]!=state[i][j]):
                total+=1
    return total
#启发函数excu_h_1计算曼哈顿距离 
def excu_h_1(state,goal_state):
    total=0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if(goal_state[i][j]==state[k][l]):
                        total+=abs(i+j-k-l)
                        break
                if(goal_state[i][j]==state[k][l]):
                        break
    return total
#启发函数excu_h_2计算直线距离 
def excu_h_2(state,goal_state):
    total=0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if(goal_state[i][j]==state[k][l]):
                        total+=cmath.sqrt((i-k)*(i-k)+(j-l)*(j-l))
                        break
                if(goal_state[i][j]==state[k][l]):
                        break
    return total.real
#启发函数excu_h_3等比例调用excu_h_0与excu_h_1生成新的启发函数
def excu_h_3(state,goal_state):
    return float(excu_h_0(state,goal_state)+2*excu_h_1(state,goal_state))
#选择不同的启发式函数
def excu_h(state,goal_state,switch):
    #选择启发函数0
    if(switch==0):
        return excu_h_0(state,goal_state)
    #选择启发函数1
    if(switch==1):
        return excu_h_1(state,goal_state)
    #选择启发函数2
    if(switch==2):
        return excu_h_2(state,goal_state)
    #选择启发函数3
    if(switch==3):
        return excu_h_3(state,goal_state)
def extend(frontier,goal_state,switch):
    flag=False
    for x in range(len(frontier)):
        if(not flag and frontier[x].search==False):
            flag=True
            min=x
            min_cost=frontier[x].cost_g+frontier[x].cost_h
        if(not flag):
            continue
        if((frontier[x].cost_g+frontier[x].cost_h)<min_cost)and(not frontier[x].search):
            min=x
            min_cost=frontier[x].cost_g+frontier[x].cost_h
    frontier[min].search=True

    for i in range(3):
        for j in range(3):
            if(frontier[min].state[i][j]==0):
                break
        if(frontier[min].state[i][j]==0):
                break          
    child_state=[]
    if(i>0):
        mid=deepcopy(frontier[min].state)
        t=mid[i][j]
        mid[i][j]=mid[i-1][j]
        mid[i-1][j]=t
        child_state.append(mid)
    if(i<2):
        mid=deepcopy(frontier[min].state)
        t=mid[i][j]
        mid[i][j]=mid[i+1][j]
        mid[i+1][j]=t
        child_state.append(mid)
    if(j<2):
        mid=deepcopy(frontier[min].state)
        t=mid[i][j]
        mid[i][j]=mid[i][j+1]
        mid[i][j+1]=t
        child_state.append(mid)
    if(j>0):
        mid=deepcopy(frontier[min].state)
        t=mid[i][j]
        mid[i][j]=mid[i][j-1]
        mid[i][j-1]=t
        child_state.append(mid)
    
    temp=[]
    for i in range(len(child_state)):
        for j in frontier:
            if(child_state[i]==j.state):
                temp.append(child_state[i])
    for i in temp:
        child_state.remove(i)

    for i in child_state:
        j=Node(i,frontier[min].cost_g+1,excu_h(i,goal_state,switch),min,False,0)
        frontier.append(j)
        if(i==goal_state):
            return True
    return False
def print_solve(frontier,index):
    if(frontier[index].parent!=-1):
        print_solve(frontier,frontier[index].parent)
    aaa.append(frontier[index].state)
    frontier[index].path=1
    print(frontier[index].state)

#创建一个app应用
#__name__指向程序所在的包
app=Flask(__name__)

#生成前端主页面
@app.route('/',methods=['GET','POST'])
def index1():
    return render_template("index1.html",aaa=aaa)

#获取前端用户选择的八数码初始状态、结束状态、启发函数到后端
@app.route('/2',methods=['GET','POST'])
def index2():
    if request.method=='POST':
        #获取初始状态
        input1=request.form.get('input1')
        input2=request.form.get('input2')
        input3=request.form.get('input3')
        input4=request.form.get('input4')
        input5=request.form.get('input5')
        input6=request.form.get('input6')
        input7=request.form.get('input7')
        input8=request.form.get('input8')
        input9=request.form.get('input9')
        #获取结束状态
        output1=request.form.get('output1')
        output2=request.form.get('output2')
        output3=request.form.get('output3')
        output4=request.form.get('output4')
        output5=request.form.get('output5')
        output6=request.form.get('output6')
        output7=request.form.get('output7')
        output8=request.form.get('output8')
        output9=request.form.get('output9')
        #获取用户选择的启发函数类型并打印
        excu_h_type=request.form.get('aaa')
        excu_h_type=int(excu_h_type)
        print("excu_h_type")
        print(excu_h_type)
        #将初始状态放入一个列表
        initial_state=[]
        initial_state.append([])
        initial_state.append([])
        initial_state.append([])
        initial_state[0].append(input1)
        initial_state[0].append(input2)
        initial_state[0].append(input3)
        initial_state[1].append(input4)
        initial_state[1].append(input5)
        initial_state[1].append(input6)
        initial_state[2].append(input7)
        initial_state[2].append(input8)
        initial_state[2].append(input9)
        initial_state[0] = [ int(x) for x in initial_state[0] ]
        initial_state[1] = [ int(x) for x in initial_state[1] ]
        initial_state[2] = [ int(x) for x in initial_state[2] ]
        #print(initial_state)
        #将结束状态放入一个列表
        goal_state=[]
        goal_state.append([])
        goal_state.append([])
        goal_state.append([])
        goal_state[0].append(output1)
        goal_state[0].append(output2)
        goal_state[0].append(output3)
        goal_state[1].append(output4)
        goal_state[1].append(output5)
        goal_state[1].append(output6)
        goal_state[2].append(output7)
        goal_state[2].append(output8)
        goal_state[2].append(output9)
        goal_state[0] = [ int(x) for x in goal_state[0] ]
        goal_state[1] = [ int(x) for x in goal_state[1] ]
        goal_state[2] = [ int(x) for x in goal_state[2] ]
        #判断是否有解
        if(exam_solve(initial_state,goal_state)==False):
            print("问题不可解")
            frontier=[]
            costtime=0
            frontier1=[]
            node_num2=0
        else:   
            start1 =time.perf_counter()
            start=Node(initial_state,0,excu_h(initial_state,goal_state,excu_h_type),-1,False,0)
            frontier=[start]

            if(frontier[0].state!=goal_state):
                while(True):
                    if(extend(frontier,goal_state,excu_h_type)):
                        break
            end1=time.perf_counter()
            costtime=end1-start1
            print_solve(frontier,-1)
            #后端打印运行时间
            print("运行时间：")
            print(end1-start1)
            #后端打印生成结点数
            print("节点数：")
            print(len(frontier))
            frontier1=[]
            node_num2=0
            for i in range(0,len(frontier)):
                frontier1.append({'state':frontier[i].state,'parent':frontier[i].parent,'search':frontier[i].search,'path':frontier[i].path})
                if(frontier[i].search==True):
                    node_num2=node_num2+1
                print(frontier[i].state)
    print(aaa)
    bbb=aaa[:]
    aaa[:]=[]
    return jsonify({'data':bbb,'node_num':len(frontier),'time':costtime,'frontier':frontier1,'node_num2':node_num2})

if __name__=='__main__':
    #web服务器的入口
    app.run(debug=True,port=5001)