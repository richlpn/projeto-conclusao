# %%
from src.models.agents.code_reviwer_agent import CodeReviwerAgent
from src.tests.script_generation_test import state
from src.models.agents.script_generator_agent import ScriptGeneratorAgent

# %%

code_gen_agent = ScriptGeneratorAgent()

# %%
task = state.requirements.tasks[1]
code_state = "This is an empty python module."
script = code_gen_agent.invoke(TASK=task, MODULE_STATE=code_state)

# %%
reviwer = CodeReviwerAgent()
review = reviwer.invoke(TASK=task, CODE=script.code)
print(review)

# %%
review_task = review.description
review_state = f"This is the current python module script.```python\n{script.code}```"
review_script = code_gen_agent.invoke(TASK=review_task, MODULE_STATE=review_state)

# %%
