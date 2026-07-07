from revit_bim_project.ai.openai_agent import generate_bim_quality_report


def main():
    report = generate_bim_quality_report()
    print(report)


if __name__ == "__main__":
    main()