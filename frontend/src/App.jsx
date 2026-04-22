import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Home from "./pages/Home";
import StartInterview from "./pages/StartInterview";
import UploadResume from "./pages/UploadResume";
import Interview from "./pages/Interview";
import ResultDashboard from "./pages/ResultDashboard";

export default function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* 🔥 FIXED ROUTES */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />   {/* ✅ IMPORTANT */}

        {/* Home Dashboard */}
        <Route path="/home" element={<Home />} />

        {/* Interview Workflow */}
        <Route path="/start" element={<StartInterview />} />
        <Route path="/upload-resume" element={<UploadResume />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/result/:interviewId" element={<ResultDashboard />} />

      </Routes>

    </BrowserRouter>

  );

}