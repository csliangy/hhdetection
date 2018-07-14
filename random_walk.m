function data = random_walk(length_of_ts,number_of_ts)

% Creates some test data.

data = [];


for i = 1 : number_of_ts
    
    x = 0; 
    
    for j = 2 : length_of_ts
       
        x(j) = x(j-1) + randn;
  
    end;
      
    data = [data  x'];

end;
