import React from 'react'
import css from 'components/Story.module.css'

/**
 * - make a field in the gamestate object
 * - numTimesLookedAtToolbox
 * - update this correctly, so whenever we enter the page "look toolbox"
 * - increment this += 1
 * - edit the content field of look toolbox to be dependent on numTimes
 * - You've sure looked at that toolbox a lot. Have you lost something?
 * - Your date is getting worried.
 */

export type Memory =
    "memory1"
  | "memory2"
  | "memory3"

export type GameState = {
  numTimesLookedAtToolbox: number
}

export type PageName = 
    "start"
  | "because"
  | "help"
  | "look"
  | "look toolbox"
  | "look girl"
  | "examine girl"
  | "sorry"

export type Page = {
    content: (userInput: string, memories: Memory[], gameState: GameState) => [html: React.ReactNode, gameState: GameState]
    next: (userInput: string, memories: Memory[], gameState: GameState) => PageName
}

export const STORY: Record<PageName, Page> = {
  "look": {
    content: (_userInput, _memories, gameState) => {
      
      return (
        [<>
          <p>
            You are in a Whataburger in Bumfuck Nowhere, New Mexico.
          </p>
          <p>
            Across from you sits a <span className={css.highlight}>girl</span>. She is smiling at you expectantly.
          </p>
          <p>
            You notice the table is slightly sticky. There are two <span className={css.highlight}>menus</span>, 
            two <span className={css.highlight}>glasses of water</span>, 
            two mugs, and a steaming pot of coffee in front of you.
            Also on the table are your <span className={css.highlight}>keys</span>, 
            your <span className={css.highlight}>phone</span>, and 
            your <span className={css.highlight}>wallet</span>.
            Next to you on the booth is a <span className={css.highlight}>toolbox</span>.
          </p>
        </>,
        gameState]
      )
    },
    next: () => {
      return "look";
    }
  },
  "help": {
    content: (_userInput, _memories, gameState) => {
      return (
        [<>
          <p>
            No worries, talking to girls is hard.
          </p>
          <p>
            Some commands you can use:
            <ul>
              <li>
                <b>help</b>: pull up this menu again
              </li>
              <li>
                <b>undo</b>: undo previous command
              </li>
              <li>
                <b>look</b>: look around the scene
              </li>
            </ul>
          </p>
        </>,
        gameState]
      )
    },
    next: () => {
      return "help";
    }
  },
  "start": {
    content: (_userInput, _memories, gameState) => {
      return (
        [<>
          <p>
            You are not very good at talking to girls. You remind yourself that 
            you are, in fact, a girl yourself -- but this does not really seem to 
            have any effect on the fact that you are not very good at talking to girls.
          </p>
          <p>
            Nevertheless, there is a <span className={css.highlight}>girl</span> sitting in front of you. She is happy 
            to be here with you; she has told you as much. You do not entirely 
            believe this.
          </p>
          <p>
            You two are sitting in a booth in a Whataburger in the middle of 
            Bumfuck Nowhere, New Mexico.
          </p>
          {/* <p>
            This morning you woke up in a panic, disoriented, immersed in an amnesiac
            haze. You do not remember your name. You do not remember her name. 
            You do not know how old you are -- twenty-something, perhaps, but the specific year escapes you.
            You recall your life in fragments -- the vague notion
            that the two of you are on a road trip, that you are escaping from somewhere,
            and uneasily heading somewhere else. 
          </p>
          <p>
            Louder than anything else, a thought resounds in your mind:
            you are horrifically, irrevocably in love with this girl. The weight of it 
            grips you like a drowning man intent on taking you down with him.
          </p> */}
          <p>
            What will you do next?
          </p>
          <p className={css.ooc}>
            For new players, feel free to write "help" for ideas on how to proceed.
          </p>
        </>, 
        gameState]
      )
    },
    next: (userInput) => {
      if (userInput.includes("why")) {
        return "because";
      } else if (userInput.includes("look at") && userInput.includes("toolbox")) {
        return "look toolbox";
      }
      return "sorry";
    }
  },
  "because": {
    content: (_userInput, _memories, gameState) => {
      return (
        [<>
          <p>
            Because that's who you are.
          </p>
        </>,
        gameState]
      )
    },
    next: () => {
      return "because";
    }
  },
  "look toolbox": {
    content: (_userInput, _memories, gameState) => {
      const nextGameState = {...gameState, numTimesLookedAtToolbox: gameState.numTimesLookedAtToolbox + 1}
      return (
        [<>
          <p>
            You've sure looked at that toolbox a lot. {nextGameState.numTimesLookedAtToolbox} times, even. 
            Have you lost something?
            Your date is getting worried.
          </p>
          <p>
            You take your eyes off the beautiful girl in front of you to look at your toolbox. Nice going!
          </p>
          <p>
            You are deeply fond of your toolbox. You've had it since you were a teenager, and it's
            accompanied you through a great many life transition. It seems to be locked right now.
          </p>
          <p>
            The girl in front of you raises her eyebrows. You had basically begged her to let you take
            the toolbox in. <em>I'll leave the <span className={css.highlight}>key</span> in the <span className={css.highlight}>car</span></em>, you'd said. An uneasy compromise.
          </p>
        </>,
        nextGameState]
      )
    },
    next: () => {
      return "start";
    }
  },
  "look girl": {
    content: (_userInput, _memories, gameState) => {
      const nextGameState = {...gameState, numTimesLookedAtToolbox: gameState.numTimesLookedAtToolbox + 1}
      return (
        [<>
          <p>
            Well, I guess you could just look -- you might have better luck learning more
            if you <span className={css.highlight}>compliment</span> her, though!
          </p>
          <p>
            You see a girl. She has long, wavy, blonde hair. 
            Her eyes somehow look simultaneously focused on you and on something far away.
          </p>
        </>,
        nextGameState]
      )
    },
    next: () => {
      return "start";
    }
  },
  "examine girl": {
    content: (_userInput, _memories, gameState) => {
      const nextGameState = {...gameState, numTimesLookedAtToolbox: gameState.numTimesLookedAtToolbox + 1}
      return (
        [<>
          <p>
            Have you no manners? Who just goes around <em>examining</em> people?
          </p>
          <p>
            You might have better luck learning more
            if you <span className={css.highlight}>compliment</span> her!
          </p>
        </>,
        nextGameState]
      )
    },
    next: () => {
      return "start";
    }
  },
  "sorry": {
    content: (_userInput, _memories, gameState) => {
      return (
        [<>
          <p>
            That is not something you can do, at least right now.
          </p>
        </>, 
        gameState]
      )
    },
    next: (userInput) => {
      if (userInput.includes("look at") && userInput.includes("toolbox")) {
        return "look toolbox";
      }
      return "sorry";
    }
  },
};