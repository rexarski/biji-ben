from pylab import *
from numpy import *



#def F(x):
#    return cos(x)

#def D(x):
#    if (x<.5): return 2*x
#        
#    elif (x<1): return 2*x-1

def D(x):
    return mod(2*x,1)

def graph_D(color):
    plot([0,0.5],[0,1],color)
    plot([0.5,1],[0,1],color)

def orbit(func, x0, N, pontos=100, limits=[0.,pi/2.,-1,1]):
    exec define_F(func)

    x=[]
    x.append(x0*1.)

    for i in range(N):
        x1=F(x0)
        x.append(x1*1.)
        x0=x1*1.

    return x



def graph_func(func,N=100,limits=[-1,3,-1,1]):
    exec define_F(func)

    pts=arange(N)*float(limits[1]-limits[0])/N+limits[0]

    func=[]
    for i in range(N):
        func.append(F(pts[i]))

    plot(pts,pts,'darkgreen')
    plot(pts,func,'red')
    axis(limits)

def cobweb_orbit(x):
    N = len(x)
    xx=[]
    yy=[]    
    for i in range(N-1):
        xx.append(x[i]*1.)
        yy.append(x[i]*1.)
        xx.append(x[i]*1.)
        yy.append(x[i+1]*1.)

    xx.append(x[N-1]*1.)
    yy.append(x[N-1]*1.)

    plot(xx,yy,'blue')

    N = len(xx)
    for i in range(N-1):
        arrow(array([xx[i],xx[i+1]]),array([yy[i],yy[i+1]]),'blue')
        

    return [xx,yy]


def i_cobweb_orbit(x):
    N = len(x)
    xx=[]
    yy=[]    
    for i in range(N-1):
        xx.append(x[i]*1.)
        yy.append(x[i]*1.)
        xx.append(x[i]*1.)
        yy.append(x[i+1]*1.)

    xx.append(x[N-1]*1.)
    yy.append(x[N-1]*1.)

    #plot(xx,yy,'blue')

    N = len(xx)
    resp=' '
    for i in range(N-1):
        plot([xx[i],xx[i+1]],[yy[i],yy[i+1]],'blue')
        arrow([xx[i],xx[i+1]],[yy[i],yy[i+1]],'blue')
        
        if resp!='r':
            resp=raw_input()
                        
        if (resp=='q'):
            break


    return [xx,yy]



def define_F(str):
    string = '''def F(x): return %s''' % str    
    return string

def orbit_F(func,seed,iter,limits=[-1,3,-1,1]):
    figure()
    x = orbit(func,seed,iter)
    graph_func(func,100,limits)
    [xx,yy]=cobweb_orbit(x)
    return [x,xx,yy]

def plot_orbit(func, seed, iter):
    x = orbit(func,seed,iter)
    pts=arange(iter+1)+1.
    figure()
    plot(pts,x,'.')
    return x



def arrow(x,y,color,L=15.):
    #
    # Given two points A=(x[0],y[0]) and B=(x[1],y[1]), it makes an arrow in the center of the vector AB point from A to B
    # (the size of the arrow is L=15 times smaller than the segment)

    arrow=array([(x[0]+x[1])/2.,(y[0]+y[1])/2.])
    vec=array([x[1]-x[0],y[1]-y[0]])
    vec_perp=array([y[1]-y[0],x[0]-x[1]])

    dir1=(-vec+vec_perp)/L
    dir2=-(vec_perp+vec)/L
    
    
    ptsx=[arrow[0]+dir1[0],arrow[0],arrow[0]+dir2[0]]
    ptsy=[arrow[1]+dir1[1],arrow[1],arrow[1]+dir2[1]]
    
    #figure()
    #plot(x,y)
    plot(ptsx,ptsy,color)
    #axis('equal')



def i_orbit_F(func,seed,iter,limits=[0,1,0,1]):
    figure()
    x = orbit(func,seed,iter)
    graph_func(func,100,limits)
    i_cobweb_orbit(x)
    return x



#    maxWeight = 2**N.ceil(N.log(N.max(N.abs(W)))/N.log(2))

#    P.fill(N.array([0,width,width,0
