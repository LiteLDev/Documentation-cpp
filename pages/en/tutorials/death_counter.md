# Death Counter {#death_counter}

[![GitHub](https://img.shields.io/badge/GitHub-Futrime%2FLLDeathCounter-orange?style=for-the-badge&logo=github)](https://github.com/Futrime/LLDeathCounter)
[![License](https://img.shields.io/github/license/Futrime/LLDeathCounter?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter/blob/main/LICENSE)
[![Downloads](https://img.shields.io/github/downloads/Futrime/LLDeathCounter/total?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter/releases/latest)
[![Issues](https://img.shields.io/github/issues/Futrime/LLDeathCounter?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter/issues)
[![Stars](https://img.shields.io/github/stars/Futrime/LLDeathCounter?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter)

This tutorial analyze the plugin LLDeathCounter created by [Futrime](https://github.com/Futrime).
For full code, visit [the repository](https://github.com/Futrime/LLDeathCounter).

LLDeathCounter is a plugin recording the number of player deaths, presenting them on the escape menu.

This plugin is too simple to use more than one file, so all code is written in `/src/Plugin.cpp`.

## Include Necessary Headers

The headers in need are:

* EventAPI.h
* ScheduleAPI.h
* MC/Scoreboard.hpp

At the same time, we should include some other headers to ensure every type parsed.

All `#include` lines are:

```cpp
#include <EventAPI.h>
#include <ScheduleAPI.h>

#include <MC/Objective.hpp>
#include <MC/Player.hpp>
#include <MC/Scoreboard.hpp>
#include <MC/Types.hpp>
#include <string>
```

## Initialize the Plugin

When LiteLoaderBDS starts, the `PluginInit()` function of each plugin will be called.
You can treat it as the `main()` function in a normal C++ program, but for a plugin.
But you should take special care that in `PluginInit()` function you **CANNOT access any API related to the game**, which is likely to cause SEH exception, for the plugins are intialized before the game loads.

If you would like to do some setup jobs on objects of the game, you ought to put the code in the callback of `ServerStartedEvent` , which will execute as soon as the game loads.

We assume that you have mastered the usage of `scoreboard` command and the scoreboard mechanism of Minecraft.
If you are confused about this, please visit [Minecraft Wiki](https://minecraft.fandom.com/wiki/Scoreboard) for further information.

In function `PluginInit()`:

```cpp
Event::ServerStartedEvent::subscribe([](const Event::ServerStartedEvent& event) {
  auto* objective = Scoreboard::newObjective("lldeathcounter", "Death Count");
  objective->setDisplay(/*slotName=*/"list",
                        /*sort=*/ObjectiveSortOrder::Descending);
  return true;
});
```

Here we use the read-only subscription method in order to optimize the performace as well as prevent accidentally modification to the event.

```cpp
Event::ServerStartedEvent::subscribe([](const Event::ServerStartedEvent& event) {
  // ...
});
```

We first create a scoreboard objective, whose ID is "lldeathcounter" and display name is "Death Count".

```cpp
auto* objective = Scoreboard::newObjective("lldeathcounter", "Death Count");
```

Then we make the objective appear on the player list of the escape menu.

```cpp
objective->setDisplay(/*slotName=*/"list",
                      /*sort=*/ObjectiveSortOrder::Descending);
```

Though this event cannot be suppressed, the callback function should return a boolean value.
You can either return true or false, which does not matter.
For reviewer-friendliness, we recommend that you use `return true`.

## Add Score When Players Die

If you would like to make a player death recorder with command blocks, you have to let the command block exeucte its commands every tick to test if the player is still alive, which sounds a waste of performance and not elegant.

With the powerfull event system of LiteLoaderBDS, you can just listen to PlayerDieEvent and operate the scoreboard when the event is triggered.

You can subscribe to an event anywhere, anytime, and unsubscribe it by calling `listener.remove()` anywhere, anytime.
However, we recommend putting the creation of subscriber in `PluginInit()` function, making your code easier to understand.

In function `PluginInit()`:

```cpp
Event::PlayerDieEvent::subscribe([](const Event::PlayerDieEvent& event) {
  Scoreboard::addScore("lldeathcounter", event.mPlayer, 1);
  return true;
});
```

When the event is triggered, the plugin simply add one score to the scoreboard with ID "lldeathcounter" of the player and return true.

## Compile and Run

Now you can compile the plugin and put the DLL file of your plugin to `/plugins/` directory of BDS.
If you can see the menu like this, you've made it.

![The death count menu](../images/tutorial_death_counter_01.png)