from langchain_core.output_parsers import OutputParserException, BaseOutputParser

class PythonCodeParser(BaseOutputParser):
    def parse(self, text: str):
        # Extract the code from the response, assuming it's enclosed in triple quotes (```python ... ```)
        code_start = text.find("```python")
        code_end = text.find("```", code_start + 1)

        if code_start == -1 or code_end == -1:
            raise OutputParserException("No code block found.")
            
        # Extract the code and remove the ```python markers
        python_code = text[code_start + len("```python"):code_end].strip()
        return python_code
        
    def get_format_instructions(self):
            return "The output should be a valid Python code block enclosed in triple backticks (```python ... ```)."