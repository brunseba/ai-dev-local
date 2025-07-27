# Langfuse Service

Langfuse provides comprehensive observability for large language models (LLMs). It enables you to track usage, analyze performance metrics, and debug workflow issues within AI-driven applications.

## Architecture Diagram

```mermaid
graph TD;
    A[User Interaction] -->|Requests| B[API Gateway];
    B -->|Forward| C[Langfuse Service];
    C -->|Metrics| D[Analytics Dashboard];
    C -->|Logs| E[Log Storage];
    C -->|Alerts| F[Alert System];
    
    %% Styling
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef gatewayClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef serviceClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef storageClass fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef alertClass fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000
    
    class A userClass
    class B gatewayClass
    class C serviceClass
    class D,E storageClass
    class F alertClass
```

## Features

- Real-time LLM usage tracking
- Comprehensive performance analysis
- AI workflow debugging
- Query and event logging
- Custom alerts and notifications

## Access

The Langfuse dashboard is accessible at:

```
http://localhost:3000/
```

## Online Resources

- **GitHub Repository:** [Langfuse GitHub](https://github.com/langfuse/langfuse)
- **Web Documentation:** [Langfuse Docs](https://docs.langfuse.io)

Langfuse is ideal for teams needing detailed insights into LLM usage patterns and operational metrics.
