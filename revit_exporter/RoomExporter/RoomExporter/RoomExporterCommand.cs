using System;
using System.IO;
using System.Linq;
using System.Text.Json;

using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace RoomExporter
{
    [Transaction(TransactionMode.Manual)]
    public class RoomExporterCommand : IExternalCommand
    {
        public Result Execute(
            ExternalCommandData commandData,
            ref string message,
            ElementSet elements)
        {
            UIDocument uidoc = commandData.Application.ActiveUIDocument;
            Document doc = uidoc.Document;

            var rooms = new FilteredElementCollector(doc)
                .OfCategory(BuiltInCategory.OST_Rooms)
                .WhereElementIsNotElementType()
                .Cast<SpatialElement>()
                .Select(room => new
                {
                    room_id = room.Number,
                    room_name = room.Name,
                    floor = doc.GetElement(room.LevelId)?.Name ?? "Unknown",
                    area_m2 = UnitUtils.ConvertFromInternalUnits(
                        room.Area,
                        UnitTypeId.SquareMeters
                    ),
                    volume_m3 = 0,
                    material = "Unknown",
                    has_window = false
                })
                .ToList();

            string outputPath = @"C:\Users\patri\VScodeProjects\revit-bim-project\data\raw\revit_rooms_api_export.json";

            string json = JsonSerializer.Serialize(
                rooms,
                new JsonSerializerOptions { WriteIndented = true }
            );

            File.WriteAllText(outputPath, json);

            TaskDialog.Show(
                "Room Exporter",
                $"Exported {rooms.Count} rooms to JSON"
            );

            return Result.Succeeded;
        }
    }
}