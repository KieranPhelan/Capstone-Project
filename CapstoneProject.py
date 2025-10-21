import random


class Card:
    def __init__(self, value: str, colour: str, name: str, sort_value: int):
        self.value = value
        self.colour = colour
        self.name = name
        self.sort_value = sort_value

    def set_colour(self, colour):
        self.colour = colour


class Deck:
    def __init__(self):
        self.deck_list = []
        self.throw_pile = []
        self.top_card = None

        self.create_deck()
        self.shuffle_deck()

    def get_top_card(self):
        return self.top_card

    def set_top_card(self, new_card):
        self.top_card = new_card

    def remove_card_from_deck(self, card):
        self.deck_list.remove(card)

    def create_deck(self):
        colours = ["Blue", "Green", "Red", "Yellow"]
        specials = ["Draw", "Reverse", "Skip"]

        for _ in range(2):
            for colour in colours:
                for value in range(0, 10):
                    sort_value = colours.index(colour) * 13 + value
                    card = Card(value=str(value),
                                colour=colour,
                                name=f"{colour[0]} {value}",
                                sort_value=sort_value)
                    self.deck_list.append(card)

                for special in specials:
                    sort_value = colours.index(
                        colour) * 13 + 10 + specials.index(special)
                    card = Card(value=special,
                                colour=colour,
                                name=f"{colour[0]} {special}",
                                sort_value=sort_value)
                    self.deck_list.append(card)

        for _ in range(4):
            wild_card = Card(value="Wild",
                             colour="",
                             name="Wild",
                             sort_value=52)
            self.deck_list.append(wild_card)

            wild_draw_card = Card(value="Wild Draw",
                                  colour="",
                                  name="Wild Draw",
                                  sort_value=53)
            self.deck_list.append(wild_draw_card)

    def shuffle_deck(self):
        random.shuffle(self.deck_list)

    def clear_deck(self):
        self.deck_list.clear

    def clear_throw_pile(self):
        self.throw_pile.clear

    def add_to_throw_pile(self):
        self.throw_pile.append(self.top_card)

    def check_and_recycle(self):
        if len(self.deck_list) == 0:
            self.deck_list = self.throw_pile
            self.shuffle_deck()
            self.clear_throw_pile()


class Hand:
    def __init__(self, name, hand_list: Card):
        self.name = name
        self.hand_list = hand_list

        self.sort_hand()

    def get_card(self, index):
        return self.hand_list[index]

    def remove_card(self, card):
        self.hand_list.remove(card)

    def display_hand(self):
        i = 1
        for card in self.hand_list:
            print(f"{i}: {card.name}")
            i += 1

    def sort_hand(self):
        sorted_hand = [self.hand_list[0]]
        self.hand_list.remove(sorted_hand[0])

        for card in self.hand_list:
            for sorted_index in range(len(sorted_hand)):
                if card.sort_value < sorted_hand[sorted_index].sort_value:
                    sorted_hand.insert(sorted_index, card)
                    break

                if sorted_index == len(sorted_hand) - 1:
                    sorted_hand.append(card)

        self.hand_list = sorted_hand

    def draw_card(self, deck, num_of_cards):
        how_many_drew = 0
        for _ in range(num_of_cards):
            deck.check_and_recycle()
            if len(deck.deck_list) != 0:
                card = deck.deck_list[0]
                deck.deck_list.remove(card)
                self.hand_list.append(card)
                how_many_drew += 1
            else:
                print("No cards left in the deck!")
                break

        if how_many_drew > 0:
            self.sort_hand()

        return how_many_drew


def ask_user_for_number(message, min, max):
    n = input(message)

    is_number = False
    while not is_number:
        try:
            n = int(n)
            if n >= min and n <= max:
                is_number = True
            else:
                n = input(message)
        except:
            n = input(message)
    return n


