import random
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())

#Functions
def create_deck():
    deck = [(str(i), i) for i in range(1, 11)] * 4
    deck += [("Jack", 10), ("Queen", 10), ("King", 10)] * 4
    random.shuffle(deck)
    return deck

def draw_card():
    deck = create_deck()
    suit = ["Spades", "Clubs", "Hearts", "Diamonds"]
    card = deck.pop()
    return random.choice(suit), card

#Command to draw card
@bot.command()
async def drawcard(ctx):
    card_embed = discord.Embed(
        title="Drawing card",
        description="Drawing a card",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=card_embed)
    for i in range(1, 4):
        await asyncio.sleep(0.55)
        card_embed.description = f"Drawing a card{'.' * i}"
        await message.edit(embed=card_embed)
    suit, card = draw_card()
    card_embed.title = "Result"
    card_embed.description = f"Card: {card[0]} of {suit}"
    await message.edit(embed=card_embed)

#Command to play blackjack
# Command to play blackjack
@bot.command()
async def blackjack(ctx):
    await ctx.send("Let's play Blackjack! Type 'hit' to draw a card, 'stand' to end your turn, or 'quit' to end the game.")
    player_hand, dealer_hand = [], []
    player_total, dealer_total = 0, 0
    deck = create_deck()
    

    # Initial Draw
    for i in range(2):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())

    player_total = sum(card[1] for card in player_hand)
    dealer_total = sum(card[1] for card in dealer_hand)

    card_names = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}
    formatted_hand = [card_names.get(card, str(card)) for card in player_hand]
    def calculate_total(hand):
        total = sum(card[1] for card in hand)
        aces = sum(1 for card in hand if card[0] == 'Ace')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def format_hand(hand):
        return ', '.join(card[0] for card in hand)

    while True:
        await ctx.send(f"Your hand: {format_hand(player_hand)}, (total: {player_total})")
        await ctx.send(f"Dealer's hand: {dealer_hand[0][0]}")
        
        # User Input
        message = await ctx.send(f"React to hit, stand, or quit.")
        await message.add_reaction("👍")
        await message.add_reaction("🤚")
        await message.add_reaction("🛑")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ['👍', '🤚', '🛑']    

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '👍':
                new_card = deck.pop()
                player_hand.append(new_card)
                player_total = calculate_total(player_hand)
                if player_total > 21:
                    await ctx.send(f"{new_card[0]}. You've busted with {player_total}. You lost..")
                    print([player_hand])
                    break

                elif player_total == 21:
                    await ctx.send(f"{new_card[0]}! Blackjack You've won!")
                    break

            elif str(reaction.emoji) == '🤚':
                # Dealer Logic
                message2 = await ctx.send("Dealer's turn")
                for i in range(1, 4):
                    await asyncio.sleep(0.65)
                    await message2.edit(content = f"Dealer's turn{'.' * i}")
                while dealer_total < 17:
                    new_card = deck.pop()
                    dealer_hand.append(new_card)
                    dealer_total = calculate_total(dealer_hand)

                # Win Conditions
                if dealer_total > 21:
                    await ctx.send(f"Dealer busts with {dealer_total}! You win!")
                    break
                elif dealer_total > player_total:
                    await ctx.send(f"Dealer wins with {dealer_total}. You lose!..")
                    break
                elif dealer_total < player_total:
                    await ctx.send(f"The dealer had {dealer_total}! You won with {player_total}!")
                    break
                else:
                    await ctx.send(f"{format_hand(dealer_hand)}.. Push. You both have {player_total}.")
                    break

            elif str(reaction.emoji) == '🛑':
                await ctx.send("Game ended.")
                break

        except asyncio.TimeoutError:
            await ctx.send("You took too long. The game has already ended..")
            break

# Command to flip a coin
@bot.command()
async def flipcoin(ctx):
    coin_embed = discord.Embed(
        title="🪙Coin Flip",
        description="Flipping a coin",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=coin_embed)
    for i in range(1, 4):
        await asyncio.sleep(0.75)
        coin_embed.description = f"Flipping a coin{'.' * i}"
        await message.edit(embed=coin_embed)

    await asyncio.sleep(0.75)
    x = random.randint(0, 1)
    coin_embed.title = "Result🪙"
    coin_embed.description = "Heads" if x == 0 else "Tails"
    await message.edit(embed=coin_embed)

# Command to roll a dice
@bot.command()
async def rolldice(ctx):
    dice_embed = discord.Embed(
        title="🎲Rolling a Dice",
        description="Rolling a dice",
        color=discord.Color.blue()
    )
    message = await ctx.send(embed=dice_embed)
    for i in range(1, 4):
        await asyncio.sleep(0.55)
        dice_embed.description = f"Rolling a dice{'.' * i}"
        await message.edit(embed=dice_embed)

    await asyncio.sleep(0.75)
    x = random.randint(1, 6)

    dice_embed.title = "Result🎲"
    dice_embed.description = f"Rolled a **{x}**!"
    await message.edit(embed=dice_embed)