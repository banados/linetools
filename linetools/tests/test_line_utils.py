# Module to run tests on initializing AbsLine

# TEST_UNICODE_LITERALS
from __future__ import print_function, absolute_import, division, unicode_literals

import numpy as np
import os, pdb
from astropy import units as u

from linetools.spectralline import AbsLine
from linetools import line_utils as ltlu


def test_parse_abslines():
    # Init AbsLines
    abslines = [AbsLine(1215.6700*u.AA), AbsLine('CII 1334')]
    # wrest
    wrest_values = ltlu.parse_speclines(abslines, 'wrest')
    np.testing.assert_allclose(wrest_values[1], 1334.5323*u.AA)
    # EW
    EW_values = ltlu.parse_speclines(abslines, 'EW')
    np.testing.assert_allclose(EW_values[1].value, 0.)
    # data
    A_values = ltlu.parse_speclines(abslines, 'A')
    np.testing.assert_allclose(A_values[0].value, 626500000.0)

def test_transtabl():
    # Init AbsLines
    abslines = [AbsLine(1215.6700*u.AA), AbsLine('CII 1334')]
    #
    tbl = ltlu.transtable_from_speclines(abslines)
    assert len(tbl) == 2
    assert 'logN' in tbl.keys()

def test_coincident_line():
    # Init AbsLines
    line1 = AbsLine(1215.6700*u.AA)
    line2 = AbsLine('CII 1334')
    # expected errors
    try:
        answer = line1.coincident_line(line2)
    except ValueError:
        pass
    line1.analy['wvlim'] = (1500,1510)*u.AA
    try:
        answer = line1.coincident_line(line2)
    except ValueError:
        pass
    line2.analy['wvlim'] = (1509,1520)*u.AA

    # expected overlap
    assert line1.coincident_line(line2)
    assert line2.coincident_line(line1)
    # not expected overlap
    line2.analy['wvlim'] = (1510.1,1520)*u.AA
    assert not line1.coincident_line(line2)
    assert not line2.coincident_line(line1)