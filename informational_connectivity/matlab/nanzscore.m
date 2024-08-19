function z = nanzscore(X)
    % Get logical indices of non-zero entries
    non_zero_indices = X ~= 0;
    
    % Calculate means and standard deviations excluding zeros, column-wise
    mean_non_zero = sum(X .* non_zero_indices, 1) ./ sum(non_zero_indices, 1);
    std_non_zero = sqrt(sum((X - mean_non_zero) .^ 2 .* non_zero_indices, 1) ./ sum(non_zero_indices, 1));
    
    % Initialise z matrix
    z = zeros(size(X));
    
    % Expand mean and std to match the size of X for broadcasting
    mean_expanded = repmat(mean_non_zero, size(X, 1), 1);
    std_expanded = repmat(std_non_zero, size(X, 1), 1);
    
    % Calculate z-scores only for non-zero elements
    z(non_zero_indices) = (X(non_zero_indices) - mean_expanded(non_zero_indices)) ./ std_expanded(non_zero_indices);
end