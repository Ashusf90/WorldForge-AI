
from app.services.story_engine import StoryEngine
from app.services.player_manager import PlayerManager
from app.services.combat_manager import CombatManager
from app.services.memory_manager import MemoryManager
from app.agents.game_agent import GameAgent
from app.agents.planner import Planner
from app.schemas.player import PlayerState
from app.agents.orchestrator import GameOrchestrator
from app.schemas.story import TurnResponse


def main():

    print("\n================================")
    print("       WORLDFORGE AI")
    print("================================")

    print("\n1. New Game")
    print("2. Load Game")
    print("3. Exit")

    option = input("\nChoose option: ").strip()

    if option == "3":
        return

    if option not in ["1", "2"]:
        print("Invalid option.")
        return

    player_name = input("\nEnter character name: ").strip()

    if not player_name:
        print("Character name cannot be empty.")
        return

    engine = StoryEngine()
    memory = MemoryManager()
    orchestrator = GameOrchestrator()

    if option == "1":

        player = PlayerManager(player_name)
        story = engine.generate_world(player_name)

        world_name = story.world_name
        previous_scene = story.scene
        previous_summary = story.story_summary

        player.update_location(world_name)

    else:

        saved_data = memory.load_game(player_name)

        if saved_data is None:
            return

        player = PlayerManager(player_name)
        player.player = PlayerState.model_validate(
            saved_data["player"]
        )

        game_state = saved_data["game_state"]

        world_name = game_state["world"]
        previous_scene = game_state["scene"]
        previous_summary = game_state["summary"]

        story = TurnResponse(
            scene=previous_scene,
            atmosphere=game_state["atmosphere"],
            choices=game_state["choices"],
            story_summary=previous_summary
        )

    combat = CombatManager(player)

    while True:

        print("\n================================")
        print("WORLD:", world_name)
        print("================================")

        player.show_status()

        print("\nSCENE:")
        print(previous_scene)

        print("\nAVAILABLE ACTIONS:")

        for i, choice in enumerate(story.choices, 1):
            print(f"{i}. {choice}")

        print("\nC. Fight Shadow Beast")
        print("P. Use Health Potion")
        print("S. View Status")
        print("V. Save Game")
        print("0. Exit")

        selection = input("\nChoose action: ").strip().lower()

        if selection == "0":
            print("\nThanks for playing!")
            break

        if selection.isdigit() and selection != "0":
            index = int(selection) - 1

            if index < 0 or index >= len(story.choices):
                print("Invalid choice.")
                continue

            action = story.choices[index]
        elif selection == "c":
            action = "Fight Shadow Beast"
        elif selection == "p":
            action = "Use Health Potion"
        elif selection == "s":
            action = "Show player status"
        elif selection == "v":
            action = "Save my adventure"
        else:
            print("Invalid choice.")
            continue

        status = player.player.model_dump()

        print("\nAI Agent is analysing your action...")

        result = orchestrator.process_action(action, status)
        decision = result["decision"]
        if decision == "STORY":
            plan = planner.create_plan(
                action,
                status,
                agent.memory.get_memory()
         )

        print("\n========== AI ACTION PLAN ==========")
        print(plan)
        print("====================================")
        agent.memory.remember_action(action)

        print("AI Agent decision:", decision)

        if decision == "STATUS":
            player.show_status()
            continue

        elif decision == "SAVE":

            game_state = {
                "world": world_name,
                "scene": previous_scene,
                "summary": previous_summary,
                "atmosphere": story.atmosphere,
                "choices": story.choices
            }

            memory.save_game(player, game_state)
            continue

        elif decision == "HEAL":
            combat.use_potion()
            continue

        elif decision == "COMBAT":

            enemy = combat.create_enemy()

            print(f"\nA {enemy.name} appears!")

            while enemy.health > 0 and player.player.health > 0:

                print(f"\nEnemy HP: {enemy.health}")
                print(f"Your HP: {player.player.health}")

                battle_action = input(
                    "\nA. Attack | P. Potion | R. Run: "
                ).strip().lower()

                if battle_action == "a":

                    result = combat.player_attack(enemy)

                    if result == "VICTORY":
                        break

                    combat.enemy_attack(enemy)

                elif battle_action == "p":

                    old_health = player.player.health
                    combat.use_potion()

                    if player.player.health > old_health:
                        combat.enemy_attack(enemy)

                elif battle_action == "r":
                    print("\nYou escaped!")
                    break

                else:
                    print("Invalid battle action.")

            if player.player.health <= 0:
                print("\nGAME OVER!")
                break

            continue

        elif decision == "STORY":

            print("\nProcessing story action...\n")

            result = engine.process_action(
                player_name,
                world_name,
                previous_scene,
                previous_summary,
                action
            )

            previous_scene = result.scene
            previous_summary = result.story_summary

            story.scene = result.scene
            story.atmosphere = result.atmosphere
            story.choices = result.choices
            story.story_summary = result.story_summary

            player.add_xp(10)

            print("\nYou earned 10 XP!")

        else:
            print("Agent returned an invalid decision.")


if __name__ == "__main__":
    main()
