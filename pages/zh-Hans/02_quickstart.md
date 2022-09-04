# 快速开始

## Prerequisites

### For You

You'll need to know the basic syntax of C++. For a refresher to C++, see the [C++ tutorial](https://cplusplus.com/doc/tutorial/).
So should you have successfully run LiteLoaderBDS at least one time and have skimmed the [LiteLoaderBDS documentation](https://docs.litebds.com/en/#/README) except the pages for plugin development in order to comprehense how LiteLoaderBDS works.

### For Your Computer

Currently we only support building plugins on a tiny set of platforms. If you could assist us in leveraging the supported platforms, we would sincerely appreciate it.

The platforms required is shown below:

* Windows 10 64-bit / Windows 11

The software required is shown below:

* Bedrock Dedicated Server for Minecraft [Download](https://www.minecraft.net/en-us/download/server/bedrock)
* Git [Download](https://git-scm.com/download/win)
* LiteLoaderBDS [Download](https://github.com/LiteLDev/LiteLoaderBDS/releases/latest)
* Microsoft Visual Studio 2022 (with Microsoft Visual C++) [Download](https://visualstudio.microsoft.com/vs/)

At the same time, we recommend that you install these software for better experience:

* CMake 3.21 or higher versions [Download](https://cmake.org/download/)
* C/C++ Extension Pack of Visual Studio Code
* GitHub Desktop [Download](https://desktop.github.com/)
* Minecraft Bedrock Edition
* Visual Studio Code [Download](https://code.visualstudio.com/download)

What's more, we highly recommend that you register a GitHub account, not only for writing the plugin but also for optimizing your future coding experience.

## Create Your First Plugin

Now that you have got the development environment ready, it is time that you create your first plugin from scratch.

1. Get the repository URL
    * If you would like to host your code on GitHub, visit [the plugin template repository](https://github.com/LiteLDev/PluginTemplate-cpp) and click the button with text "Use this template", then filling in the form to create your plugin repository.
    Then copy the URL of your repository.

    * If you would just like to develop locally, copy `https://github.com/LiteLDev/PluginTemplate-cpp` to your clipboard.

2. Clone the repository
    * Open PowerShell or Command Prompt where you would like to put the repository, and then run `git clone <repository URL>`.
    Note that you should replace the tag `<repository URL>` with the URL you copied in the previous step.

    * Run `git submodule init` to initialize the SDK.

3. Configure the plugin
    * Modify the configurations in **/src/Version.h** according to the instructions inside the file.
    Remember to delete the line starting with `static_assert`.

4. Build the plugin
    * If you would like to build with CMake in Visual Studio Code **(recommended)**, simply open the repository directory in Visual Studio Code, choose **Release** build variant (or others as you like), and click **Build**.
    Then the plugin will be generated in **/build/Release/Plugin.dll** (or others depending on the build variant you chose).

    * If you would like to build with CMake directly, create the directory **/build/**. Then open PowerShell or Command Prompt in **/build/** and run `cmake .. && cmake --build . -j`.
    Then the plugin will be generated as **/build/Plugin.dll**.

    * If you would like to build with Microsoft Visual Studio, open the repository directory in Microsoft Visual Studio, click **Build** -> **Build All** or just press `Ctrl` + `Shift` + `B` to build.
    Then the plugin will be generated as **/out/x64-Debug/Plugin.dll**.

5. Run your plugin
    * Copy the **Plugin.dll** generated in the previous step to the **/plugin/** directory of the BDS directory (if not found, you should apply LiteLoaderBDS to BDS first. Please refer to [the instructions](https://docs.litebds.com/en/#/Usage)).
    * Run **/bedrock_server_mod.dll** in the BDS directory.

6. Observe the plugin behavior
    * Now you can see the text `Hello, world!` shown on the terminal.
    Congratulations to you for successfully creating your first plugin!

## Make Furthur Modifications

I bet you not satisfied with just a hello-world trick, which can be easily implemented by any C or C++ program, so let's do some further work.

There exists a question in refreshers' mind: how to **interact** with the Minecraft world when something **happens**?

Well, this question is exactly the meaning of a LiteLoaderBDS plugin.

To go into details, let's break the question into two parts, which have been marked out, and discuss the solutions of each part.

First, the interaction with the Minecraft world.
LiteLoaderBDS provides plentiful APIs performing operations to the world directly.
Via these APIs, you can get an entity or a block, set a block, or run a line of command.
However, the definitions of these APIs are not collected in a single header file, but splitted into multiple classes.
You can refer to **/SDK/Header/GlobalServiceAPI.h** to see the classes containing these APIs.
In this article, we will use the **Level** class, the most common class for plugin development.

Second, the watcher on the occurrence of some events.
Though BDS has not provided any event related APIs like those in GameTest, we hooked some common events for you.
To check out all of them, you can have a glance at **/SDK/Header/EventAPI.h**.
In this article, we will use the **PlayerJoinEvent**.

Following the instructions below, you will create a plugin giving every player an emerald and show welcome banner on every player's screen when they join the game as well as showing the latest joined player's name when someone types command `latest`.
Are you ready?
Let's start.

Open **/src/Plugin.cpp**, and follow instructions below.

1. Include necessary headers.

```cpp

#include <string>

#include <MC/CommandOrigin.hpp>
#include <MC/CommandOutput.hpp>
#include <MC/ItemStack.hpp>
#include <MC/Level.hpp>
#include <MC/Player.hpp>
#include <MC/Types.hpp>

#include <DynamicCommandAPI.h>
#include <EventAPI.h>
#include <GlobalServiceAPI.h>

```

So many headers, right?
To better manage them, we recommend that you include a new header if and only if the type of some variables or constants is defined in the header, or without including the header, your plugin cannot be built.
Meanwhile, you should group these headers.
One possible policy is grouping headers started with **MC/** into a group, STL headers into another group, and all other headers into the final group .

2. Define the global variables.

```cpp

std::string latest_player_xuid;

```

This variable is used to store the XUID of the latest joined player.

3. Listen to the event.
Code below should be placed in the **PluginInit()** function.

```cpp

Event::PlayerJoinEvent::subscribe([](const Event::PlayerJoinEvent& event) {
  // Give the item to the player
  auto* item = ItemStack::create("minecraft:emerald", /* count = */ 1);
  event.mPlayer->giveItem(item);

  // Show banner on every player's screen
  auto all_player_list = Level::getAllPlayers();
  for (auto* player : all_player_list) {
    player->sendTitlePacket(
      event.mPlayer->getRealName() + "joined",
      TitleType::SetTitle,
      /* FadeInDuration = */ 1,
      /* RemainDuration = */ 3,
      /* FadeOutDuration = */ 1
    )
  }

  return true;
});

```

In this piece of code, we subscribe to PlayerJoinEvent with a anonymous callback function.

In the callback function, we firstly create an item stack, which representing a collection of identical items that can be picked up at a time, whose identifier is `minecraft:emerald` and whose stack count is one.
Then we directly extract the player from the event object and give the player the item stack.

Then we attempt to get all players, iterating over all of them and sending the newly joined player's name to them as titles.

Finally, we return true, indicating that the player can join the server.
Otherwise, if we return false, the player will be rejected from the server.
(If you are creative and sharp enough, you may come up with the idea that these feature can be used to create a customized whitelist rule set.)

4. Register the command
Code below should be placed in the **PluginInit()** function.

```cpp

DynamicCommand::setup(
  /* name = */ "latest",
  /* description = */ "Get latest player.",
  /* enums = */ {},
  /* params = */ {},
  /* overloads = */ {
    {},
  },
  /* callback = */ [](
    DynamicCommand const& command,
    CommandOrigin const& origin,
    CommandOutput& output,
    std::unordered_map<std::string, DynamicCommand::Result>& results
  ) {
    output.success(
      std::string("The latest player's name is ") +
      Global<Level>->getPlayer(latest_player_xuid)->getRealName()
    );
  }
);

```

If you are interested in the meanings of the parameters, please refer to the DynamicCommand class.

Now you can build the plugin and test it in LiteLoaderBDS.

## Debug Your Plugin

Open the directory of your plugin in Microsoft Visual Studio, and the project will be configured automatically.

Change **Solution Explorer** to CMake target view, right click on the project, and then select **Add Debug Configuration** to create `launch.vs.json`.

Then modify the project target value to the BDS executable `bedrock_server_mod.exe`.

Press F5 to debug you plugin.

## What's Next?

If you are still confused and not ready to create a plugin on your own, please see our [tutorials](90_tutorials_index.md).

If you are interested in more advanced techniques in plugin development, please see our [guides](91_guides_index.md).

If you have doubt about certain APIs, or if you would like to know what can your plugin do with the APIs, please [lookup the classes](/en/classes.html).

If you are eager to dive into the ocean of BDS APIs, please refer to [the API reference](/api).

If you are ready to contribute to this documentation, please go to [our documentation repository](https://github.com/LiteLDev/docs-cpp), raising issues or opening pull requests.

We sincerely wish you a wonderful plugin development experience!