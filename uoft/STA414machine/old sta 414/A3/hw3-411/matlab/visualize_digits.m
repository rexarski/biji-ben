function visualize_digits(data_matrix)
% Visualize digit images for examples in the data matrix.
%
% data_matrix should be a n_dimensions x n_examples matrix, each column is one
% example.
% 
% This is intended only to visualize a small number (say < 10) of digits.
%
figure;

n_examples = size(data_matrix, 2);
for i = 1 : n_examples
    subplot(1, n_examples, i);
    imshow(reshape(data_matrix(:,i), [16,16]), []);
end
