function plot_ICM(ICM, roi_names, sub_id, fig_path, cond_type)
    figureHandle = figure('Visible', 'off');
    imagesc(ICM);  % Plot the matrix
    colormap(hot);
    set(gca, 'CLim', [0 1]);
    colorbar;
    set(gca, 'XTick', 1:length(roi_names));  % Ensure XTicks are set for labels
    set(gca, 'XTickLabel', roi_names);
    set(gca, 'YTick', 1:length(roi_names));  % Ensure YTicks are set for labels
    set(gca, 'YTickLabel', roi_names);
    title(['Informational Connectivity Matrix: ', num2str(sub_id)]);

    % Add text annotations to each cell
    [numRows, numCols] = size(ICM);
    for row = 1:numRows
        for col = 1:numCols
            text(col, row, sprintf('%.2f', ICM(row, col)), ...
                 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
                 'Color', 'white', 'FontSize', 8);
        end
    end
    
    % Save the figure as PNG with dynamic filename
    filename = sprintf('ICM_%s_subject%s.png', cond_type, num2str(sub_id));
    saveas(figureHandle, fullfile(fig_path, filename));
end