def deal_hands(deck):
    p1_hand = []
    p2_hand = []
    p3_hand = []
    p4_hand = []
    players_hands = [p1_hand, p2_hand, p3_hand, p4_hand]

    for _ in range(7):
        for player_count in range(4):
            card = deck.deck_list[0]
            players_hands[player_count].append(card)
            deck.deck_list.remove(card)

    p1 = Hand("Player 1", p1_hand)
    p2 = Hand("Player 2", p2_hand)
    p3 = Hand("Player 3", p3_hand)
    p4 = Hand("Player 4", p4_hand)

    return [p1, p2, p3, p4]


def setup_game():
    deck = Deck()

    players = deal_hands(deck)

    for card in deck.deck_list:
        if card.value != "Wild Card":
            deck.set_top_card(card)
            deck.remove_card_from_deck(card)
            break

    return deck, players


def is_same_colour(top_card, played_card):
    return top_card.colour == played_card.colour


def is_same_number(top_card, played_card):
    return top_card.value == played_card.value


def increase_draw_amount(draw_amount, increase):
    if draw_amount == 1:
        return increase
    else:
        return draw_amount + increase


def change_colour_player(hand, played_card):
    colours = ["Blue", "Green", "Red", "Yellow"]
    print("\n")
    hand.display_hand()
    print("\n")

    for i in range(len(colours)):
        print(f"{i + 1}: {colours[i]}")

    choice = ask_user_for_number(f"Enter choice (1-4): ", 1, 4) - 1

    played_card.set_colour(colours[choice])

    print(f"Colour changed to {colours[choice]}!")


def change_colour_npc(hand, played_card):
    colours = ["Blue", "Green", "Red", "Yellow"]

    playable_colours = []

    for card in hand.hand_list:
        if card.colour == "":
            continue
        if card.colour not in playable_colours:
            playable_colours.append(card.colour)

    if len(playable_colours) == 0:
        random_colour = colours[random.randint(0, 3)]
    else:
        random_colour = playable_colours[random.randint(
            0, len(playable_colours) - 1)]

    played_card.set_colour(random_colour)

    print(f"Colour changed to {random_colour}!")


def display_player_turn(total_turns, player, top_card, draw_amount):
    print(f"\n\n\nTurn {total_turns}")
    if len(player.hand_list) == 1:
        print(f"{player.name}'s turn - {len(player.hand_list)} card\n")
    else:
        print(f"{player.name}'s turn - {len(player.hand_list)} cards\n")

    if top_card.name == "Wild" or top_card.name == "Wild Draw":
        card_name = f"{top_card.name} ({top_card.colour})"
    else:
        card_name = top_card.name

    print(f"Top card: {card_name}\n")

    player.display_hand()
    print(f"{len(player.hand_list) + 1}: Draw Card +{draw_amount}\n")


def display_npc_turn(total_turns, player, top_card):
    print(f"\n\n\nTurn {total_turns}")
    if len(player.hand_list) == 1:
        print(f"{player.name}'s turn - {len(player.hand_list)} card\n")
    else:
        print(f"{player.name}'s turn - {len(player.hand_list)} cards\n")

    if top_card.name == "Wild" or top_card.name == "Wild Draw":
        card_name = f"{top_card.name} ({top_card.colour})"
    else:
        card_name = top_card.name

    print(f"Top card: {card_name}")


def is_move_legal(top_card, played_card):
    return top_card == "" or played_card.colour == "" or is_same_colour(top_card=top_card, played_card=played_card) or is_same_number(top_card=top_card, played_card=played_card)


def get_playable_cards(player, top_card, draw_amount):
    playable_cards = []
    if draw_amount > 1 and top_card.value == "Wild Draw":
        for card in player.hand_list:
            if card.value == "Wild Draw":
                playable_cards.append(card)

    elif draw_amount > 1 and top_card.value == "Draw":
        for card in player.hand_list:
            if card.value == "Draw":
                playable_cards.append(card)

    elif draw_amount == 1:
        for card in player.hand_list:
            if is_move_legal(top_card, card):
                playable_cards.append(card)

    return playable_cards


