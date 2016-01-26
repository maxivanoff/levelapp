from django.utils.encoding import smart_str
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SubmitJobForm
import os
import uuid
import numpy as np
import parse

def handle_pes_file(f, m1, m2, i1, i2, findex):
    E = []
    R = []
    for line in f:
        if line.startswith('Coordinate'):
            continue
        r, e = map(lambda t: float(t), line.split(','))
        R.append(r)
        E.append(e)
    npt = len(R)
    vlim = E[-1]
    E = np.array(E) - vlim
    E = E*627.503
    s = '%i %i  %i %i  0  1\n\
    Carbon Monoxide \n\
    0.001  0.6  15.   0.0001                          %% RH RMIN RMAX EPS \n\
    %i  -1  0  0.0D0                             %% NTP LPPOT IOMEG  VLIM \n\
    8 0  2  1  0.D5                                   %% NUSE IR2 ILR NCN CNN \n\
    1.D0 349.75D0 0.d0                                %% RFACT EFACT VSHIFT \n' % (i1, m1, i2, m2, npt)
    for i in xrange(npt):
        rs = '%.2f' % (R[i])
        rs = rs.ljust(5, '0')

        es = '%.3f' % (E[i])
        es = es.ljust(6, '0')
        s += '%s     %s  ' % (rs, es)
        if (i+1) % 5 == 0: 
            s += '\n'
    s += '\n-1  1  0  0  23 1  -1 0                              % NLEV1 AUTO1 LCDC LXPCT NJM JDJR IWR LPRWF \n\
    0 0'
    fname = 'data/%s' % findex
    with open(fname, 'w') as lvfile:
        lvfile.write(s)
    os.system('./run %s' % fname)
    parse.parse_level_outfile(fname)


# Create your views here.
def download_levels_pdf(request, findex):
    filename = 'data/%s-pes-levels.pdf' % findex
    wrapper = FileWrapper( open( filename, "r" ) )
    response = HttpResponse(wrapper, content_type='level/download_levels_pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(filename)
    response['Content-Length'] = os.path.getsize(filename)
    return response

def index(request):
    if request.method == 'POST':
        form = SubmitJobForm(request.POST, request.FILES)
        if form.is_valid():
            # do stuff
            os.system('touch file.txt')
            molecule_name = request.POST['name']
            m1 = int(request.POST['m1'])
            m2 = int(request.POST['m2'])
            i1 = int(request.POST['i1'])
            i2 = int(request.POST['i2'])
            findex = str(uuid.uuid4())
            handle_pes_file(request.FILES['inputfile'], m1, m2, i1, i2, findex)
            return render(request, 'level/results.html', {'findex':findex})
        else:
            print form.errors
    else:
        form = SubmitJobForm()

    return render(request, 'level/index.html', {'form':form})
