import React, { useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import About from "./components/About";
import Skills from "./components/Skills";
import Projects from "./components/Projects";
import AIChat from "./components/AIChat";
import Contact from "./components/Contact";
import Footer from "./components/Footer";

const Home: React.FC = () => {
  // Ensure page loads at the top - delayed to override any component scrolling
  useEffect(() => {
    // Use a timeout to ensure all components have loaded before scrolling to top
    const timeoutId = setTimeout(() => {
      window.scrollTo(0, 0);
    }, 200);
    
    return () => clearTimeout(timeoutId);
  }, []);

  return (
    <div className="min-h-screen">
      <Header />
      <Hero />
      <About />
      <Skills />
      <Projects />
      <AIChat />
      <Contact />
      <Footer />
    </div>
  );
};

function App(): React.JSX.Element {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;