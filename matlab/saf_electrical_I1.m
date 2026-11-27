function T = saf_electrical_I1(inFile, outFile)
% SAF_ELECTRICAL_I1  Independent re-implementation of the Increment-1 electrical and
% production equations (no Python code is used). Runs in MATLAB and GNU Octave.
%
%   T = saf_electrical_I1('model/inputs/octave_scenarios.csv', 'results/model/I1_octave_numeric.csv')
%
% Input columns : idx, P_mean (-1 = full rating), PF, LF, SEC, S_rated, C3, D_m, V_HV_kV
% Output columns: idx, P_mean, P_on, S_on, Q_on, loading_%, I_primary_A, I_e_kA, V_LL_V,
%                 R_mohm, X_mohm, J_A_cm2, E_MWh_d, production_t_d
% Equations (balanced three-phase, star equivalent per electrode):
%   P_mean = S*PF*LF (full rating) ; P_on = P_mean/LF ; S_on = P_on/PF ; Q = S_on*sin(acos PF)
%   I_e = C3*P_on^(2/3) [Westly, estimate] ; V_LL = S_on/(sqrt(3) I_e) ; R = P_on/(3 I_e^2)
%   X = R*tan(acos PF) ; J = I_e/(pi D^2/4) ; E = 24 P_mean ; M = E/SEC
  if nargin < 1, inFile  = fullfile('model','inputs','octave_scenarios.csv'); end
  if nargin < 2, outFile = fullfile('results','model','I1_octave_numeric.csv'); end
  A = csvread(inFile, 1, 0);
  n = size(A, 1);
  T = zeros(n, 14);
  for k = 1:n
    idx = A(k,1); Pm = A(k,2); PF = A(k,3); LF = A(k,4); SEC = A(k,5);
    S = A(k,6); C3 = A(k,7); D = A(k,8); Vhv = A(k,9);
    if Pm < 0, Pm = S*PF*LF; end
    Pon  = Pm/LF;
    Son  = Pon/PF;
    Qon  = Son*sin(acos(PF));
    Ipri = Son*1e6/(sqrt(3)*Vhv*1e3);
    Ie   = C3*Pon^(2/3);                         % kA
    Vll  = Son*1e6/(sqrt(3)*Ie*1e3);            % V
    R    = Pon*1e6/(3*(Ie*1e3)^2);              % ohm
    X    = R*tan(acos(PF));
    J    = Ie*1e3/(pi/4*(D*100)^2);             % A/cm2
    E    = 24*Pm;
    M    = E/SEC;
    T(k,:) = [idx Pm Pon Son Qon 100*Son/S Ipri Ie Vll R*1e3 X*1e3 J E M];
  end
  fid = fopen(outFile, 'w');
  fprintf(fid, 'idx,P_mean_MW,P_on_MW,S_on_MVA,Q_on_Mvar,loading_on_pct,I_primary_A_at_HV,I_electrode_kA_est,V_secondary_LL_V_est,R_phase_mohm_est,X_phase_mohm_est,J_A_cm2_est,E_daily_MWh,production_tpd\n');
  for k = 1:n
    fprintf(fid, '%d', T(k,1)); fprintf(fid, ',%.15g', T(k,2:end)); fprintf(fid, '\n');
  end
  fclose(fid);
end