def players_turn(deck, player, total_turns, draw_amount, is_reversed):
    draw_card = False
    top_card = deck.get_top_card()
    turns_to_skip = 1

    display_player_turn(total_turns, player, top_card, draw_amount)

    is_move_illegal = True
    while is_move_illegal:
        choice = ask_user_for_number(
            f"Enter choice (1-{len(player.hand_list) + 1}): ",
            1,
            len(player.hand_list) + 1) - 1

        if choice == len(player.hand_list):
            draw_card = True
            break

        played_card = player.get_card(choice)

        if draw_amount > 1 and top_card.value == "Wild Draw" and played_card.value != "Wild Draw":
            continue
        elif draw_amount > 1 and top_card.value == "Draw" and played_card.value != "Draw":
            continue
        else:
            if is_move_legal(top_card, played_card):
                is_move_illegal = False
                break

    if draw_card:
        how_many_drew = player.draw_card(deck, draw_amount)

        if how_many_drew == 0:
            print(f"{player.name} couldn't draw any cards!")
        elif how_many_drew == 1:
            print(f"{player.name} drew 1 card!")
        else:
            print(f"{player.name} drew {how_many_drew} cards!")
        draw_amount = 1
    else:
        player.remove_card(played_card)

        print(f"\n{player.name} played a {played_card.name}!")

        if played_card.value == "Wild":
            change_colour_player(player, played_card)
        elif played_card.value == "Wild Draw":
            change_colour_player(player, played_card)
            draw_amount = increase_draw_amount(draw_amount, 4)
        elif played_card.value == "Draw":
            draw_amount = increase_draw_amount(draw_amount, 2)
        elif played_card.value == "Reverse":
            is_reversed = not is_reversed
        elif played_card.value == "Skip":
            turns_to_skip = 2

        deck.add_to_throw_pile()
        deck.set_top_card(played_card)

    return turns_to_skip, draw_amount, is_reversed


def npc_turn(deck, player, total_turns, draw_amount, is_reversed):
    top_card = deck.get_top_card()
    turns_to_skip = 1

    display_npc_turn(total_turns, player, top_card)

    playable_cards = get_playable_cards(player, top_card, draw_amount)

    if len(playable_cards) == 0:
        how_many_drew = player.draw_card(deck, draw_amount)

        if how_many_drew == 0:
            print(f"{player.name} couldn't draw any cards!")
        elif how_many_drew == 1:
            print(f"{player.name} drew 1 card!")
        else:
            print(f"{player.name} drew {how_many_drew} cards!")
        draw_amount = 1
    else:
        choice = random.randint(0, len(playable_cards) - 1)
        played_card = playable_cards[choice]
        player.remove_card(played_card)

        print(f"\n{player.name} played a {played_card.name}!")

        if played_card.value == "Wild":
            change_colour_npc(player, played_card)
        elif played_card.value == "Wild Draw":
            change_colour_npc(player, played_card)
            draw_amount = increase_draw_amount(draw_amount, 4)
        elif played_card.value == "Draw":
            draw_amount = increase_draw_amount(draw_amount, 2)
        elif played_card.value == "Reverse":
            is_reversed = not is_reversed
        elif played_card.value == "Skip":
            turns_to_skip = 2

        deck.add_to_throw_pile()
        deck.set_top_card(played_card)

    return turns_to_skip, draw_amount, is_reversed


def main():
    deck, players = setup_game()

    total_turns = 1
    turn = 0

    is_reversed = False
    draw_amount = 1

    while True:
        player = players[turn]
        turns_to_skip = 1

        if player.name == "Player 1":
            turns_to_skip, draw_amount, is_reversed = players_turn(
                deck, player, total_turns, draw_amount, is_reversed)
        else:
            turns_to_skip, draw_amount, is_reversed = npc_turn(
                deck, player, total_turns, draw_amount, is_reversed)

        for _ in range(turns_to_skip):
            if not is_reversed:
                turn += 1

                if turn % 4 == 0:
                    turn = 0
            else:
                turn -= 1

                if turn < 0:
                    turn = 3

        total_turns += 1

        if len(player.hand_list) == 0:
            break

    print(f"\n\n\nCongratulations {player.name}!")
    print("You Win!\n")


if __name__ == "__main__":
    main()
