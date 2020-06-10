function [inputs_train, inputs_valid, inputs_test, target_train, target_valid, target_test] = load_data()
load digits;
inputs_train = [train2 train3];
inputs_valid = [valid2 valid3];
inputs_test = [test2 test3];
target_train = [zeros(size(train2, 2), 1) ; ones(size(train2, 2), 1)]';
target_valid = [zeros(size(valid2, 2), 1) ; ones(size(valid2, 2), 1)]';
target_test = [zeros(size(test2, 2), 1) ; ones(size(test2, 2), 1)]';

return
end
