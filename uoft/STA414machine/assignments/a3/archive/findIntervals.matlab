function [test_x, test_y, train_y, train_x] = findIntervals(index, train1x, train1y)
% calutes the right intervlas for test_x, test_y, train_y, train_x given the
% index
end_num = 25*index;
if index == 1
    start_num = 1;
else
    start_num = (index-1)*25+1;
end
test_x = train1x(start_num:end_num,:);
test_y = train1y(start_num:end_num);
if index == 1
    train_y = train1y(end_num+1:end);
    train_x = train1x(end_num+1:end,:);
elseif index == 10
    train_x = train1x(1:start_num-1,:);
    train_y = train1y(1:start_num-1);
else
    x_1 = train1x(1:start_num-1,:);
    x_2 = train1x(end_num+1:end,:);
    train_x = [x_1; x_2];
    y_1 = train1y(1:start_num-1);
    y_2 = train1y(end_num+1:end);
    train_y = [y_1; y_2];
end
end