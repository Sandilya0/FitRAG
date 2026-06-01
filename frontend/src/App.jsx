import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import Dashboard from './pages/Dashboard'
import AskFitRAG from './pages/AskFitRAG'
import Profile from './pages/Profile'
import WhoopData from './pages/WhoopData'
import History from './pages/History'

export default function App() {
  // Shared state across pages
  const [profile, setProfile] = useState(null)
  const [history, setHistory] = useState([])
  const [whoopProfile, setWhoopProfile] = useState(null)

  const addToHistory = (entry) => {
    setHistory(prev => [entry, ...prev])
  }

  return (
    <div className="flex h-screen bg-bg">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar />
        <main className="flex-1 overflow-y-auto p-8">
          <Routes>
            <Route path="/" element={
              <Dashboard profile={profile} addToHistory={addToHistory} />
            } />
            <Route path="/ask" element={
              <AskFitRAG profile={profile} addToHistory={addToHistory} />
            } />
            <Route path="/profile" element={
              <Profile profile={profile} setProfile={setProfile} />
            } />
            <Route path="/whoop" element={
              <WhoopData whoopProfile={whoopProfile} setWhoopProfile={setWhoopProfile} setProfile={setProfile} />
            } />
            <Route path="/history" element={
              <History history={history} />
            } />
          </Routes>
        </main>
      </div>
    </div>
  )
}