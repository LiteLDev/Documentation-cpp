# Overview

LiteLoaderBDS C++ plugin, in brief, is the modifier to Minecraft Bedrock Dedicated Server (BDS), providing plentiful gameplayes, game rules, and utilities in Minecraft.
In our point of view, LiteLoaderBDS C++ plugin is the most hardcore approach to interact with low-level code of BDS, which is both the most outstanding advantage and the worst drawback for developers.

For advantage, with the help of so massive APIs, you can implement all kinds of functions, whose ceiling depend on your imagination, just as a Minecraft official developer does.
(In fact, the APIs are exactly the native APIs of BDS, for they are extracted from the debugging file offered by Mojang.)

For disadvantage, due to the lack of official plugin support, we re-implemented some important APIs by some "magical" methods like Windows hook and memeory patch, making these APIs not stable enough, which may result in accidental crashes and loss of player data.

Not only the native BDS APIs (with prefix `MCAPI`) are available, but also we create some handful APIs (with prefix `LIAPI`) in place of the ridiculous ones in the native BDS APIs, aiming to give developers the greatest convenience.
If you find some native BDS APIs hard to use, please open an issue to notify us.
We will take creating corresponding APIs into consideration.

What's more, we provide various utilities, including database helper, web packet helper, permission APIs, form helper, schedule helper and so on.
We have integrate a few third-party libraries as well, for instance, the well-known Nlohmann's JSON library and the base64 library.

Then let's have a glance at a piece of code.
This piece is aimed at presenting a welcome title to newly joined players and hinting at the BDS console.

```cpp

#include <EventAPI.h>
#include <LoggerAPI.h>
#include <MC/Player.hpp>
#include <MC/Types.hpp>

void PluginInit()
{
  Logger logger;

  Event::PlayerJoinEvent::subscribe([](const Event::PlayerJoinEvent& event) {
    auto player = event.mPlayer;
    
    player->sendTitlePacket(
      "Welcome!",
      TitleType::SetTitle,
      /* FadeInDuration =  */ 1,
      /* RemainDuration =  */ 2,
      /* FadeOutDuration =  */ 1
    );

    logger.info("Player {} has joined the server.", player->getName());
  });
}

```

The program first defines a logger for printing information to the BDS console, then subscribing the Player Join Event.
Once the player (we assume his/her name is Notch) joins, the program will send a title with content "Welcome!" to the player, remaining for two seconds, and print "Player Notch has joined the server.".

If you have got ready to write a plugin, or just think the code elegant, please refer to the next page [Quickstart](02_quickstart.md) for more instructions on creating your first LiteLoaderBDS C++ plugin.