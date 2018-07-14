fid = fopen('Window2.txt','r')
s = fscanf(fid, '%d')
fclose(fid)
t = 1:2:length(s);
subplot(511);plot(s)
[ca1,cd1]=dwt(s,'haar');
subplot(512);plot(t, ca1)
ylabel('haar(ca1)');
subplot(513);plot(t, cd1);
ylabel('haar(cd1)');
%[lo_d,hi_d]=wfilters('haar','d');
%[ca2,cd2]=dwt(s,lo_d,hi_d);
%subplot(514);plot(t, ca2)
%ylabel('haar(ca2)');
%subplot(5,1,5);plot(t, cd2)
%ylabel('haar(cd2)');

N=length(s);
x=s

t=0:N-1;
subplot(611)
stem(t,x);
xlabel('Time (s)');
ylabel('Amplitude');
title('Input sequence')

subplot(612); 
stem(0:N-1,abs(fft(x)));  
xlabel('Frequency');
ylabel('|X(k)|');
title('Magnitude Response'); 

subplot(613); 
stem(0:N-1,angle(fft(x)));
xlabel('Frequency');
ylabel('Phase');
title('Phase Response'); 

freq_n = 5
fft_data_v = fft(x);
s_fft_data_v = zeros(1,length(x));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(614); 
stem(0:N-1,s_data_v);
xlabel('Time (s)');
ylabel('Amplitude');
title('Inverse FFT Sequence - Frequency Less than 5'); 

freq_n = 20
fft_data_v = fft(x);
s_fft_data_v = zeros(1,length(x));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(615); 
stem(0:N-1,s_data_v);
xlabel('Time (s)');
ylabel('Amplitude');
title('Inverse FFT Sequence - Frequency Less than 20'); 


freq_n = 50
fft_data_v = fft(x);
s_fft_data_v = zeros(1,length(x));
s_fft_data_v(1:freq_n) = fft_data_v(1:freq_n);
s_fft_data_v(end-freq_n:end) = fft_data_v(end-freq_n:end);
s_data_v = real(ifft(s_fft_data_v));

subplot(616); 
stem(0:N-1,s_data_v);
xlabel('Time (s)');
ylabel('Amplitude');
title('Inverse FFT Sequence - Frequency Less than 50'); 


