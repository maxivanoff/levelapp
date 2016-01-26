import numpy as np
import matplotlib.pyplot as plt

def parse_level_outfile(fname):
    R, E = [], []
    with open('%s.8' % fname, 'r') as f:
        for line in f:
            if 'function values with asymptotic' in line:
                continue
            values = map(lambda t: float(t), line.split())
            for i in [0, 2, 4]:
                try:
                    r, e = values[i], values[i+1]
                    R.append(r)
                    E.append(e)
                except IndexError:
                    pass
    npt = len(R)
    vlim = E[-1]
    E = np.array(E)
    E = E - vlim

    levels = {}
    with open('%s.6' % fname, 'r') as f:
        while True:
            line = f.readline()
            if line == '':
                break
            if 'For vibrational level' in line:
                v = int(line.split()[5])
                levels[v] = {}
                line = f.readline()
                line = f.readline()
                while True:
                    line = f.readline()
                    try:
                        values = map(lambda t: float(t), line.split())
                        n = len(values)
                        for i in xrange(n/2):
                            J = values[2*i]
                            level = values[2*i+1]
                            levels[v][J] = level
                    except:
                        break

    minE = np.amin(E)
    E = E - minE
    #print 'Well Depth = ', minE, 'cm-1'

    plt.grid(True)
    xlim = [0.8, 1.4]
    plt.xlim(xlim)
    plt.ylim([0., 5000.])
    plt.plot(R, E, '-', lw=3, color='green')
    for v, Jlevels in levels.items():
        for J, level in Jlevels.items():
            level += -minE
            tmp = [level]*len(xlim)
            plt.plot(xlim, tmp, '-', color='black', lw=1)
    plt.savefig('%s-pes-levels.pdf' % fname)


