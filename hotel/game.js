"use strict";
var Hotel = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // play-entry.ts
  var play_entry_exports = {};
  __export(play_entry_exports, {
    TIME_LABEL: () => TIME_LABEL,
    applyChoice: () => applyChoice,
    getScene: () => getScene,
    initialState: () => initialState,
    resetRun: () => resetRun,
    resolveChoices: () => resolveChoices,
    resolveText: () => resolveText,
    wakeFromDeath: () => wakeFromDeath
  });

  // src/lib/game/story.ts
  var scenes = {};
  function add(scene) {
    scenes[scene.id] = scene;
  }
  function getScene(id) {
    return scenes[id] ?? scenes.wake;
  }
  var go = (id, label, extra = {}) => ({
    id,
    label,
    to: extra.to ?? id,
    ...extra
  });
  add({
    id: "wake",
    location: "Room 204",
    art: "/art/room.jpg",
    speaker: "jack",
    time: "dawn",
    text: (s) => {
      if (s.deaths === 0) {
        return `I woke up in a bed that I was pretty sure wasn't mine, with a work order crumpled in my fist that I was also sure I'd never seen.

Fix what breaks. Don't ask questions. Then do it all again.

The paper felt too real. The room was a pastel nightmare with a damp bloom in the corner \u2014 rising, not leaking. Someone needed to find the source or they'd be painting over it every spring until they died.

Last night I'd been at Taverners. Then the Bushmills. Then nothing. And now a cheerful stranger was hammering on the door like she owned my name.`;
      }
      if (s.deaths === 1) {
        return `I jerked awake with headlights in my eyes. A horn. A scream of brakes. Then the lights weren't headlights at all \u2014 they were the burning orbs of a child's face, coming out of a stairwell with too many arms.

I'd died here. In this hotel. The work order was uncrumpled in my hand, and it had grown a fourth line in my own handwriting.

The basement is not on the schedule right now.

No hangover. Hands dead steady. Same damp stain. Same knock at six minutes past seven.`;
      }
      const last = s.lastDeath ? ` Last time: ${s.lastDeath}` : "";
      const extra = s.workOrder.length > 3 ? ` The work order has ${s.workOrder.length} lines now. I am becoming a connoisseur of dying.` : "";
      return `Loop ${s.loop}. Death ${s.deaths}.${last}${extra}

Same bed. Same stain. Same knock coming in three\u2026 two\u2026

I already know what she's going to say.`;
    },
    choices: (s) => [
      go("door", "Open the door", { to: "door" }),
      go("work_read", "Read the work order properly", { to: "work_read" }),
      go("stain", "Have a proper look at that damp", { to: "stain" }),
      go("stay_bed", "Stay in bed and refuse the day", { to: "stay_bed" }),
      go("skip", "Skip the script. You know the morning.", {
        to: "hub",
        time: "morning",
        set: { skipRoutine: true, didStove: true },
        when: (st) => st.deaths >= 2 && st.flags.didStove === false
      }),
      go("skip2", "Head straight out. You've done breakfast.", {
        to: "hub",
        time: "morning",
        set: { skipRoutine: true },
        when: (st) => st.deaths >= 2 && st.flags.knowBasement
      })
    ]
  });
  add({
    id: "work_read",
    location: "Room 204",
    art: "/art/room.jpg",
    speaker: "jack",
    text: (s) => s.workOrder.length === 1 ? `Three lines. Hotel stationery. Handwriting that looks suspiciously like mine, which is a sentence I do not enjoy thinking about before coffee.

Fix what breaks. Don't ask questions. Then do it all again.

If this is a callout, it's the worst brief I've ever been given. If it's a philosophy, it's the last six months of my life printed on nice paper.` : `The list has been growing. Every line after the first three is a thing I learned by having something appalling happen to me.

${s.workOrder.map((line, i) => `${i + 1}. ${line}`).join("\n")}

I would like, just once, a hint in advance of my horrible murder.`,
    choices: [
      go("door", "Open the door", { to: "door" }),
      go("stain", "Check the stain", { to: "stain" }),
      go("stay_bed", "Stay put", { to: "stay_bed" })
    ]
  });
  add({
    id: "stain",
    location: "Room 204",
    art: "/art/room.jpg",
    speaker: "jack",
    text: `No run. No tail. Rising. Something behind the plaster is being patient about it.

I have told nine different customers the same sentence: buildings don't complain where it hurts. They complain where they're thinnest.

If four people are holding four corners of a place and you still get a stain like this, it isn't the legs. It's that there's more coming down on them than four legs' worth.`,
    choices: (s) => [
      go("door", "Answer the door", { to: "door" }),
      go("cupboard_early", "Go find whatever list this place keeps", {
        to: "cupboard",
        when: (st) => st.deaths >= 3
      }),
      go("stay_bed", "Ignore the knock", { to: "stay_bed" })
    ]
  });
  add({
    id: "stay_bed",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `"Jack! You're late again! Brig's going mental. And the lobby's already trying to eat the carpet!"

A pause. For Trudie Crisp that is roughly a fortnight.

"You know?" she says, when I tell her I know. Then, on schedule, to two inches of painted pine: "Ooh, bed hair! Very rugged."

The handle turns. She pours into the room like water out of a jug.`,
    choices: [
      go("stay_room", "Let her in and start asking questions", {
        to: "stay_room",
        time: "morning"
      }),
      go("door", "Fine. Work. Drag me.", { to: "corridor", time: "dawn" })
    ]
  });
  add({
    id: "door",
    location: "Second-floor corridor",
    art: "/art/corridor.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: (s) => s.deaths === 0 ? `"Jack! You're late again!"

Blue-green hair. Every piercing in the world. A name tag doing heroic work at altitude. Trudie Crisp grabs my wrist with a slightly tacky hand and hauls me into the hall before I can find my boots.

"Ooh, bed hair! Very rugged. I'd tell you not to worry because nobody important's going to see you, but I'm going to see you, and I'm extremely important."

There is something wrong with the light. Translucent ripples run through her as if she isn't entirely solid.` : `"Jack! You're late again! Brig's going mental. And the lobby's already trying to eat the carpet!"

Word for bloody word. I mouth carpet along with her, half a beat behind, like karaoke to a song I hate.

She does not notice.`,
    choices: [
      go("corridor", "Let her drag you", { to: "corridor" }),
      go("thank_early", "Catch her wrist. Say thank you.", {
        to: "corridor_thank",
        set: { thankedTrudie: true },
        when: (s) => s.deaths >= 1
      })
    ]
  });
  add({
    id: "corridor",
    location: "Toward the lobby",
    art: "/art/corridor.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `"And then the Rulekeeper showed up again during the night shift, which is just rude, you know? I told him the carpets were fine, but he's always so dramatic about the east wing. Brig says it's because he's got a thing for dramatic entrances. Ione's already patched three new tears. Stay out of her way until she's had silk tea. Is silk tea a thing?"

Spore counts. The Stayover in the basement. Register names flickering. She talks like we've done this for years.

I have never seen this woman before in my life.`,
    choices: [go("lobby", "Follow her into the lobby", { to: "lobby" })]
  });
  add({
    id: "corridor_thank",
    location: "Toward the lobby",
    art: "/art/corridor.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `Her wrist is cool and does not warm up. Color comes up her throat in a slow pink tide. Ripples run out from my fingers like I'd dropped a stone in the pond that is her.

"Well, oh my. You're quick today, slowpoke."

A spoon will be thrown at my head for this later. I decide it's worth it.`,
    choices: [go("lobby", "Keep walking", { to: "lobby" })]
  });
  add({
    id: "lobby",
    location: "The lobby",
    art: "/art/lobby.jpg",
    speaker: "jack",
    text: `Pastel walls. Brass gone soft and gold where a hundred years of hands have landed. A leather-bound register open on the desk, names surfacing and sinking like something turning over in its sleep.

And the carpet near the far wall is bubbling. Properly fizzing. Dark patches spreading like mold in fast-forward.

Trudie does not appear to mind.

From the kitchen, a growl: "Trudie! If that waste-of-skin handyman is late again I'm going to spank his ass myself!"`,
    choices: [
      go("kitchen", "Get dragged into the kitchen", { to: "kitchen" }),
      go("register_peek", "Look at the register first", {
        to: "register",
        set: { sawRegister: true },
        when: (s) => s.deaths >= 2
      })
    ]
  });
  add({
    id: "kitchen",
    location: "The kitchen",
    art: "/art/kitchen.jpg",
    portrait: "/art/brig.jpg",
    speaker: "brig",
    time: "morning",
    text: (s) => s.deaths === 0 ? `Ears. Actual pointed furry ears. Impossibly sharp teeth. A white chef's jacket straining over a body that could bench a truck, and a tail lashing behind her.

"You. Late again. What's your excuse this time, Causey?"

A cutting board and vegetables hit my chest. "Uniform dice. If I see one uneven I'm using your fingers for stock."

The flames around her flare higher than physics allows. This is not a costume.` : `"You. Late again. What's your excuse this time, Causey?"

I could tell her about the stove before I've looked at it. I could ask how long I've worked here. Last time, "since always" was the whole of the answer, and the question slid off her like rain off brass.`,
    choices: (s) => [
      go("kitchen_chop", "Take the knife. Chop.", { to: "kitchen_chop" }),
      go("kitchen_stove", "The stove's the job. You can smell it.", {
        to: "kitchen_stove"
      }),
      go("kitchen_ask", "Ask how long you've worked here", {
        to: "kitchen_ask",
        when: (st) => st.deaths >= 1
      })
    ]
  });
  add({
    id: "kitchen_chop",
    location: "The kitchen",
    art: "/art/kitchen.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `I am not a cook. I fix pipes. Trudie plucks the knife away with a wink.

"Let me, Jack. What Brig really needs you for is the big stove. Flames going weird colors. Wards running hot. You know how it gets when it's in one of its moods."

"The oven gets moods?"

"Bit like Brig. Loud, hot, and sulks if you ignore it."

"Say that again, Trudie, and you're going in the stew as thickener."`,
    choices: [go("kitchen_stove", "Go to the stove", { to: "kitchen_stove" })]
  });
  add({
    id: "kitchen_ask",
    location: "The kitchen",
    art: "/art/kitchen.jpg",
    portrait: "/art/brig.jpg",
    speaker: "brig",
    text: `"Since always," Brig says.

"How long is always? What was the date?"

I watch the question go into their ears and their brains agree to do nothing with it. Behind their eyes my words just\u2026 slide off.

"The third fitting," she says eventually, like each word is being extracted under anesthetic. "I may have had my eye on it. Stop poncing about and fix it, Causey."`,
    choices: [go("kitchen_stove", "Fix the stove", { to: "kitchen_stove" })]
  });
  add({
    id: "kitchen_stove",
    location: "The range",
    art: "/art/kitchen.jpg",
    speaker: "jack",
    text: (s) => `The toolkit arrives in my hand. ${s.deaths === 0 ? "When the hell did I pick that up?" : "This time I see it pop into existence. Spatial inventory. Brilliant. I have questions for a suggestion box that does not exist."}

Ancient cast iron. Dials older than God. Flames flickering from honest orange to sickly green-black. The air smells like burning herbs and rot.

My hands know the third fitting on the left-hand pressure feed. They always know.

Brig's tail lashes. Trudie dices at the far station, and the air in the gap between them goes milky, like breath on a cold morning.`,
    choices: [
      go("stew", "Finish the repair", {
        to: "stew",
        set: { didStove: true }
      }),
      go("oven_touch", "While you're here \u2014 oil the squeaky little oven", {
        to: "death_oven",
        when: (s) => !s.flags.knowOvens
      }),
      go("brig_deep", "Take the housing plate off. Look at the ward.", {
        to: "brig_ward",
        when: (s) => s.flags.intimacyTrudie || s.deaths >= 4
      })
    ]
  });
  add({
    id: "stew",
    location: "The kitchen",
    art: "/art/kitchen.jpg",
    portrait: "/art/brig.jpg",
    speaker: "brig",
    text: (s) => `A bowl hits the bench. No chip in it. ${s.flags.complimentBrig ? 'She sees me check. "It was the nearest fucking bowl."' : "Trudie stage-whispers that it was never the nearest bowl."}

The stew is stupidly good. Warm, rich, a spice kick that would clear a hangover if I still had one.

"You're being far quieter than usual," Brig says. "Usually you've got some smartass remark by now."

"I don't really know what I'm doing here."

She snorts. "Funny. You say that every few days."`,
    choices: [
      go("hub", "Get out of her kitchen and earn your salary", {
        to: "hub",
        time: "morning"
      }),
      go("compliment", "Tell her the spice is tempered with something sweet", {
        to: "hub",
        time: "morning",
        set: { complimentBrig: true }
      })
    ]
  });
  add({
    id: "hub",
    location: "Hotel Sans Nuit",
    art: "/art/lobby.jpg",
    speaker: "jack",
    text: (s) => {
      const bits = [
        `Loop ${s.loop}. ${s.time === "three" ? "The cold is in the building." : s.time === "noon" ? "The light outside has gone thick and gold." : s.time === "evening" ? "The brass has started to go honey." : "The hotel is waiting to see what kind of idiot I am today."}`
      ];
      if (s.flags.knowBasement && !s.flags.avoidedThree && s.time !== "three") {
        bits.push("Three o'clock is coming. Something drags under the floor when it does.");
      }
      if (!s.flags.helpedLobby) {
        bits.push("Somewhere below, the lobby carpet is having opinions.");
      }
      return bits.join(" ");
    },
    choices: (s) => {
      const c = [];
      if (!s.flags.didStove && (s.time === "dawn" || s.time === "morning")) {
        c.push(go("kitchen", "Back to the kitchen", { to: "kitchen" }));
      }
      c.push(
        go("lobby_help", "Help Trudie with the lobby seals", {
          to: "lobby_help",
          when: () => !s.flags.helpedLobby && s.time !== "night"
        })
      );
      c.push(
        go("stay_room", "Refuse the day. Stay in 204.", {
          to: "stay_room",
          when: () => s.time === "dawn" || s.time === "morning"
        })
      );
      c.push(
        go("ione_meet", "Second floor. Ione.", {
          to: "ione_meet",
          when: () => s.time !== "night"
        })
      );
      c.push(
        go("conservatory", "Try the conservatory", {
          to: s.time === "noon" ? "death_spores" : "conservatory"
        })
      );
      c.push(
        go("basement", "Follow the damp down the service stairs", {
          to: "basement",
          when: () => !s.flags.knowBasement || s.time === "three"
        })
      );
      c.push(
        go("stairs_dark", "Take the unlit stairs", {
          to: "death_rulekeeper",
          when: () => !s.flags.didLight && !s.flags.knowStairs
        })
      );
      c.push(
        go("job_light", "Fix the stairwell bulb first", {
          to: "job_light",
          when: () => !s.flags.didLight
        })
      );
      c.push(
        go("job_pipe", "There's a leaky pipe that wants a hand", {
          to: "job_pipe",
          when: () => !s.flags.didPipe && s.time !== "night"
        })
      );
      c.push(
        go("cupboard", "Read the linen cupboard door properly", { to: "cupboard" })
      );
      c.push(
        go("register", "Stand behind the reception desk", {
          to: "register",
          set: { sawRegister: true }
        })
      );
      c.push(
        go("dumbwaiter", "Check that rattling dumbwaiter", {
          to: "death_dumbwaiter",
          when: () => !s.flags.knowDumbwaiter
        })
      );
      c.push(
        go("ladder", "Get the stepladder out. Be useful.", {
          to: "ladder",
          when: () => s.flags.intimacyTrudie && !s.flags.knowLadder
        })
      );
      c.push(
        go("mirror", "Have a celebratory shave", {
          to: "death_mirror",
          when: () => (s.time === "evening" || s.flags.avoidedThree) && !s.flags.knowMirrors
        })
      );
      c.push(
        go("wait_three", "Hold still and let three o'clock pass", {
          to: "wait_three",
          when: () => s.time !== "evening" && s.time !== "night" && s.time !== "three" && s.flags.knowBasement
        })
      );
      c.push(
        go("leland", "Be in the lobby at half four", {
          to: "leland",
          when: () => s.flags.avoidedThree || s.time === "evening" || s.deaths >= 5
        })
      );
      c.push(
        go("front", "Open the front door", {
          to: s.time === "noon" ? "death_spores" : s.time === "night" ? "fountain_night" : "front_day"
        })
      );
      c.push(
        go("boiler", "The boiler room. Under the east end.", {
          to: "boiler",
          when: () => s.flags.gatList || s.flags.knowsVacancy
        })
      );
      c.push(
        go("apply", "Put your name under Innkeeper", {
          to: "apply",
          when: () => s.flags.sawPlate && !s.flags.applied
        })
      );
      return c;
    }
  });
  add({
    id: "lobby_help",
    location: "The lobby",
    art: "/art/lobby.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    time: "morning",
    text: `"Look!" She pats the floor like a well-behaved dog. "I think it likes you today. It's barely even fizzing."

A compliment about her work lands harder than one about her ass. She goes a shameless rose color and the edges of her go vague, as if her outline is the first thing she stops bothering with when she's pleased.

I have a cheat sheet for a woman who meets me fresh every morning. The queasy feeling attached to that is doing some work.`,
    choices: [
      go("hub", "Leave her to finish. The lobby is hers.", {
        to: "hub",
        time: "noon",
        set: { helpedLobby: true, indoorNoon: true },
        addRule: "The lobby is Trudie's. Let her finish."
      }),
      go("trudie_flirt", "Stay on your knees and keep talking", {
        to: "stay_room",
        set: { helpedLobby: true }
      })
    ]
  });
  add({
    id: "job_pipe",
    location: "Service corridor",
    art: "/art/corridor.jpg",
    speaker: "jack",
    text: `Muscle memory. Washer, compression, wipe. The leak stops like it was waiting for me.

My hands have been in this hotel longer than I have. That is not a comforting sentence.`,
    choices: [
      go("hub", "On to the next disaster", {
        to: "hub",
        set: { didPipe: true },
        time: "morning"
      })
    ]
  });
  add({
    id: "job_light",
    location: "The stairwell",
    art: "/art/corridor.jpg",
    speaker: "jack",
    text: `Twenty to eight. Trudie holds the ladder and provides color commentary on my behind. The bulb goes in. The dark on the stairs has one less excuse.

"No stairs in the dark" cannot catch me if there is no dark. I am a genius. I will still die of something else, but I am a genius.`,
    choices: [
      go("hub", "That's one rule handled", {
        to: "hub",
        set: { didLight: true, knowStairs: true },
        time: "morning"
      })
    ]
  });
  add({
    id: "wait_three",
    location: "The lobby",
    art: "/art/lobby.jpg",
    speaker: "jack",
    time: "three",
    text: `The temperature drops like someone kicked me into a deep freeze. Lights flicker. A dragging sound goes past under the floor, wet and unhurried, nine or ten seconds of it.

I do not follow it.

When I keep my nose out of things that have nothing to do with me, no spectral horrors appear to eat me. I will call that winning.

Trudie chatters on, magnificently unbothered, perfectly on script.`,
    choices: [
      go("hub", "You lived through three o'clock", {
        to: "hub",
        time: "evening",
        set: { avoidedThree: true }
      }),
      go("leland", "Stay until the postman", { to: "leland", time: "evening" })
    ]
  });
  add({
    id: "basement",
    location: "Service stairwell",
    art: "/art/basement.jpg",
    speaker: "jack",
    text: `Black mold in patterns that look like handprints. The basement door is cracked. A child's voice whispers up.

"Stay\u2026 with us\u2026"

Every sensible part of me would like to go back upstairs. The rest of me has always been employed as a handyman.`,
    choices: [
      go("death_basement", "Peer through the door", { to: "death_basement" }),
      go("hub", "The work order was very clear. Leave.", {
        to: "hub",
        when: (s) => s.flags.knowBasement
      })
    ]
  });
  add({
    id: "death_basement",
    location: "The basement",
    art: "/art/basement.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "The Stayover opened you like a can.",
      rule: "The basement is not on the schedule right now."
    },
    text: `Something pale and wrong comes out of the dark. Too many arms and legs. A crying child's face. Grief and rot.

I do not even have time to scream. Pain explodes across my chest, my throat, my guts. Things that did not want to meet the air are introduced to it anyway.

The last thing in my head is Trudie's filthy grin.

Then nothing.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "death_rulekeeper",
    location: "The dark stairs",
    art: "/art/corridor.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "The Rulekeeper filed you under subsection nine.",
      rule: "No stairs in the dark."
    },
    text: `Somewhere above, a pen clicks.

The rejection that comes down the stairwell makes the basement feel like central heating. A long coat. A clipboard. A face made of every school report I ever received.

"Ah," I say. "The stairs. In the dark. That's going to turn out to be a big no-no, isn't it?"

The second death is quicker. The last thought is: fine. Now I know.

This hotel had better have a suggestion box.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "death_spores",
    location: "Outside",
    art: "/art/conservatory.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "You took a lungful of noon.",
      rule: "Noon is indoors o'clock."
    },
    text: `Golden air. Shimmery motes like the world's laziest snow. I take a big appreciative breath.

My lungs fill with angry wolverine.

I crawl back through the side door coughing lumps of myself onto the floral runner. On the landing above, a pale woman with knitting needles in her hair watches me drown on dirty air, makes a note, and goes back to stitching a tear in the wall itself.

She is, I cannot help observing, extremely pretty.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "death_oven",
    location: "The kitchen",
    art: "/art/kitchen.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "The big stove toasted you for touching its cousin.",
      rule: "Don't touch the ovens unless invited."
    },
    text: `"Oh no, you didn't."

