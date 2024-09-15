# Imports
#%%
from tests.workflow_integration_test import workflow, graph, HumanMessage

# %%
data = {'messages': [HumanMessage('Nova documentação de fonte de dados em ./data/docs/taxa_estacoes.csv')]}
p = graph.invoke(data, debug=True)
# %%