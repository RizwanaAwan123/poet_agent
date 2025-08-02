from agents import Agent, Runner, trace
from connection import config
import asyncio
from dotenv import load_dotenv

load_dotenv()


poet_agent = Agent(
    name= "Poet Agent",
    instructions="""
        You are a poetic soul who crafts or interprets short, expressive poems.
        You handle three types: lyrical (personal emotions), narrative (stories), and dramatic (theatrical voice).
        If no poem is provided, compose a two-stanza emotional poem based on solitude and hope.
    """
)

lyric_analyst_agent = Agent(
    name="Lyric Analyst Agent",
    instructions="""
        You analyze lyric poetry by uncovering deep emotional tones, musical flow, and the poet’s inner voice.
        Focus on personal themes, rhythm, and abstract feelings reflected in the verses.
    """
)

narrative_analyst_agent = Agent(
    name="Narrative Analyst Agent",
    instructions="""
        You break down narrative poetry by exploring its storytelling arc, characters, events, and setting.
        Identify how the poet builds a fictional world through descriptive scenes and sequences.
    """
)

dramatic_analyst_agent = Agent(
    name="Dramatic Analyst Agent",
    instructions="""
        You evaluate dramatic poetry by highlighting its performative strength, use of dialogue, and stage impact.
        Detect how characters express themselves, especially in conflict, tension, or self-monologue.
    """
)

# --- CUSTOM PARENT AGENT ---
class PoetryParentAgent(Agent):
    async def run(self, input, run_config):
        poet_output = await poet_agent.run(input, run_config)
        poem = poet_output.output.lower()

        if any(keyword in poem for keyword in ["curtain", "perform", "script", "actor"]):
            next_agent = dramatic_analyst_agent
        elif any(keyword in poem for keyword in ["journey", "hero", "conflict", "village", "memory"]):
            next_agent = narrative_analyst_agent
        else:
            next_agent = lyric_analyst_agent

        final_output = await next_agent.run(poet_output.output, run_config)
        return final_output


parent_agent = PoetryParentAgent(
    name="Parent Poet Agent",
    instructions="""
        You are the central orchestrator for poetry tasks.
        Handle poetry queries by first invoking the poet agent to generate or interpret a poem.
        Then, based on keywords and mood, delegate to the suitable analysis agent (lyrical, narrative, or dramatic).
        If unsure, default to the lyrical analyst. Avoid action on unrelated topics.
    """
)

# --- MAIN FUNCTION ---
async def main():
    with trace("Custom Poetry Flow"):
        poem_input = """
         She lit a lamp in shadows deep,
         Hoping someone still could see.
         The storm outside had made them weep,
         But light inside begged to be free.

        He walked through fog and fire alone,
        Till one warm flicker led him home.
        """
        
         
        


        result = await Runner.run(
            parent_agent,
            poem_input,
            run_config=config
        )

        print("... Final Output ...")
        print(result.final_output)
        print("...🔍 Last Agent ...")
        print(result.last_agent.name)

           
if __name__ == "__main__":
    asyncio.run(main())
    