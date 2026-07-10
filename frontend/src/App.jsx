import { useState } from 'react'
import './App.css'
function App() {

  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("study");
  const [messages, setMessage] = useState([]);
  const [loading, setLoading] = useState(false);


  async function sendQuestion() {
     if (question.trim() === "") {
        return;
    }
    setLoading(true)
  try{  
    const result = await fetch(
    "http://127.0.0.1:8000/ask",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question,
        mode: mode
      })
    }

  );

  const data = await result.json();
  setMessage([
    ...messages,
    {
      sender: "user",
      text: question
    },
    {
    sender: "assistant",
    text: data.response
    }
  ])

  setQuestion("");

    } finally {
        setLoading(false);
    }
}

return (
  <div className="app">

    <div className="chat-container">

      <header className="header">
        <h1>Clive</h1>
      </header>


      <div className="messages">

        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender}`}
          >
            <div className="bubble">
              {message.text}
            </div>
          </div>
        ))}


        {loading && (
          <div className="message assistant">
            <div className="bubble">
              Thinking...
            </div>
          </div>
        )}

      </div>



      <div className="input-area">

        <select
          value={mode}
          onChange={(event) => setMode(event.target.value)}
        >
          <option value="study">
            Study
          </option>

          <option value="quiz">
            Quiz
          </option>

          <option value="simplify">
            Simplify
          </option>

        </select>


        <input
          type="text"
          placeholder="Ask anything..."
          value={question}
          onChange={(event)=>setQuestion(event.target.value)}
          onKeyDown={(event)=>{
            if(event.key==="Enter"){
              sendQuestion();
            }
          }}
        />


        <button 
          onClick={sendQuestion}
          disabled={loading}
        >
          Send
        </button>


      </div>

    </div>

  </div>
);
}

export default App