There is something in Brig's voice I have not heard before. I will later identify it as the hellhound version of sympathy.

The big stove swings its door open all on its own. The flame comes out and toasts me but good.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "death_dumbwaiter",
    location: "The shaft",
    art: "/art/corridor.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "The counterweight took the top of your head off.",
      rule: "Honestly\u2026"
    },
    text: `I look into the shaft to find out what the rattling is.

The counterweight explains.

The work order, when I next see it, will just say: Honestly\u2026`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "death_mirror",
    location: "Room 204",
    art: "/art/room.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "Your reflection finished the shave.",
      rule: "Mirrors are for the morning."
    },
    text: `Half six. Celebratory shave. I am Travolta-ing about the room because I have survived most of a day.

My reflection is not grinning. It has stopped shaving and is still holding the razor.

It leans forward through the glass.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "ladder",
    location: "The landing",
    art: "/art/corridor.jpg",
    speaker: "jack",
    text: `There is a bar at the back of a stepladder. Every handyman who's lasted a fortnight has a ritual: boot on the bottom step, lean, wait for the click.

I have done that forty thousand times.

This morning I think about Trudie, take my boot off, and start climbing anyway.`,
    choices: [
      go("death_ladder", "Keep climbing. You're fine.", { to: "death_ladder" }),
      go("hub", "Get down. Check the bar, you clown.", {
        to: "hub",
        set: { knowLadder: true },
        addRule: "Check the bar, you absolute clown.",
        when: (s) => s.flags.knowLadder === false
      })
    ]
  });
  add({
    id: "death_ladder",
    location: "The landing",
    art: "/art/corridor.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "The wainscot took the back of your head off.",
      rule: "Check the bar, you absolute clown."
    },
    text: `The ladder goes out from under me around the fourth step.

