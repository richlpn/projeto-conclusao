# State Model

## Description
- A shared data structure that represents the current snapshot of the graph.

- Uses the `add` reducer to keep track of the messages send by the LLM's.

- Multiple states can be used for example a state to hold tool calls/return's and another one to hold the history of the conversation.

## Workflow

1. The initial state must be a `OverallState`.
    - List of messages
    - Origin: "Analyst"
2. The 1st event will be a `new data source`.
    - Input e.g: "A new data source documentation arrived, access it on "C://data/docs/somefuckingfile.pdf"
3. The 2nd event will be a tool call to `extract documentation schema`.
    - This will trigger a new state, that includes a follow up or next node call.
    - This state is different since it has a pre-defined structure.
    - Could be a schema or a code block.
4. The analyst recives the new __schema__ and create's a `ScriptGenerationState`.
    - The **schema** will be storaged on the state
    - The new state keep's track of which ``type`` of pipeline is being created.
        - Extraction
        - Transformation
        - Loading
    - This state keeps track of the amount of run time errors.
        - Upon 5 errors, the process if finnished with a unsuccessful status.
        - On the transition of a pipeline type the error count will be reset to zero.
4. The analyst passes the __schema__ `generate script tool` with the current step.
5. The generated script is written to a file.
   - The file name will be generated using the pipeline **type** as prefix + the data source name.
6. The analyst runs the script and gets the results.
    - if an exception is raised, the state will be updated with the error message.
    - if the script was successful, the state will be updated with the results.
7. If the new state is an error state go to 8 otherwise go to 9
8. The analyst passes the code block and the error to the LLM to be corrected. Go to 5.
9. The state is updated with a new pipeline type