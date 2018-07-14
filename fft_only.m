fid = fopen('Window2.txt','r')
s = fscanf(fid, '%d')
fclose(fid)
fid = fopen('Window2.txt','r')
s = fscanf(fid, '%d')
fclose(fid)
t = 1:2:length(s);
subplot(211);plot(s)
xlabel('Time (s)')
ylabel('KB')


Fs = 1
T = 1
L = 221
t = (0:L-1)*T

NFFT = 2^nextpow2(L);
Y = fft(y,NFFT)/L;
f = Fs/2*linspace(0,1,NFFT/2+1);

subplot(212); 
plot(f,2*abs(Y(1:NFFT/2+1))) 
title('Single-Sided Amplitude Spectrum of y(t)')
xlabel('Frequency (Hz)')
ylabel('|Y(f)|')
