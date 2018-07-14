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
ylabel('Amplitude');
title('Traffic Time Series Data')

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
xlabel('Time (s)');
ylabel('Amplitude');
title('Inverse FFT Sequence - Frequency Less than 5'); 

freq_n = L/16
fft_data_v = fft(s);
s_fft_data_v = zeros(1,length(s));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(4,4,9)
plot(0:N-1,s_data_v);
xlabel('Time (s)');
ylabel('Amplitude');
title('Inverse FFT Sequence - Frequency Less than 20'); 


freq_n = L/4
fft_data_v = fft(s);
s_fft_data_v = zeros(1,length(s));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(4,4,13)
plot(0:N-1,s_data_v);
xlabel('Time (s)');
ylabel('Amplitude');
title('Inverse FFT Sequence - Frequency Less than 50'); 

% DWT - HAAR
[C,L] = wavedec(s, 6, 'db1');
A1 = wrcoef('a',C,L,'db1',2); %1/4
A2 = wrcoef('a',C,L,'db1',4); %1/16
A3 = wrcoef('a',C,L,'db1',3); %1/64

subplot(4,4,2)
plot(t,s);

subplot(4,4,6)
plot(t,A3)

subplot(4,4,10)
plot(t,A2)

subplot(4,4,14)
plot(t,A1)

% Piecewise 
subplot(4,4,3)
plot(t,s);

subplot(4,4,7);
y = hpfilter(s)
plot(y)


