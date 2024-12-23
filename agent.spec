agent HelloWorldAgent {
    spec_version 1.0.0
    description "A simple Hello World agent."

    permissions {
        allow network_access
    }

    tasks {
        task GreetTask {
            description "This task sends a greeting message to an LLM and expects a response."
            actions {
                action SendGreeting {
                    type "llm_inference"
                    parameters {
                        message: "Hey there!"
                    }
                }
            }
            retry {
                max_attempts 3
                delay 5s
                backoff_strategy linear
            }
        }
    }

    telemetry {
        emit metrics {
            on task_completion
            data {
                field response_time: float
                field status: string
            }
        }
    }

    input {
        type JSON
        structure {
            field prompt: string
        }
    }

    output {
        type JSON
        structure {
            field response: string
        }
    }

    connectors {
        connector OpenAILLM {
            type "OpenAI"
            config {
                api_key: "${OPEN_AI_API_KEY}"
                model: "gpt-3.5-turbo"
            }
        }
    }

    actions {
        action LogResponse {
            type "logging"
            parameters {
                log_level: "INFO"
                message: "Received response from LLM"
            }
        }
    }

    limits {
        max_runtime 10s
        memory_usage 128MB
        parallel_tasks 1
    }

    llm {
        provider "OpenAI"
        model "gpt-3.5-turbo"
        settings {
            max_tokens 50
            temperature 0.7
        }
    }

    test {
        dryrun {
            input {
                type JSON
                structure {
                    field prompt: string
                }
            }
            expected_output {
                type JSON
                structure {
                    field response: string
                }
            }
        }
    }

    deployment {
        target "development"
        strategy "rolling"
    }

    documentation "This agent sends a greeting to an LLM and returns the response."
}
