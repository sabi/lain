import os
import json
import click
import requests

lain_version = '0.1.0'


def ensure_exists(path):
    """Ensure that the file or directory at the given path exists.
    If it doesn't exist, create it.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def get_webhooks_dir():
    """Get the directory to use for the webhooks file.
    If the user has permission to edit /opt/sabi, use /opt/sabi.
    Otherwise, use a config file in their home directory.
    """
    opt_sabi_dir = '/opt/sabi/lain'
    if os.path.exists(opt_sabi_dir) and os.access(opt_sabi_dir, os.W_OK):
        return opt_sabi_dir
    home_dir = os.path.expanduser('~')
    config_dir = os.path.join(home_dir, '.config/lain')
    return config_dir


@click.group()
def lain():
    pass


# lain add
@lain.command()
@click.option('--channel', help='Name of the channel to add.')
@click.option('--url', help='URL to associate with the channel.')
def add(channel, url):
    """Add a Discord channel to manifest"""
    webhooks_dir = get_webhooks_dir()
    webhooks_file = os.path.join(webhooks_dir, 'webhooks')
    ensure_exists(webhooks_dir)
    webhooks = {}
    if os.path.exists(webhooks_file):
        with open(webhooks_file, 'r') as f:
            webhooks = json.load(f)
    webhooks[channel] = url
    with open(webhooks_file, 'w') as f:
        json.dump(webhooks, f)
    click.echo(f"Added {channel} with URL {url} to webhooks.")


# lain delete
@lain.command()
@click.option('--channel', help='Name of the channel to delete.')
def delete(channel):
    """Delete a Discord channel from manifest"""
    webhooks_dir = get_webhooks_dir()
    webhooks_file = os.path.join(webhooks_dir, 'webhooks')
    ensure_exists(webhooks_dir)
    webhooks = {}
    if os.path.exists(webhooks_file):
        with open(webhooks_file, 'r') as f:
            webhooks = json.load(f)
    if channel in webhooks:
        del webhooks[channel]
        with open(webhooks_file, 'w') as f:
            json.dump(webhooks, f)
        click.echo(f"Deleted {channel} from webhooks.")
    else:
        click.echo(f"{channel} not found in webhooks.")


@lain.command()
@click.option('--channel', help='Name of the channel to send the message.')
@click.option('--msg', help='Message to send to the channel URL.')
@click.option('--img', help='Path to the image file to send.')
def img(channel, msg, img):
    """Send an image to a Discord channel with optional text"""
    webhooks_dir = get_webhooks_dir()
    webhooks_file = os.path.join(webhooks_dir, 'webhooks')
    ensure_exists(webhooks_dir)
    image_path = os.path.expanduser(img)  # expand tilde
    if not os.path.exists(webhooks_file):
        click.echo("No webhooks found.")
        return
    with open(webhooks_file, 'r') as f:
        webhooks = json.load(f)
    if channel in webhooks:
        url = webhooks[channel]
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                data = {'content': msg}
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                click.echo(f"Sent image to {channel}: {image_path}")
        except requests.exceptions.RequestException as e:
            click.echo(f"Failed to send image to {channel}: {e}")
    else:
        click.echo(f"{channel} not found in webhooks.")


# lain ls
@lain.command()
def ls():
    """List available Discord channels"""
    webhooks_dir = get_webhooks_dir()
    webhooks_file = os.path.join(webhooks_dir, 'webhooks')
    ensure_exists(webhooks_dir)
    if not os.path.exists(webhooks_file):
        click.echo("No webhooks found.")
        return
    with open(webhooks_file, 'r') as f:
        webhooks = json.load(f)
    channels = list(webhooks.keys())
    click.echo(f"Channels: {', '.join(channels)}")


# lain msg
@lain.command()
@click.option('--channel', help='Name of the channel to send the message.')
@click.option('--msg', help='Message to send to the channel URL.')
def msg(channel, msg):
    """Send a message to a Discord channel"""
    webhooks_dir = get_webhooks_dir()
    webhooks_file = os.path.join(webhooks_dir, 'webhooks')
    ensure_exists(webhooks_dir)
    if not os.path.exists(webhooks_file):
        click.echo("No webhooks found.")
        return
    with open(webhooks_file, 'r') as f:
        webhooks = json.load(f)
    if channel in webhooks:
        url = webhooks[channel]
        try:
            response = requests.post(url, data={'content': msg})
            response.raise_for_status()
            click.echo(f"Sent message to {channel}: {msg}")
        except requests.exceptions.RequestException as e:
            click.echo(f"Failed to send message to {channel}: {e}")
    else:
        click.echo(f"{channel} not found in webhooks.")


@lain.command()
def version():
    """Display the current version"""
    click.echo(f"Version {lain_version}")


if __name__ == "__main__":
    lain()
