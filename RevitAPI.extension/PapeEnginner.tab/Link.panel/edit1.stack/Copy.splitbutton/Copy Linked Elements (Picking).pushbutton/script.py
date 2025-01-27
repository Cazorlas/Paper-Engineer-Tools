# -*- coding: utf-8 -*-
import sys

#  ©️ Copyright:
#  - This script belongs to Paper Engineer.
#  - If you appreciate my content, please give credit when using it.
#
#  Please contact to: trinhvutuanhung@gmail.com,
#  or visit: https://www.youtube.com/@paper.engineer
#  to get more information
#

# TODO: Import libraries and modules
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit
import Revit  # Import Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager  # Document management in Revit
from RevitServices.Transactions import TransactionManager  # Transaction management

# TODO: Prepare variables and input
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
version = int(app.VersionNumber)
selection = uidoc.Selection

"""----------------------Functions----------------------------"""

def SelectLinkedElements():
    try:
        result = selection.PickObjects(ObjectType.LinkedElement, "Select elements from linked models")
        return result
    except Exception as e:
        TaskDialog.Show("Error", "Error selecting linked elements: {0}".format(e))
        return None

def ShowTaskDialog(title, mainInstruction, icon, mainContent, footerText, footerUrl):
    dialog = TaskDialog(title)
    dialog.TitleAutoPrefix = False
    dialog.MainInstruction = mainInstruction

    # Set icon only if not None
    if icon is not None:
        dialog.MainIcon = icon

    dialog.MainContent = mainContent
    dialog.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel

    # Add footer with link
    dialog.FooterText = '<a href="{0}">{1}</a>'.format(footerUrl, footerText)

    return dialog.Show()

def CopyLinkElements():
    selectedLinkEles = SelectLinkedElements()

    if selectedLinkEles:
        with TransactionGroup(doc, "Copy Link Elements") as tg:
            # transform = Transform.Identity
            opt = CopyPasteOptions()

            copiedElementIds = set()
            copiedElements = []

            tg.Start()
            with Transaction(doc, "Copy Elements") as t:
                t.Start()
                for ele in selectedLinkEles:
                    linkInstance = doc.GetElement(ele)

                    if linkInstance is None:
                        transform = Transform.Identity
                    else:
                        transform = linkInstance.GetTransform()

                    if isinstance(linkInstance, RevitLinkInstance):
                        docLink = linkInstance.GetLinkDocument()

                        if docLink:
                            linkElementId = ele.LinkedElementId
                            if linkElementId not in copiedElementIds:
                                copiedElementIds.add(linkElementId)

                                linkedElement = docLink.GetElement(linkElementId)

                                if linkedElement:
                                    copiedIds = ElementTransformUtils.CopyElements(
                                        docLink, List[ElementId]([linkElementId]), doc, transform, opt
                                    )
                                    copiedElements.extend(copiedIds)
                t.Commit()
            tg.Assimilate()

"""----------------------Main Code----------------------------"""
try:
    dialog = ShowTaskDialog(
        title="Paper Engineer",
        mainInstruction="Copy Link Elements to Active Model",
        icon=None,
        mainContent="Click Ok to process the script\n\nClick Cancel if you would like to call off",
        footerText="Get help",
        footerUrl="https://www.youtube.com/@paper.engineer"
    )

    if dialog == TaskDialogResult.Cancel:
        sys.exit()
    else:
        CopyLinkElements()

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {0}".format(ex))
