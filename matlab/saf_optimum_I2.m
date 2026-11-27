function T = saf_optimum_I2()
% SAF_OPTIMUM_I2  Closed-form optimum hot-charge temperature for 450 t/d (independent check).
% T* = Tref + 100*(SEC0 - 24*S*PF*LF/450)/s  at PF* = 0.95 (upper bound), LF* = LF_max.
  S = 65; SEC0 = 3.5; s = 0.07; LFmax = [0.95 0.96 0.965 0.972 0.975 0.98];
  T = [ 0 + 100*(SEC0 - 24*S*0.95*LFmax/450)/s ; 25 + 100*(SEC0 - 24*S*0.95*LFmax/450)/s ];
  fid = fopen(fullfile('results','model','I2_octave_optimum.csv'), 'w');
  fprintf(fid, 'LF_max,T_ref0,T_ref25\n');
  for k = 1:numel(LFmax), fprintf(fid, '%.6g,%.15g,%.15g\n', LFmax(k), T(1,k), T(2,k)); end
  fclose(fid);
end
