from revit_bim_project.ai.tools import (
    area_by_floor_tool,
    material_summary_tool,
    largest_rooms_tool,
    anomalies_tool,
)


def main():
    print("\nArea by floor:")
    print(area_by_floor_tool())

    print("\nMaterial summary:")
    print(material_summary_tool())

    print("\nLargest rooms:")
    print(largest_rooms_tool(limit=5))

    print("\nAnomalies:")
    print(anomalies_tool())


if __name__ == "__main__":
    main()