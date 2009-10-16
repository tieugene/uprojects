#!/bin/env python
# -*- coding: utf-8 -*-
#PATH = 'project1/static/fonts/'

import datetime, os
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet	# стили
from reportlab.lib import units
from reportlab.lib import colors	# для цветов
from reportlab.lib.units import inch, cm	# для дюймов
from reportlab.pdfbase import pdfmetrics	# для шрифтов
from reportlab.pdfbase import ttfonts
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape	# размеры страниц
from reportlab import rl_config

class genPDF(object):
    Title = u"Привет, Мир!"
    styles = getSampleStyleSheet()
    font_name = 'Times New Roman'
    font_size = 9
    #
    def __init__(self):
        #self._set_registerFont()
        self.setStyle()
    #
    def _set_registerFont(self):
        Times_New_Roman = ttfonts.TTFont('Times New Roman', "times.ttf")
        pdfmetrics.registerFont(Times_New_Roman)
        #
        Times_New_Roman_Bold = ttfonts.TTFont('Times New Roman Bold', "timesbd.ttf")
        pdfmetrics.registerFont(Times_New_Roman_Bold)
    #
    def _set_font(self, canvas):
        canvas.setFont(self.font_name, self.font_size)
    #
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        self._set_font(canvas)
        canvas.restoreState()
    #
    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        self._set_font(canvas)
        canvas.restoreState()
    #
    def run(self):
        DocName = datetime.datetime.now().strftime('genpdf_%Y%m%d_%H%M.pdf')
        doc = SimpleDocTemplate(DocName, 
                                pagesize = landscape(A4), # размер страницы == альбомный A4
                                leftMargin = 2 * cm, # отступ слева
                                rightMargin = 2 * cm, # отступ справа
                                bottomMargin = 2 * cm, # отступ сверху
                                topMargin = 2 * cm, # отступ снизу
                                )
        style = self.styles["Normal"]
        #
        DataTable = [[u'заголовок 1', u'заголовок 2', ], [u'колонка 1 '*100, u'колонка 2', ]]
        GridObj = Table(DataTable, 
                        colWidths = [150,150,], 
                        rowHeights = None, 
                        style = self._style, 
                        splitByRow = 1, 
                        #repeatRows = 1, 
                        #repeatCols = 0,
                        )
        #
        BGridObj = Table([[GridObj,GridObj]], 
                        colWidths = [320,320,], 
                        rowHeights = None, 
                        style = self._style, 
                        splitByRow = 1, 
                        repeatRows = 1, 
                        #repeatCols = 0,
                        )
        doc.build([BGridObj,], onFirstPage = self.myFirstPage, onLaterPages = self.myLaterPages)
    #----------------------------------------------------------------------------------------------------------        
    # установка стилей и шрифтов
    def setStyle(self, style = None):
        self._set_registerFont()
        if not style:
            self._style = [('TEXTCOLOR', (0,0), (0,-1), colors.blue),
                           ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                           ('VALIGN', (0,0), (0,-1), 'TOP'),
                           ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
                           ('INNERGRID', (0,0), (-1,-1), 0.1, colors.black),
                           ('BOX',(0,0),(-1,-1),0.1,colors.black),
                           ('FONTNAME', (0,0),(-1,-1), self.font_name),
                           ('FONTSIZE', (0,0),(-1,-1), self.font_size),
                          ]
        else:
            self._style = style

if __name__ == '__main__':
    genPDF().run()
