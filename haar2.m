fid = fopen('Window2.txt','r')
s = fscanf(fid, '%d')
ls = length(s);
fclose(fid)
t = 1:2:length(s);

figure(1)
subplot(711);plot(s)
legend('signal')
[ca1,cd1]=dwt(s,'haar');
subplot(712);plot(1:ls,s,'k',1:2:ls,ca1,'b');
legend('signal','A^1')
ylabel('1-level Haar DWT')
%subplot(7,1,3)
%plot(1:ls,s,'k',1:2:ls,cd1,'b')
%legend('signal','D^1')
%ylabel('1-level Haar DWT')

[C,L] = wavedec(s,1,'db1');
CA1 = wrcoef('a',C,L,'db1',1);
CD1 = wrcoef('d',C,L,'db1',1);


 
[C,L] = wavedec(s,3,'db1');
A1 = wrcoef('a',C,L,'db1',1);
A2 = wrcoef('a',C,L,'db1',2);
A3 = wrcoef('a',C,L,'db1',3);
D1 = wrcoef('d',C,L,'db1',1);
D2 = wrcoef('d',C,L,'db1',2);
D3 = wrcoef('d',C,L,'db1',3) ;
% Plot signal and the 3rd level averaged signal

subplot(7,1,3)
plot(1:ls,s,'k',1:ls,A1,'b')
legend('signal','A^1')
ylabel('3-level Haar DWT')

subplot(7,1,4)
plot(1:ls,s,'k',1:ls,A2,'b')
legend('signal','A^2')
ylabel('3-level Haar DWT')

subplot(7,1,5)
plot(1:ls,s,'k',1:ls,A3,'b')
legend('signal','A^3')
ylabel('3-level Haar DWT')

subplot(7,1,6)
plot(1:ls,s,'k',1:ls,A2,'b')
legend('signal','D^2')
ylabel('3-level Haar DWT')

subplot(7,1,7)
plot(1:ls,s,'k',1:ls,D2,'b')
legend('signal','D^2')
ylabel('3-level Haar DWT')

figure(2)
subplot(5,1,1)
plot(1:ls,s,'k')
legend('signal')

subplot(5,1,2)
plot(1:ls,CA1+CD1,'b')
legend('A^1+D^1')
ylabel('1-level Haar DWT')

subplot(5,1,3)
plot(1:ls,A1+D1,'b')
legend('A^1+D^1')
ylabel('3-level Haar DWT')

subplot(5,1,4)
plot(1:ls,A2+D2,'b')
legend('A^2+D^2')
ylabel('3-level Haar DWT')

subplot(5,1,5)
plot(1:ls,A3+D3,'b')
legend('A^3+D^3')
ylabel('3-level Haar DWT')


