-- a simple grid

width = 3;
height = 15;

a = Vector3:new{x=0.0, y=0.0};
b = Vector3:new{x=10 , y=0.0};
c = Vector3:new{x=10 , y=15};
d = Vector3:new{x=0.0, y=15};

patch = CoonsPatch:new{p00=a, p10=b, p11=c, p01=d};
grid = StructuredGrid:new{psurface=patch, niv=width+1, njv=height+1};

registerFluidGrid{grid=grid, fsTag="initial"};
