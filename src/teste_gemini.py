# Imports
#%%
from tests.workflow_integration_test import workflow, graph

# %%
data = {'messages': [('human','Extrai as informações para o engenheiro de dados da fonte de dados em ./data/docs/taxa_estacoes.csv')]}
p = graph.invoke(data, debug=True)
# %%