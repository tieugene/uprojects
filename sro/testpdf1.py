#!/bin/env python
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
c = canvas.Canvas("hello.pdf")
c.translate(cm,cm)				# move the origin up and to the left
#c.setPageSize(
c.setFont("Helvetica", 12)			# define a large font
c.drawString(3*cm, -3*cm, "Hello World")	# say hello (note after rotate the y coord needs to be negative!)
c.showPage()
c.save()
