from src.main import summarizer
import pytest

def test_summarizer_non_interactive(monkeypatch):
    """
    Tests the main summarizer flow in a non-interactive way.
    It mocks user input to select 'no' for any prompts.
    """
    # Mock input() to always return 'n' (for no) to any prompts.
    monkeypatch.setattr('builtins.input', lambda _: "n")

    # We can't easily assert the full output, but we can check that it runs without crashing.
    # The main logic is in summarizer(), which is called by the CLI entrypoint.
    # We call it here to simulate a run.
    try:
        summarizer()
    except Exception as e:
        pytest.fail(f"Summarizer crashed with an unexpected exception: {e}")
