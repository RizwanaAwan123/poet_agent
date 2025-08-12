from agents import Agent, Runner, trace, function_tool
from connection import config
import asyncio
from dotenv import load_dotenv

load_dotenv()


@function_tool
def poetic_mood():
    return "Silence and light"



poet_agent = Agent(
    name="Poet Agent",
    instructions="""
        You are a poetic soul who creates or interprets short poems.
        Handle lyrical, narrative, and dramatic styles.
        If no poem is given, write one based on silence and light.
    """
)

lyric_analyst_agent = Agent(
    name="Lyric Analyst Agent",
    instructions="""
        You analyze lyric poetry by understanding emotions, rhythm, and inner thoughts.
    """
)

narrative_analyst_agent = Agent(
    name="Narrative Analyst Agent",
    instructions="""
        You analyze storytelling poems with characters, journeys, and emotions.
    """
)

dramatic_analyst_agent = Agent(
    name="Dramatic Analyst Agent",
    instructions="""
        You analyze poems with performative tone, stage impact, and dramatic expression.
    """
)

# --- Parent Agent  ---

parent_agent = Agent(
    name="Parent Poet Agent",
    instructions="""
        Your job is to handle poetry queries.
        First, send any input to the Poet Agent.

        Then:
        - If poem has words like 'curtain', 'actor', 'perform', delegate to Dramatic Analyst Agent.
        - If it has 'journey', 'conflict', 'hero', 'memory', delegate to Narrative Analyst Agent.
        - Otherwise, send to Lyric Analyst Agent by default.

        Do not answer non-poetry queries yourself.
        Use poetic_mood tool if needed.
    """,
    handoffs=[poet_agent, lyric_analyst_agent, narrative_analyst_agent, dramatic_analyst_agent],
    tools=[poetic_mood]
)



async def main():
    with trace("Poet Flow "):
        input_text = """
        The curtain rose, and there she stood,  
        Alone beneath the blinding light.  
        Her script was shaking in her hand,  
        But still, she spoke with all her might.
        """

        result = await Runner.run(
            parent_agent,
            input_text,
            run_config=config
        )

        print("✅ Final Output:\n", result.final_output)
        print("🔍 Last Agent:", result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())