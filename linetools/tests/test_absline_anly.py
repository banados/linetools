# Module to run tests on AbsLine analysis

# TEST_UNICODE_LITERALS
from __future__ import print_function, absolute_import, division, unicode_literals

import numpy as np
import os, pdb
import pytest
from astropy import units as u

from linetools.spectralline import AbsLine
from linetools.spectra import io as lsio
from linetools import spectralline
from linetools.lists.linelist import LineList

def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), '../spectra/tests/files')
    return os.path.join(data_dir, filename)


def test_aodm_absline():
    # Init CIV 1548
    abslin = AbsLine(1548.195*u.AA)

    # Set spectrum
    abslin.analy['spec'] = lsio.readspec(data_path('UM184_nF.fits')) # Fumagalli+13 MagE spectrum
    abslin.analy['wvlim'] = [6080.78, 6087.82]*u.AA
    #
    abslin.measure_aodm()
    N, sig_N, flgN = [abslin.attrib[key] for key in ['N','sig_N','flag_N']]

    np.testing.assert_allclose(N.value, 300010067404184.0)
    assert N.unit == 1/u.cm**2
    assert flgN == 1
    # Now velocity limits

    abslin.analy['wvlim'] = np.zeros(2)*u.AA
    abslin.analy['vlim'] = (-150., 150.)*u.km/u.s
    abslin.attrib['z'] = 2.92929
    #
    abslin.measure_aodm()
    N, sig_N, flgN = [abslin.attrib[key] for key in ['N','sig_N','flag_N']]
    np.testing.assert_allclose(N.value, 80369217498895.17)
    return

def test_boxew_absline():
    # Text boxcar EW evaluation
        # Init CIV 1548
    abslin = AbsLine(1548.195*u.AA)

    # Set spectrum
    abslin.analy['spec'] = lsio.readspec(data_path('UM184_nF.fits')) # Fumagalli+13 MagE spectrum
    abslin.analy['wvlim'] = [6080.78, 6087.82]*u.AA
    # Measure EW (not rest-frame)
    abslin.measure_ew()
    ew = abslin.attrib['EW']

    np.testing.assert_allclose(ew.value, 0.9935021012055584)
    assert ew.unit == u.AA

    abslin.measure_restew()
    restew = abslin.attrib['EW']
    np.testing.assert_allclose(restew.value, 0.9935021012055584/(1+abslin.attrib['z']))

def test_gaussew_absline():
    # Text Gaussian EW evaluation
    # Init CIV 1548
    abslin = AbsLine(1548.195*u.AA)

    # Set spectrum
    abslin.analy['spec'] = lsio.readspec(data_path('UM184_nF.fits')) # Fumagalli+13 MagE spectrum
    abslin.analy['wvlim'] = [6080.78, 6087.82]*u.AA
    # Measure EW (not rest-frame)
    abslin.measure_ew(flg=2)
    ew = abslin.attrib['EW']

    np.testing.assert_allclose(ew.value, 1.02,atol=0.01)
    assert ew.unit == u.AA

    abslin.measure_ew(flg=2,initial_guesses=(0.5,6081,1))

def test_measurekin_absline():
    # Test Simple kinematics
    abslin = AbsLine('NiII 1741')

    # Set spectrum
    abslin.analy['spec'] = lsio.readspec(data_path('PH957_f.fits'))
    abslin.analy['vlim'] = [-70., 70.]*u.km/u.s
    abslin.attrib['z'] = 2.307922

    # Measure Kin
    abslin.measure_kin()
    np.testing.assert_allclose(abslin.attrib['kin']['Dv'].value, 75.)
    np.testing.assert_allclose(abslin.attrib['kin']['fedg'], 0.20005782376000183)


def test_ismatch():
    # Test Simple kinematics
    abslin1 = AbsLine('NiII 1741')
    abslin1.attrib['z'] = 1.
    abslin2 = AbsLine('NiII 1741')
    abslin2.attrib['z'] = 1.
    # Run
    answer = abslin1.ismatch(abslin2)
    assert answer == True
    # Tuple too
    answer2 = abslin1.ismatch((1., abslin1.wrest))
    assert answer2 == True

def test_repr():
    abslin = AbsLine('NiII 1741')
    print(abslin)

def test_manyabslines():
    lines = [1215.670*u.AA, 1025.7222*u.AA, 972.5367*u.AA]*2
    llist = LineList('HI')
    alines = spectralline.many_abslines(lines, llist)


