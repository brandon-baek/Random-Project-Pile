from os import system as sys


class StoryNode:
    def __init__(self, story, options, outcome):
        self.story = story
        self.options = options
        self.outcome = outcome

    def display(self):
        sys('clear')
        print(self.story)
        for order, option in enumerate(self.options, start=1):
            print(f'{order}. {option}')

    def get_choice(self):
        user_choice = 0
        while len(self.options) >= user_choice > 0:
            user_choice = int(input('Enter number of what you would like to do.\n'))
            print('Invalid Input')
        return self.outcome[user_choice - 1]

def main():
    spaceship_start = StoryNode(
        'You wake up, dazed and hurt. You look around to find yourself in a ruined Spaceship.',
        ['Search the Spaceship', 'Find an exit and leave the Spaceship'],
        [searching_spaceship, outside_spaceship]
    )
    searching_spaceship = StoryNode(
        'You begin to search the Spaceship and you find two doors',
        ['Navigation Quarters', 'Hibernation Pod Quarters', 'Exit the Spaceship'],
        [navigation_quarters, hibernation_pod_quarters]
    )
    navigation_quarter = StoryNode(
        'You find a rusty room with lots of screens, all of which completely fried. You find an old notebook and '
        'you open it to read,"Multiple System Failures all at once, in direct course to crash on Centurion-3281"',
        ['Exit the room'],
        [searching_spaceship]
    )
    hibernation_pod_quarters = StoryNode(
        'You find thousands upon thousands of pods, but none have humans stored in them. You begin to wonder why '
        'you weren\'t in your pod when you woke up. How did you forget everything...',
        ['Exit the room'],
        [searching_spaceship]
    )
    outside_spaceship = StoryNode(
        'You find an exit and break free from the Spaceship. You look around the see a cloud filled sky, making the '
        'atmosphere very white and gloom. The landscape is filled with black sand with nothing but plains for miles. '
        'However, although hard to make out, you see a small hibernation pod crashed onto the sand. How did it get '
        'there?',
        ['Investigate the Hibernation Pod', 'Go back and search the Spaceship'],
        [crashed_hibernation_pod, searching_spaceship]
    )
    crashed_hibernation_pod = StoryNode(
        'You walk over to the Hibernation Pod. Water vapors cloud the window, making it impossible to see inside. But '
        'water vapors can only come from a person breathing. The Hibernation Pod is shut very tightly.',
        ['Break the window', 'Go back and search the Spaceship'],
        [first_revealed_survivor, searching_spaceship]
    )
    first_revealed_survivor = StoryNode(
        'You break the window, and immediately a woman pops her head out coughing. "Who the fuck are you? Where am I?"'
        ', she says as she pulls out an emergency knife from the inside of her pod, pointing it at you.',
        ['"I\'m just as confused as you are"', 'Snatch the knife from her hand and point it towards her'],
        [talk_with_first_revealed_survivor, fight_first_revealed_survivor]
    )
    fight_first_revealed_survivor = StoryNode(
        'She lifts her hands into the air as you point the knife at her. She pulls out another knife from her '
        'pocket, pointing it at you.',
        ['"Let\'s talk"'],
        [talk1_with_first_revealed_survivor]
    )
    talk1_with_first_revealed_survivor = StoryNode(
        '"Wait, aren\'t you the..." She suddenly springs out of the hibernation pod, dropping her knife. She stands '
        'straight and lifts her right hand to her forehead to salute you.',
        ['"What are you doing?"'],
        [talk2_with_first_revealed_survivor]
    )
    talk2_with_first_revealed_survivor = StoryNode(
        '"What do you mean what am I doing sir? You are the Commander of the Ship"',
        ['"What..?"', '"You\'re trying to trick me"'],
        [talk3_with_first_revealed_survivor, talk3_with_first_revealed_survivor]
    )
    talk3_with_first_revealed_survivor = StoryNode(
        '"Are you feeling okay sir?"',
        ['"Identify yourself"', '"I\'m feeling fine. I just don\'t remember anything"'],
        [talk4_with_first_revealed_survivor, talk4_with_first_revealed_survivor]
    )
    talk4_with_first_revealed_survivor = StoryNode(
        '"I am Private S93, fully at your service."',
        ['"Okay..."', '"You got a real name?"'],
        [talk6_with_s93, talk5_with_s93]
    )
    talk5_with_s93 = StoryNode(
        '"S93 IS my real name sir."',
        ['"Strange..."', '"Okay..."'],
        [talk6_with_s93, talk6_with_s93]
    )
    talk6_with_s93 = StoryNode(
        '"Could you explain what happened, Sir?"',
        ['"I don\'t know myself"'],
        [talk7_with_s93]
    )
    talk7_with_s93 = StoryNode(
        '"Let\'s get out of here," She starts to look around, noticing the same thing you did. There is nothing. '
        'There is one place to go to, the Spaceship. It\'s either that or the plains of sand',
        ['Go to Spaceship', 'Explore the Black Sand Plains'],
        [revisiting_spaceship, explore_black_sand_plains]
    )
    revisiting_spaceship = StoryNode(
        'You reenter the Spaceship with S93. "This ship is the size of Manhattan!" S93 yells, her voice echoing through '
        'the huge abandonded ship.',
        ['"You don\'t really believe in Manhattan, do you?"', '"It really is huge!"'],
        [talk_about_manhattan_with_s93, reexplore_spaceship]
    )
    talk_about_manhattan_with_s93 = StoryNode(
        '"Of course not, but it\'s a good size to compare to this ship. There is no way people were that advanced '
        'like 3000 years ago."',
        ['"Yeah"'],
        [reexplore_spaceship]
    )
    reexplore_spaceship = StoryNode(
        '"I wonder how we crashed. I thought the Hibernation Pods wake you up during an emergency, not only was I not '
        'woken up, but my entire pod was somehow launched outside the Spaceship!" slowly, the two of you approach a two'
        ' doors. The Navigation Quarters, and the  ',
        ['"I didn\'t wake up either"']
    )

    current_node = spaceship_start
    
    while True:
        current_node.display()
        current_node = current_node.get_choice()

main()