import React, { useState, useEffect } from 'react'
import css from 'components/App.module.css'
import Chat from 'components/chat/Chat'
import { io } from 'socket.io-client'

export type ChatMessage = {
  role: 'player' | 'narrator'
  content: string
}

const socketURL = "http://10.0.0.7:6969"
const socket = io(socketURL)

function App() {

  const [inputText, setInputText] = useState<string>('')
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])

  useEffect(() => {

    setChatHistory(chatHistory => 
      [...chatHistory, 
        {
          role: 'narrator',
          content: "Hello! What can I help you with today?"
        }
      ]
    )

    function onConnect() {
      console.log("connected")
    }

    function onDisconnect() {
      console.log("disconnected")
    }

    function onCommand(command: string) {
      setChatHistory(chatHistory => 
        [...chatHistory, 
          { 
            role: 'player', 
            content: "> ".concat(command)
          }
        ]
      )
    }

    function onResponse(response: string) {
      setChatHistory(chatHistory => 
        [...chatHistory, 
          { 
            role: 'narrator', 
            content: response
          }
        ]
      )
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('command', onCommand);
    socket.on('response', onResponse);
    
    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
    };
  }, []);

  function submitText() {
    setChatHistory(chatHistory => 
      [...chatHistory, 
        { 
          role: 'player', 
          content: "> ".concat(inputText)
        }
      ]
    )
    
    socket.emit("command", inputText)

    setInputText('')

  }

  return (
    <div className={css.container}>
      <Chat chatHistory={chatHistory} />
      <input 
        type="text" 
        className={css.input}
        value={`> ${inputText}`}
        onChange={(e) => setInputText(e.target.value.slice(2))}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            submitText()
          }
        }}
      />
    </div>
  )
}

export default App
