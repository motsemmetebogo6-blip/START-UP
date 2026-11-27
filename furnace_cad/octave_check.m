% octave_check.m: independent assembly and solution of the single-electrode cell, reading only the exported arrays.
% Compares with the Python solution (octave_io/T_python.csv). Works in MATLAB and GNU Octave.
function octave_check()
  d = 'octave_io/';
  re = csvread([d 're.csv'])(:)'; ze = csvread([d 'ze.csv'])(:)';
  act = csvread([d 'active.csv']) > 0.5; kc = csvread([d 'k.csv']); qv = csvread([d 'q.csv']);
  dm = csvread([d 'dmask.csv']) > 0.5; dv = csvread([d 'dval.csv']);
  names = {'w','e','s','n'};
  for f = 1:4
    h.(names{f}) = csvread([d 'h_' names{f} '.csv']); Te.(names{f}) = csvread([d 'T_' names{f} '.csv']);
  end
  Tpy = csvread([d 'T_python.csv']);
  [nz, nr] = size(act); dr = diff(re); dz = diff(ze);
  idx = zeros(nz, nr); idx(act) = 1:nnz(act); n = nnz(act);
  I = []; J = []; V = []; b = zeros(n,1); dg = zeros(n,1);
  for iz = 1:nz
    for ir = 1:nr
      if ~act(iz,ir), continue; end
      i = idx(iz,ir); vol = pi*(re(ir+1)^2 - re(ir)^2)*dz(iz); b(i) += qv(iz,ir)*vol; k0 = kc(iz,ir);
      nb = [ 0 1 re(ir+1) dr(ir)/2 2*pi*re(ir+1)*dz(iz) 2;      % east
             0 -1 re(ir)   dr(ir)/2 2*pi*re(ir)*dz(iz)   1;     % west
            -1 0 0 dz(iz)/2 pi*(re(ir+1)^2-re(ir)^2) 3;         % south
             1 0 0 dz(iz)/2 pi*(re(ir+1)^2-re(ir)^2) 4];        % north
      for m = 1:4
        jz = iz + nb(m,1); jr = ir + nb(m,2); dd = nb(m,4); area = nb(m,5); fn = names{nb(m,6)};
        if jz>=1 && jz<=nz && jr>=1 && jr<=nr && act(jz,jr)
          if dm(jz,jr) && ~dm(iz,ir)
            g = area/(dd/k0);
          else
            if nb(m,2) ~= 0, d2 = dr(jr)/2; else, d2 = dz(jz)/2; end
            g = area/(dd/k0 + d2/kc(jz,jr));
          end
          I(end+1) = i; J(end+1) = idx(jz,jr); V(end+1) = -g; dg(i) += g;
        else
          hh = h.(fn)(iz,ir);
          if hh > 0 && area > 0
            g = area/(dd/k0 + 1/hh); dg(i) += g; b(i) += g*Te.(fn)(iz,ir);
          end
        end
      end
    end
  end
  A = sparse(I, J, V, n, n) + sparse(1:n, 1:n, dg, n, n);
  isd = dm(act); vals = dv(act);
  for i = find(isd)'
    A(i,:) = 0; A(i,i) = 1; b(i) = vals(i);
  end
  x = A\b;
  T = -ones(nz,nr); T(act) = x;
  mask = Tpy > -0.5;
  dmax = max(abs(T(mask) - Tpy(mask)));
  fprintf('cells %d, max |T_octave - T_python| = %.3e C, max T = %.2f C\n', n, dmax, max(T(mask)));
  fid = fopen('octave_io/octave_result.txt','w'); fprintf(fid,'%d,%.6e,%.6f\n', n, dmax, max(T(mask))); fclose(fid);
end
