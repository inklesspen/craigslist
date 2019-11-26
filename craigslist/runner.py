import argparse
import discord
from .bot import bot

NEEDED_PERMISSIONS = discord.Permissions()
NEEDED_PERMISSIONS.read_messages = True
NEEDED_PERMISSIONS.send_messages = True


parser = argparse.ArgumentParser()
parser.add_argument('token')
parser.add_argument('client_id')


def runner(args: argparse.Namespace):
    url = discord.utils.oauth_url(client_id=args.client_id, permissions=NEEDED_PERMISSIONS)
    print(f'Add to a server with {url}')
    bot.run(args.token)


if __name__ == "__main__":
    args = parser.parse_args()
    runner(args)
