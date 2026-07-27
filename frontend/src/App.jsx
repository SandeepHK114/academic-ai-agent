import { useState } from 'react'
import './App.css'
function App() {

  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("study");
  const [messages, setMessage] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);


  async function sendQuestion() {

    if (question.trim() === "") {
    return;
    } 

    if (!selectedFile) {
    alert("Please select a PDF first.");
    return;
    
  }
    const formdata = new FormData();
    formdata.append("question", question)
    formdata.append("mode", mode)
    formdata.append("file", selectedFile)

    setLoading(true)
  try{  
    const result = await fetch(
    "http://127.0.0.1:8000/ask",
    {
      method: "POST",
      body: formdata
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
        type="file"
        accept=".pdf"
        onChange={(event) => {
        setSelectedFile(event.target.files[0]);
        }}
      />
      <p>
        {selectedFile ? selectedFile.name : "No file selected"}
      </p>
        <input
        type="text"
        value={question}
         onChange={(event) => setQuestion(event.target.value)}
         placeholder="Ask a question about the PDF"
        onKeyDown={(event) => {
         if (event.key === "Enter" && !loading) {
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