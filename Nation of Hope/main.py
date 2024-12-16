from random import choice


class Nation:
    def __init__(self, name, territories):
        self.name = name
        self.territories = territories

    def get_power(self):
        return sum(territory.pow for territory in self.territories)

    def __str__(self):
        return self.name


class Territory:
    def __init__(self, name, prod, pow):
        self.name = name
        self.prod = prod
        self.pow = pow

    def generate(self):
        self.pow += self.prod

    def __str__(self):
        return self.name

hills = Territory('Hills', 10000, 1000000)
caladan = Territory('Caladan', 1000, 10000000000)
mountains = Territory('Mountains', 100000, 100)
plateau = Territory('Plateau', 10, 100000000000000)

class Game:
    def __init__(self):
        self.nations = []
        self.territories = []
        self.conversation = {
            'declare_war': [
                'We, the people of {give_nation}, declare war upon {take_nation}.',
                '{give_nation} officially declares war on {take_nation}.'
            ],
            'attack': [
                'We, the people of {give_nation}, have decided to attack the territory, {territory}.',
                'We do not show peace towards {take_nation}, we will bring hellfire upon {territory}.',
                '{territory} will be a part of {give_nation}.',
                'May the people of {territory} beware of {give_nation}, for we will conquer the land with ease.'
            ],
            'no_attack_treaty': [
                'We, the people of {give_nation}, offer a peace treaty with the nation of {take_nation}.',
                '{give_nation} wishes to start a no-attack treaty with {take_nation}.'
            ]
        }

    def add_nation(self, name, territories):
        self.nations.append(Nation(name, territories))

    def add_territory(self, name, prod, pow):
        self.territories.append(Territory(name, prod, pow))

    def get_territory_by_name(self, name):
        for territory in self.territories:
            if territory.name == name:
                return territory
        return None

    def get_nation_by_name(self, name):
        for nation in self.nations:
            if nation.name == name:
                return nation
        return None

    def declare_war(self, give_nation, take_nation):
        return self.letter('declare_war', give_nation, take_nation, None)

    def attack_territory(self, give_nation, territory):
        return self.letter('attack', give_nation, None, territory)

    def no_attack_treaty(self, give_nation, take_nation):
        return self.letter('no_attack_treaty', give_nation, take_nation, None)

    def letter(self, meaning, give_nation, take_nation, territory):
        replace_with_details = ['{give_nation}', '{take_nation}', '{territory}']

        if meaning == 'declare_war':
            text = choice(self.conversation['declare_war'])
        elif meaning == 'attack':
            text = choice(self.conversation['attack'])
        elif meaning == 'no_attack_treaty':
            text = choice(self.conversation['no_attack_treaty'])
        else:
            return None

        for i in replace_with_details:
            while i in text:
                if i == '{give_nation}':
                    text = text.replace(i, give_nation.name)
                elif i == '{take_nation}':
                    text = text.replace(i, take_nation.name)
                elif i == '{territory}':
                    text = text.replace(i, territory.name)
        return text

    def simulate_war(self, give_nation, take_nation):
        # For simplicity, let's assume the stronger nation always wins
        if give_nation.get_power() > take_nation.get_power():
            # Transfer all territories from the weaker nation to the stronger nation
            give_nation.territories.extend(take_nation.territories)
            take_nation.territories = []

            return f"{give_nation.name} wins the war and annexes all territories of {take_nation.name}."
        else:
            return f"{take_nation.name} wins the war and annexes all territories of {give_nation.name}."

# Instantiate the game
game = Game()

# Add nations
game.add_nation('100', [hills, caladan])
game.add_nation('Origin', [mountains, plateau])
# Add more nations and territories here...

# Example usage
nation_100 = game.get_nation_by_name('100')
origin = game.get_nation_by_name('Origin')
print(game.declare_war(nation_100, origin))
print(game.attack_territory(nation_100, hills))
print(game.no_attack_treaty(nation_100, origin))

# Simulate a war between nations
print(game.simulate_war(nation_100, origin))
