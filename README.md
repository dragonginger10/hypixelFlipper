# Hypixel Bazaar Flipper

## Description

This app is a basic CLI app to pull down information from the Hypixel API about the Skyblock's
Bazaar. Built using Typer and Pandas, for CLI usability and data organization respectively.

## Install

### Nix/NixOS

`nix profile install github:dragonginger10/hypixelFlipper`

### From Source 

`git clone https://github.com/dragonginger10/hypixelFlipper.git
cd ./hypixelFlipper
pip install .`

## Usage
running `flipper` will pull up a table showing information for bazaar sales with a 5% margin and 10,000 instant buys in the last week.

`flipper --help` for full all options.

## Credits

Code for DF to rich table function courtesy of [neelabalan](https://gist.github.com/neelabalan/33ab34cf65b43e305c3f12ec6db05938)

