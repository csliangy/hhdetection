% Test for lsq_lut_piecewise function

fid = fopen('Window2.txt','r')
y = fscanf(fid, '%d')
fclose(fid)
x = [1:1:length(y)]'

% plot fit
subplot(611); 
plot(x,y,'.',x,y,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')
title('Original Traffic Data')

% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),5);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(612); 
plot(x,y,'.',XI,YI,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')
title('Piecewise 1-D look-up table least square estimation with 5 points')

% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),10);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(613); 
plot(x,y,'.',XI,YI,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')
title('Piecewise 1-D look-up table least square estimation with 10 points')

% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),20);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(614); 
plot(x,y,'.',XI,YI,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')
title('Piecewise 1-D look-up table least square estimation with 20 points')

% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),50);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(615); 
plot(x,y,'.',XI,YI,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')
title('Piecewise 1-D look-up table least square estimation with 50 points')

% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),100);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(616); 
plot(x,y,'.',XI,YI,'+-')
title('Piecewise 1-D look-up table least square estimation with 100 points')
