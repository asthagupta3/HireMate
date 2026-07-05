import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const registerUser = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/users/register",
        {
          name: name,
          email: email,
          password: password,
        }
      );

      alert("Registration Successful!");
      console.log(response.data);
    } catch (error) {
      console.error(error);
      alert(error.response.data.detail);;
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1>HireMate</h1>
        <p>Your AI Career Assistant</p>

        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button>Login</button>

        <p style={{ marginTop: "20px" }}>
          Don't have an account?
        </p>

        <button
          className="register-btn"
          onClick={registerUser}
        >
          Register
        </button>
      </div>
    </div>
  );
}

export default App;