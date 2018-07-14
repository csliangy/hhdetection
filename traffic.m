K = 5


fid = fopen('traffic4_Step1.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:1:length(cell2mat(y_value))-1
plot(x, cell2mat(y_value))
hold on


fid = fopen('traffic4_Step2.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)
hold on


line([0 (length(cell2mat(y_value))-1)*K], [100000 100000],'Color','c','LineWidth',3)
hold on

figure()
fid = fopen('traffic4_Step3.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window1.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window2.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window3.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window4.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window5.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window6.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window7.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)

figure()
fid = fopen('Window8.txt','r')
y_value = textscan(fid, '%d')
fclose(fid)
celldisp(y_value)
x = 0:K:(length(cell2mat(y_value))-1)*K

plot(x, cell2mat(y_value),'--','Color',[1,0,0],'LineWidth',2)