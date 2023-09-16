# Service for Integration with Livetex
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/greasecake/coinkeeper/blob/master/README.md)
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](https://github.com/greasecake/coinkeeper/blob/master/README-ru.md)

## Overview

This is a Python application created using Flask to handle webhook events. It integrates with the Livetex Bot API to respond to visitor actions and route messages to operators.

## Getting Started

Follow these steps to set up and run the project locally.

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

- In the application folder, create a `channel_tokens.json` file with the mapping of [contact point IDs](https://my.livetex.ru/settings/touch_points) to [tokens](https://my.livetex.ru/channels/bot).

Example:
```json
{
  "123456": "112233:00000000-aaaa-0000-aaaa-00000000aaaa",  
  "789012": "445566:11111111-bbbb-1111-bbbb-11111111bbbb"
}
```

## Usage

```bash
python app.py
```

The application listens for incoming POST requests at the `/bot-api/webhook` endpoint. It processes webhook events, responds to visitor actions, and routes messages to operators.

### Webhook Endpoints

- `POST /bot-api/webhook`: Processing incoming webhook events.
- `GET /bot-api/webhook`: Getting initial settings.

For more detailed information on interacting with the API, refer to the [Livetex documentation](https://support.livetex.ru/hc/ru/articles/4411890908305-Bot-API) and the provided example script (`conversation_tree.yml`).

## Logging and Error Handling

The project includes logging and error handling. Logs are written to `stdout`, and errors are additionally logged to the `error.log` file.

### Logging

- Event logs: Incoming POST requests, including `channel_id` and `visitor_id`, are logged for event tracking.

### Error Handling

- All request handlers (`get_reply` and `get_settings`) include error handling and log errors in case they occur.

- In case of an error, a corresponding error message with the appropriate status and status code is returned to the client.

---

# Structure of the `conversation_tree.yml` File

The `conversation_tree.yml` file is used to define the structure and content of responses to various webhook events in the project. This YAML file organizes responses into a hierarchical structure, allowing for flexible chatbot response customization.

## YAML Structure

The `conversation_tree.yml` file follows a hierarchical structure with nested nodes representing different stages of a conversation or responses. Each node can contain text and button options.

### Example `conversation_tree.yml` Structure:

```yaml
root:
  text: "Welcome to our chatbot! How can we assist you today?"
  children:
    greeting:
      text: "Hello! How can I help you?"
      children:
        menu:
          text: "Here are some options:"
          children:
            option1:
              text: "Option 1: Learn more"
            option2:
              text: "Option 2: Clarify your request"
            operator:
              text: "Option 3: Contact an operator"
```

In this example:

- `root` is the top-level node and serves as the starting point of the conversation.
- Each node can have a `text` field containing the chatbot's response text.
- Nodes can have children (subnodes) to create a hierarchy of responses.
- `operator` is a reserved node name. If a user lands there, their request is transferred to an available operator in the group. Multiple such nodes can exist at different points in the tree.

### Response Parameters

For each node, you can define the following parameters:

- `text`: The textual message the chatbot will send.
- `children`: Nested nodes representing possible next responses.
- `button`: An optional field that defines the text on the response button.

### Usage

The `conversation_tree.yml` file is used in the code to determine text responses and buttons based on the received webhook event. Nodes in the YAML structure are identified using keys and can be used in payload data.

Example of using a key in payload data: `"payload": "options.option1"` means that the chatbot will retrieve the text response from the `option1` node in the `options` structure.

### Configuration

Configure the `conversation_tree.yml` file according to your chatbot's requirements and the desired dialog structure.
```