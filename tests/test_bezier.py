import os

import pathins.bezier
import pytest
from fontTools.ttLib import TTFont

TESTFONT_PATH_1 = os.path.join(
    "tests", "testfiles", "fonts", "NotoSans-Regular.subset1.ttf"
)


def test_quadratic_path_no_contours_default():
    tt = TTFont(TESTFONT_PATH_1)
    glyf_table = tt["glyf"]
    test_glyph = glyf_table[".notdef"]
    assert pathins.bezier.quadratic_path(test_glyph, glyf_table) == []


def test_quadratic_path_no_contours_include_implied():
    tt = TTFont(TESTFONT_PATH_1)
    glyf_table = tt["glyf"]
    test_glyph = glyf_table[".notdef"]
    assert (
        pathins.bezier.quadratic_path(test_glyph, glyf_table, include_implied=True) == []
    )


def test_quadratic_path_simple_glyph_default():
    tt = TTFont(TESTFONT_PATH_1)
    glyf_table = tt["glyf"]
    test_glyph = glyf_table["comma"]
    qpath = pathins.bezier.quadratic_path(test_glyph, glyf_table)
    first = qpath[0]
    second = qpath[1]
    third = qpath[2]
    fourth = qpath[3]
    fifth = qpath[4]
    sixth = qpath[5]
    seventh = qpath[6]
    eighth = qpath[7]
    ninth = qpath[8]

    assert len(qpath) == 9

    for point in qpath:
        assert point.implied is False

    assert first.x == 185
    assert first.y == 116
    assert first.oncurve is True
    assert first.startpoint is True
    assert first.endpoint is False
    assert first.coord_next == second
    assert first.coord_previous is None

    assert second.x == 192
    assert second.y == 105
    assert second.oncurve is True
    assert second.startpoint is False
    assert second.endpoint is False
    assert second.coord_next == third
    assert second.coord_previous == first

    assert third.x == 178
    assert third.y == 52
    assert third.oncurve is False
    assert third.startpoint is False
    assert third.endpoint is False
    assert third.coord_next == fourth
    assert third.coord_previous == second

    assert fourth.x == 130
    assert fourth.y == -75
    assert fourth.oncurve is False
    assert fourth.startpoint is False
    assert fourth.endpoint is False
    assert fourth.coord_next == fifth
    assert fourth.coord_previous == third

    assert fifth.x == 106
    assert fifth.y == -129
    assert fifth.oncurve is True
    assert fifth.startpoint is False
    assert fifth.endpoint is False
    assert fifth.coord_next == sixth
    assert fifth.coord_previous == fourth

    assert sixth.x == 41
    assert sixth.y == -129
    assert sixth.oncurve is True
    assert sixth.startpoint is False
    assert sixth.endpoint is False
    assert sixth.coord_next == seventh
    assert sixth.coord_previous == fifth

    assert seventh.x == 55
    assert seventh.y == -72
    assert seventh.oncurve is False
    assert seventh.startpoint is False
    assert seventh.endpoint is False
    assert seventh.coord_next == eighth
    assert seventh.coord_previous == sixth

    assert eighth.x == 84
    assert eighth.y == 64
    assert eighth.oncurve is False
    assert eighth.startpoint is False
    assert eighth.endpoint is False
    assert eighth.coord_next == ninth
    assert eighth.coord_previous == seventh

    assert ninth.x == 91
    assert ninth.y == 116
    assert ninth.oncurve is True
    assert ninth.startpoint is False
    assert ninth.endpoint is True
    assert ninth.coord_next is None
    assert ninth.coord_previous == eighth


def test_quadratic_path_simple_glyph_with_implied():
    tt = TTFont(TESTFONT_PATH_1)
    glyf_table = tt["glyf"]
    test_glyph = glyf_table["comma"]
    qpath = pathins.bezier.quadratic_path(test_glyph, glyf_table, include_implied=True)
    first = qpath[0]
    second = qpath[1]
    third = qpath[2]
    fourth = qpath[3]
    fifth = qpath[4]
    sixth = qpath[5]
    seventh = qpath[6]
    eighth = qpath[7]
    ninth = qpath[8]
    tenth = qpath[9]
    eleventh = qpath[10]

    assert len(qpath) == 11

    assert first.x == 185
    assert first.y == 116
    assert first.oncurve is True
    assert first.implied is False
    assert first.startpoint is True
    assert first.endpoint is False
    assert first.coord_next == second
    assert first.coord_previous is None

    assert second.x == 192
    assert second.y == 105
    assert second.oncurve is True
    assert second.implied is False
    assert second.startpoint is False
    assert second.endpoint is False
    assert second.coord_next == third
    assert second.coord_previous == first

    assert third.x == 178
    assert third.y == 52
    assert third.oncurve is False
    assert third.implied is False
    assert third.startpoint is False
    assert third.endpoint is False
    assert third.coord_next == fourth
    assert third.coord_previous == second

    assert fourth.x == 154
    assert fourth.y == -11
    assert fourth.oncurve is True
    assert fourth.implied is True
    assert fourth.startpoint is False
    assert fourth.endpoint is False
    assert fourth.coord_next == fifth
    assert fourth.coord_previous == third

    assert fifth.x == 130
    assert fifth.y == -75
    assert fifth.oncurve is False
    assert fifth.implied is False
    assert fifth.startpoint is False
    assert fifth.endpoint is False
    assert fifth.coord_next == sixth
    assert fifth.coord_previous == fourth

    assert sixth.x == 106
    assert sixth.y == -129
    assert sixth.oncurve is True
    assert sixth.implied is False
    assert sixth.startpoint is False
    assert sixth.endpoint is False
    assert sixth.coord_next == seventh
    assert sixth.coord_previous == fifth

    assert seventh.x == 41
    assert seventh.y == -129
    assert seventh.oncurve is True
    assert seventh.implied is False
    assert seventh.startpoint is False
    assert seventh.endpoint is False
    assert seventh.coord_next == eighth
    assert seventh.coord_previous == sixth

    assert eighth.x == 55
    assert eighth.y == -72
    assert eighth.oncurve is False
    assert eighth.implied is False
    assert eighth.startpoint is False
    assert eighth.endpoint is False
    assert eighth.coord_next == ninth
    assert eighth.coord_previous == seventh

    assert ninth.x == 70
    assert ninth.y == -4
    assert ninth.oncurve is True
    assert ninth.implied is True
    assert ninth.startpoint is False
    assert ninth.endpoint is False
    assert ninth.coord_next == tenth
    assert ninth.coord_previous == eighth

    assert tenth.x == 84
    assert tenth.y == 64
    assert tenth.oncurve is False
    assert tenth.implied is False
    assert tenth.startpoint is False
    assert tenth.endpoint is False
    assert tenth.coord_next == eleventh
    assert tenth.coord_previous == ninth

    assert eleventh.x == 91
    assert eleventh.y == 116
    assert eleventh.oncurve is True
    assert eleventh.implied is False
    assert eleventh.startpoint is False
    assert eleventh.endpoint is True
    assert eleventh.coord_next is None
    assert eleventh.coord_previous == tenth
