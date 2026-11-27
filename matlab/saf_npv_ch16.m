function [npv, cf, irr] = saf_npv_ch16(inFile, outFile)
% SAF_NPV_CH16  Independent MATLAB/Octave check of the Chapter 16 base-case NPV (Ch. 15 method).
  if nargin < 1, inFile  = fullfile('model','inputs','octave_npv.csv'); end
  if nargin < 2, outFile = fullfile('results','model','CH16_octave_npv.csv'); end
  v = csvread(inFile, 1, 0);
  prod=v(1); prod0=v(2); Pc=v(3); Pa=v(4); price=v(5); fx=v(6); elec=v(7); capc=v(8); cont=v(9); shut=v(10);
  orer=v(11); orep=v(12); redr=v(13); redp=v(14); flr=v(15); flp=v(16); pk=v(17); pp=v(18); tax=v(19); r=v(20); n=v(21);
  dt = (prod - prod0)*365;
  rev = dt*price*fx/1e6;
  capex = capc*(1+cont) + shut;
  opex = (Pc-Pa)*8760*elec/1e3 + dt*(orer*orep + redr*redp + flr*flp + pk/1000*pp)/1e6 + 0.015*capc + 2;
  profit = rev - opex;
  cf = profit - tax*(profit - capex/n);
  npv = cf*(1-(1+r)^-n)/r - capex;
  f = @(i) cf*(1-(1+i).^-n)./i - capex;
  irr = fzero(f, [1e-6 10]);
  fid = fopen(outFile,'w'); fprintf(fid,'npv,cf,irr\n%.15g,%.15g,%.15g\n', npv, cf, irr); fclose(fid);
end
