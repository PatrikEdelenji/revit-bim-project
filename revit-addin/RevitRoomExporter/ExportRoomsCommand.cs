using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace RevitRoomExporter
{
    [Transaction(TransactionMode.Manual)]
    public class ExportRoomsCommand : IExternalCommand
    {
        public Result Execute(
            ExternalCommandData commandData,
            ref string message,
            ElementSet elements)
        {
            TaskDialog.Show("Revit Room Exporter", "Add-in is working!");
            return Result.Succeeded;
        }
    }
}