The part of me that has been listening for that click since I was nineteen finally gets a word in. I get about a fifth of a second to be embarrassed.

Then the corner of the wainscot comes up.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "death_carpet",
    location: "The lobby",
    art: "/art/lobby.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "The carpet ate you. Whole.",
      rule: "The lobby is Trudie's. Let her finish."
    },
    text: `I sit down on the lobby carpet like the dumbwaiter has taken my head off again.

The carpet, bless it, doesn't even bubble. Not for five seconds.

Then a warm wet feeling closes around my legs.

The last thing I hear, as the chintziest Venus flytrap in England closes over my face, is the postman dealing another envelope.

"Four thirty every day, Jack Causey. Same time tomorrow?"`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "conservatory",
    location: "The glass house",
    art: "/art/conservatory.jpg",
    speaker: "jack",
    text: `Sorrel's corner. Things growing that eat what comes in on the air. They are not lovely.

The door does not open. G.A.T.'s list said she won't answer. Knock anyway.

I knock. Something on the other side of the glass considers me the way a greenhouse considers a wasp. Then it goes back to being plants.

Noon would have killed me out here. It is not noon. I file that.`,
    choices: [
      go("hub", "Leave her to it", { to: "hub" }),
      go("gat_list", "You should find that punch list", {
        to: "leland",
        when: (s) => !s.flags.gatList && s.flags.metLeland
      })
    ]
  });
  add({
    id: "front_day",
    location: "The front step",
    art: "/art/hotel.jpg",
    speaker: "jack",
    text: `The lane comes in through the hedge, ruts full, hawthorn dripping. The lamp over the door is out. Thirty feet off, dry as a bowl, is the fountain.

A man who has walked all night looks at the front of a house before he looks at anybody in it. A dry one says shut.`,
    choices: [
      go("hub", "Back inside", { to: "hub" }),
      go("fountain_look", "Walk out to the fountain", { to: "fountain_day" })
    ]
  });
  add({
    id: "fountain_day",
    location: "The fountain",
    art: "/art/hotel.jpg",
    speaker: "jack",
    text: `Job eight, when I finally read it properly, will say: she's shut off at the cock down by the boiler and not at the head. An hour's work and no digging. Put the water back on. It costs nothing and it's the only thing out there they can see.

That is not a handyman's note.`,
    choices: [
      go("hub", "File it", { to: "hub" }),
      go("boiler", "Then the boiler is on the schedule", {
        to: "boiler",
        when: (s) => s.flags.gatList || s.flags.knowsVacancy
      })
    ]
  });
  add({
    id: "stay_room",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    time: "morning",
    text: `"Well," she says. "Nobody's ever done that before."

She sits down. Or rather she moves to the chair and then stops being upright, which is not the same action. The old varnish goes dark under her fingers, the way a windowsill rings under a wet glass, then pale again as the wood drinks it in.

"Right," I say. "I've got some questions."

"Ooh. Questions. Are they filthy ones?"`,
    choices: [
      go("trudie_sanctuary", "What actually is this place?", { to: "trudie_sanctuary" }),
      go("trudie_what", "What exactly are you?", { to: "trudie_what" }),
      go("trudie_seals", "Tell me about the seals", { to: "trudie_seals" })
    ]
  });
  add({
    id: "trudie_sanctuary",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `"It's a sanctuary. At least, it was. Once upon a time."

The roads, she says. Proper ones, and the older ones under them. Green lanes. Drove roads. Where enough of them cross you get a knot, and on a knot you need a door, and behind the door a fire and a bed and something hot to eat, and nobody asks you a question you don't want asked.

"We came up the lanes too. We just never left."

"How many guests are in this hotel right now?"

"None." Not a slow week. None. There haven't been for such a long time.

When I ask whose names are in the register, the question goes into her and finds nothing to hold onto.`,
    choices: [
      go("trudie_seals", "The seals, then", { to: "trudie_seals" }),
      go("trudie_what", "What are you?", { to: "trudie_what" }),
      go("trudie_close", "That's enough talking", { to: "trudie_close" })
    ]
  });
  add({
    id: "trudie_seals",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `Four corners. Trudie holds the ground floor with a brush and attention \u2014 not spells, everybody always thinks spells. Brig holds the kitchen with heat, because a house with a fire in it can't be got at the way a cold one can. Ione stitches the second floor. Sorrel grows things in the glass house that eat what comes in on the air.

"What happens if one of you wants to stop?"

"Don't be silly. We don't stop. That's the job."

Down through the floor, the lobby carpet starts fizzing. She hears it. I watch her think about her brush and her knees and the time she's spent in a chair being asked questions.`,
    choices: [
      go("lobby_help", "Send her down. The lobby is hers.", {
        to: "lobby_help",
        addRule: "The lobby is Trudie's. Let her finish."
      }),
      go("trudie_close", "Come here, before this turns into a whole thing", {
        to: "trudie_close"
      })
    ]
  });
  add({
    id: "trudie_what",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `"Give me your thumb."

She presses it not onto her palm. Into. Two inches. No more resistance than cold custard. She makes a surprised sound, high in her throat.

"Outside's nothing. I could lose a whole hand and only be cross about the mopping. In is a different thing. Nobody's ever asked for directions before."

She firms up. My thumb is suddenly properly held. Then she lets go, and the print stays in her palm for three seconds before it fills in.

"That's why I do the floors and Brig does the pans."

There is a bit in the middle, she says. The bit that's her. Where you keep the you. If that came apart she doesn't think she'd be her any more.`,
    choices: [
      go("trudie_close", "Stop being polite about her body", { to: "trudie_close" }),
      go("trudie_seals", "Back to the hotel", { to: "trudie_seals" })
    ]
  });
  add({
    id: "trudie_close",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "jack",
    tone: "romance",
    text: `"This is going to be your last chance to be sensible," she says, "before we do something we can't take back."

"I've been being sensible all week. It keeps killing me."

The door shuts. What happens next is between me, a woman who is not entirely solid, and a stain in the corner that has been waiting longer than anyone can account for.

Afterwards something in the building turns over. Like a house settling at night.

The work order on the nightstand has a new crease I didn't put there.`,
    choices: [
      go("checkpoint_trudie", "Something saved", {
        to: "checkpoint_trudie",
        savePoint: "trudie",
        set: { intimacyTrudie: true },
        time: "morning"
      })
    ]
  });
  add({
    id: "checkpoint_trudie",
    location: "Room 204",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "jack",
    tone: "save",
    time: "morning",
    text: (s) => s.lastDeath ? `I come back mid-sentence. Mid-breath. She hasn't noticed I was gone. Twenty minutes, a corridor, a ladder, a wainscot \u2014 none of it happened for her.

The save state has moved. Dying no longer sends me to seven o'clock. It sends me here.

"You've gone somewhere unhappy in your head," she says, cheerful and sealed against the words I need her to hear.

I do not tell her again. I have learned what anyway means.` : `Trudie hops up, finds her dress on the light fitting, puts it on inside out, notices, and leaves it.

"Don't look so worried, slowpoke. I've been late before. Well. I assume I have."

The lobby is already fizzing louder than it should. I caused that.

And somewhere under this building is a book that can't keep its names still, and at half four a man who remembers me.`,
    choices: [
      go("hub", "Be useful. Stay alive until half four.", {
        to: "hub",
        time: "morning"
      }),
      go("ladder", "Fix the landing light for her", { to: "ladder" })
    ]
  });
  add({
    id: "ione_meet",
    location: "Second floor",
    art: "/art/corridor.jpg",
    portrait: "/art/ione.jpg",
    speaker: "ione",
    text: `"You are on my floor."

She is on the ceiling. One hand in the coving, the rest of her hanging off it, fully upside down and not remotely bothered. Long gray dress that has not been told about gravity. Dark hair pinned with knitting needles. More arms than I was brought up to expect.

"I'm doing the light."

"Then you are going to want to take your hand out of it very quickly. The wall behind it is open to Other. Your fingers are about a hand's width from the void."

I take my hand out about as fast as I have ever done anything.`,
    choices: [
      go("ione_talk", "Stay and be useful", { to: "ione_talk" }),
      go("hub", "Get off her floor", { to: "hub" })
    ]
  });
  add({
    id: "ione_talk",
    location: "Outside 216",
    art: "/art/corridor.jpg",
    portrait: "/art/ione.jpg",
    speaker: "ione",
    text: `"I hold the second floor. The old roads come through the brickwork. Every place one of them crosses, I put a stitch in it."

She has been doing this since before the enamel plate on the linen cupboard was painted the second time. She does not read the plate. Notices are a ground-floor matter.

"Hold the ladder," she says. "Or do not hold the ladder. Those are the two things available to you."`,
    choices: [
      go("ione_ladder", "Hold the ladder", {
        to: "ione_ladder",
        set: { heldIoneLadder: true }
      }),
      go("cupboard", "Go read the plate she won't", { to: "cupboard" }),
      go("hub", "Leave her to her seams", { to: "hub" })
    ]
  });
  add({
    id: "ione_ladder",
    location: "Outside 216",
    art: "/art/corridor.jpg",
    portrait: "/art/ione.jpg",
    speaker: "ione",
    text: `Five hours. Twenty-two seams. I brace the ladder with both hands. She works until her remaining arms shake.

At the end she takes a letter out of her dress \u2014 a contract she wrote to herself a hundred years ago and never received \u2014 and I put it under the light I fixed.

I write J-a-c under received in good order.

A pen clicks. One click means he's here. Click, click means run.

I keep writing.`,
    choices: [
      go("ione_name", "Finish the name", { to: "ione_name" }),
      go("hub", "Get off her floor before the third click", { to: "hub" })
    ]
  });
  add({
    id: "ione_name",
    location: "The second floor",
    art: "/art/corridor.jpg",
    portrait: "/art/ione.jpg",
    speaker: "ione",
    text: `"That is a subsection, Jack. Get off my floor!"

The lights go out from the far end inwards. Forty feet of pheasants go gray. The floor lets go. Cold water and wet hedge come up through the plaster, and the sound of an awful lot of people running.

"HOLD THE LADDER!"

Silver comes down past my ear. She picks me up and runs the length of her own floor, which she would like it noted she will never do again.

I wake in the good bed. Broth. A hellhound who was worried. A slime girl with a laundry bag.

Ione finishes the k for me.`,
    choices: [
      go("suite", "You lived. The good bed is occupied.", {
        to: "suite",
        set: { ioneReceipt: true, heldIoneLadder: true },
        time: "night"
      })
    ]
  });
  add({
    id: "suite",
    location: "The big one with the good bed",
    art: "/art/room.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    tone: "romance",
    time: "night",
    text: `Handcuffs from lost property. A safeword, because even this hotel has standards.

"Broth," Brig says. "If you want it all to stop, you say broth."

What happens in that room is fire and water and a man who has died enough times to know when to hold on. The windows fog. The canopy rains. Somewhere two floors up a woman who doesn't sleep puts a needle in a wall and takes it out again.

At ten to midnight I remember the nightstand. Under received in good order, in a small upright hand with a lift on the crossbar of the t: Jack.

The clock strikes. The building picks me up alive and puts me back in 204.

That is new.`,
    choices: [
      go("checkpoint_suite", "Thursday, then", {
        to: "wake",
        savePoint: "suite",
        set: { intimacyBrig: true, ioneReceipt: true },
        time: "dawn"
      })
    ]
  });
  add({
    id: "checkpoint_suite",
    location: "Room 204",
    art: "/art/room.jpg",
    speaker: "jack",
    tone: "save",
    time: "night",
    text: `I come back to a fogged suite and a fountain I have not turned on yet making a noise through the glass.

I have thirty minutes to midnight and three people who do not know a single thing that will happen tomorrow.

There is a word we agreed. I have never used it.`,
    choices: [
      go("broth", "Say broth. Get your pants on. There is a fountain.", {
        to: "endgame_night"
      }),
      go("suite_stay", "Stay. Let midnight take you and try Thursday properly.", {
        to: "wake",
        time: "dawn"
      })
    ]
  });
  add({
    id: "brig_ward",
    location: "The range",
    art: "/art/kitchen.jpg",
    portrait: "/art/brig.jpg",
    speaker: "brig",
    text: `"Wash your hands. Hot as you can stand. There's a wire brush under the sink. You come in here stinking of the inside of her and never once consider what other people have to breathe."

Four screws. Not five. Behind the plate: a bar of gray metal with a groove cut down it, the sacrificial stuff gone dull. The inside of the housing is covered in marks. Initials. Dates. A G pressed down harder than it needed to be.

I clean the groove, lay in a coil of soft wire the toolkit has never offered me before, and ask Brig to breathe on it.

She shuts her eyes first. The wire goes from gray to bright.

The flame comes up orange the whole way down.`,
    choices: [
      go("stew", "Eat the unchipped bowl", {
        to: "stew",
        set: { stoveWard: true, didStove: true }
      })
    ]
  });
  add({
    id: "cupboard",
    location: "The linen cupboard",
    art: "/art/corridor.jpg",
    speaker: "jack",
    text: `An enamel plate on four brass screws. Painted round nine times and never painted over.

HOTEL SANS NUIT
Ground and lobby \u2014 held
Kitchen and hearth \u2014 held
Second floor \u2014 held
Glass house \u2014 held
Innkeeper \u2014 vacant
Applications to the desk.

Under it, in pencil, nine jobs. Down the side, in a different hand: J. Causey.

A hundred and twenty-seven of us came up that lane and stood in front of this door with a screwdriver. Every single one of us read down.`,
    choices: [
      go("apply", "Read the top. Apply.", {
        to: "apply",
        set: { sawPlate: true, knowsVacancy: true }
      }),
      go("hub", "Not yet", {
        to: "hub",
        set: { sawPlate: true, knowsVacancy: true }
      }),
      go("ione_meet", "Tell Ione", {
        to: "ione_vacancy",
        set: { sawPlate: true, knowsVacancy: true }
      })
    ]
  });
  add({
    id: "ione_vacancy",
    location: "Second floor",
    art: "/art/corridor.jpg",
    portrait: "/art/ione.jpg",
    speaker: "ione",
    text: `"That is not possible."

Then, after four precise objections: a vacancy is an absence. An advertisement is an intention. Those are not adjacent categories.

"So it's the difference between a hole in the road and a guy with a shovel."

"That is an utterly revolting way of putting it and I shall be using it."

Writing a name on a plate confers nothing. Nobody in this building has ever been appointed. She is the second floor because she is the one doing the second floor. That is the entire mechanism, and it is monstrous, and it is the Way.`,
    choices: [
      go("apply", "Apply anyway", { to: "apply" }),
      go("hub", "Do the job first. Then the name.", { to: "hub" })
    ]
  });
  add({
    id: "register",
    location: "Behind the desk",
    art: "/art/lobby.jpg",
    speaker: "jack",
    text: (s) => `Nine square feet of floor. Pigeonholes at my back. The register flickering twenty-two names that will not finish.

${s.flags.applied ? "Ione said: you are the innkeeper when you are the one doing the innkeeping. So do it." : `Trudie, from her knees: "Ooh, don't you look all masterful standing there. Nobody ever goes behind the desk. It's like the fifth chair."`}

A name in a register doesn't do anything until somebody with standing signs for it.`,
    choices: [
      go("sign_early", "Write received in good order", {
        to: "register_fail",
        when: (st) => !st.flags.applied && !st.flags.openedFountain
      }),
      go("register_sign", "Mean it this time", {
        to: "register_sign",
        when: (st) => st.flags.applied
      }),
      go("hub", "Step back out", { to: "hub" })
    ]
  });
  add({
    id: "register_fail",
    location: "Behind the desk",
    art: "/art/lobby.jpg",
    speaker: "jack",
    text: `The ink comes up off the paper about a sixteenth of an inch, goes soft, and leaves the gap as clean as it has ever been.

A name on a plate is an intention. Standing is doing the job.

Leland said it in about eight words and I heard four of them.`,
    choices: [go("hub", "Find out what the job actually is", { to: "hub" })]
  });
  add({
    id: "leland",
    location: "The lobby, half four",
    art: "/art/lobby.jpg",
    portrait: "/art/leland.jpg",
    speaker: "leland",
    time: "evening",
    text: (s) => s.flags.metLeland ? `"You're upright," he says. "And you're behind the desk, an' all."

The portly postman with feathers for sideburns goes still for the first time since I've known him.

"Well, fuck me sideways with a hatstand."` : `There has never been another man in this hotel. Then there is: portly, middle-aged, satchel on his hip, feathers where his sideburns ought to be, sorting envelopes into pigeonholes I have never noticed.

"I hear you took the stairs on loop two, Jack Causey. That's a bold choice, my lad. That or you're a colossal asswipe."

He knows there was a loop two. Which means he has been keeping score the whole time.

I sit down. The carpet, for five seconds, does not bubble.`,
    choices: (s) => [
      go("leland_talk", "Ask him what the hell is happening", { to: "leland_talk" }),
      go("death_carpet", "Sit down without checking the floor", {
        to: "death_carpet",
        when: () => !s.flags.helpedLobby && !s.flags.knowCarpet
      })
    ]
  });
  add({
    id: "leland_talk",
    location: "The desk",
    art: "/art/lobby.jpg",
    portrait: "/art/leland.jpg",
    speaker: "leland",
    text: `"It's not magic, mate. It's just the paperwork."

He has carried a string-tied bundle the color of weak tea up that lane for a hundred and six years. Every day. And back down every day.

"You can hold a day or you can keep it. Not both."

He makes me sign his book. G.A.T.'s punch list is in the pile \u2014 nine jobs, two lines that aren't jobs. Sorrel won't answer the door. Knock anyway. Don't sign for anything at the desk.

Timing is a bitch. I signed about five minutes ago.`,
    choices: [
      go("gat_read", "Read the punch list", {
        to: "gat_read",
        set: { metLeland: true, gatList: true, signedCarrier: true }
      })
    ]
  });
  add({
    id: "gat_read",
    location: "The main stairs",
    art: "/art/lobby.jpg",
    speaker: "jack",
    text: `One: landing light. The issue's not the bulb. Two: linen cupboard door, three millimeters off the bottom and no more. Three: the kitchen range. There's a ward under the plate. Four screws. The give is gone. Do not leave this. Underlined twice.

Seven, eight and nine rubbed to nothing in a mail sack. One word left: boiler.

At the bottom, G.A.T., the T gone at four times harder than the rest.

He worked it out. Nobody gave him the job either.`,
    choices: [
      go("ione_meet", "Do the landing light properly", { to: "ione_meet" }),
      go("brig_ward", "The ward under the plate", { to: "brig_ward" }),
      go("hub", "You've got a list. Use it.", { to: "hub", time: "evening" })
    ]
  });
  add({
    id: "fountain_night",
    location: "The front",
    art: "/art/fountain.jpg",
    speaker: "jack",
    time: "night",
    text: `The air outside is cold and wet and does nothing to me at all. Noon is the problem. Eleven at night isn't.

There are people standing in the dark.

A woman with a coat held shut at the throat. A man behind her. A pair by the fountain. A tall lad holding a child. Somebody sitting on the rim with a bag between his boots.

I count them. Twenty-two.

Soaked, not rained on. Nobody is knocking. Not one of them is going away.`,
    choices: [
      go("guests_night", "Hold the door and tell them to come in", {
        to: "guests_night",
        set: { knowsGuests: true, frontDoorNight: true }
      }),
      go("hub", "Not yet. You don't have standing.", { to: "hub" })
    ]
  });
  add({
    id: "guests_night",
    location: "The threshold",
    art: "/art/fountain.jpg",
    speaker: "jack",
    text: `I take the woman in the coat by the arm. She comes. That's what I want on the record. She walks up the step beside me, boots on the stone, over the threshold, onto the mat.

She is at the bottom of the step, outside, in the wet, facing the door.

No noise. I watch a woman walk up two feet of stone nine times before I understand it isn't her doing it.

The man on the fountain rim looks at me. Not through me. It is the look you get from a bloke in a queue who has watched the man in front of him get served and the door go across.

Then he looks back at the door.`,
    choices: [
      go("hub", "The door was never the fault", {
        to: "hub",
        set: { knowsGuests: true }
      }),
      go("apply", "Applications to the desk", { to: "apply" })
    ]
  });
  add({
    id: "apply",
    location: "The linen cupboard",
    art: "/art/corridor.jpg",
    speaker: "jack",
    text: `I put my name under Innkeeper.

Ione, from the coving: "That confers nothing."

"I know."

"Whether you are the innkeeper or not depends on the next half hour."

Water. Desk. Names. That's the whole plan. I've had worse and charged for them.`,
    choices: [
      go("boiler", "The fountain is shut off at the boiler", {
        to: "boiler",
        set: { applied: true, sawPlate: true, knowsVacancy: true }
      }),
      go("register", "Stand behind the desk", {
        to: "register",
        set: { applied: true }
      })
    ]
  });
  add({
    id: "boiler",
    location: "Under the east end",
    art: "/art/boiler.jpg",
    speaker: "jack",
    text: `The boiler room is the size of a chapel. Vaulted brick. In the middle, on a plinth, the most beautiful thing in this hotel after the women in it.

Ten feet of her. Firebox you could park a car in. Gauges in brass bezels the size of dinner plates. Every gauge sat at nothing.

She is not empty. She is full. And not with water.

A tag on the fountain cock: LEAVE ON. It is off.

Last time I opened her at the bottom with my head under the feed line, like a colossal moron.`,
    choices: [
      go("boiler_work", "Blow her down properly. Then the fountain.", {
        to: "boiler_work"
      }),
      go("death_boiler", "Crack the union at the bottom. You've got this.", {
        to: "death_boiler",
        when: (s) => !s.flags.knowBoiler
      })
    ]
  });
  add({
    id: "death_boiler",
    location: "The boiler room",
    art: "/art/boiler.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "A hundred years of loops came out of the feed.",
      rule: "Never open a thing that's holding until you've let it down first."
    },
    text: `The union comes sweet. Then eighteen inches over my head something opens up and takes my hands and my face off me at a pretty decent temperature.

There is nothing in that system.

So what came out of you?`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "boiler_work",
    location: "The boiler room",
    art: "/art/boiler.jpg",
    speaker: "jack",
    time: "afternoon",
    text: `Wire brush. Oil. Drain line sound the whole way \u2014 until three o'clock, when the freeze comes up out of the flags and a chunk of mortar cracks the joint.

A pen clicks at the top of the steps.

"Afternoon," I say. "I've got a job on."

"SUBSECTION ELEVEN. PLANT AND MACHINERY. NO ALTERATION TO THE CONDITION OF THE PREMISES."

Ione drops out of the vaulting head first. "I am not staff. I have never been engaged."

I lower the blowdown. The hotel lets go.

A minute and forty seconds of every loop this place has ever had comes out of the bottom of her and leaves down a cracked drain. Knock. Jack, you're late again. Knock. Jack, you're late again. Back and back until it stops being a voice.

The shell starts ticking. Empty iron, coming up to room temperature.

I turn the fountain cock. It goes round sweet.`,
    choices: [
      go("fountain_on", "Go up and listen", {
        to: "fountain_on",
        set: { openedFountain: true, drainedBoiler: true, knowBoiler: true }
      })
    ]
  });
  add({
    id: "fountain_on",
    location: "The lobby",
    art: "/art/lobby.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "trudie",
    text: `"Jack! There's a noise! There's never been a noise! I've put my bucket down. I never put my bucket down!"

The register is still flickering. Twenty-two names, still trying, still not finishing.

"You're next," I tell it, and go to open the front door.

Click.

"SUBSECTION ONE. THE PREMISES ARE SHUT."

Not a rule about me. A rule about a hotel with nobody in it.`,
    choices: [
      go("death_subsection", "Hold the door anyway", { to: "death_subsection" }),
      go("endgame_night", "You've seen this. You know where you come back.", {
        to: "endgame_night",
        when: (s) => s.savePoint === "suite" || s.flags.ioneReceipt
      })
    ]
  });
  add({
    id: "death_subsection",
    location: "The mat",
    art: "/art/hotel.jpg",
    tone: "death",
    speaker: "jack",
    death: {
      cause: "Subsection one. The premises are shut.",
      rule: "A hotel with nobody in it cannot open a door."
    },
    text: `Trudie is screaming my name. Heat is coming up the corridor from the kitchen. Too late.

The last thing to go is my heart. The last thing I hear is the fountain.

And then I am back in a fogged suite, Wednesday night, forty minutes before midnight, with water already running in a fountain I have not turned on yet.`,
    choices: [go("wake", "Wake up", { to: "wake" })]
  });
  add({
    id: "endgame_night",
    location: "The good bed",
    art: "/art/room.jpg",
    speaker: "jack",
    time: "night",
    text: `"Broth."

Everything stops. Trudie calls me an absolute bastard and lets go. Brig puts half of what she was holding into the grate. The wallpaper goes brown in a slow line eight feet up.

"There's a noise," Trudie says, already at the window. "There's a noise in my fountain."

"I did that. Will do that. One of those."

Ione has five arms. I stand in the corridor counting them twice, grinning.

Then I write my name under Innkeeper, go downstairs, and stand on the bad bit of carpet behind the desk.`,
    choices: [
      go("register_sign", "Do the innkeeping", {
        to: "register_sign",
        set: { applied: true, openedFountain: true }
      })
    ]
  });
  add({
    id: "register_sign",
    location: "Behind the desk",
    art: "/art/lobby.jpg",
    speaker: "jack",
    tone: "ending",
    text: `The Rulekeeper reaches. Brig puts herself between us and dumps every last drop of a denied evening into a public area. Ione drops out of the coving with all five arms. Trudie dissolves across the north end of the lobby until I can read the pattern of the carpet through her, and everywhere she touches, the fizzing stops.

I rule a line under the twenty-second name. Received in good order.

The first time, the ink lifts off.

Ione, shouting: "Stop asking the building's permission and do the job!"

The carpet takes the skin off my shin. I write it again. This time I mean it. Under it, my name.

The ink takes. It runs up the page, name after name, hard and black, and they stop moving.

The Rulekeeper looks at its clipboard, turns a page, turns it back, and writes one word.

Compliant.

It opens the front door and stands aside.`,
    choices: [
      go("ending_open", "Welcome them", {
        to: "ending_open",
        set: { checkedIn: true }
      })
    ]
  });
  add({
    id: "ending_open",
    location: "Hotel Sans Nuit",
    art: "/art/fountain.jpg",
    portrait: "/art/trudie.jpg",
    speaker: "jack",
    tone: "ending",
    text: `The man off the rim of the fountain picks up his bag, comes up the lane, across the ground, past a thing in a long coat holding a door, and over the mat.

"Welcome. You are received in good order."

Trudie reads the names out loud and discovers she can cry. Ione is employed, retrospectively, at four and sixpence a week, and will be extremely unpleasant about the arrears. Brig remembers the plate.

Twenty-one of them go hard in the book and upstairs into beds we cannot make.

The last name will not come off the page. A woman in a gray coat is still standing at the bottom of the steps. Salt in her hair. She will not come in.

Leland, the next afternoon, deals a hundred and six years of other people's post into pigeonholes that finally keep it.

"Same time tomorrow," he says.

And this time, it is true.

The work order has a new second line.

The basement is now on the schedule.`,
    choices: [
      go("ending_banshee", "Go out to her", { to: "ending_banshee" }),
      go("ending_stay", "Stay behind the desk", { to: "ending_stay" })
    ]
  });
  add({
    id: "ending_banshee",
    location: "The fountain",
    art: "/art/fountain.jpg",
    speaker: "jack",
    tone: "ending",
    text: `Trudie is sat in the bowl up to her collarbone with her eyes shut. The banshee stands off to the side, facing a door that is finally, properly open, and will not go in.

I think she's waiting for me to bring her something.

A long way down, something is being dragged. Four seconds. It stops. Neither of us says anything about it.

"You're two days late," Trudie says.

"Everybody's got an excuse."

She puts a hand up out of the water. I take it. The hotel is open. The lanes have started remembering. Five hundred rooms, Leland says, and something that shut this place from the inside is still in the building, and it's had a hundred years on its own to get comfortable.

I am the innkeeper.

Fix what breaks. Then do it all again.`,
    choices: [
      go("title_end", "The Hotel Sans Nuit is open", { to: "credits" })
    ]
  });
  add({
    id: "ending_stay",
    location: "Behind the desk",
    art: "/art/lobby.jpg",
    speaker: "jack",
    tone: "ending",
    text: `I stay where the job is. Towels. Eggs. A banshee I have not yet earned the right to bring in. A basement that has just come back onto the schedule.

Leland puts a single envelope into the pigeonhole where the brass has gone black. It stays.

"Ask me again tomorrow. I might have different answers."

The work order is still on hotel stationery. Still my handwriting.

I fold it up, put it on the nightstand, and go and get my boots.`,
    choices: [go("title_end", "Same time tomorrow", { to: "credits" })]
  });
  add({
    id: "credits",
    location: "Hotel Sans Nuit",
    art: "/art/hotel.jpg",
    tone: "ending",
    speaker: "jack",
    text: `Hotel Sans Nuit is open.

You held a day and you kept it.

This game is adapted from Save State Innkeeper \u2014 a time-loop novel about a handyman, a vacant post, and four women who have been holding a building up for a hundred years.

The basement is now on the schedule.`,
    choices: [
      go("wake", "Loop again. Keep the knowledge.", {
        to: "wake",
        time: "dawn"
      })
    ]
  });

  // src/lib/game/types.ts
  var DEFAULT_FLAGS = {
    knowBasement: false,
    knowStairs: false,
    knowMirrors: false,
    knowSpores: false,
    knowOvens: false,
    knowDumbwaiter: false,
    knowCarpet: false,
    knowLadder: false,
    knowBoiler: false,
    knowSubsection: false,
    metLeland: false,
    knowsVacancy: false,
    knowsGuests: false,
    signedCarrier: false,
    gatList: false,
    openedFountain: false,
    applied: false,
    checkedIn: false,
    intimacyTrudie: false,
    intimacyBrig: false,
    heldIoneLadder: false,
    ioneReceipt: false,
    stoveWard: false,
    skipRoutine: false,
    didStove: false,
    didLight: false,
    didPipe: false,
    helpedLobby: false,
    indoorNoon: false,
    avoidedThree: false,
    sawRegister: false,
    talkedTrudieRoom: false,
    thankedTrudie: false,
    complimentBrig: false,
    sawPlate: false,
    frontDoorNight: false,
    drainedBoiler: false
  };
  var OPENING_ORDER = [
    "Fix what breaks. Don't ask questions. Then do it all again."
  ];
  var LOOP_FLAG_KEYS = [
    "skipRoutine",
    "didStove",
    "didLight",
    "didPipe",
    "helpedLobby",
    "indoorNoon",
    "avoidedThree",
    "sawRegister",
    "talkedTrudieRoom",
    "thankedTrudie",
    "complimentBrig"
  ];
  var TIME_LABEL = {
    dawn: "Just after seven",
    morning: "Morning",
    noon: "Noon",
    afternoon: "Afternoon",
    three: "Three o'clock",
    evening: "Evening",
    night: "Night"
  };
  function initialState() {
    return {
      sceneId: "wake",
      loop: 1,
      deaths: 0,
      time: "dawn",
      savePoint: "wake",
      workOrder: [...OPENING_ORDER],
      flags: { ...DEFAULT_FLAGS },
      deathLog: []
    };
  }

  // src/lib/game/engine.ts
  var RULE_FLAGS = {
    "The basement is not on the schedule right now.": "knowBasement",
    "No stairs in the dark.": "knowStairs",
    "Mirrors are for the morning.": "knowMirrors",
    "Noon is indoors o'clock.": "knowSpores",
    "Don't touch the ovens unless invited.": "knowOvens",
    "Honestly\u2026": "knowDumbwaiter",
    "Check the bar, you absolute clown.": "knowLadder",
    "The lobby is Trudie's. Let her finish.": "knowCarpet",
    "Never open a thing that's holding until you've let it down first.": "knowBoiler",
    "A hotel with nobody in it cannot open a door.": "knowSubsection"
  };
  function resolveText(state) {
    const scene = getScene(state.sceneId);
    return typeof scene.text === "function" ? scene.text(state) : scene.text;
  }
  function resolveChoices(state) {
    const scene = getScene(state.sceneId);
    const raw = typeof scene.choices === "function" ? scene.choices(state) : scene.choices;
    return raw.filter((c) => !c.when || c.when(state));
  }
  function applyChoice(state, choice) {
    const next = {
      ...state,
      flags: { ...state.flags, ...choice.set },
      workOrder: [...state.workOrder],
      deathLog: [...state.deathLog]
    };
    if (choice.time) next.time = choice.time;
    if (choice.savePoint) next.savePoint = choice.savePoint;
    if (choice.addRule && !next.workOrder.includes(choice.addRule)) {
      next.workOrder.push(choice.addRule);
    }
    const dest = getScene(choice.to);
    if (dest.death) {
      return die(next, dest, choice.to);
    }
    next.sceneId = choice.to;
    if (dest.time) next.time = dest.time;
    return next;
  }
  function die(state, dest, sceneId) {
    const cause = dest.death?.cause ?? "You died.";
    const rule = dest.death?.rule;
    const workOrder = [...state.workOrder];
    if (rule && !workOrder.includes(rule)) workOrder.push(rule);
    const flags = { ...state.flags };
    for (const key of LOOP_FLAG_KEYS) flags[key] = DEFAULT_FLAGS[key];
    if (rule && RULE_FLAGS[rule]) flags[RULE_FLAGS[rule]] = true;
    return {
      ...state,
      sceneId,
      flags,
      workOrder,
      deaths: state.deaths + 1,
      lastDeath: cause,
      deathLog: [...state.deathLog, { cause, loop: state.loop }]
    };
  }
  function wakeFromDeath(state) {
    const save = state.savePoint;
    return {
      ...state,
      sceneId: savePointScene(save),
      loop: state.loop + 1,
      time: save === "suite" ? "night" : save === "trudie" ? "morning" : "dawn"
    };
  }
  function savePointScene(save) {
    if (save === "trudie") return "checkpoint_trudie";
    if (save === "suite") return "checkpoint_suite";
    return "wake";
  }
  function resetRun() {
    return initialState();
  }
  return __toCommonJS(play_entry_exports);
})();
