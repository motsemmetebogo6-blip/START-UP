% saf_dashboard.m  MATLAB / GNU Octave dashboard of the SAF uprate model results.
% Reads the numeric files in matlab/dashboard_data (written by model/export_dashboard_data.py) and draws six panels
% and a KPI strip. Run:  saf_dashboard('dashboard_matlab.png')   (the file name is optional).
function saf_dashboard(outfile)
  if nargin < 1, outfile = 'dashboard_matlab.png'; end
  d = [fileparts(mfilename('fullpath')) filesep 'dashboard_data' filesep];
  nm = @(f) strtrim(strsplit(strtrim(fileread([d f '_names.txt'])), "\n"));
  scen = csvread([d 'scen.csv']); sn = nm('scen');
  mb = csvread([d 'mb.csv']); mn = nm('mb');
  opt = csvread([d 'opt.csv']); tor = csvread([d 'tornado.csv']); tn = nm('tornado');
  ax = csvread([d 'axial.csv']); kpi = csvread([d 'kpi.csv']);
  if strcmp(outfile, 'dry')
    fprintf('data check: %d scenarios, %d mass-balance streams, %d optimisation points, %d tornado rows, %d axial points, KPI %s\n', size(scen,1), size(mb,1), size(opt,1), size(tor,1), size(ax,1), mat2str(kpi, 6));
    return
  end
  fig = figure('Visible', 'off', 'Position', [50 50 1500 900], 'Color', 'w');
  blue = [0 0.34 0.59]; orange = [0.85 0.33 0.1]; grey = [0.55 0.55 0.55];

  subplot(2,3,1); b = bar(scen(:,6)); set(b, 'FaceColor', blue); hold on; plot([0 9], [450 450], 'r--', 'LineWidth', 1.4);
  set(gca, 'XTick', 1:numel(sn), 'XTickLabel', sn, 'FontSize', 8); ylim([350 480]); ylabel('t/d'); title('Production by scenario (target 450 t/d)'); grid on;

  subplot(2,3,2); b = bar(scen(:,3)); set(b, 'FaceColor', orange); hold on; plot([0 9], [100 100], 'k--');
  set(gca, 'XTick', 1:numel(sn), 'XTickLabel', sn, 'FontSize', 8); ylim([85 105]); ylabel('% of 65 MVA'); title('On-load transformer loading'); grid on;

  subplot(2,3,3); isin = mb(:,2) == 1; vals = mb(:,1);
  barh(1:numel(vals), vals, 'FaceColor', grey); hold on; barh(find(isin), vals(isin), 'FaceColor', blue);
  set(gca, 'YTick', 1:numel(mn), 'YTickLabel', mn, 'FontSize', 8, 'YDir', 'reverse'); xlabel('kg per t alloy'); title('Mass balance (blue = inputs)'); grid on;

  subplot(2,3,4); plot(opt(:,1), opt(:,2), 'o-', 'Color', blue, 'LineWidth', 1.6); hold on; plot([0.94 0.99], [500 500], 'r--');
  xlabel('Achievable load factor'); ylabel('Minimum preheat (C)'); title('Optimisation: least preheat for 450 t/d'); grid on;

  subplot(2,3,5); n = size(tor,1); base = kpi(3); [~, ord] = sort(abs(tor(:,2)-tor(:,1))); 
  for k = 1:n
    i = ord(k); lo = min(tor(i,:)); hi = max(tor(i,:));
    barh(k, hi-base, 'BaseValue', base, 'FaceColor', blue); hold on; barh(k, lo-base, 'BaseValue', base, 'FaceColor', grey);
  end
  set(gca, 'YTick', 1:n, 'YTickLabel', tn(ord), 'FontSize', 7); xlabel('NPV (R million)'); title('Tornado: effect on NPV'); grid on;

  subplot(2,3,6); m = ax(:,2) > 0; plot(ax(m,2), ax(m,1), 'r-', 'LineWidth', 1.5); hold on; m2 = ax(:,3) > 0; plot(ax(m2,3), ax(m2,1), 'b-', 'LineWidth', 1.5);
  xlabel('Temperature (C)'); ylabel('z (m)'); title('Electrode axial temperature (assumed inputs)'); legend('axis', 'surface', 'Location', 'east'); grid on;

  annotation('textbox', [0.02 0.945 0.96 0.05], 'String', sprintf('SAF uprate dashboard   |   C1 production %.1f t/d   |   Cr recovery %.1f %%   |   NPV R%.0f M   |   IRR %.1f %%   |   electrode Tmax %.0f C (assumed inputs)', kpi(1), kpi(2), kpi(3), kpi(4), kpi(5)), 'FontSize', 11, 'FontWeight', 'bold', 'EdgeColor', 'none', 'HorizontalAlignment', 'center');
  print(fig, outfile, '-dpng', '-r110');
  fprintf('dashboard written to %s\n', outfile);
end
