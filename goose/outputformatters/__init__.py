# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from goose.text import StopWords, innerTrim
from goose.parsers import Parser
from copy import deepcopy

class OutputFormatter(object):
    
    def __init__(self):
        self.topNode = None
    
    
    def getTopNode(self):
        return self.topNode
    
    
    def getFormattedText(self, topNode):
        self.topNode = topNode
        self.removeNodesWithNegativeScores()
        self.convertLinksToText()
        self.replaceTagsWithText()
        self.removeParagraphsWithFewWords()
        return self.convertToText()
    
    
    def convertToText(self):
        txts = []
        for node in list(self.getTopNode()):
            txt = Parser.getText(node)
            if txt:
                txt = HTMLParser().unescape(txt)
                txts.append(innerTrim(txt))
        return '\n\n'.join(txts)
            
    
    
    def convertLinksToText(self):
        """\
        cleans up and converts any nodes that 
        should be considered text into text
        """
        Parser.stripTags(self.getTopNode(), 'a')
    
    
    def removeNodesWithNegativeScores(self):
        """\
        if there are elements inside our top node 
        that have a negative gravity score, 
        let's give em the boot
        """
        gravityItems = self.topNode.cssselect("*[gravityScore]")
        for item in gravityItems:
            score = int(item.attrib.get('gravityScore'),0)
            if score < 1:
                item.getparent().remove(item)
    
    
    def replaceTagsWithText(self):
        """\
        replace common tags with just 
        text so we don't have any crazy formatting issues
        so replace <br>, <i>, <strong>, etc.... 
        with whatever text is inside them
        code : http://lxml.de/api/lxml.etree-module.html#strip_tags
        """
        Parser.stripTags(self.getTopNode(), 'b', 'strong', 'i', 'br')
    
    
    def removeParagraphsWithFewWords(self):
        """\
        remove paragraphs that have less than x number of words, 
        would indicate that it's some sort of link
        """
        allNodes = Parser.getElementsByTags(self.getTopNode(),['*'])#.cssselect('*')
        allNodes.reverse()
        for el in allNodes:
            text = Parser.getText(el)
            stopWords = StopWords().getStopWordCount(text)
            if stopWords.getStopWordCount() < 3 \
                and len(Parser.getElementsByTag(el, tag='object')) == 0 \
                and len(Parser.getElementsByTag(el, tag='embed')) == 0:
                Parser.remove(el)
            # TODO
            # check if it is in the right place
            else:
                trimmed = Parser.getText(el)
                if trimmed.startswith("(") and trimmed.endswith(")"):
                    Parser.remove(el)



class StandardOutputFormatter(OutputFormatter):
    pass