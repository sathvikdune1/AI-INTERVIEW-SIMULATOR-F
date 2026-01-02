import { BrowserRouter, Routes, Route } from "react-router-dom";
import StartInterview from "./pages/StartInterview";
import UploadResume from "./pages/UploadResume";
import Interview from "./pages/Interview";
import ResultDashboard from "./pages/ResultDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartInterview />} />
        <Route path="/upload-resume" element={<UploadResume />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/result/:interviewId" element={<ResultDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
