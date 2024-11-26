
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

class ModelSelection:
    
    @staticmethod
    def PickElement(uidoc):
        '''
        Select A Element.
        '''
        object_type = ObjectType.Element
        pick_reference = uidoc.Selection.PickObject(object_type, "Select Model Element")
        pick_element = uidoc.Document.GetElement(pick_reference)
        return pick_element

    @staticmethod
    def PickElements(uidoc):
        '''
        Select Mutiple Elements.
        '''
        object_type = ObjectType.Element
        pick_references = uidoc.Selection.PickObjects(object_type, "Select Model Elements")
        pick_elements = [uidoc.Document.GetElement(r) for r in pick_references]
        return pick_elements

    @staticmethod
    def SelectElementByCategory(uidoc, category_name):
        '''
        Select A Element By Category.
        '''
        filter = ModelSelection.CategorySelectionFilter([category_name])
        object_type = ObjectType.Element
        pick_reference = uidoc.Selection.PickObject(object_type, filter, "Select {} Element".format(category_name))
        pick_element = uidoc.Document.GetElement(pick_reference)
        return pick_element

    @staticmethod
    def SelectElementsByCategory(uidoc, category_names):
        '''
        Select Mutiple Elements By Category.
        '''
        filter = ModelSelection.CategorySelectionFilter(category_names)
        object_type = ObjectType.Element
        pick_references = uidoc.Selection.PickObjects(object_type, filter, "Select {} Elements".format(", ".join(category_names)))
        pick_elements = [uidoc.Document.GetElement(r) for r in pick_references]
        return pick_elements

    @staticmethod
    def SelectImportInstance(uidoc):
        '''
        Select A Import Instance.
        '''
        cad_filter = ModelSelection.CADSelectionFilter()
        object_type = ObjectType.Element
        pick_reference = uidoc.Selection.PickObject(object_type, cad_filter, "Select Import Instance")
        pick_element = uidoc.Document.GetElement(pick_reference)
        return pick_element

    class CategorySelectionFilter(ISelectionFilter):
        def __init__(self, category_names):
            self._category_names = category_names

        def AllowElement(self, element):
            return element.Category.Name in self._category_names if element.Category else False

        def AllowReference(self, reference, position):
            return False

    class CADSelectionFilter(ISelectionFilter):
        def AllowElement(self, elem):
            return isinstance(elem, ImportInstance)

        def AllowReference(self, reference, position):
            return False
