function [out1_x out2_x out1_y out2_y] = split(trainx,trainy, i )
out2_x = trainx;
out1_x = trainx(((i-1)*25+1):(i*25),:);
out2_x(((i-1)*25+1):(i*25),:) = [];
out2_y = trainy;
out1_y = trainy(((i-1)*25+1):(i*25));
out2_y(((i-1)*25+1):(i*25)) = [];
end

