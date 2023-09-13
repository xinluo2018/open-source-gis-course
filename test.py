def f(x):
    y=0
    if(x==1):
        y=1
        return y
    else:
        return x*f(x-1)
print("请输入一个数：")
x=int(input())
y=f(x)
print(y)