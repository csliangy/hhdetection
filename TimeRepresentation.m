%Prepare the raw time series data
fid = fopen('Window2.txt','r')
s = fscanf(fid, '%d')
fclose(fid)


%apca(s,30);

% FFT-IFFT
Fs = 1
T = 1
L = 256
t = (0:L-1)*T
Length1 = L/64
Length2 = L/16
Length3 = L/4

NFFT = 2^nextpow2(L);
Y = fft(s,NFFT)/L;
f = Fs/2*linspace(0,1,NFFT/2+1);

%{
subplot(711); 
plot(f,2*abs(Y(1:NFFT/2+1))) 
title('Single-Sided Amplitude Spectrum of y(t)')
xlabel('Frequency (Hz)')
ylabel('|Y(f)|')
%}

N=length(s);

t=0:N-1;
subplot(4,4,1)
plot(t,s);
xlabel('Time (s)');
y1 = ylabel('Original Traffic');
pos1=get(y1,'Pos')
title('FFT - IFFT')


%{
subplot(); 
plot(0:N-1,abs(fft(x)));  
xlabel('Frequency');
ylabel('|X(k)|');
title('Magnitude Response'); 

subplot(); 
plot(0:N-1,angle(fft(x)));
xlabel('Frequency');
ylabel('Phase');
title('Phase Response'); 
%}

freq_n = L/64
fft_data_v = fft(s);
s_fft_data_v = zeros(1,length(s));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(4,4,5)
plot(0:N-1,s_data_v);
y2 = ylabel('1/64 Representation');
pos2=get(y2,'Pos')
set(y2,'Pos',[pos1(1) pos2(2) pos2(3)])

freq_n = L/16
fft_data_v = fft(s);
s_fft_data_v = zeros(1,length(s));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(4,4,9)
plot(0:N-1,s_data_v);
ylabel('1/16 Representation');



freq_n = L/4
fft_data_v = fft(s);
s_fft_data_v = zeros(1,length(s));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(4,4,13)
plot(0:N-1,s_data_v);
ylabel('1/4 Representation');


% DWT - HAAR
[C,L] = wavedec(s, 6, 'db1');
A1 = wrcoef('a',C,L,'db1',2); %1/4
A2 = wrcoef('a',C,L,'db1',4); %1/16
A3 = wrcoef('a',C,L,'db1',6); %1/64

subplot(4,4,2)
plot(t,s);
title('Wavelet - Haar')

subplot(4,4,6)
plot(t,A3)

subplot(4,4,10)
plot(t,A2)

subplot(4,4,14)
plot(t,A1)

% Piecewise 
x = [1:1:length(s)]'
y = s

% plot fit
subplot(4,4,3); 
plot(x,y)
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')
title('Piecewise Linear')

% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),Length1);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(4,4,7); 
plot(XI,YI,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')


% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),Length2);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(4,4,11); 
plot(XI,YI,'+-')
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')


% vector of 1-D look-up table "x" points
XI = linspace(0,length(y),Length3);

% obtain vector of 1-D look-up table "y" points
YI = lsq_lut_piecewise( x, y, XI );

% plot fit
subplot(4,4,15); 
plot(XI,YI)
%legend('Traffic data (x,y(x))','LUT points (XI,YI)')

% Adaptive Piecewise
subplot(4,4,4); 
plot(t,s)
title('APCA')

subplot(4,4,8); 
apca(s,Length1,1);
box on


subplot(4,4,12); 
apca(s,Length2,0);
box on

subplot(4,4,16); 
apca(s,Length3,0);
box on





