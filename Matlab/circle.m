function [] = circle(x,y,r,R,G,B)
d = r*2;
px = x-r;
py = y-r;
rectangle('Position',[px py d d],'Curvature',[1,1],'FaceColor',[R G B],'EdgeColor',[R G B]);
daspect([1,1,1])