from test import square
def main ():
    test_oddsquare()
    test_evensquare()
def test_oddsquare():
    assert square(2)==4
    assert square(-2)==4
def test_evensquare():
    assert square(3)==9
    assert square(-3)==9
main()
