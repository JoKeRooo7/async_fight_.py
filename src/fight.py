import asyncio

from enum import Enum, auto
from random import choice


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)


class Neo:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self, agent_action):
        if agent_action == Action.HIGHKICK:
            return Action.HIGHBLOCK
        elif agent_action == Action.LOWKICK:
            return Action.LOWBLOCK
        elif agent_action == Action.HIGHBLOCK:
            return Action.LOWKICK
        elif agent_action == Action.LOWBLOCK:
            return Action.HIGHKICK
        else:
            raise ValueError("Invalid action")


def check_health(obj_one_action, obj_two, obj_two_action):
    if (obj_one_action == Action.HIGHKICK
       and obj_two_action != Action.HIGHBLOCK):
        obj_two.health -= 1
    elif (obj_one_action == Action.LOWKICK
          and obj_two_action != Action.LOWBLOCK):
        obj_two.health -= 1


async def fight(neo=Neo(), agent=Agent(), agent_id=None):
    agent_iter = agent.__aiter__()
    neo_iter = neo.__aiter__()

    while agent_iter.health > 0 and neo_iter.health > 0:
        agent_action = await agent_iter.__anext__()
        neo_action = await neo_iter.__anext__(agent_action)

        check_health(neo_action, agent_iter, agent_action)
        check_health(agent, neo_iter, neo_action)

        await asyncio.sleep(0.1)

        if agent_id is None:
            print(
                f"Agent: {agent_action}, "
                f"Neo: {neo_action}, "
                f"Agent Health: {agent_iter.health}"
            )
        else:
            print(
                f"Agent {agent_id}: {agent_action}, "
                f"Neo: {neo_action}, "
                f"Agent Health: {agent_iter.health}"
            )

    if agent_iter.health == 0:
        return neo
    elif neo_iter.health == 0:
        return agent
    else:
        return None


async def fightmany(n):
    neo = Neo()
    agents = [Agent() for _ in range(n)]
    tasks = [
        asyncio.create_task(fight(neo, agent, id+1))
        for id, agent in enumerate(agents)]
    results = await asyncio.gather(*tasks)
    return results


def main(n=505):
    result = asyncio.run(fight())

    if isinstance(result, Agent):
        print("Agent wins!")
    elif isinstance(result, Neo):
        print("Neo wins!")
    else:
        print("Matrix error")

    results = asyncio.run(fightmany(n))

    if any(isinstance(result, Agent) for result in results):
        print("Agent wins!")
    elif any(result is None for result in results):
        print("Matrix error")
    else:
        print("Neo wins!")


if __name__ == "__main__":
    main(5)
