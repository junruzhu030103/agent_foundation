from pathlib import Path
from graph.workflow import build_workflow


def main():
    app = build_workflow()
    result = app.invoke({})

    out_path = Path("outputs/grant_application_001.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result["final_markdown"], encoding="utf-8")

    print("=== Generation Complete ===")
    print("Output:", out_path)
    print("Validation:", result["validation_report"])


if __name__ == "__main__":
    main()
