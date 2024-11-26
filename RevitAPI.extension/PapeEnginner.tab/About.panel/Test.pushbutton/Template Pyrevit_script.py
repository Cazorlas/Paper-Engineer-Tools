#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import clr 
import math
import xlsxwriter
import os
from collections import OrderedDict
from pyrevit import revit,forms,script
from pyrevit.forms import ProgressBar
from Autodesk.Revit.UI.Selection import ObjectType 
from System.Collections.Generic import *
from rpw.ui.forms import Alert
import csv

#WPF
try:
    clr.AddReference('IronPython.wpf')
    clr.AddReference('PresentationCore')
    clr.AddReference('PresentationFramework')
except IOError:
    raise
from System.IO import StringReader
from System.Windows.Markup import XamlReader, XamlWriter
from System.Windows import Window,Application
from System.Windows import RoutedEventHandler
try:
    import wpf
except ImportError:
    raise


clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as DSGeo
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from  Autodesk.Revit.UI import*

clr.AddReference('RevitAPIUI')
from  Autodesk.Revit.UI.Selection import*

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
version = app.VersionNumber

#----------------------------------Main Logic---------------------------------------------------------------------------










