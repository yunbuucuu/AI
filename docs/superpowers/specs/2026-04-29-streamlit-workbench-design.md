# Streamlit Workbench Frontend Design

## Summary

Upgrade the current Streamlit chat page into a balanced AI assistant workbench. The app remains a single-page Streamlit application, but the screen will be organized into a sidebar for controls and status, a main content area for welcome content and quick prompts, and a polished chat experience for the existing Doubao/OpenAI-compatible conversation flow.

## Current State

The project currently has one main application file: `ai_partner.py`.

The app already:

- Configures Streamlit with a wide layout.
- Stores chat history in `st.session_state.messages`.
- Renders chat history with `st.chat_message`.
- Calls the Doubao API through the OpenAI-compatible client.
- Streams assistant output into the page.

Issues to address:

- Several Chinese labels render as mojibake.
- The page has only a title and chat area, so the empty state feels bare.
- There is no sidebar structure for controls, status, or session actions.
- Missing API key handling can fail at runtime instead of guiding the user.

## Chosen Direction

Use the balanced workbench layout.

This direction keeps the app lightweight while making the interface feel more complete:

- Sidebar for model status, temperature, message count, and clearing the session.
- Header area for the product name and short positioning text.
- Welcome panel for first-run guidance.
- Quick prompt buttons for common starting points.
- Chat area for existing conversation history and streaming responses.

This avoids overbuilding a dense three-column dashboard while still giving the app a clear product structure.

## User Interface

### Page Shell

The page uses Streamlit wide layout and a restrained workbench style:

- Soft neutral background.
- White panels with subtle borders.
- Compact headings and body text.
- Consistent spacing around panels and controls.
- Streamlit default chat primitives retained for reliability.

### Sidebar

The sidebar contains:

- App name and short model label.
- API connection status.
- Temperature control, defaulting to the current behavior.
- Session message count.
- Clear conversation action.

If `DOUBAO_API_KEY` is missing, the sidebar shows a clear warning and the chat submission path is disabled or stopped with a friendly message.

### Main Header

The header contains:

- `AI Partner`
- A concise Chinese subtitle describing analysis, writing, and Q&A support.
- A small status badge such as `Doubao Mini`.

### Welcome Area

When there are no messages, the main area shows:

- A short welcome message.
- A small set of capability cards.
- Quick prompts that can seed a user message.

When messages exist, the welcome area remains compact or can be skipped so chat history gets priority.

### Quick Prompts

Provide 3-4 concise Chinese prompts, for example:

- "帮我总结这段内容"
- "生成一个学习计划"
- "优化这段文案"
- "解释一个技术概念"

Clicking a quick prompt should route through the same message handling flow as typed input so behavior stays consistent.

### Chat Area

The chat area keeps:

- `st.chat_message` for user and assistant roles.
- Existing session state history.
- Streaming assistant response.

The streaming implementation should use a single assistant message container and update it incrementally, avoiding repeated nested chat blocks during the stream.

## Code Organization

Keep `ai_partner.py` as the only application entry point for this small project, but organize it into functions:

- `inject_styles()` for CSS.
- `init_session_state()` for session defaults.
- `get_client()` for cached API client creation.
- `render_sidebar()` for controls and status.
- `render_header()` for the main page heading.
- `render_welcome()` for empty-state content.
- `render_quick_prompts()` for prompt starter buttons.
- `render_chat_history()` for stored messages.
- `submit_prompt(prompt, temperature)` for API request and response streaming.

This structure keeps the file understandable without introducing premature modules.

## Error Handling

Handle these cases explicitly:

- Missing `DOUBAO_API_KEY`: show a sidebar warning and stop before calling the API.
- Empty prompt: do nothing.
- API error: show a user-facing error message and do not append a failed assistant response.

## Testing And Verification

Manual verification is sufficient for this small Streamlit UI change:

- Run `streamlit run ai_partner.py`.
- Confirm the page renders without syntax errors.
- Confirm missing API key displays a friendly warning.
- Confirm quick prompts can submit a message through the same flow as chat input.
- Confirm chat history renders after a user message.
- Confirm clear conversation resets the chat state.
- Confirm streaming assistant output appears in one assistant message.

If dependencies or network access are unavailable locally, at minimum run Python syntax compilation and report that Streamlit runtime verification was not completed.
