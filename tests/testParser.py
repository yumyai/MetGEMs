import unittest
from pyparsing import Forward, nestedExpr, Word, alphanums

# Test how to parse
enclosed = Forward()
nestedParens = nestedExpr('(', ')', content=enclosed)
enclosed << (Word(alphanums+'.'+'-'+':') | ',' | nestedParens)


class TestParsing(unittest.TestCase):

    def testParselink(self):
        s = "(PELARGONIDIN-3-GLUCOSIDE-CMPD (PWY-7259 . :INCOMING))"
        exp = [["PELARGONIDIN-3-GLUCOSIDE-CMPD", ["PWY-7259", ".", ":INCOMING"]]]
        #print(enclosed.parseString(s).asList())
        self.assertListEqual(enclosed.parseString(s).asList(), exp)


    def testParseReaction(self):
        s = "(RXN1F-461 (:LEFT-PRIMARIES CPD1F-90) (:DIRECTION :L2R) (:RIGHT-PRIMARIES CPD1F-453))"
        exp = [["RXN1F-461", [":LEFT-PRIMARIES", "CPD1F-90"], [":DIRECTION", ":L2R"], [":RIGHT-PRIMARIES", "CPD1F-453"]]]
        self.assertListEqual(enclosed.parseString(s).asList(), exp)