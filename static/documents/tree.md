.
├── src
│   ├── graph
│   │   ├── nodes
│   │   │   ├── __init__.py
│   │   │   ├── code_evaluation_node.py
│   │   │   ├── new_source_node.py
│   │   │   ├── requirement_generation_node.py
│   │   │   ├── script_generation_node.py
│   │   │   └── tool_call_node.py
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── task_workflow_router.py
│   │   │   └── tool_router.py
│   │   ├── __init__.py
│   │   └── graph.py
│   ├── models
│   │   ├── agents
│   │   │   ├── agent.py
│   │   │   ├── analyst_agent.py
│   │   │   ├── code_reviwer_agent.py
│   │   │   ├── schema_extractor_agent.py
│   │   │   ├── script_generator_agent.py
│   │   │   └── task_creation_agent.py
│   │   ├── documents
│   │   │   ├── analyst_agent.md
│   │   │   └── state.md
│   │   ├── operations
│   │   │   ├── __init__.py
│   │   │   ├── aggregate.py
│   │   │   ├── filter.py
│   │   │   └── join.py
│   │   ├── __init__.py
│   │   ├── call_tools_model.py
│   │   ├── data_docs_schemas_model.py
│   │   ├── extractor_schema.py
│   │   ├── function_model.py
│   │   ├── requirement_model.py
│   │   ├── review_model.py
│   │   ├── script_model.py
│   │   └── state.py
│   ├── output_parsers
│   │   ├── __init__.py
│   │   ├── codeblock_output_parser.py
│   │   ├── review_output_parser.py
│   │   └── tasks_output_parser.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── review_script_test.py
│   │   ├── schema_extraction_test.py
│   │   ├── script_generation_test.py
│   │   └── task_creation_test.py
│   ├── tools
│   │   ├── __init__.py
│   │   ├── extract_docs_schema_tool.py
│   │   └── read_file_tool.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── llm_logger.py
│   └── __init__.py
├── static
│   ├── data
│   │   ├── dataset
│   │   │   ├── 2024 - Famílias atendidas pelo Programa Fomento Rural, por Grupo Populacional Tradicional e Específico (GPTE).csv
│   │   │   ├── Taxas_Estacoes.csv
│   │   │   └── legislacao-dados-abertos-2023.csv
│   │   ├── docs
│   │   │   ├── Glossario - Arrecadação - Valores de Tributos e Preços Públicos_v1.txt
│   │   │   ├── dicionario-legislacao-ambiental.pdf
│   │   │   └── familias_atendidas_fomento_rural.txt
│   │   └── schema_output.json
│   └── prompts
│       ├── analyst_agent.yml
│       ├── code_reviwer_agent.yml
│       ├── schema_extractor_agent.yml
│       ├── script_generator_agent.yml
│       └── task_creation_agent.yml
├── .env
├── .env.template
├── .gitignore
├── LICENSE
├── README.md
├── app.log
├── main.py
├── requirements.txt
└── tree.md
