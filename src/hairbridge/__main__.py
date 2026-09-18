from .translation import ai_to_human_translate, human_to_ai_translate, load_cases


def main() -> None:
    print("Authored fixture demonstration — no semantic inference or RTSF measurement.\n")
    for case in load_cases():
        bridge = human_to_ai_translate(case["bridge"]["raw_input"], context=case["context"])
        print(f"{case['id']}: {bridge.raw_input}")
        print(f"Context: {case['context']}")
        print(f"Failure classes: {', '.join(bridge.failure_classes)}")
        print(ai_to_human_translate(bridge))
        print()


if __name__ == "__main__":
    main()
