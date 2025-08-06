import { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [email, setEmail] = useState("");
  const [recipients, setRecipients] = useState("");

  const generateEmail = async () => {
    const res = await axios.post("http://127.0.0.1:5000/generate-email", { prompt });
    setEmail(res.data.email);
  };

  const sendEmail = async () => {
    const recipientList = recipients.split(",");
    await axios.post("http://127.0.0.1:5000/send-email", {
      recipients: recipientList,
      body: email
    });
    alert("Email sent successfully!");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Email Generator</h1>
      <input 
        type="text" 
        placeholder="Recipients (comma separated)" 
        onChange={(e) => setRecipients(e.target.value)}
      />
      <br/><br/>
      <textarea 
        placeholder="Enter your prompt..." 
        onChange={(e) => setPrompt(e.target.value)}
      />
      <br/><br/>
      <button onClick={generateEmail}>Generate Email</button>
      <br/><br/>
      <textarea 
        value={email} 
        onChange={(e) => setEmail(e.target.value)}
        style={{width:"400px", height:"200px"}}
      />
      <br/><br/>
      <button onClick={sendEmail}>Send Email</button>
    </div>
  );
}

export default App;
