function stouffer_pvalues = stouffer_method(pvalues_all)
    [~, numRows, numCols] = size(pvalues_all);

    % Initialize matrix to store group-level p-values
    stouffer_pvalues = zeros(numRows, numCols);

    % Loop through each element in the matrices
    for row = 1:numRows
        for col = 1:numCols
            % Extract p-values for the current element across all subjects
            pvals = squeeze(pvalues_all(:, row, col));

            % Stouffer's Z-score method
            z_scores = norminv(1 - pvals);
            mean_z = mean(z_scores);
            stouffer_pvalues(row, col) = 1 - normcdf(mean_z);
        end
    end
end