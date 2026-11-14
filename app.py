import streamlit as st
from dotenv import load_dotenv

# Load environment variables from root .env before importing agents
load_dotenv()

from src.langchain_multi_agent_research_system.pipelines.pipelines import run_research_pipeline

# 1. Page Configuration
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cleaner typography and card-like containers
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #6c757d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Configuration & Pipeline Info
with st.sidebar:
    st.header("⚙️ System Architecture")
    st.markdown("""
    This autonomous pipeline coordinates four specialized AI components:
    1. **🔍 Search Agent:** Queries Tavily for live web sources.
    2. **🕷️ Reader Agent:** Scrapes full context from top URLs.
    3. **✍️ Writer Chain:** Synthesizes findings into a structured report.
    4. **⚖️ Critic Agent:** Evaluates report accuracy and depth.
    """)
    
    st.divider()
    st.subheader("💡 Example Topics")
    example_topics = [
        "Impact of Agentic AI on Enterprise Software in 2026",
        "Latest breakthroughs in Solid-State EV Batteries",
        "Quantum Error Correction milestones and commercial timeline",
        "Open-weight LLMs vs Proprietary Models for RAG"
    ]
    
    selected_example = st.selectbox("Quick-fill a topic:", ["Custom..."] + example_topics)

# 3. Main Header & Input Section
st.markdown('<div class="main-header">🔬 Multi-Agent AI Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated web research, smart scraping, report synthesis, and quality critique.</div>', unsafe_allow_html=True)

default_topic = "" if selected_example == "Custom..." else selected_example

with st.form("research_form", clear_on_submit=False):
    topic = st.text_input(
        "Research Topic",
        value=default_topic,
        placeholder="e.g., How multi-agent systems are transforming automated software testing..."
    )
    submitted = st.form_submit_button("🚀 Start Research Pipeline", use_container_width=True, type="primary")

# Initialize session state so results stay visible when clicking tabs or download buttons
if "research_state" not in st.session_state:
    st.session_state.research_state = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# 4. Pipeline Execution
if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic before starting.")
    else:
        with st.status("🤖 Orchestrating Multi-Agent Pipeline...", expanded=True) as status:
            st.write("🔍 **Step 1–4 Running:** Searching web, scraping sources, drafting report, and running critic review...")
            try:
                result_state = run_research_pipeline(topic.strip())
                st.session_state.research_state = result_state
                st.session_state.last_topic = topic.strip()
                status.update(label="✅ Research & Critique Complete!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="❌ Pipeline Failed", state="error", expanded=True)
                st.error(f"An error occurred during execution: {e}")

# 5. Results Dashboard
if st.session_state.research_state:
    state = st.session_state.research_state
    
    # Helper to extract string if LangChain returns an AIMessage object instead of raw str
    def get_text(item):
        return item.content if hasattr(item, "content") else str(item)

    report_text = get_text(state.get("report", "No report generated."))
    feedback_text = get_text(state.get("feedback", "No critique available."))
    search_text = get_text(state.get("search_results", "No search results."))
    scraped_text = get_text(state.get("scraped_content", "No scraped content."))

    st.divider()
    
    # Action Bar: Title + Download Button
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.subheader(f"📑 Research Deliverable: {st.session_state.last_topic}")
    with col_btn:
        st.download_button(
            label="📥 Download Report (.md)",
            data=report_text,
            file_name=f"{st.session_state.last_topic[:30].replace(' ', '_').lower()}_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Tabbed Interface for Clean Navigation
    tab_report, tab_critic, tab_sources = st.tabs([
        "📄 Final Report",
        "⚖️ Critic Evaluation",
        "🔍 Raw Research & Scraped Data"
    ])

    with tab_report:
        with st.container(border=True):
            st.markdown(report_text)

    with tab_critic:
        st.info("### Quality Assurance & Critic Review")
        with st.container(border=True):
            st.markdown(feedback_text)

    with tab_sources:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌐 Step 1: Tavily Search Findings")
            with st.container(border=True, height=450):
                st.markdown(search_text)
        with col2:
            st.markdown("#### 🕷️ Step 2: Smart Scraped Content")
            with st.container(border=True, height=450):
                st.markdown(scraped_text)
