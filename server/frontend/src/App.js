import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/" element={<Home />} /> 
        <Route path="/register" element={<Register />} /> 
    </Routes>
  );
}
export default App;
