function [x, rec, resid] = saf_massbalance_I2(compFile, alloyFile, outFile)
% SAF_MASSBALANCE_I2  Independent MATLAB/Octave mass balance (data reconciliation).
% Builds the 7 balance equations (Al2O3, MgO, CaO, SiO2, Cr, Fe, C) from the composition
% table and solves the weighted non-negative least-squares problem with LSQNONNEG.
% Unknowns x = [ore, reductant(dry), quartz, limestone, slag]  (kg per tonne alloy).
% Runs in MATLAB and GNU Octave. No Python code is used.
  if nargin < 1, compFile  = fullfile('model','inputs','octave_massbalance_compositions.csv'); end
  if nargin < 2, alloyFile = fullfile('model','inputs','octave_massbalance_alloy.csv'); end
  if nargin < 3, outFile   = fullfile('results','model','I2_octave_massbalance.csv'); end
  C = csvread(compFile, 1, 0);     % rows: ore, reductant, quartz, limestone, slag
  a = csvread(alloyFile, 1, 0) * 1000;   % kg/t: Cr Fe Si C
  % columns of C: 1 stream, 2 Cr2O3, 3 FeO, 4 Fe2O3, 5 Al2O3, 6 MgO, 7 CaO, 8 SiO2, 9 FC (slag: C)
  mCr = 51.996; mFe = 55.845; mSi = 28.086; mC = 12.011; mO = 15.999;
  fCr  = 2*mCr/(2*mCr+3*mO);  fFeO = mFe/(mFe+mO);  fFe2 = 2*mFe/(2*mFe+3*mO);  fSi = mSi/(mSi+2*mO);
  ore = C(1,:); red = C(2,:); qz = C(3,:); lm = C(4,:); sl = C(5,:);
  SiO2red = a(3)/fSi;
  Orem = a(1)*3*mO/(2*mCr) + a(2)*mO/mFe + a(3)*2*mO/mSi;
  Cneed = a(4) + Orem*mC/mO;
  A = [ ore(5) red(5) qz(5) lm(5) -sl(5);
        ore(6) red(6) qz(6) lm(6) -sl(6);
        ore(7) red(7) qz(7) lm(7) -sl(7);
        ore(8) red(8) qz(8) lm(8) -sl(8);
        ore(2)*fCr 0 0 0 -sl(2)*fCr;
        ore(3)*fFeO red(4)*fFe2 qz(4)*fFe2 lm(4)*fFe2 -sl(3)*fFeO;
        0 red(9) 0 0 -sl(9) ];
  b = [0; 0; 0; SiO2red; a(1); a(2); Cneed];
  sc = max(max(abs(A), [], 2)*1000, abs(b)); sc(sc == 0) = 1;
  x = lsqnonneg(A ./ repmat(sc, 1, 5), b ./ sc);
  resid = A*x - b;
  rec = a(1) / (x(1)*ore(2)*fCr);
  fid = fopen(outFile, 'w');
  fprintf(fid, 'm_ore,m_red,m_quartz,m_lime,m_slag,Cr_recovery\n');
  fprintf(fid, '%.15g,%.15g,%.15g,%.15g,%.15g,%.15g\n', x(1), x(2), x(3), x(4), x(5), rec);
  fclose(fid);
end
