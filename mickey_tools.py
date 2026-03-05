from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse



@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = deepseek_model
    else:
        model = gemma_model

    return handler(request.override(model=model))
