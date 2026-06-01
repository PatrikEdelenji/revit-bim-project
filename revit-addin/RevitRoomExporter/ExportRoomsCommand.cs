using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB.Architecture;

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;



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
            try
            {
                UIDocument uiDoc = commandData.Application.ActiveUIDocument;

                if (uiDoc == null)
                {
                    TaskDialog.Show("Revit Room Exporter", "No active Revit document found.");
                    return Result.Failed;
                }

                Document doc = uiDoc.Document;

                string outputPath = @"D:\VisualStudio\revit-bim-project\data\raw\revit_rooms_export.txt";

                List<RoomExportRow> rooms = CollectRooms(doc);

                ExportRoomsToTabDelimitedFile(rooms, outputPath);

                TaskDialog.Show(
                    "Revit Room Exporter",
                    $"Export completed successfully.\n\nRooms exported: {rooms.Count}\nFile:\n{outputPath}"
                );

                return Result.Succeeded;
            }
            catch (Exception ex)
            {
                message = ex.Message;

                TaskDialog.Show(
                    "Revit Room Exporter - Error",
                    ex.ToString()
                );

                return Result.Failed;
            }
        }

        private static List<RoomExportRow> CollectRooms(Document doc)
        {
            List<RoomExportRow> result = new List<RoomExportRow>();

            FilteredElementCollector collector = new FilteredElementCollector(doc)
                .OfCategory(BuiltInCategory.OST_Rooms)
                .WhereElementIsNotElementType();

            foreach (Element element in collector)
            {
                Room room = element as Room;

                if (room == null)
                {
                    continue;
                }

                // Skip unplaced or invalid rooms
                if (room.Area <= 0)
                {
                    continue;
                }

                string number = room.Number ?? "";
                string name = room.Name ?? "";
                string levelName = room.Level != null ? room.Level.Name : "";

                double areaM2 = UnitUtils.ConvertFromInternalUnits(
                    room.Area,
                    UnitTypeId.SquareMeters
                );

                double volumeM3 = 0.0;

                Parameter volumeParameter = room.get_Parameter(BuiltInParameter.ROOM_VOLUME);

                if (volumeParameter != null && volumeParameter.HasValue)
                {
                    volumeM3 = UnitUtils.ConvertFromInternalUnits(
                        volumeParameter.AsDouble(),
                        UnitTypeId.CubicMeters
                    );
                }

                result.Add(new RoomExportRow
                {
                    Number = number,
                    Name = name,
                    Level = levelName,
                    Area = areaM2,
                    Volume = volumeM3
                });
            }

            return result;
        }

        private static void ExportRoomsToTabDelimitedFile(
            List<RoomExportRow> rooms,
            string outputPath)
        {
            string directory = Path.GetDirectoryName(outputPath);

            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            StringBuilder sb = new StringBuilder();

            // Header must match the Python mapper:
            // Number, Name, Level, Area, Volume
            sb.AppendLine("Number\tName\tLevel\tArea\tVolume");

            foreach (RoomExportRow room in rooms)
            {
                sb.AppendLine(
                    $"{Escape(room.Number)}\t" +
                    $"{Escape(room.Name)}\t" +
                    $"{Escape(room.Level)}\t" +
                    $"{room.Area.ToString(CultureInfo.InvariantCulture)}\t" +
                    $"{room.Volume.ToString(CultureInfo.InvariantCulture)}"
                );
            }

            File.WriteAllText(outputPath, sb.ToString(), Encoding.UTF8);
        }

        private static string Escape(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                return "";
            }

            return value
                .Replace("\t", " ")
                .Replace("\r", " ")
                .Replace("\n", " ")
                .Trim();
        }

        private class RoomExportRow
        {
            public string Number { get; set; }
            public string Name { get; set; }
            public string Level { get; set; }
            public double Area { get; set; }
            public double Volume { get; set; }
        }
    }
}