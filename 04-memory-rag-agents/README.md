### AI Agent Architectures

##### 1. Simplified Tool Integration: 
With TooNode, developers can seamlessly incorporate a variety of tools into their AI Agents by passing a list of tools during initialization. This streamlined process reduces complexity and accelerates development

##### 2. Conditional Execution with tool_condition:
The tool_condition feature allows for dynamic decision making within the agent's workflow. Agents can evaluate conditions of runtime and choose appropriate actions, enabling more responsive and intelligent behavior.

##### 3. Enhanced Support for Diverse Architectures
These fetures facilitate the implementation of various AI Agent architectures
- **ReAct Aarchitecture:** Integrates reasoning and action by allowing agents to decide when to invoke tools based on current content.
- **DEPS (Describe, Explain, Plan, Select):** Supports strucutred decision-making processes by enabling conditional tool usage.
- **Reflexion Architecture:** Allows agents to reflect on actions and outcomes, adjusting behavior dynamically.
- **Talker-Reasoner Architecture:** Separates communication and reasoning processes with conditional tool invocation enhancing reasoning capabilities.
- **Cognitive Architecture (e.g., Soar):** Supports complex, human-like reasoning and decision making processes through dynamic tool integration

By providing these capabilities, Langgraph's ToolNode and tool_condition contriute to the evolution of agentic AI, moving beyond static models to more adaptive and intelligent systems.

### RAG (Retrieval Augmented Generation)
RAG is a technique used in conjunction with Large Language Models (LLMs) to enhace their performance, particularly in tasks requiring factual accuracy or domain-specific knowledge
##### What is RAG?
RAG combines two key componenet:

**1. Retrieval:**

Before generating a response, the system retrieves relevant information from external knowledge source (e.g., databases, documents, or the web)

**2. Generation:**

The LLM uses the retrievad informationto generate a response that is informed by the specific content found during retrieval.
- This approach addresses the limitationsof LLMs, such as outdated training data or hallucination of facts, by grounding their outputs in up-to-date or verfied data

##### How does RAG work?
**1. Query Creation:**

- A user provides a prompt or question
- The system may preprocess the query to optimize retrieval.

**2. Knowledge Retrieval:**

- The query is sent to a retrieval system, such as vectorsearch engine (e.g., Pinecone, Weaviate) or a traditional keyword-based search. 
- The retrieval system returns the most relevant documents or information chunks

**3. Contextual Input to LLM:**

- The retrieval content is combined with the original prompt and fed into the LLM as context.

**4 Response Generation:**

- The LLM generates a response, leveraging both the retrieved information and it's own language modeling capabilities.

##### Common Use Cases for RAG:
- **Customemr Support:**

Providing accurate answers by integrating with knowledge bases of FAQs

- **Search Driven Application:**

Generating human-like summaries of retrieved documents.

- **Research Assistane:**

Retrieving scholarly articles and summarizing them

- **Domain-Specific Application:**

Using proprietary date to answer questions (e.g., financial, legal, medical domains)

##### Popular Frameworks and Tools for RAG:
- **LangChain:** *A python library for combining LLMs with retrieval-based workflows*
- **LlamaIndex (formerly GPT Index):** *Facilitates RAG workflows by indexing and   querying large datasets*
- **Vecotr Database:** *Pincecone, Weaviate, Milvus, and other are commonly used for semantic search*

##### Advantages of RAG:
1. **Improved Accuracy:**

Reduces hallucination by grounding answers in factual content

2. **Scalability:**

Allows LLMs to work with Large, evolving datasets without retraining

3. **Customizeability**

Adapts LLMs to specific domains or usecases

##### Challenges for RAG:

1. **Retreival Quality**

The effectiveness of the response depends heavily on the quality and relevance of retrieved documents.

2. **Context Limitations:**

LLMs have token limit which may restrict the amount of retrieved content they can process

3. **Latency:**

The retrieval process introdcues additional steps, potentially increasing response times

##### RAG vs. Function Calling
RAG and function calling are both methods to enhance the capabilities of LLMs, but they differ in approach, and the kind of information they bring into the model's responses

###### Purpose and Use Cases
- **RAG**

RAG aims to enhance the factual accuracy and specificity of LLM responses by incorporating external information retrieved from knowledge bases, documents or databases, useful for:
- keeping answers up-to-date with recent information or specialized knowledge
- Hanlding complex, context specific questions that require referencing large amounts of data
- Use cases like summarizing documents, customer support (answering based on a knowledge base), and personalized recommendations

- **Fnction Calling**

It enables LLMs to invoke specific functions to perform actions or retrieve data from APIs or external systems, useful for
- Dynamically retrieving strucutred information like weather, stock prizes, or current news
- Executing actions such as creating a calender event, generating a report, or even initiating workflows.
- Bulding interactive applications where the model acts as a control interface for APIs or data-driven actions. 



| Feature | RAG | Function Calling |
|----------|----------|----------|
| Purpose    | Factual accuracy, knowledge retrieval    | Real time Data retrieval, action execution     |
| Data Source    | Knowledge Bases, documents, databases     | APIs, strucutred databases     |
| Response Type    | Flexible, unstructured answer   | Precise, strucutred answers     |
| Typical Use Cases    | Customer Support, research assistance     | Real-time data (e.g., weather, stock), task automation    |
| Limitations    | May not provide real-time info     | Limited to pre-defined functions and APIs     |
