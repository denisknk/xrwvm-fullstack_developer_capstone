import LoginPanel from "./components/Login/Login"
import Dealers from './components/Dealers/Dealers';
import PostReview from "./components/Dealers/PostReview"
import Dealer from "./components/Dealers/Dealer"
import Register from "./components/Register/Register"
import { Routes, Route } from "react-router-dom";

function App() {
    console.log("RENDER123");
  return (
    <Routes>
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/register" element={<Register />} /> 
        <Route path="/dealers" element={<Dealers/>} />
        <Route path="/dealer/:id" element={<Dealer/>} />
        <Route path="/postreview/:id" element={<PostReview/>} />
        
    </Routes>
  );
}
export default App;
