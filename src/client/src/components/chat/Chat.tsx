import { ChatMessage } from 'components/App'
import css from './Chat.module.css'
import { useRef, useEffect } from 'react'

function Chat({ chatHistory }: { chatHistory: ChatMessage[] }) {
  const chatContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [chatHistory])
  
  return (
    <div className={css.container} ref={chatContainerRef}>
      {chatHistory.map((message, index) => (
        <div key={index} 
          className={css.chat}
          style={{ 
            color: message.role === 'player' ? 'blue' : 'black',
            fontWeight: message.role === 'player' ? 'bold' : 'normal'
          }}
        >
          {message.content}
        </div>
      ))}
    </div>
  )
}

export default Chat
