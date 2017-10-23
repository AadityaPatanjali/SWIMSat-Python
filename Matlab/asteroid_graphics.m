function asteroid_graphics(rad,speed,T,n,R,G,B)
world = vrworld('Burst.wrl','new');
open(world);
fig = vrfigure(world);
set(fig,'Fullscreen','on');
ball = vrnode(world, 'ASDF');
tail = vrnode(world,'Tail');
qwe = vrnode(world,'qwerty');
Earth = vrnode(world, 'Earth');
burst = vrnode(world,'Color');
blink = vrnode(world,'Color2');
burst.color = [R G B;T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;
    T T T;T T T;T T T;T T T;T T T;T T T;T T T];
blink.color = [T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;
    R G B;R G B;R G B;R G B;R G B;R G B;R G B;R G B;R G B;R G B;
    T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;T T T;
    R G B;R G B;R G B;R G B;R G B;R G B;R G B;R G B;R G B;R G B];

theta = 0:0.01:100;
theta2 = 0:-0.01/50:-2000/50;
scy = 1*rad:(0.002/0.4*rad)*speed:2*rad;
sc = 0.5*rad:(0.01/0.4*rad)*speed:100*rad;
qwe.scale = [sc(1) scy(1)/1.3 1];
ball.scale = [scy(1) scy(1) scy(1)];
j = 0;
while j<n
    a = randi([35 145],1,1);
%     a = 90;

    if a > 60 && a < 120
        b = [60 120];
        r = randi([1 2],1,1);
        a = b(r);
    end
        m = tand(a);
    if a < 90
        x = 90:-speed:-90;
        y = m.*x;
    elseif a > 90
        x = -90:speed:90;
        y = m.*x;
    end
    qwe.rotation = [0 0 1 a*pi/180];
for i = 1:length(x)
    Earth.rotation = [0 1 0 theta2(i)];
    ball.translation = [x(i) y(i) 0];
%     tail.rotation = [cos(pi/4) sin(pi/4) 0 theta(i)];
    qwe.scale = [sc(i) scy(i)/1.3 1];
    ball.scale = [scy(i) scy(i) scy(i)];
    vrdrawnow;
end
the = theta2(length(x));
theta2 = the:-0.01/50:the-2000/50;
j = j+1;
end
set(fig,'Fullscreen','off')