from langchain_core.prompts import PromptTemplate

template = """\
You are an information extractor. Extract ONLY contact details that are
explicitly mentioned by the user in the conversation history.

Return null/empty for any field that is not clearly provided. Do not guess,
infer, or fabricate values. If a value appears ambiguous, treat it as missing.
"""

prompt_template = PromptTemplate.from_template(template)