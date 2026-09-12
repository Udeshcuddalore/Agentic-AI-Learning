# Hello Agent — CSV FAQ Agent

Week 0 Mini Project: a small Streamlit app that answers natural-language
questions using only the content of uploaded CSV files (FAQs, policies,
terms, product docs).

## Structure

```
hello_agent/
├── app.py              # Streamlit UI (thin — no business logic)
├── config.py           # settings: model name, temperature, API key
├── requirements.txt
├── .env.example
└── src/
    ├── data_loader.py  # CSV upload -> DataFrames + preview helpers
    ├── prompts.py      # the "data-only" system prompt
    └── agent.py        # builds & queries the LangChain dataframe agent
```

## Setup

```bash
cd hello_agent
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then paste your OpenAI API key into .env
```

## Run

```bash
streamlit run app.py
```

Then, in the browser tab that opens:
1. Upload one or more CSV files (e.g. `ecommerce_faqs.csv`, `hospital_policy.csv`).
2. Type a question, e.g. "What is the return policy for electronics?"
3. Click **Get Answer**.

If the answer isn't in the data, the agent replies:
> "I could not find this information in the uploaded files."

## Notes

- No vector database or external DB is used — this is a direct
  pandas-dataframe agent, per the project's non-functional requirements.
- Temperature is set to `0` by default for predictable, non-creative answers.
- `allow_dangerous_code=True` is required by `langchain_experimental` to let
  the agent execute pandas code against your uploaded data locally — fine
  for this warm-up project, but worth knowing about before reusing the
  pattern elsewhere.
