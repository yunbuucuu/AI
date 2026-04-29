import os

import streamlit as st


MODEL_NAME = "doubao-seed-2-0-mini-260215"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
SYSTEM_PROMPT = "You are a helpful assistant"

QUICK_PROMPTS = [
    "帮我总结这段内容",
    "生成一个学习计划",
    "优化这段文案",
    "解释一个技术概念",
]


def inject_styles():
    st.markdown(
        """
        <style>
            .stApp {
                background: #f5f7fb;
            }

            [data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid #d9e0ea;
            }

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #172033;
            }

            .app-header {
                padding: 1.2rem 1.4rem;
                border: 1px solid #d9e0ea;
                border-radius: 8px;
                background: #ffffff;
                box-shadow: 0 12px 32px rgba(23, 32, 51, 0.08);
                margin-bottom: 1rem;
            }

            .app-header-top {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                align-items: flex-start;
            }

            .app-title {
                font-size: 1.85rem;
                font-weight: 760;
                color: #172033;
                margin: 0;
                line-height: 1.2;
            }

            .app-subtitle {
                margin: .4rem 0 0;
                color: #667085;
                font-size: .98rem;
                line-height: 1.6;
            }

            .status-badge {
                flex: 0 0 auto;
                display: inline-flex;
                align-items: center;
                border-radius: 999px;
                border: 1px solid #c9dafd;
                background: #e7efff;
                color: #2563eb;
                font-size: .8rem;
                font-weight: 650;
                padding: .35rem .65rem;
                margin-top: .15rem;
            }

            .welcome-card {
                border: 1px solid #d9e0ea;
                border-radius: 8px;
                background: #ffffff;
                padding: 1.15rem;
                margin-bottom: 1rem;
            }

            .welcome-title {
                color: #172033;
                font-size: 1.15rem;
                font-weight: 720;
                margin-bottom: .35rem;
            }

            .welcome-copy {
                color: #667085;
                line-height: 1.65;
                margin: 0;
            }

            .capability-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: .75rem;
                margin: .9rem 0 .2rem;
            }

            .capability-card {
                border: 1px solid #d9e0ea;
                border-radius: 8px;
                background: #fbfcff;
                padding: .85rem;
                min-height: 5.8rem;
            }

            .capability-title {
                color: #172033;
                font-weight: 700;
                margin-bottom: .3rem;
            }

            .capability-copy {
                color: #667085;
                font-size: .88rem;
                line-height: 1.5;
            }

            .section-label {
                color: #475467;
                font-weight: 700;
                margin: .4rem 0 .55rem;
            }

            .chat-shell {
                border: 1px solid #d9e0ea;
                border-radius: 8px;
                background: #ffffff;
                padding: 1rem 1rem .35rem;
                margin-top: 1rem;
            }

            div[data-testid="stChatMessage"] {
                border-radius: 8px;
                border: 1px solid rgba(217, 224, 234, .72);
                background: #fbfcff;
                padding: .45rem .7rem;
            }

            div[data-testid="stChatInput"] {
                background: #f5f7fb;
            }

            @media (max-width: 900px) {
                .app-header-top {
                    display: block;
                }

                .status-badge {
                    margin-top: .8rem;
                }

                .capability-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


@st.cache_resource
def get_client(api_key):
    from openai import OpenAI

    return OpenAI(api_key=api_key, base_url=BASE_URL)


def render_sidebar():
    api_key = os.getenv("DOUBAO_API_KEY")

    with st.sidebar:
        st.title("AI Partner")
        st.caption("智能工作台")

        st.divider()
        st.markdown("**模型**")
        st.caption(MODEL_NAME)

        if api_key:
            st.success("API 已连接")
        else:
            st.warning("未检测到 DOUBAO_API_KEY")

        temperature = st.slider(
            "创造性",
            min_value=0.0,
            max_value=2.0,
            value=1.3,
            step=0.1,
            help="数值越高，回答越发散；数值越低，回答越稳定。",
        )

        st.divider()
        st.metric("会话消息", len(st.session_state.messages))

        if st.button("清空会话", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

    return api_key, temperature


def render_header():
    st.markdown(
        f"""
        <section class="app-header">
            <div class="app-header-top">
                <div>
                    <h1 class="app-title">AI Partner</h1>
                    <p class="app-subtitle">
                        一个面向分析、写作和问答的智能工作台，帮助你更快整理想法并完成任务。
                    </p>
                </div>
                <span class="status-badge">Doubao Mini</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_welcome():
    if st.session_state.messages:
        return

    st.markdown(
        """
        <section class="welcome-card">
            <div class="welcome-title">今天想完成什么？</div>
            <p class="welcome-copy">
                你可以直接提问，也可以从下方快捷问题开始。AI Partner 会保留当前会话上下文，
                方便你连续追问、修改和扩展答案。
            </p>
            <div class="capability-grid">
                <div class="capability-card">
                    <div class="capability-title">内容整理</div>
                    <div class="capability-copy">总结长文本、提炼重点、生成结构化笔记。</div>
                </div>
                <div class="capability-card">
                    <div class="capability-title">写作协作</div>
                    <div class="capability-copy">优化表达、扩写段落、生成可用草稿。</div>
                </div>
                <div class="capability-card">
                    <div class="capability-title">技术解释</div>
                    <div class="capability-copy">拆解概念、比较方案、辅助学习和排错。</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_quick_prompts():
    if st.session_state.messages:
        return

    st.markdown('<div class="section-label">快速开始</div>', unsafe_allow_html=True)
    columns = st.columns(2)

    for index, prompt in enumerate(QUICK_PROMPTS):
        with columns[index % 2]:
            if st.button(prompt, key=f"quick_prompt_{index}", use_container_width=True):
                st.session_state.pending_prompt = prompt


def render_chat_history():
    if not st.session_state.messages:
        return

    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    st.markdown("</div>", unsafe_allow_html=True)


def submit_prompt(prompt, temperature, api_key):
    if not prompt:
        return

    if not api_key:
        st.error("请先配置环境变量 DOUBAO_API_KEY，然后再发送消息。")
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        try:
            client = get_client(api_key)
        except ModuleNotFoundError as exc:
            if exc.name != "openai":
                raise
            st.error("当前环境缺少 openai 依赖，请先安装 openai 包后再调用模型。")
            return

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *st.session_state.messages,
            ],
            stream=True,
            temperature=temperature,
        )

        full_content = ""
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content is None:
                    continue
                full_content += content
                response_placeholder.markdown(full_content + "▌")
            response_placeholder.markdown(full_content)

        st.session_state.messages.append({"role": "assistant", "content": full_content})
    except Exception as exc:
        st.error(f"调用模型失败：{exc}")


def main():
    st.set_page_config(
        page_title="AI Partner",
        page_icon="AI",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={},
    )
    inject_styles()
    init_session_state()

    api_key, temperature = render_sidebar()
    render_header()
    render_welcome()
    render_quick_prompts()
    render_chat_history()

    typed_prompt = st.chat_input("请输入您的问题或需求...")
    prompt = st.session_state.pending_prompt or typed_prompt
    st.session_state.pending_prompt = None
    submit_prompt(prompt, temperature, api_key)


if __name__ == "__main__":
    main()
